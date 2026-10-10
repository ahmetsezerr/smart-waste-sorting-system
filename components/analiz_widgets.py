from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                               QLabel, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QIcon, QColor, QPainter, QPainterPath, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import os

class AnalizGlassPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, rgba(21, 28, 37, 0.7) 0%, rgba(13, 20, 28, 0.9) 100%);
                border: 1px solid rgba(58, 74, 64, 0.15);
                border-radius: 20px;
            }
            QLabel { border: none; background: transparent; }
        """)

class MetricCard(AnalizGlassPanel):
    def __init__(self, title, icon_name, value, unit="", highlight=False, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        header_layout = QHBoxLayout()
        title_lbl = QLabel(title.upper())
        # font-label text-xs text-on-surface-variant uppercase tracking-widest
        title_lbl.setStyleSheet("color: #b9cbbd; font-family: 'Space Grotesk'; font-size: 12px; letter-spacing: 2px; font-weight: 500;")
        
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        icon_color = "#00ffaa" if highlight else "#849589"
        icon_lbl.setStyleSheet(f"color: {icon_color}; border: none;")
        
        icon_map = {
            "Toplam Tespit": "memory",
            "En Aktif Kategori": "category",
            "Ortalama Güven": "radar",
            "Çalışma Süresi": "timer"
        }
        actual_icon = icon_map.get(title, icon_name)
        
        import os
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(root_dir, "assets", "icons", f"{actual_icon}.svg")
        if os.path.exists(icon_path):
            icon_lbl.setPixmap(QIcon(icon_path).pixmap(20, 20))
        else:
            # Fallback if svg doesn't exist
            pass
            
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(icon_lbl)
        
        layout.addLayout(header_layout)
        layout.addStretch()
        
        val_layout = QHBoxLayout()
        self.val_lbl = QLabel(str(value))
        
        if highlight:
            # cyber-glow border-b border-b-primary-container/50
            self.setStyleSheet("""
                QFrame {
                    background: linear-gradient(135deg, rgba(21, 28, 37, 0.8) 0%, rgba(13, 20, 28, 0.95) 100%);
                    border: 1px solid rgba(58, 74, 64, 0.15);
                    border-bottom: 2px solid #00ffaa;
                    border-radius: 20px;
                }
                QLabel { border: none; background: transparent; }
            """)
            # font-display text-4xl font-bold text-primary-container text-glow
            self.val_lbl.setStyleSheet("color: #00ffaa; font-family: 'Space Grotesk'; font-size: 36px; font-weight: bold; border: none;")
            
            # Combine panel glow and text glow effects
            container_glow = QGraphicsDropShadowEffect()
            container_glow.setBlurRadius(20)
            container_glow.setColor(QColor(0, 255, 170, 60))
            container_glow.setOffset(0, 0)
            self.setGraphicsEffect(container_glow)
            
            text_glow = QGraphicsDropShadowEffect()
            text_glow.setBlurRadius(10)
            text_glow.setColor(QColor(0, 255, 170, 150))
            text_glow.setOffset(0, 0)
            self.val_lbl.setGraphicsEffect(text_glow)
        else:
            # font-label text-4xl font-bold text-primary (Reduced from 5xl/48px to prevent squeezing)
            self.val_lbl.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 32px; font-weight: bold; border: none;")
            
        val_layout.addWidget(self.val_lbl)
        
        if unit:
            # text-lg text-on-surface-variant
            self.unit_lbl = QLabel(unit)
            self.unit_lbl.setStyleSheet("color: #b9cbbd; font-family: 'Space Grotesk'; font-size: 18px; margin-bottom: 8px; border: none;")
            val_layout.addWidget(self.unit_lbl)
            
        val_layout.addStretch()
        val_layout.setAlignment(Qt.AlignBottom)
        layout.addLayout(val_layout)

    def set_value(self, value):
        self.val_lbl.setText(str(value))

    def set_unit(self, unit):
        if hasattr(self, 'unit_lbl'):
            self.unit_lbl.setText(unit)

class BarChartCard(AnalizGlassPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        header_layout = QHBoxLayout()
        title = QLabel("Saatlik Tespit Yoğunluğu")
        title.setStyleSheet("color: #f6fff6; font-family: 'Inter'; font-size: 18px; font-weight: 500;")
        
        badge = QLabel("24 SAAT")
        badge.setStyleSheet("color: #00e296; background-color: rgba(0, 226, 150, 0.1); border-radius: 4px; padding: 4px 8px; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: bold;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(badge)
        
        layout.addLayout(header_layout)
        layout.addSpacing(24)
        
class CustomBarChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(220)
        self.heights = [0] * 12 # Start with empty bars

    def update_data(self, data):
        self.heights = data
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        n = len(self.heights)
        if n == 0:
            return
        bar_w = w / n
        
        max_val = max(self.heights) if self.heights else 0
        if max_val == 0: max_val = 1
        
        for i, val in enumerate(self.heights):
            pct = val / max_val
            bar_h = pct * h
            rect = QRectF(i * bar_w, h - bar_h, bar_w, bar_h)
            
            color = QColor("#00ffaa")
            if val == max_val and val > 0:
                # Active/Highest bar
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
            else:
                opacity = int(max(0.2, pct * 0.8) * 255) if val > 0 else 50
                color.setAlpha(opacity)
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                
            painter.drawRect(rect)

class BarChartCard(AnalizGlassPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop) # Ensure items start from the top
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop) # Anchor header to top-left
        title = QLabel("Saatlik Tespit Yoğunluğu")
        title.setStyleSheet("color: #f6fff6; font-family: 'Inter'; font-size: 18px; font-weight: 500;")
        
        badge = QLabel("24 SAAT")
        badge.setStyleSheet("color: #00e296; background-color: rgba(0, 226, 150, 0.1); border-radius: 4px; padding: 4px 8px; font-family: 'JetBrains Mono'; font-size: 10px; font-weight: bold;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(badge)
        
        layout.addLayout(header_layout)
        layout.addSpacing(24) # Controlled spacing after title
        
        # Custom Painter Chart
        self.chart = CustomBarChart()
        layout.addWidget(self.chart)
        
        # X-axis labels
        axis_layout = QHBoxLayout()
        axis_layout.setContentsMargins(0, 8, 0, 0)
        axis_style = "color: #b9cbbd; font-family: 'JetBrains Mono'; font-size: 10px; background: transparent;"
        
        # Add a separator line above labels
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: rgba(58, 74, 64, 0.3); border: none;")
        layout.addWidget(sep)
        
        labels = ["00:00", "06:00", "12:00", "18:00", "23:59"]
        for lbl in labels:
            l = QLabel(lbl)
            l.setStyleSheet("color: #b9cbbd; font-family: 'JetBrains Mono'; font-size: 12px; background: transparent; font-weight: normal;") # JetBrains Mono 12px as per photo 4
            axis_layout.addWidget(l)
            if lbl != "23:59":
                axis_layout.addStretch()
                
        layout.addLayout(axis_layout)

    def update_data(self, data):
        self.chart.update_data(data)

class DonutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 220)
        self.data = [
            (0, QColor("#00FFAA")), # Plastik
            (0, QColor("#00DAF3")), # Kağıt
            (0, QColor("#F6FFF6")), # Cam
            (0, QColor("#FFB4A2"))  # Metal
        ]
        self.total = 0

    def update_data(self, data, total):
        self.data = data
        self.total = total
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(20, 20, 180, 180)
        
        # Draw base shadow glow
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 255, 170, 15)))
        painter.drawEllipse(rect.adjusted(-5, -5, 5, 5))
        
        start_angle = 90 * 16
        
        for value, color in self.data:
            if value > 0:
                span_angle = int((value / 100.0) * 360 * 16)
                
                pen = QPen(color)
                pen.setWidth(24) # Slightly thicker
                pen.setCapStyle(Qt.FlatCap)
                painter.setPen(pen)
                
                painter.drawArc(rect, start_angle, -span_angle)
                start_angle -= span_angle
            
        # Draw inner text
        painter.setPen(QPen(QColor("#f6fff6")))
        font = painter.font()
        font.setFamily("JetBrains Mono")
        font.setPointSize(30) # text-3xl as per photo 5
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, str(self.total))
        
        font.setPointSize(10)
        font.setBold(False)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        painter.setPen(QPen(QColor("#b9cbbd")))
        painter.setFont(font)
        # Shift slightly down for the "TOPLAM" text
        text_rect = QRectF(rect.x(), rect.y() + 42, rect.width(), rect.height())
        painter.drawText(text_rect, Qt.AlignCenter, "TOPLAM")

class DonutChartCard(AnalizGlassPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop) # Ensure items start from the top
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop) # Anchor header to top-left
        title = QLabel("Atık Türü Dağılımı")
        title.setStyleSheet("color: #f6fff6; font-family: 'Inter'; font-size: 18px; font-weight: 500;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addSpacing(24) # Controlled spacing after title
        
        content_layout = QHBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(40)
        
        self.donut = DonutWidget()
        content_layout.addWidget(self.donut)
        
        legend_layout = QVBoxLayout()
        legend_layout.setAlignment(Qt.AlignVCenter)
        legend_layout.setSpacing(16)
        
        self.legend_items = {}
        items = [
            ("Plastik", "%0", "#00FFAA"),
            ("Kağıt", "%0", "#00DAF3"),
            ("Cam", "%0", "#F6FFF6"),
            ("Metal", "%0", "#FFB4A2")
        ]
        
        for name, pct, color in items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(12)
            
            dot = QFrame()
            dot.setFixedSize(12, 12)
            dot.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
            
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 14px;")
            name_lbl.setFixedWidth(60)
            
            pct_lbl = QLabel(pct)
            pct_lbl.setStyleSheet("color: #b9cbbd; font-family: 'Space Grotesk'; font-size: 14px;")
            
            item_layout.addWidget(dot)
            item_layout.addWidget(name_lbl)
            item_layout.addWidget(pct_lbl)
            legend_layout.addLayout(item_layout)
            
            self.legend_items[name] = {
                "dot": dot,
                "pct_lbl": pct_lbl,
                "color": color
            }
            
        content_layout.addLayout(legend_layout)
        layout.addLayout(content_layout)

    def update_data(self, category_counts):
        total = sum(category_counts.values())
        if total == 0:
            total = 1 # avoid division by zero
            
        color_map = {
            "Plastik": QColor("#00FFAA"),
            "Kağıt": QColor("#00DAF3"),
            "Cam": QColor("#F6FFF6"),
            "Metal": QColor("#FFB4A2")
        }
        
        donut_data = []
        max_pct_val = 0
        
        for name in ["Plastik", "Kağıt", "Cam", "Metal"]:
            count = category_counts.get(name, 0)
            pct = int((count / total) * 100) if total > 1 or count > 0 else 0
            if pct > max_pct_val:
                max_pct_val = pct
            donut_data.append((pct, color_map[name]))
            
        real_total = sum(category_counts.values())
        self.donut.update_data(donut_data, real_total)
        
        for name in ["Plastik", "Kağıt", "Cam", "Metal"]:
            count = category_counts.get(name, 0)
            pct = int((count / total) * 100) if total > 1 or count > 0 else 0
            item = self.legend_items[name]
            item["pct_lbl"].setText(f"%{pct}")
            
            # Apply glow if highest percentage
            if pct == max_pct_val and max_pct_val > 0:
                glow = QGraphicsDropShadowEffect()
                glow.setBlurRadius(10)
                glow.setColor(QColor(item["color"]))
                glow.setOffset(0, 0)
                item["dot"].setGraphicsEffect(glow)
            else:
                item["dot"].setGraphicsEffect(None)

class InsightPanel(AnalizGlassPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        icon_frame = QFrame()
        icon_frame.setFixedSize(52, 52)
        icon_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 255, 170, 0.1); 
                border: 1px solid rgba(0, 255, 170, 0.3); 
                border-radius: 26px;
            }
            QLabel { border: none; background: transparent; }
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_lbl = QLabel()
        # psychology icon from HTML
        icon_path = "assets/icons/psychology.svg"
        if not os.path.exists(icon_path): icon_path = "assets/icons/info.svg"
        icon_lbl.setPixmap(QIcon(icon_path).pixmap(28, 28))
        icon_layout.addWidget(icon_lbl)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        title = QLabel("AKILLI YORUM")
        # font-label text-xs uppercase tracking-widest text-primary-container
        title.setStyleSheet("color: #00ffaa; font-family: 'Fira Code'; font-size: 12px; letter-spacing: 3px; font-weight: bold;")
        
        desc = QLabel('"Bugün en çok plastik atık algılandı, verimlilik %5 arttı"')
        # font-body text-base text-primary
        desc.setStyleSheet("color: #f6fff6; font-family: 'Inter'; font-size: 16px; font-weight: 500;")
        
        text_layout.addWidget(title)
        text_layout.addWidget(desc)
        
        layout.addWidget(icon_frame)
        layout.addLayout(text_layout)
        layout.addStretch()

class StatusPanel(AnalizGlassPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        text_layout = QVBoxLayout()
        title = QLabel("SİSTEM DURUMU")
        title.setStyleSheet("color: #b9cbbd; font-family: 'Fira Code'; font-size: 11px; letter-spacing: 2px; border: none;")
        
        desc = QLabel("Model Durumu: Kararlı")
        desc.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 18px; font-weight: bold; border: none;")
        
        text_layout.addWidget(title)
        text_layout.addWidget(desc)
        
        self.dot = QFrame()
        self.dot.setFixedSize(16, 16)
        self.dot.setStyleSheet("background-color: #00ffaa; border-radius: 8px;")
        
        # Add pulse animation effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(0, 255, 170, 200))
        glow.setOffset(0, 0)
        self.dot.setGraphicsEffect(glow)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.dot)
        
        # Note: Pulse animation can be implemented with QPropertyAnimation on blur radius if needed, 
        # but a static high-glow already matches the "powered-on" feel.

