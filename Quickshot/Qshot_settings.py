# pyqt5
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QSlider, QCheckBox, QPushButton, QMessageBox, QGroupBox, QColorDialog, QFileDialog, QAction
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

# other imports
import json
import sys
import os

class Qshot_settings(QMainWindow):

    # pyqtsignal has a bug so I have to write these here
    oppcity_emitter = pyqtSignal(float)
    background_color_emitter = pyqtSignal(str)
    accent_color_emitter = pyqtSignal(str)
    update_frame_emitter = pyqtSignal()
    hide_frame_emitter = pyqtSignal(bool)

    def __init__(self, cfg_path, icon_path):
        super().__init__()
        self.cfg_path = cfg_path
        self.icon_path = icon_path

        self.is_settings_started = False


    # start frame and options
    def start_settings(self):
        """starts settings window
        this is not in the constructor because it slows startup of the main frame
        and if there is an error on the cfg file I want settings popup after main frames popup
        """
        self.is_settings_started = True # once frame started I don't want to recreate it again
        self.init_variables()
        self.init_ui()

        cfg_status = self.read_cfg_file()
        if(cfg_status):
            self.variable_to_ui()
    
    def update_settings_ui(self):
        """refreshes the settings frame without recreating ui elements"""
        cfg_status = self.read_cfg_file()
        if(cfg_status):
            self.variable_to_ui()
        self.show()

    def init_ui(self):
        """inits ui"""
        self.setWindowTitle("Qshot Settings")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        self.menu_bar()
        self.block1()
        self.block2()
        self.block3()
        self.block4()
        self.block5()

        self.setup_ui()
        self.show()

    def init_variables(self):
        """inits class variables"""
        self.ss_extensions_list = [".png", ".jpg"]
        self.png_compression_level_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.tooltips = {
        "colors_and_opacity" :
        """
Color and opacity settings.
        """,

        "hotkeys" : 
        """
Specify hotkeys.
Use <> on metakeys and + for adding more keys.
Leave it empty if you don't want.

ex: 
a+b+c
<ctrl>+<space>
        """,

        "save_path" : 
        """
Save path for the screenshots.

'HOME' tries to find user desktop or home automatically.
Leave it empty if you want the screenshot to be saved in the Quickshots directory.
        """,

        "root_file" : 
        """
Root filename for screenshots.
Specify a filename for screenshots to be saved, 
it will be created under the save path you specified.
Leave it empty if you don't want.
        """,

        "text_before_ss-text_after_ss" : 
        """
Text before and after the screenshot name.
Specify a text for placing before and after screenshot name.
Leave it empty if you don't want.

ex: 
(20_01_01).png  
screen_shot_20_01_01_end_of_ss.png
        """,
        
        "text_before_ss_number-text_after_ss_number" : 
        """
Text before and after screenshot number.
If multiple screenshots exists with the same name new one will be numbered, 
you can specify what text will be before and after that number.
Leave it empty if you don't want.

ex: 
qs_20_01_01(1).png  
qs_20_01_01[1].png  
qs_20_01_01-1.png         
        """,

        "date_formatting" : 
        """
Date formatting keywords

%Y year full
%y year 2 digit

%m month digit
%B month text

%d day
%A weekday long
%a weekday short

%H hour 24
%I hour 12
%p am/pm
%M minute
%S second

ex: 
%Y-%m-%d_%H-%M 
2020-01-01_01-00.png

%y-%B-%d-%A 
20-January-01-Mon.png
        """,

        "Use_local_date_naming" : 
        """
Check if you want date names to be your systems language.
        """,

        "extension" : 
        """
Extension of the screenshots.
        """,

        "png_compression_level" :
        """
Higher the level is smaller the png images will be.
        """,

        "default_screen" :
        """
When Quickshot is hidden it takes fullscreen screenshots, select default screen for full screen screenshots.
If 'All' box is checked Quickshot takes screenshot from all screens and combines them.
        """,
        
        "save_clipboard" :  
        """
Copies screenshot to clipboard.
        """

        }

        self.about_text = """
Quickshot is a simple, quick, customizable screenshot tool.

<br/><br/>
It is an open-sourced application you can check the <a href='https://github.com/cccaaannn/Quickshot'>Quickshot github</a> page.
        """
        
        self.default_cfg = {
                            "general":{
                                "background_color": "#000000",
                                "accent_color": "#ffffff",
                                "opacity" : 0.5,
                                "ss_hotkey" : "<alt>+s",
                                "hide_hotkey" : "<alt>+h"
                            },
                            "ss_options":{
                                "ss_extension" : ".png",
                                "save_path" : "HOME", 
                                "create_root_file" : "Qshot", 
                                "before_ss_name" : "qs_", 
                                "after_ss_name" : "", 
                                "before_number" : "(", 
                                "after_number" : ")", 
                                "date_formatting" : "%y-%B-%d_%H-%M",
                                "use_system_local_date_naming" : 1,
                                "png_compression_level" : 9, 
                                "default_screen" : 1,
                                "save_clipboard" : 1
                            }
                        }

        self.new_cfg = {
                            "general":{
                                "background_color" : "",
                                "accent_color" : "", 
                                "opacity" : "",
                                "ss_hotkey" : "",
                                "hide_hotkey" : ""
                            },
                        
                            "ss_options":{
                                "ss_extension" : "",
                                "save_path" : "", 
                                "create_root_file" : "", 
                                "before_ss_name" : "", 
                                "after_ss_name" : "", 
                                "before_number" : "", 
                                "after_number" : "", 
                                "date_formatting" : "",
                                "use_system_local_date_naming" : 0,
                                "png_compression_level" : 9, 
                                "default_screen" : 1,
                                "save_clipboard" : 0
                            }
                        }



    # read options and assign to local variable (file -> ui)
    def read_cfg_file(self):
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
            self.default_screen = cfg["ss_options"]["default_screen"]
            self.save_clipboard = cfg["ss_options"]["save_clipboard"]

            return True
        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with cfg file please reset settings and restart Quickshot")
            return False
    
    def variable_to_ui(self):
        """assigns local variables to ui"""
        try:
            # colors and opacity
            self.opacity_slider.setSliderPosition(int(self.opacity * 100))
            self.background_color_line.setText(self.background_color)
            self.background_color_prew.setStyleSheet("background-color: {0};".format(self.background_color))
            self.accent_color_line.setText(self.accent_color)
            self.accent_color_prew.setStyleSheet("background-color: {0};".format(self.accent_color))

            # hotkeys
            self.ss_key_line.setText(self.ss_hotkey)
            self.hide_key.setText(self.hide_hotkey)

            # path and naming
            self.save_path_line.setText(self.save_path)
            self.root_file_line.setText(self.create_root_file)
            self.before_ss_name_line.setText(self.before_ss_name)
            self.after_ss_name_line.setText(self.after_ss_name)
            self.before_number_line.setText(self.before_number)
            self.after_number_line.setText(self.after_number)
            self.date_formatting_line.setText(self.date_formatting)
           
            if(self.use_system_local_date_naming):
                self.local_date_naming_checkbox.setChecked(True)
            else:
                self.local_date_naming_checkbox.setChecked(False)

            # ss options
            extension_index = self.extension_combobox.findText(self.ss_extension, QtCore.Qt.MatchFixedString)
            self.extension_combobox.setCurrentIndex(extension_index)

            compression_level_index = self.png_compression_combobox.findText(str(self.png_compression_level), QtCore.Qt.MatchFixedString)
            self.png_compression_combobox.setCurrentIndex(compression_level_index)

            # if all_screens_checkbox is checked disable the default_screen_selector
            if(self.default_screen == 0):
                self.all_screens_checkbox.setChecked(True)
                self.default_screen_selector.setDisabled(True)
            else:
                self.all_screens_checkbox.setChecked(False)
                self.default_screen_selector.setDisabled(False)
                self.default_screen_selector.setValue(self.default_screen)

            if(self.save_clipboard):
                self.save_clipboard_checkbox.setChecked(True)
            else:
                self.save_clipboard_checkbox.setChecked(False)

        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with cfg file please reset settings and restart Quickshot")

    # get options from ui and write them to file (ui -> file)
    def ui_to_variable(self):
        """assign selected settings to new_cfg variable"""
        try:
            # colors and opacity
            self.new_cfg["general"]["opacity"] = self.opacity_slider.value() / 100
            self.new_cfg["general"]["background_color"] = self.background_color_line.text()
            self.new_cfg["general"]["accent_color"] = self.accent_color_line.text()

            # hotkeys
            self.new_cfg["general"]["ss_hotkey"] = self.ss_key_line.text()
            self.new_cfg["general"]["hide_hotkey"] = self.hide_key.text()


            # path and naming
            self.new_cfg["ss_options"]["save_path"] = self.save_path_line.text()
            self.new_cfg["ss_options"]["create_root_file"] = self.root_file_line.text()
            self.new_cfg["ss_options"]["before_ss_name"] = self.before_ss_name_line.text()
            self.new_cfg["ss_options"]["after_ss_name"] = self.after_ss_name_line.text()
            self.new_cfg["ss_options"]["before_number"] = self.before_number_line.text()
            self.new_cfg["ss_options"]["after_number"] = self.after_number_line.text()
            self.new_cfg["ss_options"]["date_formatting"] = self.date_formatting_line.text()
           
            if(self.local_date_naming_checkbox.isChecked()):
                self.new_cfg["ss_options"]["use_system_local_date_naming"] = 1
            else:
                self.new_cfg["ss_options"]["use_system_local_date_naming"] = 0

            # ss options
            self.new_cfg["ss_options"]["ss_extension"] = self.extension_combobox.currentText()

            self.new_cfg["ss_options"]["png_compression_level"] = int(self.png_compression_combobox.currentText())

            if(self.all_screens_checkbox.isChecked()):
                self.new_cfg["ss_options"]["default_screen"] = 0
            else:
                self.new_cfg["ss_options"]["default_screen"] = self.default_screen_selector.value()

            if(self.save_clipboard_checkbox.isChecked()):
                self.new_cfg["ss_options"]["save_clipboard"] = 1
            else:
                self.new_cfg["ss_options"]["save_clipboard"] = 0
            
            return True
        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with saving values please check the values or reset settings")
            return False

    def write_cfg_file(self, cfg):
        try:
            with open(self.cfg_path, "w") as file:
                json.dump(cfg, file, indent=4)
            return True
        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with saving values please check the values or reset settings")
            return False



    # ui elements
    def setup_ui(self):
        """sets up ui by assigning elements to layouts"""
        self.grid = QGridLayout()
        self.main_grid = QGridLayout()

        # top grid
        self.grid.addWidget(self.block1_group_box, 0, 0)
        self.grid.addWidget(self.block2_group_box, 0, 1)
        self.grid.addWidget(self.block3_group_box, 1, 0)
        self.grid.addWidget(self.block4_group_box, 1, 1)

        # bottom grid
        self.main_grid.addLayout(self.grid, 0, 0)
        self.main_grid.addLayout(self.bottom_layout, 1, 0)
        
        # central widget is required when using Q mainwindow
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setLayout(self.main_grid)
        self.setCentralWidget(self.central_widget)

    def block1(self):
        self.block1_group_box = QGroupBox("Colors and opacity")
        self.block1_group_box.setToolTip(self.tooltips["colors_and_opacity"])

        b1 = QPushButton()
        b1.setText("Background color")
        b1.setObjectName("background_color_button")
        b1.clicked.connect(self.on_click)
        
        self.background_color_line = QLineEdit()
        self.background_color_line.setReadOnly(True)

        self.background_color_prew = QLabel()
        self.background_color_prew.setMinimumSize(20,1)


        b2 = QPushButton()
        b2.setText("Accent color")
        b2.setObjectName("accent_color_button")
        b2.clicked.connect(self.on_click)

        self.accent_color_line = QLineEdit()
        self.accent_color_line.setReadOnly(True)

        self.accent_color_prew = QLabel()
        self.accent_color_prew.setMinimumSize(20,1)


        l1 = QLabel()
        l1.setText("Opacity")

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        self.opacity_label = QLabel()
        self.opacity_label.setText("10.0")


        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(b1)
        hbox1.addStretch()
        hbox1.addWidget(self.background_color_prew)
        hbox1.addWidget(self.background_color_line)

        hbox2.addWidget(b2)
        hbox2.addStretch()
        hbox2.addWidget(self.accent_color_prew)
        hbox2.addWidget(self.accent_color_line)

        hbox3.addWidget(l1)
        hbox3.addWidget(self.opacity_label)
        hbox3.addWidget(self.opacity_slider)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.block1_group_box.setLayout(vbox)

    def block2(self):
        self.block2_group_box = QGroupBox("Hotkeys")
        self.block2_group_box.setToolTip(self.tooltips["hotkeys"])

        l1 = QLabel()
        l1.setText("Screenshot key")
        
        self.ss_key_line = QLineEdit()
        self.ss_key_line.setText("")

        l2 = QLabel()
        l2.setText("Hide key")

        self.hide_key = QLineEdit()
        self.hide_key.setText("")

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(l1)
        hbox1.addStretch()
        hbox1.addWidget(self.ss_key_line)
        

        hbox2.addWidget(l2)
        hbox2.addStretch()
        hbox2.addWidget(self.hide_key)
       

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)


        self.block2_group_box.setLayout(vbox)

    def block3(self):
        self.block3_group_box = QGroupBox("Path and naming")

        # Save Path
        # l1 = QLabel()
        # l1.setText("Save Path")
        # l1.setToolTip(self.tooltips["save_path"])
        b1 = QPushButton()
        b1.setText("Chose save path")
        b1.setObjectName("save_path_button")
        b1.clicked.connect(self.on_click)

        self.save_path_line = QLineEdit()
        self.save_path_line.setToolTip(self.tooltips["save_path"])

        # Root file
        l2 = QLabel()
        l2.setText("Root file")
        l2.setToolTip(self.tooltips["root_file"])

        self.root_file_line = QLineEdit()
        self.root_file_line.setToolTip(self.tooltips["root_file"])

        # Text before ss name
        l3 = QLabel()
        l3.setText("Text before ss name")
        l3.setToolTip(self.tooltips["text_before_ss-text_after_ss"])

        self.before_ss_name_line = QLineEdit()
        self.before_ss_name_line.setToolTip(self.tooltips["text_before_ss-text_after_ss"])

        # Text after ss name
        l4 = QLabel()
        l4.setText("Text after ss name")
        l4.setToolTip(self.tooltips["text_before_ss-text_after_ss"])

        self.after_ss_name_line = QLineEdit()
        self.after_ss_name_line.setToolTip(self.tooltips["text_before_ss-text_after_ss"])

        # Text before ss number
        l5 = QLabel()
        l5.setText("Text before ss number")
        l5.setToolTip(self.tooltips["text_before_ss_number-text_after_ss_number"])

        self.before_number_line = QLineEdit()
        self.before_number_line.setToolTip(self.tooltips["text_before_ss_number-text_after_ss_number"])

        # Text after ss number
        l6 = QLabel()
        l6.setText("Text after ss number")
        l6.setToolTip(self.tooltips["text_before_ss_number-text_after_ss_number"])

        self.after_number_line = QLineEdit()
        self.after_number_line.setToolTip(self.tooltips["text_before_ss_number-text_after_ss_number"])

        # Date formatting
        l7 = QLabel()
        l7.setText("Date formatting")
        l7.setToolTip(self.tooltips["date_formatting"])

        self.date_formatting_line = QLineEdit()
        self.date_formatting_line.setToolTip(self.tooltips["date_formatting"])

        # Use local date naming
        l8 = QLabel()
        l8.setText("Use local date naming")
        l8.setToolTip(self.tooltips["Use_local_date_naming"])

        self.local_date_naming_checkbox = QCheckBox()
        self.local_date_naming_checkbox.setToolTip(self.tooltips["Use_local_date_naming"])


        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(b1)
        hbox1.addStretch()
        hbox1.addWidget(self.save_path_line)
        
        hbox2.addWidget(l2)
        hbox2.addStretch()
        hbox2.addWidget(self.root_file_line)

        hbox3.addWidget(l3)
        hbox3.addStretch()
        hbox3.addWidget(self.before_ss_name_line)

        hbox4.addWidget(l4)
        hbox4.addStretch()
        hbox4.addWidget(self.after_ss_name_line)

        hbox5.addWidget(l5)
        hbox5.addStretch()
        hbox5.addWidget(self.before_number_line)

        hbox6.addWidget(l6)
        hbox6.addStretch()
        hbox6.addWidget(self.after_number_line)

        hbox7.addWidget(l7)
        hbox7.addStretch()
        hbox7.addWidget(self.date_formatting_line)

        hbox8.addWidget(l8)
        hbox8.addStretch()
        hbox8.addWidget(self.local_date_naming_checkbox)  


        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)


        self.block3_group_box.setLayout(vbox)

    def block4(self):
        self.block4_group_box = QGroupBox("Screeshot options")
        
        # extension
        l1 = QLabel()
        l1.setText("Extension")
        l1.setToolTip(self.tooltips["extension"])

        self.extension_combobox = QComboBox()
        self.extension_combobox.addItems(self.ss_extensions_list)
        self.extension_combobox.setToolTip(self.tooltips["extension"])

        # png compression level
        l2 = QLabel()
        l2.setText("png compression level")
        l2.setToolTip(self.tooltips["png_compression_level"])

        self.png_compression_combobox = QComboBox()
        self.png_compression_combobox.addItems(self.png_compression_level_list)
        self.png_compression_combobox.setToolTip(self.tooltips["png_compression_level"])

        # Default screen
        l4 = QLabel()
        l4.setText("Default screen")
        l4.setToolTip(self.tooltips["default_screen"])

        l5 = QLabel()
        l5.setText("All")
        l5.setToolTip(self.tooltips["default_screen"])

        self.all_screens_checkbox = QCheckBox()
        self.all_screens_checkbox.setObjectName("all_screens_checkbox")
        self.all_screens_checkbox.clicked.connect(self.on_click)
        self.all_screens_checkbox.setToolTip(self.tooltips["default_screen"])

        self.default_screen_selector = QSpinBox()
        self.default_screen_selector.setMinimum(1)
        self.default_screen_selector.setToolTip(self.tooltips["default_screen"])

        # save clipboard
        l6 = QLabel()
        l6.setText("Copy ss to clipboard")
        l6.setToolTip(self.tooltips["save_clipboard"])

        self.save_clipboard_checkbox = QCheckBox()
        self.save_clipboard_checkbox.setToolTip(self.tooltips["save_clipboard"])

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(l1)
        hbox1.addStretch()
        hbox1.addWidget(self.extension_combobox)
        
        hbox2.addWidget(l2)
        hbox2.addStretch()
        hbox2.addWidget(self.png_compression_combobox)

        hbox4.addWidget(l4)
        hbox4.addStretch()
        hbox4.addWidget(l5)
        hbox4.addWidget(self.all_screens_checkbox)
        hbox4.addWidget(self.default_screen_selector)

        hbox5.addWidget(l6)
        hbox5.addStretch()
        hbox5.addWidget(self.save_clipboard_checkbox)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        self.block4_group_box.setLayout(vbox)

    def block5(self):
        self.bottom_layout = QHBoxLayout()

        l1 = QLabel()
        l1.setText("Hover over sections for tips")
        l1.setFont(QFont('Arial', 8, weight=QtGui.QFont.Bold))

        b1 = QPushButton()
        b1.setText("Save changes")
        b1.setObjectName("save_changes_button")
        b1.clicked.connect(self.on_click)

        b2 = QPushButton()
        b2.setText("Reset to default")
        b2.setObjectName("reset_button")
        b2.clicked.connect(self.on_click)


        self.bottom_layout.addWidget(l1)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(b2)
        self.bottom_layout.addWidget(b1)

    def menu_bar(self):
        """adds menu bar and actions under it"""
        # menu items
        self.bar = self.menuBar()

        self.file_menu = self.bar.addMenu("File")
        self.help_menu = self.bar.addMenu("Help")

        # File actions
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setObjectName("save")
        self.save_action.triggered.connect(self.on_click)
    
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setObjectName("exit")
        self.exit_action.triggered.connect(self.on_click)

        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)

        # Help actions
        self.about_action = QAction("About", self)
        self.about_action.setObjectName("about")
        self.about_action.triggered.connect(self.on_click)

        self.help_menu.addAction(self.about_action)



    # popups
    def show_alert_popup(self, alert_str):
        """shows alert popup with given message"""
        self.hide_frame_emitter.emit(True) # hide the ss frame when showing popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowIcon(QtGui.QIcon(self.icon_path))
        msg.setWindowTitle("Alert")
        msg.setText(alert_str)
        msg.exec()
        self.hide_frame_emitter.emit(False)  

    def show_success_popup(self, success_str):
        """shows success popup with given message"""
        self.hide_frame_emitter.emit(True) # hide the ss frame when showing popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon(self.icon_path))
        msg.setWindowTitle("Success")
        msg.setText(success_str)
        msg.exec()
        self.hide_frame_emitter.emit(False)        

    def show_about_popup(self):
        """shows about popup"""
        self.hide_frame_emitter.emit(True) # hide the ss frame when showing popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon(self.icon_path))
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)
        msg.setText(self.about_text)
        msg.exec()
        self.hide_frame_emitter.emit(False)  



    # preview functions
    def activate_preview(self):
        """activates preview mode"""
        self.background_color_emitter.emit(self.background_color_line.text())
        self.accent_color_emitter.emit(self.accent_color_line.text())
        self.oppcity_emitter.emit(self.opacity_slider.value()/100)

        # self.setWindowOpacity(self.opacity_slider.value()/100)

    def revert_preview(self):
        """reverts to default values"""
        self.background_color_emitter.emit(None)
        self.accent_color_emitter.emit(None)
        self.oppcity_emitter.emit(-1)

        # self.setWindowOpacity(1)



    # event listeners
    def closeEvent(self, event):
        """actions before close"""
        self.revert_preview()

    def update_opacity(self, value):
        """updates opacity value on frame and emits signal to main frame to update opacity"""
        self.opacity_label.setText(str(value/100))
        self.oppcity_emitter.emit(value/100)

    def on_click(self):
        """on click function for listeners"""
        sender = self.sender()

        # buttons
        if(sender.objectName() == "background_color_button"):
            """writes background color code to lineedit, shows color on color label, emits color change signal to main frame"""
            self.hide_frame_emitter.emit(True) # hide the ss frame when opening color picker
            color = QColorDialog.getColor()
            self.hide_frame_emitter.emit(False)
            if(color.isValid()):
                self.background_color_line.setText(color.name())
                self.background_color_prew.setStyleSheet("background-color: {0};".format(color.name()))
                self.background_color_emitter.emit(color.name())
            
        elif(sender.objectName() == "accent_color_button"):
            """writes accent color code to lineedit, shows color on color label, emits color change signal to main frame"""
            self.hide_frame_emitter.emit(True) # hide the ss frame when opening color picker
            color = QColorDialog.getColor()
            self.hide_frame_emitter.emit(False)
            if(color.isValid()):
                self.accent_color_line.setText(color.name())
                self.accent_color_prew.setStyleSheet("background-color: {0};".format(color.name()))
                self.accent_color_emitter.emit(color.name())

        elif(sender.objectName() == "save_path_button"):
            """opens a folder dialog for save path location"""
            save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if(save_path):
                self.save_path_line.setText(save_path)

        elif(sender.objectName() == "reset_button"):
            """writes default values to cfg file, reads cfg file and updates ui, emits signal to main frame for updating, shows success popup (write_cfg_file has error popup so I don't need here)"""
            write_status = self.write_cfg_file(self.default_cfg)
            if(write_status):
                self.read_cfg_file()
                self.variable_to_ui()
                self.update_frame_emitter.emit()
                self.show_success_popup("Settings reset to default")

        elif(sender.objectName() == "save_changes_button" or sender.objectName() == "save" ):
            """takes settings from ui writes them to cfg file, emits signal to main frame for updating, shows success popup (write_cfg_file has error popup so I don't need here)"""
            variable_status = self.ui_to_variable()
            if(variable_status):
                write_status = self.write_cfg_file(self.new_cfg)
                if(write_status):
                    self.update_frame_emitter.emit()
                    self.show_success_popup("Settings saved")

        # menu items
        elif(sender.objectName() == "exit"):
            self.close()
        elif(sender.objectName() == "about"):
            self.show_about_popup()

        # checkboxes
        elif(sender.objectName() == "all_screens_checkbox"):
            # if all_screens_checkbox is checked disable the default_screen_selector
            if(self.all_screens_checkbox.isChecked()):
                self.default_screen_selector.setDisabled(True)
            else:
                self.default_screen_selector.setDisabled(False)





def start_settings_with_event_loop(cfg_path, icon_path):
    """if the main window can not open because of the cfg file is being broken, settings needs its own event loop to stay open"""
    application = QApplication(sys.argv)    

    settings = Qshot_settings(cfg_path, icon_path)
    settings.start_settings()

    sys.exit(application.exec_())