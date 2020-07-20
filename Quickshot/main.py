from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from Quickshot import Qshot
import sys

def build_application():
    app = QApplication(sys.argv)


    # instantiate frame
    frame = Qshot(cfg_path="Quickshot/Qshot.cfg")

    # create tray menu
    menu = QMenu()
    take_ss_action = menu.addAction("Take ss")
    take_ss_action.triggered.connect(frame.take_ss)

    hide_show_action = menu.addAction("Hide/Show")
    hide_show_action.triggered.connect(frame.hide_show)

    exit_action = menu.addAction("Exit")
    exit_action.triggered.connect(app.quit)

    # create tray
    tray_icon = QSystemTrayIcon(QIcon("icons/3.ico"), parent = app)
    tray_icon.setToolTip("Quickshot")
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    
    sys.exit(app.exec())



if __name__ == '__main__':
    build_application()
