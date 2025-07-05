from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.launcher import start_minecraft

class LauncherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brown Launcher Alpha")
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # logo
        logo = QLabel()
        pixmap = QPixmap("assets/logo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation) # <- J'en ai marre sa s'affiche une fois sur 10
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # pseudo
        self.pseudo_input = QLineEdit()
        self.pseudo_input.setPlaceholderText("Minecraft Username...")
        layout.addWidget(self.pseudo_input)

        # ram
        ram_layout = QHBoxLayout()
        ram_layout.addWidget(QLabel("Allowed ram:"))
        self.ram_select = QComboBox()
        self.ram_select.addItems(["1024M", "2G", "4G", "6G", "8G"])
        ram_layout.addWidget(self.ram_select)
        layout.addLayout(ram_layout)

        # bouton demarer
        self.start_btn = QPushButton("Launch Minecraft")
        self.start_btn.clicked.connect(self.launch_game)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

    def launch_game(self):
        pseudo = self.pseudo_input.text() or "OfflinePlayer"
        ram = self.ram_select.currentText()
        self.start_btn.setText("Installing Minecraft, this may take a while...")
        self.start_btn.setEnabled(False)
        start_minecraft(pseudo, ram)
        self.start_btn.setText("Launch Game")
        self.start_btn.setEnabled(True)
