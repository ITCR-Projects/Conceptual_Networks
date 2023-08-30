import textract
from abc import ABC
from Codigo.Model.File import File


class DocxFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        try:
            text = textract.process(self.url_file, encoding="utf8").decode('utf8')
            # Escribe el texto en un archivo de texto
            path = self.path + self.name + ".txt"
            with open(path, "w", encoding="utf8") as f:
                f.write(text)
            return {
                'response': False,
                'message': text,

            }
        except FileNotFoundError as e:
            return {
                'response': True,
                'message': f"Error: El archivo {self.url_file} no se encontró.",
            }
        except Exception as e:
            return {
                'response': True,
                'message': "Error: No se logró cargar el archivo.",
            }

