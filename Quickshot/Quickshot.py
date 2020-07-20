# pyqt5
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QSizeGrip                   
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QFont
from PyQt5 import QtCore

# other imports
from pynput import keyboard
import json
import sys
import os

# my classes
from global_keylistener import global_keylistener
from ss_handler import ss_handler


class Qshot(QWidget):

    def __init__(self, cfg_path="options.cfg"):
        super().__init__()

        self.cfg_path = cfg_path
        self.set_options()
        
        self.init_variables()
        self.init_ui()

        self.init_global_keylistener()
        self.init_ss_handler()





    # set up frame and options
    def set_options(self):
        """Reads cfg file and makes assignment to local variables
        shows error popup if cfg file has errors
        """
        try:
            # read cfg file
            with open(self.cfg_path,"r") as file:
                cfg = json.load(file)

            # general
            self.opacity = cfg["general"]["opacity"]
            self.background_color = cfg["general"]["background_color"]
            self.accent_color = cfg["general"]["accent_color"]
            self.ss_hotkey = cfg["general"]["ss_hotkey"]
            self.hide_hotkey = cfg["general"]["hide_hotkey"]

            # ss options
            self.ss_extension = cfg["ss_options"]["ss_extension"]
            self.save_path = os.path.normpath(cfg["ss_options"]["save_path"]) # convert to path
            self.create_root_file = cfg["ss_options"]["create_root_file"]
            self.before_ss_name = cfg["ss_options"]["before_ss_name"]
            self.after_ss_name = cfg["ss_options"]["after_ss_name"]
            self.before_number = cfg["ss_options"]["before_number"]
            self.after_number = cfg["ss_options"]["after_number"]
            self.date_formatting = cfg["ss_options"]["date_formatting"]
            self.use_system_local_date_naming = cfg["ss_options"]["use_system_local_date_naming"]
            self.png_compression_level = cfg["ss_options"]["png_compression_level"]
            self.multi_screen = cfg["ss_options"]["multi_screen"]

        except Exception as e:
            print(e)

            self.show_alert_popup("There is a problem with cfg file")
            sys.exit()

    def init_ui(self):
        """inits ui"""

        # set main frame options
        self.setStyleSheet(self.window_style)
        self.setWindowOpacity(self.opacity)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # init ui elements
        self.layouts()
        self.labels()
        self.buttons()
        self.sizegrips()
        self.setup_ui()
        self.show()

    def init_variables(self):
        """init variables"""
        self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color, self.accent_color)
        self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color, self.accent_color)
        self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color, self.accent_color)

    def init_global_keylistener(self):
        """inits global keylistener on a QThread"""
        self.global_keylistener_thread = global_keylistener(self.ss_hotkey, self.hide_hotkey)
        self.global_keylistener_thread.start()

        # connect emitters to local class functions
        self.global_keylistener_thread.ss_trigger.connect(self.take_ss)
        self.global_keylistener_thread.hide_trigger.connect(self.hide_show)
        self.global_keylistener_thread.error_trigger.connect(self.global_keylistener_error)

    def init_ss_handler(self):
        """inits ss_handler 
        ss_handler handles taking ss and saving it to given path
        """
        self.ss_handler = ss_handler()
        self.ss_handler.set_options(ss_extension = self.ss_extension,
                            save_path = self.save_path, 
                            create_root_file = self.create_root_file, 
                            before_ss_name = self.before_ss_name, 
                            after_ss_name = self.after_ss_name, 
                            before_number = self.before_number, 
                            after_number = self.after_number, 
                            date_formatting = self.date_formatting,
                            use_system_local_date_naming = self.use_system_local_date_naming,
                            png_compression_level = self.png_compression_level, 
                            multi_screen = self.multi_screen)



    # add ui elements
    def setup_ui(self):
        """set up ui"""
        self.horizontal_layout_top.addWidget(self.sizegrip1)
        self.horizontal_layout_top.addStretch()
        self.horizontal_layout_top.addWidget(self.info_label)
        self.horizontal_layout_top.addStretch()
        self.horizontal_layout_top.addWidget(self.sizegrip2)

        self.horizontal_layout_bottom.addWidget(self.sizegrip3)
        self.horizontal_layout_bottom.addStretch()
        self.horizontal_layout_bottom.addWidget(self.ss_button)
        self.horizontal_layout_bottom.addStretch()
        self.horizontal_layout_bottom.addWidget(self.sizegrip4)

        self.vertical_layout.addLayout(self.horizontal_layout_top)
        self.vertical_layout.addStretch()
        self.vertical_layout.addLayout(self.horizontal_layout_bottom)

        self.setLayout(self.vertical_layout)

    def layouts(self):
        """adds layouts"""
        self.horizontal_layout_top = QHBoxLayout()
        self.horizontal_layout_bottom = QHBoxLayout()

        self.vertical_layout = QVBoxLayout()
    
    def labels(self):
        """adds labels"""
        self.info_label = QLabel()
        self.info_label.setText("Qshot")
        self.info_label.resize(150,150)
        self.info_label.setFont(QFont('Arial', 12)) 
        self.info_label.setStyleSheet(self.label_style)

    def buttons(self):
        """adds buttons"""
        self.ss_button = QPushButton(self)
        self.ss_button.setText("shot")
        self.ss_button.setObjectName("ss_button")
        self.ss_button.setFont(QFont('Arial', 12)) 
        self.ss_button.setStyleSheet(self.button_style)
        self.ss_button.clicked.connect(self.on_button_click)

    def sizegrips(self):
        """adds sizegrips"""
        self.sizegrip1 = QSizeGrip(self)
        self.sizegrip1.setVisible(True)

        self.sizegrip2 = QSizeGrip(self)
        self.sizegrip2.setVisible(True)

        self.sizegrip3 = QSizeGrip(self)
        self.sizegrip3.setVisible(True)

        self.sizegrip4 = QSizeGrip(self)
        self.sizegrip4.setVisible(True)



    # event listeners
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def keyPressEvent(self, event):
        """regular keylistener"""
        if(event.key() == Qt.Key_Escape):
            sys.exit()

    def on_button_click(self):
        """button click listener"""
        sender = self.sender()

        if(sender.objectName() == "ss_button"):
            self.take_ss()



    # error handling
    def show_alert_popup(self, alert_str):
        """shows alert popup with given message"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Alert")
        msg.setText(alert_str)
        msg.exec()

    def global_keylistener_error(self):
        """global keylistener error function"""
        self.show_alert_popup("Hotkey error, please fix hotkeys on cfg file")
        sys.exit()



    # functionality
    def take_ss(self):
        """takes ss, uses ss_handler
        if frame is visible takes a partial ss if not takes all screen
        """ 
        if(self.isVisible()):
            bbox = self.geometry().getRect()
            bbox = {"top": bbox[1], "left" : bbox[0], "width" : bbox[2], "height" : bbox[3]}
            
            self.hide()
            ss_state, ss_info = self.ss_handler.take_ss(ss_bbox=bbox)
            self.show()
        else:
            ss_state, ss_info = self.ss_handler.take_ss()

        # on error
        if(not ss_state):
            self.show_alert_popup(ss_info)
    
    def hide_show(self):
        """hide show frame function for global keylistener"""
        if(self.isVisible()):
            self.hide()
        else:
            self.show()

