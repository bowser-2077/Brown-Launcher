from ui_launcher import LauncherUI
from PySide6.QtWidgets import QApplication
import sys
import time

if __name__ == "__main__":
    print("[*] Brown Launcher Console - Beta V3 Launcher")
    time.sleep(1)
    print("[*] Aviable version(s) : Every Vanilla + Fabric Versions")
    time.sleep(2)
    print("[*] New Update : Added Server Creation -> Broken for now")
    print("[*] This window will be used to show you logs, you cant disable it for good reasons")
    app = QApplication(sys.argv)
    window = LauncherUI()
    window.show()
    sys.exit(app.exec())
