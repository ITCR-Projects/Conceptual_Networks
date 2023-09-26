# PyQt6 dependencies
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QTableWidget, QSpinBox, QTableWidgetItem, QTabWidget, QMessageBox, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QPushButton, QLineEdit, QWidget, QLabel, QProgressBar
from PyQt6.QtGui import QIcon
import sys
import os

codigo_dir = os.path.dirname(os.path.abspath(__file__))
codigo_dir = os.path.join(codigo_dir, '..')  # Path file level up
codigo_dir = os.path.join(codigo_dir, '..')
sys.path.append(codigo_dir)

# Import the main controller
from Codigo.Controller.Controller import MainController

# Import the Ignore word dialog
from Codigo.View.IgnoreWordsDialog import IgnoreWordsDialog

# Import the Thread using to the interface process
from Codigo.View.GraphThread import GraphThread

# Import the Thread using to the interface process
from Codigo.Model.StructureStemming import StructureStemming

import os
path = ""
def resource_path(relative_path):
    global path
    try:
        base_path = os.path.dirname(__file__)
        path = base_path
    except:
        base_path = os.path.abspath(".")
        path = base_path
    return os.path.join(base_path, relative_path)

# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Interface control variables
        self.page_size = 50  # Table Page Size
        self.current_page = 1  # Actual page
        self.word_freq_dict = StructureStemming()

        # Main controller class
        self.mainController = MainController()

        # IgnoreWords dialog
        self.ignore_words_dialog = IgnoreWordsDialog(self.mainController)

        # Define the layout of the window
        self.setWindowTitle("Conceptual Networks")
        self.resize(1000, 600)  # Set the window size

        self.mwlayout = QGridLayout()
        self.mwlayout.setSpacing(10)

        url_layout = QHBoxLayout()
        files_layout = QVBoxLayout()

        # The list widget
        list_widget_container = QWidget()
        list_widget_container_layout = QVBoxLayout()
        list_widget_container.setLayout(list_widget_container_layout)
        lbl_layout = QVBoxLayout()
        list_widget_container_layout.addLayout(lbl_layout)



        list_label = QLabel("Lista de Archivos")
        list_label.setStyleSheet(
            "QLabel { padding: 5px; font-weight: bold; font-size: 16px; }"
        )

        lbl_layout.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(
            "QListWidget { background-color: #f0f0f0;  }"
            "QListWidget::item { background-color: #ffffff; border: 1px solid #d0d0d0; padding: 10px; }"
            "QListWidget::item:selected { background-color: #3498db; color: white; }"
        )

        list_widget_container_layout.addWidget(self.file_list)
        lbl_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        list_widget_container_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)




        self.mwlayout.addWidget(list_widget_container, 0, 0)

        # Title lable of the file space
        lbl_actions_title_layout = QVBoxLayout()
        file_label = QLabel("Acciones")
        file_label.setStyleSheet(
            "QLabel { padding: 5px; font-weight: bold; font-size: 16px; }"
        )
        lbl_actions_title_layout.addWidget(file_label)

        lbl_actions_title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        files_layout.addLayout(lbl_actions_title_layout)
        # Text box to contain the URL
        self.url_txb = QLineEdit()
        self.url_txb.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; border: 2px solid #3498db; padding: 5px; color: #333; }"
            "QLineEdit:hover { border-color: #2980b9; }"
            "QLineEdit:focus { border-color: #e74c3c; }")
        url_layout.addWidget(self.url_txb)

        # Button to add the URL to the file list
        url_path = resource_path("Icons/globo.png")
        url_icon = QIcon(url_path)
        add_url_btn = QPushButton("Añadir URL")
        add_url_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")
        add_url_btn.setIcon(url_icon)
        add_url_btn.clicked.connect(self.add_url_to_list)
        url_layout.addWidget(add_url_btn)

        files_layout.addLayout(url_layout)

        file_btn_layout = QHBoxLayout()
        # Add a button to add files
        doc_path = resource_path("Icons/documento.png")
        doc_icon = QIcon(doc_path)
        add_files_frame_btn = QPushButton("Añadir Archivo")
        add_files_frame_btn.setIcon(doc_icon)
        add_files_frame_btn.clicked.connect(self.add_files)
        add_files_frame_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")

        file_btn_layout.addWidget(add_files_frame_btn)

        # Add a remove item button
        remove_path = resource_path("Icons/basura.png")
        remove_icon = QIcon(remove_path)
        self.remove_button = QPushButton("Remover Archivo")
        self.remove_button.setIcon(remove_icon)
        self.remove_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #e74c3c; color: white; }"
            "QPushButton:hover { background-color: #c0392b; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
            "QPushButton:pressed { background-color: #d35400; }"
        )
        self.remove_button.clicked.connect(self.remove_item)
        self.remove_button.setEnabled(False)  # Desactivate the button

        file_btn_layout.addWidget(self.remove_button)

        # Add ignored words
        ignore_path = resource_path("Icons/comprobacion-de-lista.png")
        ignore_icon = QIcon(ignore_path)
        ignore_btn = QPushButton("Añadir Palabras Ignoradas")
        ignore_btn.setIcon(ignore_icon)
        ignore_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
            "QPushButton:hover { background-color: darkgray;}")
        ignore_btn.clicked.connect(self.open_dialog)
        file_btn_layout.addWidget(ignore_btn)

        files_layout.addLayout(file_btn_layout)

        self.file_list.itemSelectionChanged.connect(self.update_remove_button)

        files_layout.addStretch(1)
        self.mwlayout.addLayout(files_layout, 0, 2)

        # Add a button to start the creation of the graph
        add_path = resource_path("Icons/agregar.png")
        graph_icon = QIcon(add_path)
        self.create_graph_btn = QPushButton("Procesar Texto")
        self.create_graph_btn.setIcon(graph_icon)
        self.create_graph_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }")
        self.create_graph_btn.clicked.connect(self.create_graph)
        self.create_graph_btn.setEnabled(False)
        self.mwlayout.addWidget(self.create_graph_btn, 1, 1)

        # Creation of a widget with a label and a progress bar
        self.progressb_widget = QWidget()

        self.progressbar_layout = QHBoxLayout()

        self.pbar_lb = QLabel("Iniciando Proceso")
        self.pbar_lb.setStyleSheet(
            "QLabel { background-color: #3498db; color: white; padding: 10px; border-radius: 5px; max-width: 250px; }"
        )
        self.progressbar_layout.addWidget(self.pbar_lb)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(
            "QProgressBar { background-color: #f0f0f0; border: 1px solid #d0d0d0; border-radius: 5px; text-align: center; }"
            "QProgressBar::chunk { background-color: #3498db; border-radius: 5px; }"
        )
        self.progressbar_layout.addWidget(self.progress_bar)

        self.progressb_widget.setLayout(self.progressbar_layout)
        self.mwlayout.addWidget(self.progressb_widget, 2, 0)

        self.progressb_widget.setVisible(False)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.tab_widget)

        # About button
        info_path = resource_path("Icons/informacion.png")
        about_icon = QIcon(info_path)
        self.about_button = QPushButton("")
        self.about_button.setIcon(about_icon)
        self.about_button.setFixedSize(30, 30)
        self.about_button.setStyleSheet(
            "QPushButton {border-radius: 10px; padding: 10px; background-color: #3498db; color: white; border: 2px solid #2980b9; }"
            "QPushButton:hover {background-color: #2980b9;}"
        )
        self.about_button.clicked.connect(self.show_about_dialog)
        self.central_layout.addWidget(self.about_button)

        # Tab widgets
        self.files_widget = QWidget()
        self.table_widget = QWidget()

        # Set the widgets to the window
        self.tab_widget.addTab(self.files_widget, "Archivos")
        self.tab_widget.addTab(self.table_widget, "Estadísticas")

        # Set the content
        # Files menus
        self.files_widget.setLayout(self.mwlayout)

        # Table and graph menus
        statistics_layout = QHBoxLayout()

        # Create a table with the necessary columns and buttons
        self.table_view_widget = QWidget()
        table_view_widget_layout = QVBoxLayout()
        self.table_view_widget.setLayout(table_view_widget_layout)

        # Creation of the table interface
        self.table_info_widget = QTableWidget()
        self.table_info_widget.setColumnCount(4)
        header = self.table_info_widget.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #3498db; color: white; }")
        self.table_info_widget.setHorizontalHeaderLabels(["Raíz", "Palabras", "Frecuencia", "Porcentaje"])
        table_view_widget_layout.addWidget(self.table_info_widget)

        # Creation of the page menu of the table
        self.pagination_widget = QWidget()
        pagination_layout = QHBoxLayout()
        self.pagination_widget.setLayout(pagination_layout)

        prev_path = resource_path("Icons/angulo-izquierdo.png")
        prevIcon = QIcon(prev_path)
        self.prevButton = QPushButton("")
        self.prevButton.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }")
        self.prevButton.setIcon(prevIcon)
        self.prevButton.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prevButton)

        self.pageLabel1 = QLabel("Página ")
        self.tpg_number_input = QSpinBox(self)
        self.tpg_number_input.setMinimum(1)  # Valor mínimo permitido
        self.tpg_number_input.setMaximum(10000)
        self.tpg_number_input.setValue(1)  # Valor predeterminado
        self.tpg_number_input.editingFinished.connect(self.validate_table_nav_text)

        self.pageLabel2 = QLabel(" de 1")
        self.pageLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pageLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pagination_layout.addWidget(self.pageLabel1)
        pagination_layout.addWidget(self.tpg_number_input)
        pagination_layout.addWidget(self.pageLabel2)

        next_path = resource_path("Icons/angulo-derecho.png")
        nextIcon = QIcon(next_path)
        self.nextButton = QPushButton("")
        self.nextButton.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }")
        self.nextButton.setIcon(nextIcon)
        self.nextButton.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.nextButton)

        table_view_widget_layout.addWidget(self.pagination_widget)

        statistics_layout.addWidget(self.table_view_widget)

        # ----------------------------------------
        self.root_list = QWidget()
        root_list_layout = QVBoxLayout()
        self.root_list_list = QListWidget()
        self.root_list_list.setStyleSheet(
            "QListWidget { background-color: #f0f0f0;  }"
            "QListWidget::item { background-color: #ffffff; border: 1px solid #d0d0d0; padding: 10px; }"
            "QListWidget::item:selected { background-color: #3498db; color: white; }"
        )
        root_list_layout.addWidget(self.root_list_list)

        self.botton_bar = QWidget()
        botton_bar_layout = QHBoxLayout()

        add_root_button = QPushButton('Añadir')
        add_root_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")
        self.remove_root_button = QPushButton('Eliminar')
        self.remove_root_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #e74c3c; color: white; }"
            "QPushButton:hover { background-color: #c0392b; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
            "QPushButton:pressed { background-color: #d35400; }")
        combine_root_button = QPushButton('Combinar')
        combine_root_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
            "QPushButton:hover { background-color: darkgray; }")

        add_root_button.clicked.connect(self.add_item_to_root_list)
        self.remove_root_button.clicked.connect(self.remove_item_from_root_list)

        self.remove_root_button.setEnabled(False)

        self.root_list_list.itemSelectionChanged.connect(self.update_root_remove_button)

        combine_root_button.clicked.connect(self.combine_roots)

        botton_bar_layout.addWidget(add_root_button)
        botton_bar_layout.addWidget(self.remove_root_button)
        botton_bar_layout.addWidget(combine_root_button)

        self.botton_bar.setLayout(botton_bar_layout)

        root_list_layout.addWidget(self.botton_bar)

        self.root_list.setLayout(root_list_layout)

        statistics_layout.addWidget(self.root_list)

        self.table_widget.setLayout(statistics_layout)

        self.tab_widget.setTabEnabled(1, False)

        self.setCentralWidget(self.central_widget)


    # Function that adds the files to the list
    def add_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt *.docx)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.file_list.addItems(selected_files)
            self.update_graph_button_state()

    # Function that adds the URLs to the list
    def add_url_to_list(self):
        text = self.url_txb.text()
        if text:
            self.file_list.addItem(text)
            self.url_txb.clear()
            self.update_graph_button_state()

    # Function that take the file list and send it to process
    def create_graph(self):
        self.current_page = 1
        self.progressb_widget.setVisible(True)
        self.graph_thread = GraphThread(self.file_list, self.mainController)  # Here the thread is created
        self.graph_thread.update_signal.connect(self.update_progressbar)
        self.graph_thread.error_signal.connect(self.error_report)
        self.graph_thread.finished.connect(self.graph_thread_finished)
        self.graph_thread.start()


    # Action when the thread updates the progress bar
    def update_progressbar(self, file, progress):
        self.pbar_lb.setText(file)
        self.progress_bar.setValue(int(progress))

    # Function that remove a selected element of the list
    def remove_item(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.file_list.takeItem(self.file_list.row(item))
        self.update_graph_button_state()

    # Function that handle the select element event
    def update_remove_button(self):
        selected_items = self.file_list.selectedItems()
        self.remove_button.setEnabled(len(selected_items) > 0)

    def update_graph_button_state(self):
        if self.file_list.count() > 0:
            self.create_graph_btn.setEnabled(True)
        else:
            self.create_graph_btn.setEnabled(False)

    # Action when the thread finishes its job
    def graph_thread_finished(self):
        self.word_freq_dict = self.mainController.getStatistics()
        self.populate_table()
        # self.plot_bar_chart(word_freq_dict)
        self.tab_widget.setTabEnabled(1, True)
        alert = QMessageBox()
        alert.setWindowTitle("Proceso Terminado")
        alert.setText("¡Proceso Terminado!")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()
        self.pbar_lb.setText("Empezando Proceso")
        self.progress_bar.setValue(0)
        self.progressb_widget.setVisible(False)

    #  Function to manage the process files errors
    def error_report(self, error_message):
        alert = QMessageBox()
        alert.setWindowTitle("ERROR!")
        alert.setText(f"{error_message}")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()

    # Function that shows the dialog window, this window is to manage the ignore words in the files
    def open_dialog(self):
        self.ignore_words_dialog.show()

    # Dialog that shows information about the program
    def show_about_dialog(self):
        about_message_box = QMessageBox()
        about_message_box.setWindowTitle("Acerca de la Aplicación")
        about_message_box.setIcon(QMessageBox.Icon.Information)
        about_message_box.setText("Aplicación Creadora de Redes Conceptuales")
        about_message_box.setDetailedText(
            "Versión 1.0.0\n"
            "Conceptual Networks es un programa para la composición de redes conceptuales y su representación gráfica\n"
            "Fecha de Lanzamiento: 14 Setiembre, 2023\n"
            "TEC  | Instituto Tecnológico De Costa Rica\n"
            "UNED | Universidad Estatal a Distancia\n"
            "LIIT | Laboratorio de Investigación e Innovación Tecnológica\n"
            "Desarrollado por: Jose Arce Morales, Gerson Gorgona Vargas, Josué Barrientos Sandoval, Álvaro Moreira Villalobos, Ronaldo Vindas Barboza\n"
            "Agradecimientos:\n Rodolfo Mora Zamora - Profesor y Supervisor \n Adriana López Vindas - Supervisora"
        )
        about_message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        about_message_box.exec()

    # Function that input a map of words and frequency to introduce in the table
    def populate_table(self):
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        data_to_display = list(self.word_freq_dict.getStemWords().items())[start:end]
        self.table_info_widget.setRowCount(0)

        for i, (word, value) in enumerate(data_to_display):
            item_word = QTableWidgetItem(word)
            item_freq = QTableWidgetItem(str(value[1]))
            words = ", ".join(value[0].keys())
            words_item = QTableWidgetItem(words)
            item_percent = QTableWidgetItem(f"{(value[1] / self.word_freq_dict.count_words) * 100:.2f}%")

            self.table_info_widget.insertRow(i)
            self.table_info_widget.setItem(i, 0, item_word)
            self.table_info_widget.setItem(i, 1, words_item)
            self.table_info_widget.setItem(i, 2, item_freq)
            self.table_info_widget.setItem(i, 3, item_percent)

        self.setup_pagination()

    # Function that set up the information of the pages
    def setup_pagination(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1

        self.tpg_number_input.setValue(self.current_page)
        self.pageLabel2.setText(f" de {total_pages}")
        self.prevButton.setEnabled(self.current_page > 1)
        self.nextButton.setEnabled(self.current_page < total_pages)

    # Move to the previous page
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            #self.setup_pagination()

    # Move to the next page
    def next_page(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_table()
            #self.setup_pagination()

    # Validate the page number of the number input
    def validate_table_nav_text(self):
        total_pages = len(self.word_freq_dict.getStemWords()) // self.page_size + 1
        current_page = self.tpg_number_input.value()
        if current_page <= total_pages:
            self.current_page = current_page
            self.populate_table()
        else:
            self.tpg_number_input.setValue(self.current_page)

    # Add the selected item of the table to the list of roots
    def add_item_to_root_list(self):
        selected_item = self.table_info_widget.currentItem()
        selected_column = self.table_info_widget.currentColumn()
        if selected_column == 0:
            if selected_item:
                text = selected_item.text()
                self.root_list_list.addItem(text)


    # Delete the selected item of the list of roots
    def remove_item_from_root_list(self):
        selected_item = self.root_list_list.currentItem()
        if selected_item:
            self.root_list_list.takeItem(self.root_list_list.row(selected_item))

    # Update the root remove botton
    def update_root_remove_button(self):
        selected_items = self.root_list_list.selectedItems()
        self.remove_root_button.setEnabled(len(selected_items) > 0)

    def combine_roots(self):
        items = []
        fileCount = self.root_list_list.count()
        for i in range(fileCount):
            items.append(self.root_list_list.item(i).text())
        self.mainController.combine_roots(items)
        alert = QMessageBox()
        alert.setWindowTitle("Alerta")
        alert.setText("¡Palabras Combinadas!")
        alert.setIcon(QMessageBox.Icon.Information)
        alert.exec()
        self.root_list_list.clear()



app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()