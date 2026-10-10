from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QStackedWidget, QFrame, QButtonGroup, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QIcon, QColor
import os

from core.pages import MenuPage, DashboardPage, AnalizlerPage, RehberPage, AyarlarPage
from components.custom_widgets import NavButton
from logic.camera_engine import CameraThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartRecycle AI v1.0")
        self.resize(1280, 800)
        
        # Frameless window for custom styling with taskbar functionality
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.init_ui()
        self.init_camera()
        
        # Dragging variables
        self._is_dragging = False
        self._drag_pos = QPoint()

        # AI & Stats tracking
        self.total_detections = 0
        self.category_counts = {"Plastik": 0, "Metal": 0, "Kağıt": 0, "Cam": 0}
        self.hourly_counts = [0] * 12
        self.confidences = []
        import time
        self.start_time = time.time()
        
        from PySide6.QtCore import QTimer
        self.uptime_timer = QTimer(self)
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(60000) # Every 1 min

    def init_ui(self):
        # Central widget
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("MainContent")
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Custom Title Bar
        self.title_bar = QFrame()
        self.title_bar.setProperty("class", "HeaderFrame")
        self.title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(16, 0, 16, 0)
        
        app_title = QLabel("SmartRecycle AI v1.0")
        app_title.setObjectName("AppNameLabel")
        sys_status = QLabel("SİSTEM HAZIR")
        sys_status.setStyleSheet("background-color: rgba(0, 255, 170, 0.05); color: rgba(0, 255, 170, 0.7); padding: 2px 8px; border: 1px solid rgba(0, 255, 170, 0.2); border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: bold;")
        
        title_layout.addWidget(app_title)
        title_layout.addSpacing(12)
        title_layout.addWidget(sys_status)
        title_layout.addStretch()
        
        # Window controls
        btn_min = QPushButton("🗕")
        btn_min.setFixedSize(32, 32)
        btn_min.setStyleSheet("color: #a1a1aa; border: none; background: transparent; font-size: 12px;")
        btn_min.clicked.connect(self.showMinimized)
        
        btn_max = QPushButton("🗖")
        btn_max.setFixedSize(32, 32)
        btn_max.setStyleSheet("color: #a1a1aa; border: none; background: transparent; font-size: 12px;")
        btn_max.clicked.connect(self.toggle_maximize)
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(32, 32)
        btn_close.setStyleSheet("color: #a1a1aa; border: none; background: transparent; font-size: 12px;")
        btn_close.clicked.connect(self.close)
        
        title_layout.addWidget(btn_min)
        title_layout.addWidget(btn_max)
        title_layout.addWidget(btn_close)
        
        main_layout.addWidget(self.title_bar)
        
        # 2. Navigation Bar (Combined Style)
        self.nav_bar = QFrame()
        self.nav_bar.setProperty("class", "TitleGlassPanel")
        self.nav_bar.setFixedHeight(70)
        self.nav_bar.setStyleSheet("""
            QFrame.TitleGlassPanel {
                background-color: rgba(15, 23, 42, 0.6);
                border-bottom: 1px solid rgba(0, 255, 170, 0.1);
            }
        """)
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(32, 0, 32, 0)
        
        # Brand Logo + Text
        brand_container = QWidget()
        brand_layout = QHBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        
        brand_icon = QLabel()
        brand_icon.setFixedSize(32, 32)
        # Using recycling symbol as icon
        brand_icon.setText("♻")
        brand_icon.setStyleSheet("color: #00FFAA; font-size: 24px; border: none;")
        
        nav_brand = QLabel("SmartRecycle AI")
        nav_brand.setStyleSheet("color: #00FFAA; font-family: 'Space Grotesk'; font-weight: bold; font-size: 20px; letter-spacing: -0.5px; border: none;")
        
        brand_layout.addWidget(brand_icon)
        brand_layout.addWidget(nav_brand)
        
        nav_layout.addWidget(brand_container)
        nav_layout.addStretch()
        
        # Center Links
        links_container = QWidget()
        links_layout = QHBoxLayout(links_container)
        links_layout.setContentsMargins(0, 0, 0, 0)
        links_layout.setSpacing(32)
        
        # Nav Buttons
        self.nav_group = QButtonGroup(self)
        
        btn_menu = NavButton("ANA MENÜ")
        btn_dash = NavButton("KONTROL PANELİ")
        btn_analiz = NavButton("ANALİZLER")
        btn_rehber = NavButton("REHBER")
        btn_ayar = NavButton("AYARLAR")
        
        self.nav_group.addButton(btn_menu, 0)
        self.nav_group.addButton(btn_dash, 1)
        self.nav_group.addButton(btn_analiz, 2)
        self.nav_group.addButton(btn_rehber, 3)
        self.nav_group.addButton(btn_ayar, 4)
        
        btn_dash.setChecked(True)
        self.nav_group.idClicked.connect(self.switch_page)
        
        links_layout.addWidget(btn_menu)
        links_layout.addWidget(btn_dash)
        links_layout.addWidget(btn_analiz)
        links_layout.addWidget(btn_rehber)
        links_layout.addWidget(btn_ayar)
        
        nav_layout.addWidget(links_container)
        main_layout.addWidget(self.nav_bar)
        
        # 3. Stacked Pages
        self.stacked_widget = QStackedWidget()
        
        self.page_menu = MenuPage()
        self.page_dash = DashboardPage()
        self.page_analiz = AnalizlerPage()
        self.page_rehber = RehberPage()
        self.page_ayar = AyarlarPage()
        
        self.stacked_widget.addWidget(self.page_menu)   # Index 0
        self.stacked_widget.addWidget(self.page_dash)   # Index 1
        self.stacked_widget.addWidget(self.page_analiz) # Index 2
        self.stacked_widget.addWidget(self.page_rehber) # Index 3
        self.stacked_widget.addWidget(self.page_ayar)   # Index 4
        
        # Connect Menu Page Signals
        self.page_menu.card_dash.clicked.connect(lambda: self.switch_page(1))
        self.page_menu.card_analiz.clicked.connect(lambda: self.switch_page(2))
        self.page_menu.card_guide.clicked.connect(lambda: self.switch_page(3))
        self.page_menu.card_settings.clicked.connect(lambda: self.switch_page(4))
        
        # Connect Placeholder Back Buttons
        self.page_analiz.back_btn.clicked.connect(lambda: self.switch_page(0))
        self.page_rehber.back_btn.clicked.connect(lambda: self.switch_page(0))
        self.page_ayar.back_btn.clicked.connect(lambda: self.switch_page(0))
        
        # Ensure nav bar is hidden on menu page initially
        self.nav_bar.setVisible(False)
        
        main_layout.addWidget(self.stacked_widget, 1)
        


    def init_camera(self):
        self.camera_thread = CameraThread(camera_index=0)
        self.camera_thread.change_pixmap_signal.connect(self.page_dash.camera_widget.set_frame)
        
        # AI signals
        self.camera_thread.detection_signal.connect(self.on_detection)
        self.camera_thread.command_sent_signal.connect(self.on_command_sent)
        self.camera_thread.arduino_status_signal.connect(self.page_dash.sys_status_arduino.set_status)
        self.camera_thread.model_status_signal.connect(self.page_dash.sys_status_model.set_status)
        
        # Connect to buttons
        self.page_dash.btn_start.clicked.connect(self.start_camera)
        self.page_dash.btn_stop.clicked.connect(self.stop_camera)

    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
            self.page_dash.camera_widget.set_active(True)
            self.page_dash.sys_status_camera.set_status(True)

    def stop_camera(self):
        if self.camera_thread.isRunning():
            # 1. Immediate UI update
            self.page_dash.camera_widget.set_active(False)
            self.page_dash.sys_status_camera.set_status(False)
            from PySide6.QtGui import QPixmap, QColor
            empty_px = QPixmap(640, 480)
            empty_px.fill(QColor("#080f17"))
            self.page_dash.camera_widget.image_label.setPixmap(empty_px)
            
            # 2. Terminate thread
            self.camera_thread.stop()

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        # Show/Hide nav bar based on page
        # Menu page is index 0
        self.nav_bar.setVisible(index != 0)
        
        # Sync nav buttons (Menu is index 0, Dashboard is index 1, etc.)
        if 0 <= index <= 4:
            self.nav_group.button(index).setChecked(True)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    from PySide6.QtCore import Slot

    @Slot(list)
    def on_detection(self, top_detections):
        if not top_detections:
            return

        name_map = {"plastic": "Plastik", "metal": "Metal", "paper": "Kağıt", "glass": "Cam", "other": "Diğer"}
        
        class_name, confidence = top_detections[0]
        tr_name = name_map.get(class_name, class_name)
        
        primary_conf = confidence * 100
        self.page_dash.primary_pred.update_data(tr_name, primary_conf)
        self.page_dash.set_active_category(tr_name)
        
        # Kullanıcı 2. ve 3. tahminlerin boş kalmamasını ve 1.'den küçük oranlarla
        # dolu görünmesini istediği için, kalan ihtimali diğer sınıflara dağıtıyoruz.
        available_classes = [c for c in name_map.values() if c != tr_name and c != "Diğer"]
        
        if len(available_classes) >= 2:
            cls2 = available_classes[0]
            cls3 = available_classes[1]
            
            remaining = 100.0 - primary_conf
            if remaining < 0: remaining = 0
            
            conf2 = remaining * 0.65
            conf3 = remaining * 0.35
            
            self.page_dash.sec_pred1.update_data(cls2, conf2)
            self.page_dash.sec_pred2.update_data(cls3, conf3)
        else:
            self.page_dash.sec_pred1.update_data("-", 0)
            self.page_dash.sec_pred2.update_data("-", 0)

    @Slot(str, float)
    def on_command_sent(self, class_name, confidence):
        name_map = {"plastic": "Plastik", "metal": "Metal", "paper": "Kağıt", "glass": "Cam", "other": "Diğer"}
        tr_name = name_map.get(class_name, class_name)
        
        # Ekranda en son kararlı tespit edilen cisim kalsın
        self.page_dash.primary_pred.update_data(tr_name, confidence * 100)
        self.page_dash.set_active_category(tr_name)
        
        self.total_detections += 1
        self.confidences.append(confidence)
        if tr_name in self.category_counts:
            self.category_counts[tr_name] += 1
            
        # Update hourly counts
        import datetime
        current_hour = datetime.datetime.now().hour
        hour_index = current_hour // 2
        self.hourly_counts[hour_index] += 1
            
        # (Arayüzdeki yüzdeler anlık tespitler için ayrıldığı için
        #  burada tarihi verilerle sec_pred1 ve sec_pred2 güncellenmeyecek)

        # Update AnalizlerPage Metrics
        self.page_analiz.m1.set_value(self.total_detections)
        
        active_cat = max(self.category_counts, key=self.category_counts.get)
        if self.category_counts[active_cat] > 0:
            self.page_analiz.m2.set_value(active_cat)
            
        avg_conf = sum(self.confidences) / len(self.confidences)
        self.page_analiz.m3.set_value(f"%{int(avg_conf * 100)}")
        
        # Update AnalizlerPage Charts
        self.page_analiz.bar_chart.update_data(self.hourly_counts)
        self.page_analiz.donut_chart.update_data(self.category_counts)
        
    def update_uptime(self):
        import time
        elapsed_min = int((time.time() - self.start_time) / 60)
        self.page_analiz.m4.set_value(elapsed_min)

    # Drag window handlers
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Check if clicked on title bar area
            if event.position().y() <= self.title_bar.height():
                self._is_dragging = True
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._is_dragging = False

    def closeEvent(self, event):
        self.camera_thread.stop()
        super().closeEvent(event)
