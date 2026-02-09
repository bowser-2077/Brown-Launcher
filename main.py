from ui_launcher import LauncherUI
from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
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

class SplashScreen(QSplashScreen):
    def __init__(self):
        self.pixmap = QPixmap(450, 250)
        self.pixmap.fill(QColor(28, 28, 28))
        super().__init__(self.pixmap)

        self.setFixedSize(450, 250)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)

        self.progress = 0

        # fake loading thing
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance)
        self.timer.start(30)

    def advance(self):
        self.progress += 1
        if self.progress > 100:
            self.timer.stop()
        self.repaint()

    def drawContents(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        # title
        painter.setPen(QColor(240, 240, 240))
        painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, "CascadeMC")

        # sous le titre?
        painter.setFont(QFont("Segoe UI", 11))
        painter.setPen(QColor(180, 180, 180))
        painter.drawText(
            self.rect().adjusted(0, 40, 0, 0),
            Qt.AlignCenter,
            "Minecraft Launcher"
        )

        # bg
        bar_width = 300
        bar_height = 8
        x = (self.width() - bar_width) // 2
        y = self.height() - 50

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(50, 50, 50))
        painter.drawRoundedRect(x, y, bar_width, bar_height, 4, 4)

        # loadb
        fill_width = int(bar_width * (self.progress / 100))
        painter.setBrush(QColor(59, 130, 246))
        painter.drawRoundedRect(x, y, fill_width, bar_height, 4, 4)

        # loadtxt
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor(150, 150, 150))
        painter.drawText(
            self.rect().adjusted(0, 0, 0, -20),
            Qt.AlignBottom | Qt.AlignCenter,
            f"Loading... {self.progress}%"
        )


import os, sys

if __name__ == "__main__":
    print("[*] CascadeMC - logs")
    time.sleep(0.3)
    print("[*] Starting...")
    # we je sais ca charge pas vraiment un truc mais c'est pour l'estetique tkt
    time.sleep(0.5)
    print("[*] Done")
    print("[*] This window will be used to show game logs!")

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    # display splash
    splash = SplashScreen()
    splash.show()
    
    # stackoverflow thing that someone told it was required
    app.processEvents()
    
    # fake waiting time
    QTimer.singleShot(2000, lambda: splash.close())
    
    # display launcher
    window = LauncherUI()
    
    # show launcher after splash close
    QTimer.singleShot(2000, window.show)
    
    sys.exit(app.exec())
