import cv2
import numpy as np
import time
import serial
import sys
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage, QPixmap
from ultralytics import YOLO

MODEL_PATH = "best.pt"
SERIAL_PORT = "COM5"
BAUD_RATE = 9600

CONF_THRESHOLD = 0.70
REQUIRED_STABLE_FRAMES = 5
COOLDOWN = 4.0
DELAY_BEFORE_SEND = 0.7

# Arduino koduna göre:
# a = cam
# b = plastik
# c = kağıt
# d = metal
CLASS_TO_COMMAND = {
    "glass": "a",
    "cam": "a",

    "plastic": "b",
    "plastik": "b",

    "paper": "c",
    "kagit": "c",
    "kağıt": "c",

    "metal": "d"
}


class CameraThread(QThread):
    change_pixmap_signal = Signal(QPixmap)

    # UI update signals
    detection_signal = Signal(list)       # list of (class_name, confidence) tuples
    command_sent_signal = Signal(str, float)    # class_name sent to arduino, confidence
    arduino_status_signal = Signal(bool)
    model_status_signal = Signal(bool)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self._run_flag = True

    def run(self):
        # 1. Arduino bağlantısı
        arduino = None
        try:
            arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

            # Python seri portu açınca Arduino resetlenebilir.
            # Bu yüzden Arduino'nun setup() kısmı bitsin diye bekliyoruz.
            time.sleep(3)

            arduino.reset_input_buffer()
            arduino.reset_output_buffer()

            print(f"Arduino bağlantısı başarılı: {SERIAL_PORT}")
            self.arduino_status_signal.emit(True)

        except Exception as e:
            print("Arduino portu açılamadı:", e)
            self.arduino_status_signal.emit(False)

        # 2. YOLO modeli yükleme
        model = None
        try:
            model = YOLO(MODEL_PATH)
            print("YOLO modeli başarıyla yüklendi.")
            self.model_status_signal.emit(True)
        except Exception as e:
            print("YOLO modeli yüklenemedi:", e)
            self.model_status_signal.emit(False)

        # Stabil tespit değişkenleri
        last_class = None
        stable_count = 0
        last_sent_time = 0

        # Kamera başlatma
        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            print("Kamera açılamadı.")
            return

        while self._run_flag:
            ret, cv_img = cap.read()

            if not ret:
                print("Kameradan görüntü alınamadı.")
                break

            if model is not None:
                results = model(cv_img, conf=CONF_THRESHOLD, verbose=False)

                detected_class = None
                best_conf = 0.0
                all_detections = []

                for r in results:
                    if r.boxes is not None:
                        for box in r.boxes:
                            conf = float(box.conf[0])
                            cls_id = int(box.cls[0])

                            # Sınıf ismini küçük harfe çeviriyoruz.
                            # Böylece Plastic / plastic / PLASTIC farkı sorun olmaz.
                            class_name = str(model.names[cls_id]).lower().strip()
                            all_detections.append((class_name, conf))

                            if conf > best_conf:
                                best_conf = conf
                                detected_class = class_name

                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            label = f"{class_name} {conf:.2f}"

                            cv2.rectangle(
                                cv_img,
                                (x1, y1),
                                (x2, y2),
                                (0, 255, 0),
                                2
                            )

                            cv2.putText(
                                cv_img,
                                label,
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (0, 255, 0),
                                2
                            )

                # Stabil tespit kontrolü
                if detected_class == last_class and detected_class is not None:
                    stable_count += 1
                else:
                    last_class = detected_class
                    stable_count = 1 if detected_class is not None else 0

                all_detections.sort(key=lambda x: x[1], reverse=True)
                self.detection_signal.emit(all_detections[:3])

                current_time = time.time()

                # Arduino'ya komut gönderme şartları
                if (
                    detected_class is not None
                    and detected_class in CLASS_TO_COMMAND
                    and stable_count >= REQUIRED_STABLE_FRAMES
                    and (current_time - last_sent_time) > COOLDOWN
                ):
                    command = CLASS_TO_COMMAND[detected_class]

                    print(f"Kararlı tespit: {detected_class} ({best_conf:.2f})")
                    print(f"Gönderilecek komut: {command}")

                    # Komut göndermeden önce kısa bekleme
                    time.sleep(DELAY_BEFORE_SEND)

                    if arduino is not None and arduino.is_open:
                        try:
                            # Serial Monitor'de Enter'a basmış gibi gönderiyoruz.
                            # Örnek: a\n
                            arduino.reset_output_buffer()
                            arduino.write((command + "\n").encode("utf-8"))
                            arduino.flush()

                            print(f"Arduino'ya gönderildi: {command}")

                            self.command_sent_signal.emit(detected_class, best_conf)

                        except Exception as e:
                            print("Arduino yazma hatası:", e)
                            self.arduino_status_signal.emit(False)
                    else:
                        print(
                            f"Arduino bağlı değil, {command} komutu gönderilemedi. "
                            f"Sanal olarak algılandı."
                        )
                        self.command_sent_signal.emit(detected_class, best_conf)

                    last_sent_time = time.time()
                    stable_count = 0
                    last_class = None

                elif detected_class is not None and detected_class not in CLASS_TO_COMMAND:
                    print(f"Bu sınıf için komut tanımlı değil: {detected_class}")

                cv2.putText(
                    cv_img,
                    f"Tespit: {detected_class} | Stable: {stable_count}",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2
                )

            # OpenCV görüntüsünü Qt görüntüsüne çevirip arayüze gönderme
            qt_img = self.convert_cv_qt(cv_img)
            self.change_pixmap_signal.emit(qt_img)

        # Kamera ve Arduino kapatma
        cap.release()

        if arduino is not None and arduino.is_open:
            arduino.close()
            print("Arduino bağlantısı kapatıldı.")

    def convert_cv_qt(self, cv_img):
        """OpenCV görüntüsünü QPixmap formatına çevirir."""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        convert_to_qt_format = QImage(
            rgb_image.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        p = convert_to_qt_format.scaled(
            640,
            480,
            Qt.KeepAspectRatio
        )

        return QPixmap.fromImage(p)

    def stop(self):
        """Thread'i durdurur."""
        self._run_flag = False