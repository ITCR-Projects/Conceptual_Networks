from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon
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

# Class that define a dialog to add and delete words to ignore
class IgnoreWordsDialog(QDialog):
    def __init__(self, main_controller):
        super().__init__()
        self.mainController = main_controller
        self.setWindowTitle("Palabras Ignoradas")
        self.setGeometry(200, 200, 400, 300)
        self.setModal(True)  # Hacer que la ventana secundaria sea modal (bloquear la ventana principal)

        # Layout del diálogo
        dialog_layout = QVBoxLayout()

        # Lista de palabras ignoradas
        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet(
            "QListWidget { background-color: #f0f0f0;  }"
            "QListWidget::item { background-color: #ffffff; border: 1px solid #d0d0d0; padding: 10px; }"
            "QListWidget::item:selected { background-color: #3498db; color: white; }"
        )
        dialog_layout.addWidget(self.list_widget)

        # Campo de entrada de palabra a ignorar
        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet(
            "QLineEdit { background-color: #f0f0f0; border: 2px solid #3498db; padding: 5px; color: #333; }"
            "QLineEdit:hover { border-color: #2980b9; }"
            "QLineEdit:focus { border-color: #e74c3c; }")
        dialog_layout.addWidget(self.input_field)

        # Botones (Añadir, Borrar, Guardar, Guardar Permanente)
        button_layout = QHBoxLayout()

        add_button_icon = QIcon(resource_path("Icons/agregar.png"))
        add_button = QPushButton("Añadir", self)
        add_button.setIcon(add_button_icon)
        add_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #3498db; color: white; }"
            "QPushButton:hover { background-color: #2980b9; }")

        remove_button_icon = QIcon(resource_path("Icons/basura.png"))
        self.remove_ignore_button = QPushButton("Borrar", self)
        self.remove_ignore_button.setIcon(remove_button_icon)
        self.remove_ignore_button.setEnabled(False)
        self.remove_ignore_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #e74c3c; color: white; }"
            "QPushButton:hover { background-color: #c0392b; }"
            "QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }"
            "QPushButton:pressed { background-color: #d35400; }")

        save_button_icon = QIcon(resource_path("Icons/controlar.png"))
        save_ignore_words_button = QPushButton("Guardar", self)
        save_ignore_words_button.setIcon(save_button_icon)
        save_ignore_words_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: gray; color: white; }"
            "QPushButton:hover { background-color: darkgray; }")

        saveP_button_icon = QIcon(resource_path("Icons/disco.png"))
        saveP_ignore_words_button = QPushButton("Guardar Permanente", self)
        saveP_ignore_words_button.setIcon(saveP_button_icon)
        saveP_ignore_words_button.setStyleSheet(
            "QPushButton { border-radius: 10px; padding: 10px; background-color: #FFA500; color: white; }"
            "QPushButton:hover { background-color: #FFC04D; }")

        button_layout.addWidget(add_button)
        button_layout.addWidget(self.remove_ignore_button)
        button_layout.addWidget(save_ignore_words_button)
        button_layout.addWidget(saveP_ignore_words_button)

        self.list_widget.itemSelectionChanged.connect(self.update_iword_remove_button)

        dialog_layout.addLayout(button_layout)

        # Conectar los botones a las funciones correspondientes
        add_button.clicked.connect(self.add_ignore_word)
        self.remove_ignore_button.clicked.connect(self.remove_ignore_items)
        save_ignore_words_button.clicked.connect(self.set_ignore_words)
        saveP_ignore_words_button.clicked.connect(self.add_words_to_ignore)

        self.setLayout(dialog_layout)

    def add_ignore_word(self):
        item_text = self.input_field.text()
        if item_text:
            self.list_widget.addItem(item_text)
            self.input_field.clear()

    def remove_ignore_items(self):
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))

    def set_ignore_words(self):
        iwords = []
        words_count = self.list_widget.count()
        for i in range(words_count):
            iwords.append(self.list_widget.item(i).text().lower())
        self.mainController.setIgnoreWords(iwords)
        self.hide()

    def add_words_to_ignore(self):
        iwords = []
        words_count = self.list_widget.count()
        for i in range(words_count):
            iwords.append(self.list_widget.item(i).text().lower())
        self.mainController.addwordstoignore(iwords)
        self.hide()

    def update_iword_remove_button(self):
        selected_items = self.list_widget.selectedItems()
        self.remove_ignore_button.setEnabled(len(selected_items) > 0)