from PyQt5.QtWidgets import QApplication
from Sshot import Sshot
import sys

def main():
    app = QApplication(sys.argv)
    frame = Sshot(cfg_path="options.cfg")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()