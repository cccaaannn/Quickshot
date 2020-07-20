from PyQt5.QtWidgets import QApplication
from Quickshot import Qshot
import sys

def main():
    app = QApplication(sys.argv)
    frame = Qshot(cfg_path="Quickshot/Qshot.cfg")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()