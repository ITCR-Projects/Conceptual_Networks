# PyQt6 dependencies
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QTabWidget, QDialog, QMessageBox, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QPushButton, QLineEdit, QWidget, QLabel, QProgressBar
from PyQt6.QtGui import QIcon
import sys
import os

codigo_dir = os.path.dirname(os.path.abspath(__file__))
codigo_dir = os.path.join(codigo_dir, '..')  # Retroceder un nivel
codigo_dir = os.path.join(codigo_dir, '..')
sys.path.append(codigo_dir)
# Import the main controller
from Codigo.Controller.Controller import MainController

# Import the Thread using to the interface process
from Codigo.View.GraphThread import GraphThread




# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Interface control variables
        self.page_size = 50  # Table Page Size
        self.current_page = 1  # Actual page
        self.word_freq_dict = {}

        # Main controller class
        self.mainController = MainController()

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
        url_icon = QIcon("Icons/globo.png")
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
        doc_icon = QIcon("Icons/documento.png")
        add_files_frame_btn = QPushButton("Añadir Archivo")
        add_files_frame_btn.setIcon(doc_icon)
        add_files_frame_btn.clicked.connect(self.add_files)
        add_files_frame_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")

        file_btn_layout.addWidget(add_files_frame_btn)

        # Add a remove item button
        remove_icon = QIcon("Icons/basura.png")
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
        ignore_icon = QIcon("Icons/comprobacion-de-lista.png")
        ignore_btn = QPushButton("Añadir Palabras Ignoradas")
        ignore_btn.setIcon(ignore_icon)
        ignore_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
            "QPushButton:hover { background-color: darkgray;}")
        ignore_btn.clicked.connect(self.open_dialog)
        file_btn_layout.addWidget(ignore_btn)

        #file_btn_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        files_layout.addLayout(file_btn_layout)

        self.file_list.itemSelectionChanged.connect(self.update_remove_button)

        files_layout.addStretch(1)
        self.mwlayout.addLayout(files_layout, 0, 2)

        # Add a button to start the creation of the graph
        graph_icon = QIcon("Icons/agregar.png")
        self.create_graph_btn = QPushButton("Procesar Texto")
        self.create_graph_btn.setIcon(graph_icon)
        self.create_graph_btn.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }")
        self.create_graph_btn.clicked.connect(self.create_graph)
        self.create_graph_btn.setEnabled(False)
        self.mwlayout.addWidget(self.create_graph_btn, 1,1)

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
        about_icon = QIcon("Icons/informacion.png")
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
        self.table_info_widget.setColumnCount(3)
        header = self.table_info_widget.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #3498db; color: white; }")
        self.table_info_widget.setHorizontalHeaderLabels(["Palabra", "Frecuencia", "Porcentaje"])
        table_view_widget_layout.addWidget(self.table_info_widget)

        # Creation of the page menu of the table
        self.pagination_widget = QWidget()
        pagination_layout = QHBoxLayout()
        self.pagination_widget.setLayout(pagination_layout)

        prevIcon = QIcon("Icons/angulo-izquierdo.png")
        self.prevButton = QPushButton("")
        self.prevButton.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }")
        self.prevButton.setIcon(prevIcon)
        self.prevButton.clicked.connect(self.prev_page)
        pagination_layout.addWidget(self.prevButton)

        self.pageLabel = QLabel("Página 1 de 1", self)
        self.pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pagination_layout.addWidget(self.pageLabel)

        nextIcon = QIcon("Icons/angulo-derecho.png")
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


        # Create a bar graph
       # self.bar_widget = pg.PlotWidget()
       # statistics_layout.addWidget(self.bar_widget)

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
        self.graph_thread = GraphThread(self.file_list, self.mainController) # Here the thread is created
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
        self.dialog.show()

    # Function to add the items in the Dialog window
    def add_ignore_word(self):
        # Obtener el texto del campo de entrada
        item_text = self.input_field.text()

        # Agregar el texto como un elemento en la lista
        if item_text:
            self.list_widget.addItem(item_text)
            self.input_field.clear()  # Limpiar el campo de entrada después de agregar

    # Function to remove the items in the Dialog window
    def remove_ignore_items(self):
        # Obtener los elementos seleccionados en la lista
        selected_items = self.list_widget.selectedItems()

        # Eliminar los elementos seleccionados de la lista
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))

    # add the ignore words to the UI list
    def setIgnoreWords(self):
        iwords = []
        words_count = self.list_widget.count()
        for i in range(words_count):
            iwords.append(self.list_widget.item(i).text().lower())
        self.mainController.setIgnoreWords(iwords)

        if self.dialog is not None:
            self.dialog.hide()

    # Set to the controller class the word that going to be ignored
    def addwordstoignore(self):
        iwords = []
        words_count = self.list_widget.count()
        for i in range(words_count):
            iwords.append(self.list_widget.item(i).text().lower())
        self.mainController.addwordstoignore(iwords)

        if self.dialog is not None:
            self.dialog.hide()

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
        data_to_display = list(self.word_freq_dict.items())[start:end]

        sorted_word_freq = sorted(data_to_display, key=lambda x: x[1], reverse=True)
        self.table_info_widget.setRowCount(0)

        for i, (word, freq) in enumerate(sorted_word_freq):
            item_word = QTableWidgetItem(word)
            item_freq = QTableWidgetItem(str(freq))
            item_percent = QTableWidgetItem(f"{(freq / sum(self.word_freq_dict.values())) * 100:.2f}%")

            self.table_info_widget.insertRow(i)
            self.table_info_widget.setItem(i, 0, item_word)
            self.table_info_widget.setItem(i, 1, item_freq)
            self.table_info_widget.setItem(i, 2, item_percent)

        self.setup_pagination()

    def setup_pagination(self):
        total_pages = len(self.word_freq_dict) // self.page_size + 1

        self.pageLabel.setText(f"Página {self.current_page} de {total_pages}")
        self.prevButton.setEnabled(self.current_page > 1)
        self.nextButton.setEnabled(self.current_page < total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            #self.setup_pagination()

    def next_page(self):
        total_pages = len(self.word_freq_dict) // self.page_size + 1
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_table()
            #self.setup_pagination()

    # Function that input a map of words and frequency to create a bar graph
    # def plot_bar_chart(self, word_freq_dict):
    #     sorted_word_freq = sorted(word_freq_dict.items(), key=lambda x: x[1], reverse=True)
    #
    #     labels = [word for word, freq in sorted_word_freq[:20]]
    #     freqs = [freq for word, freq in sorted_word_freq[:20]]
    #
    #     self.bar_widget.setTitle("Frecuencia de Palabras")
    #     self.bar_widget.setLabel("left", "Frecuencia")
    #     self.bar_widget.setLabel("bottom", "Palabras")
    #
    #     x = range(len(labels))
    #     bar = pg.BarGraphItem(x=x, height=freqs, width=0.6, brush='b')
    #     self.bar_widget.addItem(bar)
    #
    #     # Configurar etiquetas personalizadas en el eje X
    #     ticks = [(i, label) for i, label in enumerate(labels)]
    #     self.bar_widget.getAxis("bottom").setTicks([ticks])

if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()

    # Creation of a secondary window that contain the ignore words menu
    main_window.dialog = QDialog(main_window)
    main_window.dialog.setWindowTitle("Palabras Ignoradas")
    main_window.dialog.setGeometry(200, 200, 400, 300)
    main_window.dialog.setModal(True)  # Hacer que la ventana secundaria sea modal (bloquear la ventana principal)

    # Secondary window layout
    dialog_layout = QVBoxLayout()

    # Ignore words list
    main_window.list_widget = QListWidget(main_window.dialog)
    main_window.list_widget.setStyleSheet(
            "QListWidget { background-color: #f0f0f0;  }"
            "QListWidget::item { background-color: #ffffff; border: 1px solid #d0d0d0; padding: 10px; }"
            "QListWidget::item:selected { background-color: #3498db; color: white; }"
    )
    dialog_layout.addWidget(main_window.list_widget)

    # Ignore Word input
    main_window.input_field = QLineEdit(main_window.dialog)
    main_window.input_field.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; border: 2px solid #3498db; padding: 5px; color: #333; }"
            "QLineEdit:hover { border-color: #2980b9; }"
            "QLineEdit:focus { border-color: #e74c3c; }")
    dialog_layout.addWidget(main_window.input_field)

    # Add, delete and save buttons
    button_layout = QHBoxLayout()

    add_button_icon = QIcon("Icons/agregar.png")
    add_button = QPushButton("Añadir", main_window.dialog)
    add_button.setIcon(add_button_icon)
    add_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")

    remove_button_icon = QIcon("Icons/basura.png")
    remove_ignore_button = QPushButton("Borrar", main_window.dialog)
    remove_ignore_button.setIcon(remove_button_icon)
    remove_ignore_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #e74c3c; color: white; }"
            "QPushButton:hover { background-color: #c0392b; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
            "QPushButton:pressed { background-color: #d35400; }")

    save_button_icon = QIcon("Icons/controlar.png")
    save_ignore_words_button = QPushButton("Guardar", main_window.dialog)
    save_ignore_words_button.setIcon(save_button_icon)
    save_ignore_words_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
            "QPushButton:hover { background-color: darkgray; }")

    saveP_button_icon = QIcon("Icons/disco.png")
    saveP_ignore_words_button = QPushButton("Guardar Permanente", main_window.dialog)
    saveP_ignore_words_button.setIcon(saveP_button_icon)
    saveP_ignore_words_button.setStyleSheet(
        "QPushButton { border-radius: 10px; padding: 10px; background-color: #FFA500; color: white; }"
        "QPushButton:hover { background-color: #FFC04D; }")

    button_layout.addWidget(add_button)
    button_layout.addWidget(remove_ignore_button)
    button_layout.addWidget(save_ignore_words_button)
    button_layout.addWidget(saveP_ignore_words_button)

    dialog_layout.addLayout(button_layout)

    # Connect the button to the functions
    add_button.clicked.connect(main_window.add_ignore_word)
    remove_ignore_button.clicked.connect(main_window.remove_ignore_items)
    save_ignore_words_button.clicked.connect(main_window.setIgnoreWords)
    saveP_ignore_words_button.clicked.connect(main_window.addwordstoignore)

    main_window.dialog.setLayout(dialog_layout)

    main_window.show()
    app.exec()