# PyQt6 dependencies
from PyQt6.QtCore import Qt, QThread, pyqtSignal

#Class that create a thread to process the files
class GraphThread(QThread):

    finished = pyqtSignal()

    def __init__(self, file_list, main_controller):
        super().__init__()
        self.file_list = file_list
        self.main_controller = main_controller

    def run(self):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            self.main_controller.addFiles(item.text())
        self.finished.emit()