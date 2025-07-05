from ui_launcher import LauncherUI
from PySide6.QtWidgets import QApplication
import sys
import time

if __name__ == "__main__":
    print("[*] Brown Launcher Console - Alpha Launcher")
    time.sleep(1)
    print("[*] Aviable version(s) : 1.16.5 - More are comming")
    time.sleep(2)
    print("[*] This window will be used to show you logs, you cant disable it for good reasons")
    app = QApplication(sys.argv)
    window = LauncherUI()
    window.show()
    sys.exit(app.exec())
