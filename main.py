import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from core.main_window import MainWindow
import os

def main():
    app = QApplication(sys.argv)
    
    # Load custom fonts
    fonts_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(".ttf") or font_file.endswith(".otf"):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id == -1:
                    print(f"Warning: Failed to load font {font_file}")
    
    # Load global stylesheet
    style_path = os.path.join(os.path.dirname(__file__), "assets", "styles", "main.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {style_path}")

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
