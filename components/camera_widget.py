from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer, QRect, Slot
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap, QRadialGradient

class CameraOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_active = False
        self.is_collapsed = False
        self.scan_y = 20
        self.scan_dir = 1
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scan)



    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        hud_color = QColor("#00ffaa")
        
        # 1. AI Tracking Tag (Top Right)
        tag_w, tag_h = 190, 26
        tag_rect = QRect(w - tag_w - 40, 40, tag_w, tag_h)
        
        # Background
        painter.setPen(QPen(QColor(0, 255, 170, 40), 1))
        painter.setBrush(QColor(8, 15, 23, 220))
        painter.drawRoundedRect(tag_rect, 4, 4)
        
        # Pulse Dot
        import math
        import time
        pulse = (math.sin(time.time() * 5) + 1) / 2 if self.is_active else 0
        if self.is_active:
            glow = QRadialGradient(tag_rect.left() + 14, tag_rect.center().y(), 6)
            glow.setColorAt(0, QColor(0, 255, 170, 180))
            glow.setColorAt(1, QColor(0, 255, 170, 0))
            painter.setBrush(glow)
            painter.drawEllipse(tag_rect.left() + 8, tag_rect.center().y() - 6, 12, 12)
        
        dot_color = QColor(0, 255, 170, 255) if self.is_active else QColor(82, 82, 91)
        painter.setPen(Qt.NoPen)
        painter.setBrush(dot_color)
        painter.drawEllipse(tag_rect.left() + 11, tag_rect.center().y() - 3, 6, 6)
        
        # Status Text (SHRUNK)
        status_text = "YAPAY ZEKA TAKİBİ: AKTİF" if self.is_active else "YAPAY ZEKA TAKİBİ: PASİF"
        font = painter.font()
        font.setFamily("Fira Code")
        font.setPointSize(7) # Smaller font
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(hud_color if self.is_active else QColor(161, 161, 170))
        painter.drawText(tag_rect.left() + 24, tag_rect.center().y() + 3, status_text)
        
        # 2. Viewfinder Corners (Only 4 corners, no extra accent)
        m, cl = 32, 40
        painter.setPen(QPen(hud_color, 2))
        # TL
        painter.drawLine(m, m, m + cl, m)
        painter.drawLine(m, m, m, m + cl)
        # TR
        painter.drawLine(w - m, m, w - m - cl, m)
        painter.drawLine(w - m, m, w - m, m + cl)
        # BL
        painter.drawLine(m, h - m, m + cl, h - m)
        painter.drawLine(m, h - m, m, h - m - cl)
        # BR
        painter.drawLine(w - m, h - m, w - m - cl, h - m)
        painter.drawLine(w - m, h - m, w - m, h - m - cl)

        # 3. Scanning Circle
        if self.is_active:
            radius = 144
            cx, cy = w // 2, h // 2
            
            # 1. Thin transparent solid ring
            painter.setBrush(Qt.NoBrush)
            bg_pen = QPen(QColor(0, 255, 170, int(255 * 0.2)), 1, Qt.SolidLine)
            painter.setPen(bg_pen)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

            # 2. Dashed (dotted) ring
            c_pen = QPen(QColor(0, 255, 170, int(255 * 0.7)), 1.5, Qt.DashLine)
            c_pen.setDashPattern([3, 4]) # Tighter dashed/dotted look
            painter.setPen(c_pen)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
            
            # 3. Ping animation circle (Optional subtle glow)
            ping_radius = radius + int(10 * pulse)
            ping_pen = QPen(QColor(0, 255, 170, int(255 * 0.15 * (1 - pulse))), 1)
            painter.setPen(ping_pen)
            painter.drawEllipse(cx - ping_radius, cy - ping_radius, ping_radius * 2, ping_radius * 2)
            
            # Text Pill Background
            pill_w, pill_h = 132, 28
            pill_rect = QRect(cx - pill_w // 2, cy - pill_h // 2, pill_w, pill_h)
            painter.setPen(QPen(QColor(0, 255, 170, int(255 * 0.3)), 1))
            painter.setBrush(QColor(8, 15, 23, 204))
            painter.drawRoundedRect(pill_rect, 14, 14)
            
            # SCANNING... Text
            painter.setPen(QPen(hud_color))
            scan_font = painter.font()
            scan_font.setFamily("Fira Code")
            scan_font.setPointSize(8)
            scan_font.setBold(True)
            scan_font.setLetterSpacing(scan_font.SpacingType.AbsoluteSpacing, 2)
            painter.setFont(scan_font)
            # Center text perfectly in the pill
            painter.drawText(pill_rect.adjusted(0, 0, 0, 0), Qt.AlignCenter, "TARIYOR...")

        # 4. Scanning Line (Traditional look)
        if self.is_active:
            from PySide6.QtGui import QLinearGradient
            grad = QLinearGradient(m, self.scan_y, w - m, self.scan_y)
            grad.setColorAt(0, QColor(0, 255, 170, 0))
            grad.setColorAt(0.5, QColor(0, 255, 170, 200))
            grad.setColorAt(1, QColor(0, 255, 170, 0))
            painter.setPen(QPen(grad, 2))
            painter.drawLine(m, self.scan_y, w - m, self.scan_y)

    def update_scan(self):
        if not self.is_active:
            self.update() # Keep updating for pulse
            return
        m = 32
        max_h = self.height() - m
        self.scan_y += 3 * self.scan_dir
        
        if self.scan_y >= max_h:
            self.scan_y = max_h
            self.scan_dir = -1
        elif self.scan_y <= m:
            self.scan_y = m
            self.scan_dir = 1
            
        self.update()


class CameraWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "GlassPanel")
        
        self.image_label = QLabel()
        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)
        
        self.overlay = CameraOverlay(self)

    @Slot(bool)
    def set_active(self, active):
        self.overlay.is_active = active
        if active:
            self.overlay.timer.start(50)
        else:
            self.overlay.timer.stop()
            # Clear image when inactive
            self.image_label.clear()
        self.overlay.update()


    @Slot(QPixmap)
    def update_frame(self, pixmap):
        self.image_label.setPixmap(pixmap)


    @Slot(QPixmap)
    def set_frame(self, pixmap):
        self.image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.resize(self.size())
