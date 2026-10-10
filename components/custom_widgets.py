from PySide6.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QProgressBar, QFrame, QSizePolicy, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QCursor, QColor, QPainter, QLinearGradient

class NavButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "NavButton")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setCheckable(True)

class CategoryButton(QFrame):
    def __init__(self, title, icon_path="", actv=False, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CategoryButton_checked" if actv else "CategoryButton")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.is_active = actv
        self.setFixedHeight(52) # Reduced from 64 to save space
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 12, 0)
        layout.setSpacing(8)
        
        # 1. Left Accent Glow Bar (Only if active)
        self.accent = QFrame()
        self.accent.setFixedWidth(4)
        self.accent.setStyleSheet("background-color: #00ffaa; border-radius: 2px;" if actv else "background-color: transparent;")
        layout.addWidget(self.accent)
        
        # 2. Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        if icon_path:
            self.icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            self.icon_label.setStyleSheet("background-color: rgba(255,255,255,0.05); border-radius: 4px;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # 3. Title
        self.title_label = QLabel(title.upper())
        self.title_label.setProperty("class", "CategoryTitle_checked" if actv else "CategoryTitle")
        layout.addWidget(self.title_label, 1)

        # 4. ACTV Badge
        self.badge = QLabel("ACTV")
        self.badge.setFixedSize(48, 20)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setStyleSheet("background-color: #00ffaa; color: #080f17; font-weight: bold; font-family: 'Space Grotesk'; font-size: 10px; border-radius: 4px;")
        self.badge.setVisible(actv)
        layout.addWidget(self.badge)

        # Animation state for scanner line
        self.scan_y = -20
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scan)
        if self.is_active:
            self.timer.start(30)

    def update_scan(self):
        self.scan_y += 2
        if self.scan_y > self.height() + 20:
            self.scan_y = -20
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.is_active:
            from PySide6.QtGui import QPainter, QLinearGradient, QColor
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            grad = QLinearGradient(0, self.scan_y - 15, 0, self.scan_y + 15)
            grad.setColorAt(0, QColor(0, 255, 170, 0))
            grad.setColorAt(0.5, QColor(0, 255, 170, 30))
            grad.setColorAt(1, QColor(0, 255, 170, 0))
            painter.fillRect(4, 0, self.width()-4, self.height(), grad)

    def set_active(self, active):
        if self.is_active == active:
            return
        self.is_active = active
        self.setProperty("class", "CategoryButton_checked" if active else "CategoryButton")
        self.title_label.setProperty("class", "CategoryTitle_checked" if active else "CategoryTitle")
        self.accent.setStyleSheet("background-color: #00ffaa; border-radius: 2px;" if active else "background-color: transparent;")
        self.badge.setVisible(active)
        self.style().unpolish(self)
        self.style().polish(self)
        if active:
            self.timer.start(30)
        else:
            self.timer.stop()
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.is_active:
            if self.parent():
                for child in self.parent().findChildren(CategoryButton):
                    if child != self:
                        child.set_active(False)
            self.set_active(True)

class ProbabilityBar(QWidget):
    def __init__(self, number, title, percentage, is_primary=True, parent=None):
        super().__init__(parent)
        self.is_primary = is_primary
        
        if is_primary:
            self.init_primary_ui(title, percentage)
        else:
            self.init_secondary_ui(number, title, percentage)

    def init_primary_ui(self, title, percentage):
        self.setFixedHeight(80)
        self.setObjectName("PrimaryPrediction")
        # bg-surface-container-high/50 border border-primary-container/30 rounded-lg p-4 flex justify-between items-center shadow-[inset_0_0_10px_rgba(0,255,170,0.05)] relative overflow-hidden
        self.setStyleSheet("""
            QWidget#PrimaryPrediction {
                background-color: rgba(25, 32, 41, 0.5);
                border: 1px solid rgba(0, 255, 170, 0.3);
                border-radius: 8px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(16)
        
        # 1. Left Accent Glow Bar
        # absolute left-0 top-0 bottom-0 w-1 bg-primary-container shadow-[0_0_10px_rgba(0,255,170,0.8)]
        accent = QFrame()
        accent.setFixedWidth(4)
        accent.setFixedHeight(50) # Taller accent
        accent.setStyleSheet("background-color: #00ffaa; border-radius: 2px;")
        
        glow_accent = QGraphicsDropShadowEffect()
        glow_accent.setBlurRadius(15)
        glow_accent.setColor(QColor(0, 255, 170, 200))
        glow_accent.setOffset(0, 0)
        accent.setGraphicsEffect(glow_accent)
        
        # 2. Check Icon Box
        # w-8 h-8 rounded bg-surface-container-highest/80 flex items-center justify-center border border-primary-container/50 shadow-[0_0_8px_rgba(0,255,170,0.2)]
        icon_box = QFrame()
        icon_box.setFixedSize(36, 36)
        # Removed border from icon_box as requested (relying on parent card border)
        icon_box.setStyleSheet("background-color: rgba(46, 53, 63, 0.8); border: none; border-radius: 6px;")
        icon_lay = QVBoxLayout(icon_box)
        icon_lay.setContentsMargins(0,0,0,0)
        icon_lay.setAlignment(Qt.AlignCenter)
        
        check_lbl = QLabel("✓")
        check_lbl.setStyleSheet("color: #00ffaa; font-family: 'Space Grotesk'; font-size: 20px; font-weight: bold;")
        icon_lay.addWidget(check_lbl)
        
        # 3. Class Name
        # font-headline font-semibold text-xl tracking-wide
        self.name_lbl = QLabel(title)
        self.name_lbl.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 18px; font-weight: 600; letter-spacing: 0.5px;")
        
        # 4. Percentage
        # text-primary-container font-mono font-bold text-2xl drop-shadow-[0_0_5px_rgba(0,255,170,0.5)]
        self.pct_lbl = QLabel(f"{percentage}.0%")
        self.pct_lbl.setStyleSheet("color: #00ffaa; font-family: 'Fira Code'; font-size: 28px; font-weight: bold;")
        self.pct_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        glow_pct = QGraphicsDropShadowEffect()
        glow_pct.setBlurRadius(10)
        glow_pct.setColor(QColor(0, 255, 170, 150))
        glow_pct.setOffset(0, 0)
        self.pct_lbl.setGraphicsEffect(glow_pct)
        
        layout.addWidget(accent)
        layout.addWidget(icon_box)
        layout.addWidget(self.name_lbl)
        layout.addStretch()
        layout.addWidget(self.pct_lbl)

    def init_secondary_ui(self, number, title, percentage):
        self.setFixedHeight(44)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(12)
        
        # Rank Number
        # w-6 h-6 rounded flex items-center justify-center bg-surface-container border border-surface-container-highest text-on-surface-variant font-mono text-xs font-medium shrink-0
        rank_lbl = QLabel(str(number))
        rank_lbl.setFixedSize(24, 24)
        rank_lbl.setAlignment(Qt.AlignCenter)
        rank_lbl.setStyleSheet("background-color: #1c252e; border: 1px solid #2e353f; border-radius: 4px; color: #b9cbbd; font-family: 'Fira Code'; font-size: 11px; font-weight: 500;")
        
        # Class Name
        # font-headline font-medium text-sm text-on-surface w-16 shrink-0
        self.name_lbl = QLabel(title)
        self.name_lbl.setFixedWidth(64)
        self.name_lbl.setStyleSheet("color: #dce3ef; font-family: 'Space Grotesk'; font-size: 14px; font-weight: 500;")
        
        # Progress Bar
        # flex-1 h-1.5 bg-surface-container-highest rounded-full overflow-hidden flex items-center shadow-[inset_0_1px_3px_rgba(0,0,0,0.5)]
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(percentage)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2e353f;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #00ffaa;
                border-radius: 4px;
            }
        """)
        
        # Percentage
        # font-mono text-xs text-on-surface-variant w-14 text-right shrink-0
        self.pct_lbl = QLabel(f"{percentage}.00%")
        self.pct_lbl.setFixedWidth(60)
        self.pct_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pct_lbl.setStyleSheet("color: #b9cbbd; font-family: 'Fira Code'; font-size: 11px;")
        
        layout.addWidget(rank_lbl)
        layout.addWidget(self.name_lbl)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.pct_lbl)

    def update_data(self, title, percentage):
        self.name_lbl.setText(title)
        if self.is_primary:
            self.pct_lbl.setText(f"{percentage:.1f}%")
        else:
            self.pct_lbl.setText(f"{percentage:.2f}%")
            self.progress_bar.setValue(int(percentage))

class MetricRow(QWidget):
    def __init__(self, title, value, value_class, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setProperty("class", "MetrikTitle")
        
        self.val_lbl = QLabel(value)
        self.val_lbl.setProperty("class", value_class)
        
        layout.addWidget(self.title_lbl)
        layout.addStretch()
        layout.addWidget(self.val_lbl)

class SystemStatusItem(QWidget):
    def __init__(self, text, status=True, parent=None):
        super().__init__(parent)
        self.status = status
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Stylized Indicator container
        self.indicator = QFrame()
        self.indicator.setFixedSize(18, 18)
        
        # Symbol label (Tick/Cross)
        self.symbol_lbl = QLabel(self.indicator)
        self.symbol_lbl.setAlignment(Qt.AlignCenter)
        self.symbol_lbl.setFixedSize(18, 18)
        
        self.text_lbl = QLabel(text.upper())
        self.text_lbl.setProperty("class", "StatusItem")
        self.text_lbl.setStyleSheet("color: #DCE3EF; font-family: 'Fira Code'; font-size: 11px; letter-spacing: 0.5px;")
        
        layout.addWidget(self.indicator)
        layout.addWidget(self.text_lbl)
        layout.addStretch()
        
        self.update_ui()
    def set_status(self, status):
        self.status = status
        self.update_ui()

    def update_ui(self):
        if self.status:
            # Connected / OK (Turkuaz)
            self.indicator.setStyleSheet("""
                QFrame {
                    border: 1.5px solid #00FFAA;
                    border-radius: 9px;
                    background-color: rgba(0, 255, 170, 0.1);
                }
            """)
            self.symbol_lbl.setText("✓")
            self.symbol_lbl.setStyleSheet("color: #00FFAA; font-size: 10px; font-weight: bold; background: transparent;")
        else:
            # Disconnected / Error (Red)
            self.indicator.setStyleSheet("""
                QFrame {
                    border: 1.5px solid #690005;
                    border-radius: 9px;
                    background-color: rgba(105, 0, 5, 0.2);
                }
            """)
            self.symbol_lbl.setText("✕")
            self.symbol_lbl.setStyleSheet("color: #ff4d4d; font-size: 10px; font-weight: bold; background: transparent;")


from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter, QColor, QPen, QRadialGradient

class MenuCard(QFrame):
    clicked = Signal()

    def __init__(self, mod_id, title, desc, icon_path="", parent=None):
        super().__init__(parent)
        self.setObjectName("MenuCard")
        self.setFixedSize(280, 240)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(8)
        
        # MOD ID (Top Right inside card)
        self.id_lbl = QLabel(mod_id)
        self.id_lbl.setObjectName("MenuCardID")
        self.id_lbl.setAlignment(Qt.AlignRight)
        
        # Icon
        self.icon_lbl = QLabel()
        self.icon_lbl.setObjectName("MenuCardIcon")
        if icon_path:
            self.icon_lbl.setPixmap(QIcon(icon_path).pixmap(48, 48))
        else:
            self.icon_lbl.setText("◇") # Placeholder
            self.icon_lbl.setStyleSheet("color: #00FFAA; font-size: 32px;")
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("MenuCardTitle")
        
        # Description
        self.desc_lbl = QLabel(desc)
        self.desc_lbl.setObjectName("MenuCardDesc")
        self.desc_lbl.setWordWrap(True)
        
        layout.addWidget(self.id_lbl)
        layout.addSpacing(16)
        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStretch()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class HUDBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HolographicBg")
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        
        # Outer Glowing Radial
        grad = QRadialGradient(cx, cy, min(w, h) // 1.5)
        grad.setColorAt(0, QColor(0, 226, 150, 25))
        grad.setColorAt(0.7, QColor(0, 0, 0, 0))
        painter.fillRect(self.rect(), grad)
        
        # Concentric Circles
        pen = QPen(QColor(0, 226, 150, 40), 1)
        painter.setPen(pen)
        
        for r in [200, 350, 500]:
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)
        
        # Dashed Circle
        dash_pen = QPen(QColor(0, 255, 170, 60), 1, Qt.DashLine)
        dash_pen.setDashPattern([10, 10])
        painter.setPen(dash_pen)
        painter.drawEllipse(cx - 275, cy - 275, 550, 550)

