from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, 
                                QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QScrollArea, QStackedLayout, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QRadialGradient, QColor
from components.custom_widgets import (CategoryButton, ProbabilityBar, MetricRow, 
                                       SystemStatusItem, MenuCard, HUDBackground)
from components.camera_widget import CameraWidget
from components.rehber_widgets import StepWidget, BentoCard, EcoStatsCard, SupportCard
from components.analiz_widgets import MetricCard, BarChartCard, DonutChartCard, InsightPanel, StatusPanel
import os

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # 1. LEFT PANEL (Analysis)
        left_widget = QWidget()
        left_widget.setFixedWidth(340)
        left_panel = QVBoxLayout(left_widget)
        left_panel.setContentsMargins(0,0,0,0)
        left_panel.setSpacing(16)
        
        # Probability Analysis
        analysis_card = self.create_hud_card("tahmin", "EN İYİ TAHMİNLER")
        ana_layout = QVBoxLayout()
        # Ensure we add the layout to the card's main layout
        analysis_card.layout().addLayout(ana_layout)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(12)
        
        # Primary Item
        self.primary_pred = ProbabilityBar(1, "Cisim Bekleniyor...", 0, True)
        ana_layout.addWidget(self.primary_pred)
        
        # Secondary Items Container
        sec_layout = QVBoxLayout()
        sec_layout.setContentsMargins(4, 8, 4, 8)
        sec_layout.setSpacing(4)
        
        self.sec_pred1 = ProbabilityBar(2, "-", 0, False)
        self.sec_pred2 = ProbabilityBar(3, "-", 0, False)
        
        sec_layout.addWidget(self.sec_pred1)
        sec_layout.addWidget(self.sec_pred2)
        
        ana_layout.addLayout(sec_layout)
        ana_layout.addStretch()

        left_panel.addWidget(analysis_card)
        left_panel.addStretch()
        
        layout.addWidget(left_widget)
        
        # 2. CENTER PANEL (Camera)
        center_widget = QWidget()
        center_panel = QVBoxLayout(center_widget)
        center_panel.setContentsMargins(0,0,0,0)
        center_panel.setSpacing(16)
        
        # Camera
        self.camera_widget = CameraWidget()
        center_panel.addWidget(self.camera_widget, 1)
        
        layout.addWidget(center_widget, 1) # stretch 1 to fill middle
        
        # 3. RIGHT PANEL (Commands, Status, Categories)
        right_widget = QWidget()
        right_widget.setFixedWidth(340) # Increased from 320 to match left panel and give more room
        right_panel = QVBoxLayout(right_widget)
        right_panel.setContentsMargins(0,0,0,0)
        right_panel.setSpacing(16)
        
        # Command Center
        cmd_card = self.create_hud_card("command", "KOMUTA MERKEZİ")
        cmd_layout = QGridLayout()
        cmd_card.layout().addLayout(cmd_layout)
        cmd_layout.setSpacing(8)
        
        self.btn_start = QPushButton("SİSTEMİ BAŞLAT")
        self.btn_start.setProperty("class", "PrimaryAction")
        self.btn_start.setFixedHeight(40)
        
        self.btn_stop = QPushButton("DURDUR")
        self.btn_stop.setProperty("class", "SecondaryAction")
        self.btn_stop.setFixedHeight(40)
        
        cmd_layout.addWidget(self.btn_start, 0, 0)
        cmd_layout.addWidget(self.btn_stop, 0, 1)
        
        # Sistem Durumu
        status_card = self.create_hud_card("system", "SİSTEM_DURUMU")
        status_layout = QVBoxLayout()
        status_card.layout().addLayout(status_layout)
        status_layout.setSpacing(12)
        
        self.sys_status_arduino = SystemStatusItem("Arduino bağlantısı hazır", status=False)
        self.sys_status_camera = SystemStatusItem("Kamera akışı aktif", status=False)
        self.sys_status_model = SystemStatusItem("AI Model yüklendi", status=False)
        
        status_layout.addWidget(self.sys_status_arduino)
        status_layout.addWidget(self.sys_status_camera)
        status_layout.addWidget(self.sys_status_model)
        
        # Categories
        cat_card = self.create_hud_card("categories", "KATEGORİLER")
        cat_layout = QVBoxLayout()
        cat_card.layout().addLayout(cat_layout)
        cat_layout.setContentsMargins(0, 0, 0, 0)
        cat_layout.setSpacing(4)
        
        self.btn_plastik = CategoryButton("Plastik", "assets/icons/plastic.svg")
        self.btn_kagit = CategoryButton("Kağıt", "assets/icons/paper.svg")
        self.btn_cam = CategoryButton("Cam", "assets/icons/glass.svg")
        self.btn_metal = CategoryButton("Metal", "assets/icons/metal.svg")
        
        cat_layout.addWidget(self.btn_plastik)
        cat_layout.addWidget(self.btn_kagit)
        cat_layout.addWidget(self.btn_cam)
        cat_layout.addWidget(self.btn_metal)
        cat_layout.addStretch()
        
        self.category_buttons = {
            "Plastik": self.btn_plastik,
            "Kağıt": self.btn_kagit,
            "Cam": self.btn_cam,
            "Metal": self.btn_metal
        }
        
        right_panel.addWidget(cmd_card)
        right_panel.addWidget(status_card)
        right_panel.addWidget(cat_card, 1)
        
        layout.addWidget(right_widget)    

    def set_active_category(self, category_name):
        name_map = {
            "plastic": "plastik",
            "paper": "kağıt",
            "glass": "cam",
            "metal": "metal",
            "plastik": "plastik",
            "kağıt": "kağıt",
            "cam": "cam"
        }
        target = name_map.get(category_name.lower(), category_name.lower())
        for name, button in self.category_buttons.items():
            if name.lower() == target:
                button.set_active(True)
            else:
                button.set_active(False)

    def create_hud_card(self, icon_name, title):
        card = QFrame()
        card.setProperty("class", "GlassPanel")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20) # Match p-5
        layout.setSpacing(0)
        
        header = QFrame()
        # Removed border-bottom as requested
        header.setStyleSheet("border: none; padding-bottom: 0px; margin-bottom: 4px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        
        lbl_icon = QLabel()
        lbl_icon.setFixedSize(16, 16)
        if icon_name:
            icon_path = f"assets/icons/{icon_name}.svg"
            if os.path.exists(icon_path):
                lbl_icon.setPixmap(QIcon(icon_path).pixmap(16, 16))
            else:
                lbl_icon.setText("◈")
                lbl_icon.setStyleSheet("color: #00ffaa; font-size: 14px;")
        
        lbl_title = QLabel(title)
        # font-mono text-xs font-bold tracking-widest text-primary uppercase
        lbl_title.setStyleSheet("color: #f6fff6; font-family: 'Fira Code'; font-size: 12px; font-weight: 600; letter-spacing: 2px;")
        
        header_layout.addWidget(lbl_icon)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        
        layout.addWidget(header)
        return card


class MenuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Holographic Background
        self.bg = HUDBackground(self)
        
        # Main Layout container to center everything
        center_cont = QWidget()
        center_layout = QVBoxLayout(center_cont)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(60)
        
        # Top Operator Info
        operator_info = QFrame()
        operator_info.setStyleSheet("background: rgba(21, 28, 37, 0.4); border-left: 4px solid #00FFAA; border-radius: 8px;")
        op_layout = QVBoxLayout(operator_info)
        op_layout.setContentsMargins(24, 16, 24, 16)
        
        op_lbl = QLabel("OPERATÖR: ADMIN")
        op_lbl.setStyleSheet("color: #00FFAA; font-family: 'Space Grotesk'; font-size: 20px; font-weight: bold; letter-spacing: 1px;")
        sys_lbl = QLabel("SİSTEM ÇEVRİMİÇİ // v4.2.0")
        sys_lbl.setStyleSheet("color: rgba(0, 255, 170, 0.6); font-family: 'JetBrains Mono'; font-size: 10px; letter-spacing: 1px;")
        
        op_layout.addWidget(op_lbl)
        op_layout.addWidget(sys_lbl)
        
        # Grid of Cards
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(32)
        
        self.card_dash = MenuCard("MOD_01", "KONTROL PANELİ", "Küresel kaynak genel bakışı ve sinirsel işleme metrikleri.", "assets/icons/dashboard.svg")
        self.card_analiz = MenuCard("MOD_02", "ANALİZ", "Derin öğrenme atık sınıflandırma ve verimlilik raporları.", "assets/icons/analyze.svg")
        self.card_guide = MenuCard("MOD_03", "REHBER", "Standartlaştırılmış operasyonel protokoller ve yapay zeka destekli güvenlik.", "assets/icons/guide.svg")
        self.card_settings = MenuCard("MOD_04", "AYARLAR", "Çekirdek sistem kalibrasyonu ve nöral bağ senkronizasyonu.", "assets/icons/settings.svg")
        
        grid_layout.addWidget(self.card_dash, 0, 0)
        grid_layout.addWidget(self.card_analiz, 0, 1)
        grid_layout.addWidget(self.card_guide, 1, 0)
        grid_layout.addWidget(self.card_settings, 1, 1)
        
        # Assemble
        top_h_layout = QHBoxLayout()
        top_h_layout.addWidget(operator_info)
        top_h_layout.addStretch()
        
        center_layout.addLayout(top_h_layout)
        center_layout.addWidget(grid_widget)
        
        self.layout.addWidget(center_cont)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg.setGeometry(0, 0, self.width(), self.height())

# Placeholder classes for other pages
class PlaceholderPage(QWidget):
    def __init__(self, title, mod_id, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        id_lbl = QLabel(mod_id)
        id_lbl.setStyleSheet("color: rgba(0, 255, 170, 0.3); font-family: 'JetBrains Mono'; font-size: 14px; letter-spacing: 4px;")
        
        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet("color: #00FFAA; font-family: 'Space Grotesk'; font-size: 48px; font-weight: bold; letter-spacing: 2px;")
        
        status_lbl = QLabel("YAPIM AŞAMASINDA")
        status_lbl.setStyleSheet("background-color: rgba(0, 255, 170, 0.1); color: #00FFAA; padding: 10px 30px; border: 1px solid #00FFAA; border-radius: 4px; font-family: 'JetBrains Mono'; font-weight: bold; font-size: 16px;")
        
        self.back_btn = QPushButton("← MENÜYE DÖN")
        self.back_btn.setProperty("class", "SecondaryAction")
        self.back_btn.setFixedWidth(240)
        self.back_btn.setFixedHeight(50)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        
        layout.addWidget(id_lbl)
        layout.addWidget(title_lbl)
        layout.addSpacing(20)
        layout.addWidget(status_lbl)
        layout.addSpacing(40)
        layout.addWidget(self.back_btn)

class AnalizlerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn = QPushButton()  # Dummy button for main_window.py connection
        self.back_btn.hide()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollArea > QWidget > QWidget { background-color: transparent; }
            QScrollBar:vertical {
                border: none;
                background: rgba(25, 32, 41, 0.5);
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3a4a40;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 16, 24, 24) # Reduced top margin to 16px
        content_layout.setSpacing(24) # Match gap-6 (24px)
        
        # Header
        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()
        
        title_lbl = QLabel("Analizler")
        title_lbl.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 36px; font-weight: bold; letter-spacing: -1px; border: none;")
        
        sub_lbl = QLabel("") # Hidden or removed
        sub_lbl.hide()
        
        header_text_layout.addWidget(title_lbl)
        
        status_badge = QFrame()
        status_badge.setFrameShape(QFrame.NoFrame)
        status_badge.setFrameShadow(QFrame.Plain)
        status_badge.setStyleSheet("background-color: rgba(0, 255, 170, 0.08); border-radius: 20px; border: none;")
        status_layout = QHBoxLayout(status_badge)
        status_layout.setContentsMargins(16, 8, 16, 8)
        status_layout.setSpacing(8)
        
        dot = QFrame()
        dot.setFixedSize(8, 8)
        dot.setStyleSheet("background-color: #00ffaa; border-radius: 4px;")
        
        # Pulse-like glow for badge dot
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(10)
        glow.setColor(QColor(0, 255, 170, 255))
        glow.setOffset(0, 0)
        dot.setGraphicsEffect(glow)
        
        status_text = QLabel("CANLI AKIŞ AKTİF")
        # font-label text-xs text-primary-container
        status_text.setStyleSheet("color: #00ffaa; font-family: 'Fira Code'; font-size: 12px; font-weight: bold; letter-spacing: 1px;")
        
        status_layout.addWidget(dot)
        status_layout.addWidget(status_text)
        
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        header_layout.addWidget(status_badge, 0, Qt.AlignBottom) # Match items-end
        
        # Section 1: Top Metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(24)
        
        self.m1 = MetricCard("Toplam Tespit", "analyze", 0)
        self.m2 = MetricCard("En Aktif Kategori", "categories", "-", highlight=True)
        self.m3 = MetricCard("Ortalama Güven", "tahmin", "0%")
        self.m4 = MetricCard("Çalışma Süresi", "system", "0", unit="dk")
        
        metrics_grid.addWidget(self.m1, 0, 0)
        metrics_grid.addWidget(self.m2, 0, 1)
        metrics_grid.addWidget(self.m3, 0, 2)
        metrics_grid.addWidget(self.m4, 0, 3)
        
        # Section 2: Charts
        charts_grid = QGridLayout()
        charts_grid.setSpacing(24)
        charts_grid.setColumnStretch(0, 1) # Equal stretch for column 0
        charts_grid.setColumnStretch(1, 1) # Equal stretch for column 1
        
        self.bar_chart = BarChartCard()
        self.donut_chart = DonutChartCard()
        
        charts_grid.addWidget(self.bar_chart, 0, 0)
        charts_grid.addWidget(self.donut_chart, 0, 1)
        
        # Section 3: Bottom Panels
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(24)
        
        insight = InsightPanel()
        status = StatusPanel()
        
        bottom_layout.addWidget(insight, 1)
        bottom_layout.addWidget(status)
        
        content_layout.addLayout(header_layout)
        content_layout.addLayout(metrics_grid)
        content_layout.addLayout(charts_grid)
        content_layout.addLayout(bottom_layout)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # bg-surface-container-lowest (#080f17)
        painter.fillRect(self.rect(), QColor("#080f17"))
        
        # Ambient Background Lighting (Top Right)
        # bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary-container/15 via-background/80 to-background
        radius = max(self.width(), self.height())
        gradient = QRadialGradient(self.width() * 0.9, 0, radius)
        gradient.setColorAt(0.0, QColor(0, 255, 170, 30)) # #00ffaa at 12%
        gradient.setColorAt(0.4, QColor(13, 20, 28, 200)) # #0d141c with transparency
        gradient.setColorAt(1.0, QColor(13, 20, 28, 255))
        
        painter.fillRect(self.rect(), gradient)

class RehberPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn = QPushButton()  # Dummy button for main_window.py connection
        self.back_btn.hide()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                border: none;
                background: rgba(25, 32, 41, 0.5);
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3a4a40;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(48, 24, 48, 24)
        content_layout.setSpacing(32)
        
        # Section 1: Nasıl Kullanılır
        sec1_layout = QVBoxLayout()
        sec1_layout.setAlignment(Qt.AlignCenter)
        
        title1 = QLabel("NASIL KULLANILIR?")
        title1.setStyleSheet("color: #F6FFF6; font-family: 'Space Grotesk'; font-size: 36px; font-weight: bold; letter-spacing: -0.09px; line-height: 40px;")
        title1.setAlignment(Qt.AlignCenter)
        sec1_layout.addWidget(title1)
        sec1_layout.addSpacing(16)
        
        # Create a container for the steps and the neon line
        steps_wrapper = QWidget()
        steps_wrapper.setFixedHeight(220) # Increased from 160 to prevent overlap of icons and labels
        
        wrapper_layout = QStackedLayout(steps_wrapper)
        wrapper_layout.setStackingMode(QStackedLayout.StackAll)
        
        # Layer 0: Neon line
        line_layer = QWidget()
        line_layout = QVBoxLayout(line_layer)
        line_layout.setContentsMargins(0, 96, 0, 0) # Back to 96 to be perfectly tangent as requested
        line_layout.setAlignment(Qt.AlignTop)
        
        neon_line = QFrame()
        neon_line.setFixedHeight(1) # Thinner as per Figma W:1184 H:1
        # Gradient that is slightly shorter than before to be more balanced
        neon_line.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 255, 170, 0), stop:0.4 rgba(0, 255, 170, 120), stop:0.5 rgba(0, 255, 170, 120), stop:0.6 rgba(0, 255, 170, 120), stop:1 rgba(0, 255, 170, 0)); border: none;")
        line_layout.addWidget(neon_line)
        
        # Layer 1: Steps (Placed before line in stack to be underneath? No, wait.)
        # Actually, in StackAll, the last added is on top. So if line is on top, it was added last.
        # I will ensure steps_layer is added AFTER line_layer to be on top.
        
        steps_layer = QWidget()
        steps_layout = QHBoxLayout(steps_layer)
        steps_layout.setContentsMargins(0, 0, 0, 0)
        
        step1 = StepWidget("01", "Atığı Yerleştir", "step1")
        step2 = StepWidget("02", "Analizi Bekle", "step2", has_scan_effect=True)
        step3 = StepWidget("03", "Doğru Hazneye", "step3")
        
        steps_layout.addWidget(step1)
        steps_layout.addStretch()
        steps_layout.addWidget(step2)
        steps_layout.addStretch()
        steps_layout.addWidget(step3)
        
        wrapper_layout.addWidget(line_layer) # Bottom layer
        wrapper_layout.addWidget(steps_layer) # Top layer
        
        sec1_layout.addWidget(steps_wrapper)
        
        # Section 2: Atık Ayrıştırma Kuralları
        sec2_layout = QVBoxLayout()
        
        title2 = QLabel("ATIK AYRIŞTIRMA KURALLARI")
        title2.setStyleSheet("color: #f6fff6; font-family: 'Space Grotesk'; font-size: 32px; font-weight: bold; letter-spacing: -0.5px;")
        sec2_layout.addWidget(title2)
        sec2_layout.addSpacing(4)
        
        grid_cards = QGridLayout()
        grid_cards.setSpacing(16)
        
        card1 = BentoCard("PLASTİK", "plastic", "#00ffaa", "Şişeleri ezip atın.", "Sıvı içeren kapları boşaltın", bg_name="plastic-bg.png")
        card2 = BentoCard("KAĞIT", "paper", "#00daf3", "Kutuları parçalayın.", "Yağlı ambalajları atmayın", bg_name="paper-bg.png")
        card3 = BentoCard("METAL", "metal", "#ffb4a2", "Kapakları ayırmayın.", "Yanıcı tüpleri ayrıştırın", bg_name="metal-bg.png")
        card4 = BentoCard("CAM", "glass", "#f6fff6", "Renklerine göre ayırın.", "Kırık camlara dikkat edin", bg_name="glass-bg.png")
        
        grid_cards.addWidget(card1, 0, 0)
        grid_cards.addWidget(card2, 0, 1)
        grid_cards.addWidget(card3, 0, 2)
        grid_cards.addWidget(card4, 0, 3)
        
        sec2_layout.addLayout(grid_cards)
        
        # Section 3: Eco-stats & Support
        sec3_layout = QHBoxLayout()
        sec3_layout.setSpacing(32)
        
        eco_stats = EcoStatsCard()
        
        sec3_layout.addWidget(eco_stats)
        sec3_layout.addStretch()
        
        content_layout.addLayout(sec1_layout)
        content_layout.addLayout(sec2_layout)
        content_layout.addLayout(sec3_layout)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

class AyarlarPage(PlaceholderPage):
    def __init__(self, parent=None):
        super().__init__("Ayarlar", "MOD_04", parent)
