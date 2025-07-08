from ui_launcher import LauncherUI
from PySide6.QtWidgets import QApplication
import sys
import time


STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QLineEdit, QComboBox, QTextEdit {
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #3a3a3a;
    background-color: #2b2b2b;
}
QPushButton {
    background-color: #3b82f6;
    color: white;
    padding: 10px;
    border-radius: 6px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2563eb;
}
QProgressBar {
    border: 1px solid #444;
    border-radius: 5px;
    background-color: #2a2a2a;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #00bfa5;
    width: 20px;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background-color: #2c2c2c;
    padding: 10px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background-color: #3b82f6;
    color: white;
}

QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #3b82f6;
    min-height: 25px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #1e1e1e;
    height: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:horizontal {
    background: #3b82f6;
    min-width: 25px;
    border-radius: 5px;
}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

"""

if __name__ == "__main__":
    print("[*] Brown Launcher Console - Release V1 Launcher")
    time.sleep(0.3)
    print("[*] Aviable version(s) : Every Vanilla + Fabric Versions + Server Support")
    time.sleep(0.5)
    print("[*] New Update : Added Server Creation -> Broken for now")
    print("[*] This window will be used to show you logs, you cant disable it for good reasons")

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    window = LauncherUI()
    window.show()
    sys.exit(app.exec())
