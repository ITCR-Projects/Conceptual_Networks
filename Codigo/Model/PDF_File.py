from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from abc import ABC
from Codigo.Model.File import File


class PDFFile(File, ABC):

    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        try:
            #p_layout = LAParams()
            #text = extract_text(self.url_file, laparams=p_layout, codec='utf8')
            text = extract_text(self.url_file, codec=' latin-1')
            #text = text.encode('utf8', 'ignore').decode('utf8')

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
                'message': f"Error: No se logró cargar el archivo.{e}",
            }


x = PDFFile("5", "5.pdf")
print(x.get_text())
