import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QComboBox, QProgressBar, QMessageBox, QApplication
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer, QUrl, QThread, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from core.launcher import start_minecraft, get_all_profiles, install_version
import minecraft_launcher_lib.fabric as fabric_lib

mc_base_version = "1.16.5"  # Pour bouton Fabric


class LauncherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brown Launcher Alpha")
        self.setFixedSize(500, 580)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #555;
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #3c3c3c;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #505050;
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
        """)
        self.network_manager = QNetworkAccessManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Logo
        logo = QLabel()
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo.setPixmap(pixmap)
            else:
                logo.setText("⚠️ No Logo!")
        else:
            logo.setText("⚠️ Missing Logo!")
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Pseudo
        self.pseudo_input = QLineEdit()
        self.pseudo_input.setPlaceholderText("Minecraft Username")
        self.pseudo_input.textChanged.connect(self.update_skin_preview)
        layout.addWidget(self.pseudo_input)

        # Skin preview
        self.skin_label = QLabel("Enter a username to display the skin")
        self.skin_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.skin_label)

        # RAM
        ram_layout = QHBoxLayout()
        ram_label = QLabel("RAM :")
        ram_label.setFixedWidth(80)
        self.ram_select = QComboBox()
        self.ram_select.addItems(["1024M", "2G", "4G", "6G", "8G"])
        ram_layout.addWidget(ram_label)
        ram_layout.addWidget(self.ram_select)
        layout.addLayout(ram_layout)

        # Sélecteur de profil
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Version :")
        profile_label.setFixedWidth(80)
        self.profile_select = QComboBox()
        self.refresh_profiles()
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.profile_select)
        layout.addLayout(profile_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Bouton de lancement
        self.start_btn = QPushButton("Start Minecraft")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setMaximumWidth(200)
        self.start_btn.setStyleSheet(self.start_btn.styleSheet() + """
            QPushButton {
                font-size: 16px;
            }
        """)
        self.start_btn.clicked.connect(self.launch_game)
        self.start_btn.setCursor(Qt.PointingHandCursor)

        # Centrage du bouton
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_skin_preview(self, username):
        username = username.strip()
        if not username:
            self.skin_label.setPixmap(QPixmap())
            self.skin_label.setText("Enter a username to display the skin")
            return

        url = QUrl(f"https://minotar.net/helm/{username}/64.png")
        request = QNetworkRequest(url)
        reply = self.network_manager.get(request)

        def on_finished():
            img = QImage()
            img.loadFromData(reply.readAll())
            pixmap = QPixmap.fromImage(img)
            self.skin_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            reply.deleteLater()

        reply.finished.connect(on_finished)

    def refresh_profiles(self):
        self.profile_select.clear()
        try:
            for profile in get_all_profiles():
                self.profile_select.addItem(profile)
        except Exception as e:
            QMessageBox.critical(self, "Error!", f"Error when loading versions :\n{e}")
            self.profile_select.addItem("1.20.1")

    def install_fabric(self):
        try:
            loader = fabric_lib.get_latest_loader_version()
            fabric_lib.install_fabric(
                minecraft_version=mc_base_version,
                loader_version=loader,
                minecraft_directory=os.path.abspath("minecraft_data")
            )
            QMessageBox.information(self, "Success", "Fabric successfully installed")
            self.refresh_profiles()
        except Exception as e:
            QMessageBox.critical(self, "Error Fabric", f"Cant install fabric :\n{e}")

    def launch_game(self):
        pseudo = self.pseudo_input.text().strip() or "Player"
        ram = self.ram_select.currentText()
        raw_profile = self.profile_select.currentText()
        profile = raw_profile.replace(" 📥", "").strip()

        self.start_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Preparing.....")

        # Thread de lancement
        self.launch_thread = LaunchThread(pseudo, ram, profile)
        self.launch_thread.finished.connect(self.on_launch_done)
        self.launch_thread.error.connect(self.on_launch_error)
        self.launch_thread.start()

        # Animation de la progress bar
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.animate_progress)
        self.progress_timer.start(100)

    def animate_progress(self):
        val = self.progress_bar.value()
        self.progress_bar.setValue((val + 5) % 100)

    def on_launch_done(self):
        self.progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)

    def on_launch_error(self, msg):
        self.progress_timer.stop()
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Failed to launch :\n{msg}")


class LaunchThread(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, pseudo, ram, profile):
        super().__init__()
        self.pseudo = pseudo
        self.ram = ram
        self.profile = profile

    def run(self):
        try:
            install_version(self.profile)
            start_minecraft(self.pseudo, self.ram, self.profile)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
