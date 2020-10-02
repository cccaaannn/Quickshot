from PyQt5.QtWidgets import QApplication
from Quickshot import Qshot
import sys

def build_application(cfg_path, icon_path):
    app = QApplication(sys.argv)
    frame = Qshot(cfg_path=cfg_path, icon_path=icon_path)
    sys.exit(app.exec())

if __name__ == '__main__':
    build_application("Quickshot/cfg/Qshot.cfg", "Quickshot/icons/Qs.ico")

    # pyinstaller
    # build_application("cfg/Qshot.cfg", "icons/Qs.ico")