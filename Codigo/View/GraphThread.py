# PyQt6 dependencies
from PyQt6.QtCore import Qt, QThread, pyqtSignal

import time

# Class that create a thread to process the files
class GraphThread(QThread):

    finished = pyqtSignal()
    update_signal = pyqtSignal(str, float)
    def __init__(self, file_list, main_controller):
        super().__init__()
        self.file_list = file_list
        self.main_controller = main_controller

    def run(self):
        count = 1
        fileCount = self.file_list.count()
        for i in range(fileCount):
            item = self.file_list.item(i)
            self.main_controller.addFiles(item.text())
            self.update_signal.emit(f"COMPLETED: {item.text()}", (count/fileCount)*100)
            count +=1
            time.sleep(3)
        self.finished.emit()