# PyQt6 dependencies
from PyQt6.QtCore import QThread, pyqtSignal

import time

# Class that create a thread to process the files
class NetworkThread(QThread):

    finished = pyqtSignal()
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller

    def run(self):
        print("XD")
        self.finished.emit()