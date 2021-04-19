from PyQt5.QtWidgets import QApplication
from Quickshot import Qshot
import sys

def build_application(cfg_path, icon_path):
    app = QApplication(sys.argv)
    frame = Qshot(cfg_path=cfg_path, icon_path=icon_path)
    sys.exit(app.exec())

is_dev = True
if __name__ == '__main__':
    if(is_dev):
        # dev
        build_application("Quickshot/cfg/Qshot.cfg", "Quickshot/icons/Qs.ico")
    else:
        # compile
        build_application("cfg/Qshot.cfg", "icons/Qs.ico") 
