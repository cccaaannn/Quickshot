from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, qApp
from PyQt5.QtWidgets import QMessageBox, QSlider, QComboBox, QGroupBox, QGridLayout, QHBoxLayout, QVBoxLayout, QColorDialog, QCheckBox, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QTextEdit, QFileDialog, QAction, QDesktopWidget
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import os
import json

class Qshot_settings(QMainWindow):
 
    def __init__(self, cfg_path):
        super().__init__()

        self.cfg_path = cfg_path

        self.init_variables()
        self.init_ui()

        cfg_status = self.read_cfg_file()
        if(cfg_status):
            self.variable_to_ui()

     

    # file -> ui
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
            self.multi_screen = cfg["ss_options"]["multi_screen"]

            return True
        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with cfg file please reset settings")
            return False
    
    def variable_to_ui(self):
        """assigns local variables to ui"""
        try:
            # colors and opacity
            self.opacity_slider.setSliderPosition(int(self.opacity * 100))
            self.background_color_line.setText(self.background_color)
            self.accent_color_line.setText(self.accent_color)

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

            if(self.multi_screen):
                self.multi_screen_checkbox.setChecked(True)
            else:
                self.multi_screen_checkbox.setChecked(False)

        except Exception as e:
            print(e)
            self.show_alert_popup("There is a problem with cfg file please reset settings")


    # ui -> file
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
           
            if(self.local_date_naming_checkbox.isChecked):
                self.new_cfg["ss_options"]["use_system_local_date_naming"] = "1"
            else:
                self.new_cfg["ss_options"]["use_system_local_date_naming"] = ""

            # ss options
            self.new_cfg["ss_options"]["ss_extension"] = self.extension_combobox.currentText()

            self.new_cfg["ss_options"]["png_compression_level"] = int(self.png_compression_combobox.currentText())

            if(self.multi_screen_checkbox.isChecked):
                self.new_cfg["ss_options"]["multi_screen"] = "1"
            else:
                self.new_cfg["ss_options"]["multi_screen"] = ""

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







    def init_ui(self):
        """inits ui"""
        self.setWindowTitle("Qshot Settings")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        # self.setFixedSize(700,700)
        self.menu_bar()
        self.block1()
        self.block2()
        self.block3()
        self.block4()
        self.block5()

        self.layouts()
        self.show()
        

    def init_variables(self):
        """inits class variables"""
        self.icon_path = "icons/1.ico"
        self.ss_extensions_list = [".png", ".jpg"]
        self.png_compression_level_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "-1"]

        self.hotkey_tooltip = """
        use <> on metakeys and + for more keys
        ex: a+s or <ctrl>+<space>
        """
        
        self.about_text = """
        A simple, quick, customizable screenshot tool.
        
        <br/>
        <a href='https://github.com/cccaaannn/Quickshot'>Quickshot github</a>
        """

        self.default_cfg = {
                            "general":{
                                "background_color": "#000000",
                                "accent_color": "#ffffff",
                                "opacity" : 0.5,
                                "ss_hotkey" : "<ctrl>+<alt>",
                                "hide_hotkey" : "<shift>+<space>"
                            },
                        
                            "ss_options":{
                                "ss_extension" : ".png",
                                "save_path" : "HOME", 
                                "create_root_file" : "Qshot", 
                                "before_ss_name" : "qs_", 
                                "after_ss_name" : "", 
                                "before_number" : "(", 
                                "after_number" : ")", 
                                "date_formatting" : "%y-%m-%d_%H-%M",
                                "use_system_local_date_naming" : "1",
                                "png_compression_level" : -1, 
                                "multi_screen" : ""
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
                                "use_system_local_date_naming" : "",
                                "png_compression_level" : "", 
                                "multi_screen" : ""
                            }
                        }


    def layouts(self):
        """"""
        self.grid = QGridLayout()
        self.main_grid = QGridLayout()

        self.grid.addWidget(self.group_box1, 0, 0)
        self.grid.addWidget(self.group_box2, 0, 1)
        self.grid.addWidget(self.group_box3, 1, 0)
        self.grid.addWidget(self.group_box4, 1, 1)

        self.main_grid.addLayout(self.grid, 0, 0)
        self.main_grid.addLayout(self.bottom_layout, 1, 0)
        
        # central widget is required when using Q mainwindow
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setLayout(self.main_grid)
        self.setCentralWidget(self.central_widget)



    def block1(self):
        self.group_box1 = QGroupBox("Colors and opacity")

        b1 = QPushButton()
        b1.setText("Background color")
        b1.setObjectName("background_color_button")
        b1.clicked.connect(self.on_click)
        
        self.background_color_line = QLineEdit()
        # background_color_line.setText("")
        self.background_color_line.setReadOnly(True)


        b2 = QPushButton()
        b2.setText("Accent color")
        b2.setObjectName("accent_color_button")
        b2.clicked.connect(self.on_click)

        self.accent_color_line = QLineEdit()
        # accent_color_line.setText("")
        self.accent_color_line.setReadOnly(True)

        l1 = QLabel()
        l1.setText("Opacity")

        # combobox1 = QComboBox()
        # combobox1.addItems(["ads", "asd", "ssas"])
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.valueChanged.connect(self.update_opacity_label)
        self.opacity_label = QLabel()
        self.opacity_label.setText("0.0")


        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(b1)
        hbox1.addStretch()
        hbox1.addWidget(self.background_color_line)

        hbox2.addWidget(b2)
        hbox2.addStretch()
        hbox2.addWidget(self.accent_color_line)

        hbox3.addWidget(l1)
        hbox3.addWidget(self.opacity_label)
        hbox3.addWidget(self.opacity_slider)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.group_box1.setLayout(vbox)




    def block2(self):
        self.group_box2 = QGroupBox("Hotkeys")
        self.group_box2.setToolTip(self.hotkey_tooltip)

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


        self.group_box2.setLayout(vbox)





    def block3(self):
        self.group_box3 = QGroupBox("Path and naming")

        l1 = QLabel()
        l1.setText("Save Path")
        
        self.save_path_line = QLineEdit()
        self.save_path_line.setText("")
 
        l2 = QLabel()
        l2.setText("Root file")

        self.root_file_line = QLineEdit()
        self.root_file_line.setText("")
  
        l3 = QLabel()
        l3.setText("Text before ss name")

        self.before_ss_name_line = QLineEdit()
        self.before_ss_name_line.setText("")

        l4 = QLabel()
        l4.setText("Text after ss name")

        self.after_ss_name_line = QLineEdit()
        self.after_ss_name_line.setText("")

        l5 = QLabel()
        l5.setText("Text before ss number")

        self.before_number_line = QLineEdit()
        self.before_number_line.setText("")

        l6 = QLabel()
        l6.setText("Text after ss number")

        self.after_number_line = QLineEdit()
        self.after_number_line.setText("")


        l7 = QLabel()
        l7.setText("Date formatting")

        self.date_formatting_line = QLineEdit()
        self.date_formatting_line.setText("")
    

        l8 = QLabel()
        l8.setText("Use local date naming")
        self.local_date_naming_checkbox = QCheckBox()


        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        hbox7 = QHBoxLayout()
        hbox8 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(l1)
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


        self.group_box3.setLayout(vbox)


    def block4(self):
        self.group_box4 = QGroupBox("Screeshot options")

        l1 = QLabel()
        l1.setText("Extension")

        self.extension_combobox = QComboBox()
        self.extension_combobox.addItems(self.ss_extensions_list)

        l2 = QLabel()
        l2.setText("png compression level")

        self.png_compression_combobox = QComboBox()
        self.png_compression_combobox.addItems(self.png_compression_level_list)


        l4 = QLabel()
        l4.setText("Multi screen full ss")

        self.multi_screen_checkbox = QCheckBox()
        

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addWidget(l1)
        hbox1.addStretch()
        hbox1.addWidget(self.extension_combobox)
        
        hbox2.addWidget(l2)
        hbox2.addStretch()
        hbox2.addWidget(self.png_compression_combobox)

        hbox4.addWidget(l4)
        hbox4.addStretch()
        hbox4.addWidget(self.multi_screen_checkbox)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)


        self.group_box4.setLayout(vbox)


    def block5(self):
        self.bottom_layout = QHBoxLayout()

        l1 = QLabel()
        l1.setText("Hover over sections for tooltips")
        l1.setFont(QFont('Arial', 9, weight=QtGui.QFont.Bold))

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




    def update_opacity_label(self, value):
        self.opacity_label.setText(str(value/100))


    def show_alert_popup(self, alert_str):
        """shows alert popup with given message"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Alert")
        msg.setText(alert_str)
        msg.exec()

    def show_success_popup(self, success_str):
        """shows success popup with given message"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(success_str)
        msg.exec()

    def show_about_popup(self):
        """shows about popup"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)
        msg.setText(self.about_text)
        msg.exec()



    def menu_bar(self):
        """adds menu bar and actions under it"""
        # menu items
        self.bar = self.menuBar()

        self.file_menu = self.bar.addMenu("File")
        self.help_menu = self.bar.addMenu("Help")

        # actions
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


        self.about_action = QAction("About", self)
        self.about_action.setObjectName("about")
        self.about_action.triggered.connect(self.on_click)

        self.help_menu.addAction(self.about_action)



    def on_click(self):
        """on click function for listeners"""
        sender = self.sender()

        # buttons
        if(sender.objectName() == "background_color_button"):
            color = QColorDialog.getColor()
            if(color.isValid()):
                self.background_color_line.setText(color.name())

        elif(sender.objectName() == "accent_color_button"):
            color = QColorDialog.getColor()
            if(color.isValid()):
                self.accent_color_line.setText(color.name())

        elif(sender.objectName() == "reset_button"):
            write_status = self.write_cfg_file(self.default_cfg)
            if(write_status):
                self.show_success_popup("Settings reset to default, please restart the Qshot")
                self.read_cfg_file()
                self.variable_to_ui()
 
        elif(sender.objectName() == "save_changes_button" or sender.objectName() == "save" ):
            variable_status = self.ui_to_variable()
            if(variable_status):
                write_status = self.write_cfg_file(self.new_cfg)
                if(write_status):
                    self.show_success_popup("Settings saved, please restart the Qshot")


        # menu items
        elif(sender.objectName() == "exit"):
            sys.exit()
        elif(sender.objectName() == "about"):
            self.show_about_popup()


        



def start_settings(cfg_path):
    application = QApplication(sys.argv)    

    a = Qshot_settings(cfg_path)

    sys.exit(application.exec_())