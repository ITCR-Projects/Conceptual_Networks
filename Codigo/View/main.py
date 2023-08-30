# PyQt6 dependencies
from PyQt6.QtWidgets import QApplication, QToolBar, QMainWindow, QGridLayout, QListWidget, QFileDialog, QPushButton, QLineEdit, QWidget

# Import sys to work with system operations
import sys

# Import the main controller
from Codigo.Controller.Controller import MainController

# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Main controller class
        self.mainController = MainController()
        # Define the layout of the window
        self.mwlayout = QGridLayout()
        self.mwlayout.setSpacing(10)

        # Add a toolbar on the top of the window
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        # The list widget
        self.file_list = QListWidget()
        self.mwlayout.addWidget(self.file_list, 0, 0, 1, 1)

        # Text box to contain the URL
        self.url_txb = QLineEdit()
        self.mwlayout.addWidget(self.url_txb, 0, 2)

        # Button to add the URL to the file list
        add_url_btn = QPushButton("Add URL")
        add_url_btn.clicked.connect(self.add_url_to_list)
        self.mwlayout.addWidget(add_url_btn,1, 2)

        # Add a button to add files
        add_files_frame_btn = QPushButton("Add Files")
        add_files_frame_btn.clicked.connect(self.add_files)
        self.mwlayout.addWidget(add_files_frame_btn, 2, 2)

        # Add a button to start the creation of the graph
        create_graph_btn = QPushButton("Create Graph")
        create_graph_btn.clicked.connect(self.create_graph)
        self.mwlayout.addWidget(create_graph_btn, 2,0)

        widget = QWidget()
        widget.setLayout(self.mwlayout)
        self.setCentralWidget(widget)

    # Function that adds the files to the list
    def add_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.file_list.addItems(selected_files)

    # Function that adds the URLs to the list
    def add_url_to_list(self):
        text = self.url_txb.text()
        if text:
            self.file_list.addItem(text)
            self.url_txb.clear()

    def create_graph(self):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            self.mainController.addFiles(item.text())
        self.mainController.textAnalysis()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()