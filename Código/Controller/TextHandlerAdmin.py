import os

from Código.Model.DocxFile import DocxFile
from Código.Model.WebFile import WebFile


class TextHandlerAdmin:
    def __init__(self):
        self.files = []
        self.document = ""

    def add_files(self, files):
        for filepath in files:
            name, extension = os.path.splitext(filepath)

            if extension == ".docx":
                file = DocxFile(name, filepath)
                self.files.append(file)
                print(file.get_text())
            elif extension == "":
                file = WebFile(name, filepath)
                self.files.append(file)
                print(file.get_text())

        return

    def lexical_analysis(self):
        return

    def stop_words(self):
        return

    def stemming(self):
        return

    def indexing(self):
        return
