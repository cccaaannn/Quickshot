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

# my classes
from global_keylistener import global_keylistener
from ss_handler import ss_handler


class Sshot(QWidget):

    def __init__(self, cfg_path="options.cfg"):
        super().__init__()

        # read cfg file
        self.cfg_path = cfg_path
        is_cfg_ok = self.set_options()
        

        if(not is_cfg_ok):
            # show alert
            self.show_alert_popup("There is a problem with cfg file")
            sys.exit()
        else:
            
            # init variables
            self.init_variables()
            # start ui
            self.init_ui()

            # instantiate ss_handler
            self.ss_h = ss_handler()
            self.ss_h.set_options(save_path = self.save_path, 
                                create_root_file = self.create_root_file, 
                                before_ss_name = self.before_ss_name, 
                                after_ss_name = self.after_ss_name, 
                                before_number = self.before_number, 
                                after_number = self.after_number, 
                                date_formatting = self.date_formatting, 
                                png_compression_level = self.png_compression_level, 
                                multi_screen = self.multi_screen)

            
            self.global_keylistener_thread = global_keylistener(self.ss_hotkey, self.hide_hotkey)
            self.global_keylistener_thread.start()
            self.global_keylistener_thread.ss_trigger.connect(self.take_ss)
            self.global_keylistener_thread.hide_trigger.connect(self.hide_show)


    def set_options(self):
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
            self.save_path = cfg["ss_options"]["save_path"]
            self.create_root_file = cfg["ss_options"]["create_root_file"]
            self.before_ss_name = cfg["ss_options"]["before_ss_name"]
            self.after_ss_name = cfg["ss_options"]["after_ss_name"]
            self.before_number = cfg["ss_options"]["before_number"]
            self.after_number = cfg["ss_options"]["after_number"]
            self.date_formatting = cfg["ss_options"]["date_formatting"]
            self.png_compression_level = cfg["ss_options"]["png_compression_level"]
            self.multi_screen = cfg["ss_options"]["multi_screen"]

            return True
        except Exception as e:
            print(e)
            return False

    def init_ui(self):
        """inits ui"""

        # set colors
        self.setStyleSheet(self.window_style)
        # opacity
        self.setWindowOpacity(self.opacity)
        # always on top and frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # init ui elements
        self.layouts()
        self.labels()
        self.buttons()
        self.sizegrips()
        self.set_up_ui()

        self.show()

    def init_variables(self):
        """init variables"""
        self.window_style = "background-color: {}; border: 2px solid {};".format(self.background_color, self.accent_color)
        self.label_style = "background-color: {}; color: {}; border: 0px".format(self.background_color, self.accent_color)
        self.button_style = "background-color: {0}; color: {1}; padding: 3px; border: 1px solid {1};".format(self.background_color, self.accent_color)
        


    # ui functions
    def set_up_ui(self):
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
        self.info_label.setText("Sshot")
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
        if(event.key() == Qt.Key_Escape):
            sys.exit()

    def on_button_click(self):
        """button click listeners"""
        sender = self.sender()

        if(sender.objectName() == "ss_button"):
            self.take_ss()


    # other
    def take_ss(self):
        # if frame is visible take a partial ss if not take all screen
        if(self.isVisible()):
            bbox = self.geometry().getRect()
            bbox = {"top": bbox[1], "left" : bbox[0], "width" : bbox[2], "height" : bbox[3]}
            
            self.hide()
            ss_state, ss_info = self.ss_h.take_ss(ss_bbox=bbox)
            self.show()
        else:
            ss_state, ss_info = self.ss_h.take_ss()


        if(not ss_state):
            self.show_alert_popup(ss_info)
        else:
            pass
            # self.on_ss_success(ss_info)
    
    def hide_show(self):
        if(self.isVisible()):
            self.hide()
        else:
            self.show()

    def show_alert_popup(self, alert_str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Alert")
        msg.setText(alert_str)
        msg.exec()


    def on_ss_success(self, ss_info):
        self.info_label.setText("saved")
        self.setStyleSheet(self.window_style)
        self.info_label.setStyleSheet(self.label_style)

    # def on_ss_error(self, ss_info):
    #     self.info_label.setText(ss_info)
    #     self.setStyleSheet(self.error_window_style)
    #     self.info_label.setStyleSheet(self.error_label_style)


    