import textract
from abc import ABC
from Codigo.Model.File import File


class DocxFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        #CAMBIAR EL PATH DE DONDE SE AGARRA
        text = textract.process("../"+self.url_file, encoding='utf-8').decode('utf-8')

        # Escribe el texto en un archivo de texto
        path = "../../Txts/" + self.name + ".txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        return text
