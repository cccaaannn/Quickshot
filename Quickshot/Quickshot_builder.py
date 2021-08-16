from PyQt5.QtWidgets import QApplication
from Quickshot import Qshot

from pathlib import Path
import yaml
import sys
import os


class Quickshot_builder():
    """
    This class is just for starting the application properly for different configurations.
    """

    def __init__(self) -> None:
        pass

    @staticmethod    
    def build_application(cfg_path, default_cfg_path, statics_path):
        app = QApplication(sys.argv)
        frame = Qshot(cfg_path=cfg_path, default_cfg_path=default_cfg_path, statics_path=statics_path)
        sys.exit(app.exec())

    @staticmethod
    def build(build_for):

        if(build_for == "dev"):
            # dev
            Quickshot_builder.build_application("Quickshot/cfg/Qshot.cfg", "Quickshot/cfg/Qshot_default.cfg", "Quickshot/statics")

        elif(build_for == "windows_installer"):
            # use this for compiling for windows inno setup installer

            app_abs_path = os.path.dirname(os.path.realpath(__file__))
            Quickshot_builder.build_application(os.path.join(app_abs_path, "cfg/Qshot.cfg"), os.path.join(app_abs_path, "cfg/Qshot_default.cfg"), os.path.join(app_abs_path, "statics"))

        elif(build_for == "windows_msix"):
            # use this for compiling for windows msix package
            # uses Home/user directory for cfg file since msix files can not be changed

            cfg_path = Quickshot_builder.create_cfg_on_user_home(cfg_from="cfg\\Qshot_default.cfg", cfg_to=".Quickshot\\cfg\\Qshot.cfg")
            app_abs_path = os.path.dirname(os.path.realpath(__file__))
            Quickshot_builder.build_application(cfg_path, os.path.join(app_abs_path, "cfg/Qshot_default.cfg"), os.path.join(app_abs_path, "statics"))

        elif(build_for == "linux_appimage"):
            # use this for compiling for linux appimage 
            # uses Home/user directory for cfg file since appimages can not be changed

            cfg_path = Quickshot_builder.create_cfg_on_user_home(cfg_from="cfg/Qshot_default.cfg", cfg_to=".Quickshot/cfg/Qshot.cfg")
            Quickshot_builder.build_application(cfg_path, "cfg/Qshot_default.cfg", "statics")


    @staticmethod
    def create_cfg_on_user_home(cfg_from, cfg_to):
        # Works on Windows and Linux 
        # Creates cfg file with the name given in th cfg_file_name, also creates parent folders in the quickshot_save_folder
        # Reads options on the default_cfg_path writes them to cfg_file_name file under quickshot_save_folder

        # get user home cross platform 
        user_home = Path.home()
        
        # get abs application path
        app_abs_path = os.path.dirname(os.path.realpath(__file__))  
        
        # copy cfg from
        cfg_from = os.path.join(app_abs_path, cfg_from)

        # copy cfg to
        cfg_to = os.path.join(user_home, cfg_to)

        # if cfg file does not exits
        if(not os.path.isfile(cfg_to)):
            # create parent folders
            cfg_to_path, _ = os.path.split(cfg_to)
            Path(cfg_to_path).mkdir(parents=True, exist_ok=True)

            # read default cfg file
            with open(cfg_from,"r") as file:
                cfg = yaml.safe_load(file)

            # write default cfg file contents to actual cfg file on the path
            with open(cfg_to, "w") as file:
                yaml.dump(cfg, file, indent=4)
        
        return cfg_to
