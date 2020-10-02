from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard
import time

class global_keylistener(QThread):
    ss_trigger = pyqtSignal()
    hide_trigger = pyqtSignal()
    error_trigger = pyqtSignal()

    def __init__(self, ss_key, hide_key):
        super().__init__()
        self.ss_key = ss_key
        self.hide_key = hide_key
        self.is_keys_exists = False
        self.mapped_keys = {}

        if(self.ss_key):
            self.mapped_keys.update({self.ss_key : self.emit_ss_trigger})
        if(self.hide_key):
            self.mapped_keys.update({self.hide_key : self.emit_hide_trigger})
        
        if(self.mapped_keys):
            self.is_keys_exists = True


    def emit_ss_trigger(self):
        self.ss_trigger.emit()

    def emit_hide_trigger(self):
        self.hide_trigger.emit()

    def emit_error_trigger(self):
        self.error_trigger.emit()

    def stop_keylistener(self):
        try:
            self.global_keylistener_thread.stop()
            print("global listener stopped")
        except:
            print("global listener is already stopped")

    def run(self):
        try: 
            if(self.is_keys_exists):
                self.global_keylistener_thread = keyboard.GlobalHotKeys(self.mapped_keys)
                self.global_keylistener_thread.start()
                print("global listener started")
            else:
                print("no keys specified")
        except:
            self.emit_error_trigger()




