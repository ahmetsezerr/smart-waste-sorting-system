from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                               QLabel, QPushButton, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
class StepWidget(QWidget):
    def __init__(self, step_num, title, icon_name, has_scan_effect=False, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(0) 
        
        # Circular Glass Card for Icon
        self.icon_card = QFrame()
        self.icon_card.setFixedSize(96, 96)
        self.icon_card.setStyleSheet("""
            QFrame {
                background-color: rgba(21, 28, 37, 0.95); /* Opaque background to hide the global line behind it */
                border: 1px solid rgba(58, 74, 64, 0.15);
                border-radius: 48px;
            }
        """)
        self.icon_card.setProperty("class", "StepIconCard")
        
        icon_layout = QVBoxLayout(self.icon_card)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        self.icon_lbl = QLabel()
        self.icon_lbl.setFixedSize(48, 48)
        self.icon_lbl.setStyleSheet("background: transparent; border: none;") # Ensure no background box
        self.icon_lbl.setPixmap(QIcon(f"assets/guide/{icon_name}.svg").pixmap(48, 48))
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(self.icon_lbl)
        
        if has_scan_effect:
            # Mask the icon_card to a perfect circle to clip the scan line
            from PySide6.QtGui import QRegion
            self.icon_card.setMask(QRegion(0, 0, 96, 96, QRegion.Ellipse))
            
            self.scan_line = QFrame(self.icon_card)
            self.scan_line.setFixedHeight(2)
            self.scan_line.setStyleSheet("background-color: rgba(0, 255, 170, 180); border: none;")
            
            effect = QGraphicsDropShadowEffect()
            effect.setColor(QColor(0, 255, 170, 255))
            effect.setBlurRadius(25) # Daha geniş bir parlama
            effect.setOffset(0, 0)
            self.scan_line.setGraphicsEffect(effect)
            
            self.scan_line.setGeometry(0, 0, 96, 2)
            self.scan_line.raise_() # İkonun tam üzerinde taraması için en üste alıyoruz
            
            self.anim = QPropertyAnimation(self.scan_line, b"geometry")
            self.anim.setDuration(3000)
            self.anim.setStartValue(QRect(0, 0, 96, 2))
            self.anim.setKeyValueAt(0.5, QRect(0, 94, 96, 2))
            self.anim.setEndValue(QRect(0, 0, 96, 2))
            self.anim.setLoopCount(-1)
            self.anim.start()
        
        # Step Number
        self.step_lbl = QLabel(f"ADIM {step_num}")
        self.step_lbl.setStyleSheet("color: #00FFAA; font-family: 'JetBrains Mono'; font-size: 12px; font-weight: normal; letter-spacing: 1.2px; background: transparent;")
        self.step_lbl.setAlignment(Qt.AlignCenter)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 20px; font-weight: bold; background: transparent;")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.icon_card, 0, Qt.AlignCenter)
        layout.addSpacing(24) # Slightly reduced from 32 to fit 220px height better
        layout.addWidget(self.step_lbl)
        layout.addSpacing(4)  # Reduced from 8 to tighten the text grouping
        layout.addWidget(self.title_lbl)
        layout.addStretch()

class BentoCard(QFrame):
    def __init__(self, title, icon_name, color_hex, tip_text, warning_text, bg_name=None, parent=None):
        super().__init__(parent)
        self.setProperty("class", "BentoCardGlass")
        self.setFixedSize(278, 310)
        self.setStyleSheet(f"""
            QFrame.BentoCardGlass {{
                background-color: rgba(46, 53, 63, 0.4);
                border: 1px solid rgba(58, 74, 64, 0.15);
                border-left: 4px solid {color_hex};
                border-radius: 20px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Image / Icon Container
        self.img_container = QFrame()
        self.img_container.setFixedSize(225, 110)
        self.img_container.setStyleSheet("background-color: #192029; border-radius: 12px;")
        img_layout = QGridLayout(self.img_container)
        img_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background Image
        self.bg_img = QLabel()
        self.bg_img.setAlignment(Qt.AlignCenter)
        self.bg_img.setScaledContents(True)
        self.bg_img.setStyleSheet("border-radius: 12px; background-color: transparent;")
        
        if bg_name:
            self.bg_img.setPixmap(QPixmap(f"assets/guide/{bg_name}"))
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.4)
            self.bg_img.setGraphicsEffect(opacity_effect)
            
        # Foreground Icon
        self.main_icon = QLabel()
        self.main_icon.setFixedSize(50, 50)
        self.main_icon.setAlignment(Qt.AlignCenter)
        self.main_icon.setPixmap(QIcon(f"assets/guide/{icon_name}.svg").pixmap(50, 50))
        self.main_icon.setStyleSheet("background-color: transparent; border: none;")
        
        # Add both to cell (0,0) to overlay them
        img_layout.addWidget(self.bg_img, 0, 0)
        img_layout.addWidget(self.main_icon, 0, 0, Qt.AlignCenter)
        
        # Title
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(f"color: {color_hex}; font-family: 'Space Grotesk'; font-size: 24px; font-weight: bold;")
        
        # Tip Box
        self.tip_box = QFrame()
        self.tip_box.setStyleSheet("background-color: #242a34; border: 1px solid rgba(58, 74, 64, 0.1); border-radius: 8px;")
        tip_layout = QVBoxLayout(self.tip_box)
        tip_layout.setContentsMargins(12, 8, 12, 8)
        tip_layout.setSpacing(2)
        
        tip_title = QLabel("KRİTİK İPUCU")
        tip_title.setStyleSheet("color: #b9cbbd; font-family: 'JetBrains Mono'; font-size: 10px; letter-spacing: -0.5px;")
        tip_desc = QLabel(tip_text)
        tip_desc.setStyleSheet("color: #dce3ef; font-family: 'Inter'; font-size: 12px; font-weight: 500;")
        tip_desc.setWordWrap(True)
        
        tip_layout.addWidget(tip_title)
        tip_layout.addWidget(tip_desc)
        
        # Warning Box
        self.warn_box = QFrame()
        self.warn_box.setFixedHeight(34)
        self.warn_box.setStyleSheet("background-color: rgba(147, 0, 10, 0.1); border: 1px solid rgba(255, 180, 171, 0.2); border-radius: 8px;")
        warn_layout = QHBoxLayout(self.warn_box)
        warn_layout.setContentsMargins(12, 0, 12, 0)
        warn_layout.setAlignment(Qt.AlignVCenter)
        warn_layout.setSpacing(8)
        
        warn_icon = QLabel()
        warn_icon.setFixedSize(14, 14)
        warn_icon.setPixmap(QIcon("assets/guide/warning.svg").pixmap(14, 14))
        warn_icon.setStyleSheet("border: none; background-color: transparent;")
        
        warn_desc = QLabel(warning_text)
        warn_desc.setStyleSheet("color: #ffb4ab; font-family: 'Inter'; font-size: 12px; font-weight: 600; border: none; background-color: transparent;")
        
        warn_layout.addWidget(warn_icon)
        warn_layout.addWidget(warn_desc)
        warn_layout.addStretch()
        
        layout.addWidget(self.img_container)
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.tip_box)
        layout.addWidget(self.warn_box)
        layout.addStretch()

class EcoStatsCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "GlassPanel")
        self.setStyleSheet("""
            QFrame.GlassPanel {
                background-color: rgba(46, 53, 63, 0.4);
                border: 1px solid rgba(58, 74, 64, 0.15);
                border-radius: 16px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 24, 32, 24)
        layout.setSpacing(32)
        
        # Left Stats
        left_layout = QVBoxLayout()
        left_layout.setSpacing(4)
        val_lbl1 = QLabel("1 TON")
        val_lbl1.setStyleSheet("color: #00daf3; font-family: 'Space Grotesk'; font-size: 40px; font-weight: 900; letter-spacing: -1px;")
        desc_lbl1 = QLabel("GERİ DÖNÜŞEN KAĞIT")
        desc_lbl1.setStyleSheet("color: #dce3ef; font-family: 'Inter'; font-size: 14px; font-weight: bold;")
        
        left_layout.addWidget(val_lbl1)
        left_layout.addWidget(desc_lbl1)
        left_layout.addStretch()
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setStyleSheet("background-color: rgba(58, 74, 64, 0.4);")
        divider.setFixedWidth(2)
        
        # Right Stats
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignVCenter)
        right_layout.setSpacing(4)
        
        val_container = QHBoxLayout()
        val_container.setSpacing(8)
        val_icon = QLabel()
        val_icon.setFixedSize(32, 32)
        val_icon.setPixmap(QIcon("assets/icons/yaprak.svg").pixmap(32, 32))
        val_lbl2 = QLabel("= 17")
        val_lbl2.setStyleSheet("color: #00ffaa; font-family: 'Space Grotesk'; font-size: 32px; font-weight: bold;")
        val_container.addWidget(val_icon)
        val_container.addWidget(val_lbl2)
        val_container.addStretch()
        
        desc_lbl2 = QLabel("KAZANILAN AĞAÇ")
        desc_lbl2.setStyleSheet("color: #f6fff6; font-family: 'Inter'; font-size: 14px; font-weight: bold;")
        
        right_layout.addLayout(val_container)
        right_layout.addWidget(desc_lbl2)
        right_layout.addStretch()
        
        layout.addLayout(left_layout)
        layout.addWidget(divider)
        layout.addLayout(right_layout)

class SupportCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "GlassPanel")
        self.setStyleSheet("""
            QFrame.GlassPanel {
                background-color: rgba(46, 53, 63, 0.4);
                border: 1px solid rgba(58, 74, 64, 0.15);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        
        title_lbl = QLabel("TEKNİK DESTEK")
        title_lbl.setStyleSheet("color: #dce3ef; font-family: 'Space Grotesk'; font-size: 18px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignCenter)
        
        # QR Placeholder
        qr_container = QFrame()
        qr_container.setFixedSize(140, 140)
        qr_container.setStyleSheet("background-color: rgba(246, 255, 246, 0.05); border: 1px solid rgba(0, 255, 170, 0.2); border-radius: 12px;")
        qr_layout = QVBoxLayout(qr_container)
        qr_layout.setAlignment(Qt.AlignCenter)
        qr_img = QLabel()
        qr_img.setFixedSize(100, 100)
        # Fallback QR code icon
        qr_img.setPixmap(QIcon("assets/icons/qr_code.svg").pixmap(100, 100))
        qr_layout.addWidget(qr_img)
        
        sys_id = QLabel("SYSTEM ID: SR-AI-9942")
        sys_id.setStyleSheet("color: #b9cbbd; font-family: 'JetBrains Mono'; font-size: 11px; letter-spacing: 1px;")
        sys_id.setAlignment(Qt.AlignCenter)
        
        btn_support = QPushButton("DESTEK TALEBİ")
        btn_support.setProperty("class", "PrimaryAction")
        btn_support.setFixedHeight(45)
        
        layout.addWidget(title_lbl)
        layout.addWidget(qr_container, 0, Qt.AlignCenter)
        layout.addWidget(sys_id)
        layout.addWidget(btn_support)
