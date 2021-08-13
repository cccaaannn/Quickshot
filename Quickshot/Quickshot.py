# pyqt5
from PyQt5.QtWidgets import  QLabel, QPushButton, QMessageBox, QSizeGrip, QMenu, QSystemTrayIcon 
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QPoint, Qt

# other imports
import atexit
import yaml
import time
import sys
import os

# Quickshot classes
from Qshot_settings import Qshot_settings, start_settings_with_event_loop
from global_keylistener import global_keylistener
from ss_handler import ss_handler

class Qshot(QWidget):

    def __init__(self, cfg_path, icon_path):
        super().__init__()
        self.cfg_path = cfg_path
        self.icon_path = icon_path
        self.set_options()
        
        self.init_variables()
        self.init_ui()
        self.create_context_menu()
        self.create_tray_icon()

        self.init_Qshot_settings()
        self.init_global_keylistener()
        self.init_ss_handler()

        atexit.register(self.exit_app)



    # set up frame and options
    def set_options(self):
        """Reads cfg file and makes assignment to local variables
        shows error popup if cfg file has errors
        """
        try:
            # read cfg file
            with open(self.cfg_path,"r") as file:
                cfg = yaml.safe_load(file)

            # quickshot_frame
            # theme
            self.background_color = cfg["quickshot_frame"]["theme"]["background_color"]
            self.accent_color = cfg["quickshot_frame"]["theme"]["accent_color"]
            self.opacity = cfg["quickshot_frame"]["theme"]["opacity"]

            # hotkeys
            self.ss_hotkey = cfg["quickshot_frame"]["hotkeys"]["ss_hotkey"]
            self.hide_hotkey = cfg["quickshot_frame"]["hotkeys"]["hide_hotkey"]

            # utilities
            self.frame_delay = cfg["quickshot_frame"]["utilities"]["frame_delay"]


            # ss ss_handler
            # naming
            self.save_path = os.path.normpath(cfg["ss_handler"]["naming"]["save_path"]) # convert to path
            self.create_root_file = cfg["ss_handler"]["naming"]["create_root_file"]
            self.before_ss_name = cfg["ss_handler"]["naming"]["before_ss_name"]
            self.after_ss_name = cfg["ss_handler"]["naming"]["after_ss_name"]
            self.before_number = cfg["ss_handler"]["naming"]["before_number"]
            self.after_number = cfg["ss_handler"]["naming"]["after_number"]
            self.date_formatting = cfg["ss_handler"]["naming"]["date_formatting"]
            self.use_system_local_date_naming = cfg["ss_handler"]["naming"]["use_system_local_date_naming"]

            # ss options
            self.ss_extension = cfg["ss_handler"]["ss_options"]["ss_extension"]
            self.png_compression_level = cfg["ss_handler"]["ss_options"]["png_compression_level"]
            self.default_screen = cfg["ss_handler"]["ss_options"]["default_screen"]
            self.save_clipboard = cfg["ss_handler"]["ss_options"]["save_clipboard"]

        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with cfg file")
            start_settings_with_event_loop(self.cfg_path, self.icon_path) # start settings with its own event loop
            self.exit_app()

    def init_ui(self):
        """inits ui"""
        # set main frame options
        self.setWindowTitle("Quickshot")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
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

        self.resize(self.size()) # new pyqt5 version (15.4) can't show back hidden frames properly if this line is not called at least once

    def init_variables(self):
        """init variables"""
        self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color, self.accent_color)
        self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color, self.accent_color)
        self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color, self.accent_color)

        self.background_color_temp = self.background_color
        self.accent_color_temp = self.accent_color

        # keeps old pointer position
        self.old_pos = None

        # keeps previous size for hidding and showing frame
        self.previous_size = self.size()


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
        self.ss_handler = ss_handler(ss_extension = self.ss_extension,
                            save_path = self.save_path, 
                            create_root_file = self.create_root_file, 
                            before_ss_name = self.before_ss_name, 
                            after_ss_name = self.after_ss_name, 
                            before_number = self.before_number, 
                            after_number = self.after_number, 
                            date_formatting = self.date_formatting,
                            use_system_local_date_naming = self.use_system_local_date_naming,
                            png_compression_level = self.png_compression_level, 
                            default_screen = self.default_screen,
                            save_clipboard = self.save_clipboard
                            )

    def init_Qshot_settings(self):
        """intits Qshot settings and assigns local functions to emitters"""
        self.Qs_settings = Qshot_settings(self.cfg_path, self.icon_path)
        self.Qs_settings.oppcity_emitter.connect(self.change_opacity)
        self.Qs_settings.background_color_emitter.connect(self.change_background_color)
        self.Qs_settings.accent_color_emitter.connect(self.change_accent_color)
        self.Qs_settings.update_frame_emitter.connect(self.update_frame)
        self.Qs_settings.hide_frame_emitter.connect(self.hide_by_value)


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

    def create_context_menu(self):
        """context menu for right click and tray icon"""
        self.create_context_menu = QMenu()

        self.take_ss_action = self.create_context_menu.addAction("Take ss")
        self.take_ss_action.triggered.connect(self.take_ss)

        self.hide_show_action = self.create_context_menu.addAction("Hide/Show")
        self.hide_show_action.triggered.connect(self.hide_show)

        self.maximize_action = self.create_context_menu.addAction("Maximize")
        self.maximize_action.triggered.connect(self.maximize_window)

        self.maximize_action = self.create_context_menu.addAction("Minimize")
        self.maximize_action.triggered.connect(self.minimize_window)

        self.settings = self.create_context_menu.addAction("Settings")
        self.settings.triggered.connect(self.show_settings)

        self.exit_action = self.create_context_menu.addAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)

    def create_tray_icon(self):
        """creates a tray icon if available and adds context menu to it"""
        self.create_tray_icon = QSystemTrayIcon(self)
        if(self.create_tray_icon.isSystemTrayAvailable()):
            self.create_tray_icon.setIcon(QIcon(self.icon_path))
            self.create_tray_icon.setContextMenu(self.create_context_menu)
            self.create_tray_icon.show()



    # event listeners
    def contextMenuEvent(self, event):
        """context menu functions has triggers so I don't need to use the event here, 
        but for right click menu to work function should stay"""
        action = self.create_context_menu.exec_(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, event):
        """keeps old position on first press"""
        self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        """resets old position on mouse relese to prevent moving on resize"""
        self.old_pos = None

    def mouseMoveEvent(self, event):
        """if old_pos exists moves the frame"""
        if(self.old_pos):
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def keyPressEvent(self, event):
        """regular keylistener"""
        if(event.key() == Qt.Key_Escape):
            self.exit_app()

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
        msg.setWindowIcon(QtGui.QIcon(self.icon_path))
        msg.setWindowTitle("Alert")
        msg.setText(alert_str)
        msg.exec()

    def global_keylistener_error(self):
        """global keylistener error function"""
        self.show_alert_popup("Hotkey error, please enter valid hotkeys or reset settings")
        self.show_settings()


    
    # settings functions
    def update_frame(self):
        """updates frame with new setting from config file, global keylistener has to be stop or it stays working at the background"""
        self.set_options()
        
        # update ui elements
        self.init_variables()
        self.setStyleSheet(self.window_style)
        self.setWindowOpacity(self.opacity)
        self.ss_button.setStyleSheet(self.button_style)
        self.info_label.setStyleSheet(self.label_style)
        
        # update global keylistener
        self.global_keylistener_thread.stop_keylistener()
        self.init_global_keylistener()

        # update ss handler
        self.init_ss_handler()

    def show_settings(self):
        """starts or refreshes settings frame 
        settings frame is not starts with main frame to increase startup speed.
        if settings not started, starts settings frame with ui elements.
        if settings is already started, refreshes the settings ui using form cfg file since old and not saved changes stuck in the ui
        """
        if(not self.Qs_settings.is_settings_started):
            self.Qs_settings.start_settings()
        else:
            self.Qs_settings.update_settings_ui()

    def change_background_color(self, value):
        if(value):
            self.background_color_temp = value
            self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color_temp, self.accent_color_temp)
            self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color_temp, self.accent_color_temp)
            self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color_temp, self.accent_color_temp)
        else:
            self.background_color_temp = self.background_color # reset temp color on reverting settings
            self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color, self.accent_color)
            self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color, self.accent_color)
            self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color, self.accent_color)

        self.setStyleSheet(self.window_style)
        self.ss_button.setStyleSheet(self.button_style)
        self.info_label.setStyleSheet(self.label_style)

    def change_accent_color(self, value):
        if(value):
            self.accent_color_temp = value
            self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color_temp, self.accent_color_temp)
            self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color_temp, self.accent_color_temp)
            self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color_temp, self.accent_color_temp)
        else:
            self.accent_color_temp = self.accent_color # reset temp color on reverting settings
            self.window_style = "background-color: {0}; border: 2px solid {1};".format(self.background_color, self.accent_color)
            self.label_style = "background-color: {0}; color: {1}; border: 0px".format(self.background_color, self.accent_color)
            self.button_style = "background-color: {0}; color: {1}; padding: 2px; border: 1px solid {1};".format(self.background_color, self.accent_color)

        self.setStyleSheet(self.window_style)
        self.ss_button.setStyleSheet(self.button_style)
        self.info_label.setStyleSheet(self.label_style)

    def change_opacity(self, value):
        """changes opacity or applies default if -1 is given"""
        if(value == -1):
            self.setWindowOpacity(self.opacity)
        else:
            self.setWindowOpacity(value)



    # utilities
    def hide_show(self):
        """hide show frame function for global keylistener"""
        if(self.isVisible()):
            self.hide()
            # self.create_tray_icon.showMessage("still running", "",  1)
        else:
            self.show()

    def hide_by_value(self, is_hide):
        """hide show frame function for displaying settings pop ups"""
        if(is_hide):
            self.hide()

        else:
            self.show()

    def center(self):
        """center the frame"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def maximize_window(self):
        """maximizes frame"""
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

    def minimize_window(self):
        """minimizes and centers the frame"""
        self.resize(200,100)
        self.center()
    
    def exit_app(self):
        """hides tray icon before exit, also this function added to atexit to consider any other close app"""
        try:
            self.create_tray_icon.hide()
            sys.exit()
        except Exception as e:
            print(e)



    # main functionality
    def take_ss(self):
        """takes ss, uses ss_handler
        if frame is visible takes a partial ss if not takes all screen
        """ 
        if(self.isVisible()):
            bbox = self.geometry().getRect()
            bbox = {"top": bbox[1], "left" : bbox[0], "width" : bbox[2], "height" : bbox[3]}
            
            # hide
            self.hide()
            # delay the frame visibility, on linux display compositor causes problems without delay
            time.sleep(self.frame_delay)
            ss_state, ss_info = self.ss_handler.take_ss(ss_bbox=bbox)
            # show
            self.show()
 
        else:
            ss_state, ss_info = self.ss_handler.take_ss()

        # on error
        if(not ss_state):
            self.show_alert_popup(ss_info)
    