from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard
import time

class global_keylistener(QThread):
    ss_trigger = pyqtSignal()
    hide_trigger = pyqtSignal()

    def __init__(self, ss_key, hide_key):
        super().__init__()
        self.ss_key = ss_key
        self.hide_key = hide_key
        self.mapped_keys = {self.ss_key : self.emit_ss_trigger, self.hide_key : self.emit_hide_trigger}
        
    def emit_ss_trigger(self):
        self.ss_trigger.emit()

    def emit_hide_trigger(self):
        self.hide_trigger.emit()
    
    def run(self):
        try: 
            self.global_keylistener_thread = keyboard.GlobalHotKeys(self.mapped_keys)
            self.global_keylistener_thread.start()
            print("global listener started")
        except:
            print("thread creation error")




