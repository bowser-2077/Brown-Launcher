import os, json, subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QComboBox, QProgressBar, QMessageBox, QTextEdit,
    QApplication, QCheckBox, QTabWidget
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer, QUrl, QThread, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from core.launcher import start_minecraft, get_all_profiles, install_version
import minecraft_launcher_lib.fabric as fabric_lib

base_dir = os.path.abspath(os.path.dirname(__file__))
VERSIONS_FILE = os.path.join(base_dir, "versions.json")
mc_base_version = "1.16.5"


class LauncherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brown Launcher V1 Release")
        self.setFixedSize(600, 600)
        self.java_args = ""
        self.show_modded = True
        self.base_pseudo = "Player"
        self.network_manager = QNetworkAccessManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.init_play_tab()
        self.init_server_tab()

    # === Onglet "Play"
    def init_play_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Logo
        logo = QLabel()
        logo_path = os.path.join(base_dir, "assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if pixmap and not pixmap.isNull():
                logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                logo.setText("No Logo!")
        else:
            logo.setText("Missing Logo!")
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

        # Profil
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Version :")
        profile_label.setFixedWidth(80)
        self.profile_select = QComboBox()
        self.refresh_profiles()
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.profile_select)
        layout.addLayout(profile_layout)

        # ProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Bouton Lancer
        self.start_btn = QPushButton("Start Minecraft")
        self.start_btn.setFixedHeight(40)
        self.start_btn.clicked.connect(self.launch_game)
        layout.addWidget(self.start_btn)

        # Bouton Paramètres
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(self.settings_btn)

        # Zone Paramètres
        self.settings_widget = QWidget()
        self.settings_widget.setVisible(False)
        settings_layout = QVBoxLayout()

        self.show_modded_check = QCheckBox("Display Modded Versions")
        settings_layout.addWidget(self.show_modded_check)

        self.java_args_input = QLineEdit()
        self.java_args_input.setPlaceholderText("Java Args")
        settings_layout.addWidget(self.java_args_input)

        self.base_pseudo_input = QLineEdit()
        self.base_pseudo_input.setPlaceholderText("Default Username")
        settings_layout.addWidget(self.base_pseudo_input)

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        settings_layout.addWidget(apply_btn)

        self.settings_widget.setLayout(settings_layout)
        layout.addWidget(self.settings_widget)

        self.tabs.addTab(tab, "Play")

    # === Onglet "Serveur"
    def init_server_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.server_version = QComboBox()
        self.load_server_versions()
        layout.addWidget(QLabel("PaperMC Version"))
        layout.addWidget(self.server_version)

        self.server_ram = QComboBox()
        self.server_ram.addItems(["1024M", "2G", "4G", "6G", "8G"])
        layout.addWidget(QLabel("RAM Serveur"))
        layout.addWidget(self.server_ram)

        btn = QPushButton("Start Server")
        btn.clicked.connect(self.start_server)
        layout.addWidget(btn)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        self.tabs.addTab(tab, "Server")

    def show_settings(self):
        self.settings_widget.setVisible(not self.settings_widget.isVisible())

    def apply_settings(self):
        self.show_modded = self.show_modded_check.isChecked()
        self.java_args = self.java_args_input.text().strip()
        self.base_pseudo = self.base_pseudo_input.text().strip()

    def refresh_profiles(self):
        self.profile_select.clear()
        for p in get_all_profiles():
            if not self.show_modded and "-" in p:
                continue
            self.profile_select.addItem(p)

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

    def launch_game(self):
        pseudo = self.pseudo_input.text().strip() or self.base_pseudo or "Player"
        ram = self.ram_select.currentText()
        profile = self.profile_select.currentText().strip()

        self.start_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Starting...")

        self.thread = LaunchThread(pseudo, ram, profile)
        self.thread.finished.connect(self.on_launch_done)
        self.thread.error.connect(self.on_launch_error)
        self.thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_progress)
        self.timer.start(100)

    def animate_progress(self):
        self.progress_bar.setValue((self.progress_bar.value() + 3) % 100)

    def on_launch_done(self):
        self.timer.stop()
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)

    def on_launch_error(self, msg):
        self.timer.stop()
        self.progress_bar.setVisible(False)
        self.start_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Error :\n{msg}")

    def load_server_versions(self):
        try:
            with open(VERSIONS_FILE, "r") as f:
                data = json.load(f)
            for v in sorted(data["versions"], reverse=True):
                self.server_version.addItem(v)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error :\n{e}")
            self.server_version.addItem(mc_base_version)

    def start_server(self):
        version = self.server_version.currentText()
        ram = self.server_ram.currentText()
        try:
            with open(VERSIONS_FILE, "r") as f:
                data = json.load(f)
            url = data["versions"][version]
            jar_name = f"paper-{version}.jar"
            jar_path = os.path.join("server", jar_name)
            os.makedirs("server", exist_ok=True)

            if not os.path.exists(jar_path) or os.path.getsize(jar_path) < 10000:
                import requests
                r = requests.get(url)
                with open(jar_path, "wb") as f_out:
                   f_out.write(r.content)

            # ❗ jar_name et pas jar_path
            cmd = ["java", f"-Xmx{ram}", "-jar", jar_name, "nogui"]
            self.console.clear()
            self.proc = subprocess.Popen(
                cmd, cwd="server",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            QTimer.singleShot(100, self.poll_console)

        except Exception as e:
            self.console.append(f"[Error] {e}")




    def poll_console(self):
        if self.proc.poll() is None:
            line = self.proc.stdout.readline()
            if line:
                self.console.append(line.rstrip())
            QTimer.singleShot(50, self.poll_console)
        else:
            self.console.append("[*] Serveur arrêté")


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
