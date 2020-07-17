from PyQt5.QtWidgets import QApplication
from Sshot import Sshot
import sys

app = QApplication(sys.argv)
frame = Sshot()
sys.exit(app.exec()) 