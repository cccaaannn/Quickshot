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

            cfg_path = Quickshot_builder.create_cfgs_on_user_home(cfg_path_from="cfg", cfg_name_from="Qshot_default.cfg", cfg_path_to=".Quickshot\\cfg", cfg_name_to="Qshot.cfg")
            app_abs_path = os.path.dirname(os.path.realpath(__file__))
            Quickshot_builder.build_application(cfg_path, os.path.join(app_abs_path, "cfg/Qshot_default.cfg"), os.path.join(app_abs_path, "statics"))

        elif(build_for == "linux_appimage"):
            # use this for compiling for linux appimage 
            # uses Home/user directory for cfg file since appimages can not be changed

            cfg_path = Quickshot_builder.create_cfgs_on_user_home(cfg_path_from="cfg", cfg_name_from="Qshot_default.cfg", cfg_path_to=".Quickshot/cfg", cfg_name_to="Qshot.cfg")
            Quickshot_builder.build_application(cfg_path, "cfg/Qshot_default.cfg", "statics")


    @staticmethod
    def copy_file(file_from, file_to):
        """copies a file, since coping can require higher than user privileges this function reads and writes the file back"""
        with open(file_from,"rb") as file:
            content = file.read()

        with open(file_to, "wb") as file:
            file.write(content)

    @staticmethod
    def create_cfgs_on_user_home(cfg_path_from, cfg_name_from, cfg_path_to, cfg_name_to):
        """
        Works on cross platform
        Checks cfg files existence and version then copies cfg files from the app to users HOME if needed
        
        cfg_path_from : cfg path from relative to apps location
        cfg_name_from : cfg name from
        cfg_path_to : cfg path to relative to users HOME
        cfg_name_to : cfg name to
        """
        # if cfg version key is not exists use this (for old cfg files that des not have version)
        cfg_fallback_version = { "cfg_version": "1.0" }

        # get user home cross platform 
        user_home = Path.home()
        
        # get abs application path
        app_abs_path = os.path.dirname(os.path.realpath(__file__))  
        
        # paths from
        cfg_folder_from = os.path.join(app_abs_path, cfg_path_from) # relative to applications path
        cfg_file_from = os.path.join(cfg_folder_from, cfg_name_from)

        # paths to
        cfg_folder_to = os.path.join(user_home, cfg_path_to) # relative to users HOME
        cfg_file_to = os.path.join(cfg_folder_to, cfg_name_to)

        # if any of the cfg files don't exists copy from application
        if(not os.path.isfile(cfg_file_to)):
            print("Required cfg files could not be found, creating cfg files under {}".format(cfg_folder_to))

            # create parent folders
            Path(cfg_folder_to).mkdir(parents=True, exist_ok=True)

            # copy cfg files
            Quickshot_builder.copy_file(cfg_file_from, cfg_file_to)

        # if cfg versions don't match copy from application
        else:
            with open(cfg_file_from, "r") as file:
                versions_on_app = yaml.safe_load(file)

            with open(cfg_file_to, "r") as file:
                versions_on_system = yaml.safe_load(file)

            cfg_version_on_app = versions_on_app["versions"]["cfg_version"]
            cfg_version_on_system = versions_on_system.get("versions", cfg_fallback_version).get("cfg_version") # get allows us to pass a defauşt value, so if cfg file is old and does not have version key this is not going to die.

            if(cfg_version_on_system != cfg_version_on_app):
                print("cfg version on the system '{}' is different than the apps current cfg version '{}', replacing cfg files under {}".format(cfg_version_on_system, cfg_version_on_app, cfg_folder_to))

                # copy cfg files
                Quickshot_builder.copy_file(cfg_file_from, cfg_file_to)

        return cfg_file_to

