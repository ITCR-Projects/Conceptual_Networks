from abc import ABC
from Codigo.Model.File import File

class TextFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        path = "../../Txts/" + self.name + ".txt"
        try:
            # Abre el archivo de entrada en modo lectura
            with open(self.url_file, 'r') as archivo_entrada:
                # Lee el contenido del archivo de entrada
                contenido = archivo_entrada.read()

            with open(path, 'w') as archivo_salida:
                # Escribe el contenido en el archivo de salida
                archivo_salida.write(contenido)

                print(f'El contenido de {self.url_file} se ha guardado en {path}')
        except FileNotFoundError:
            print(f'El archivo {self.url_file} no se encontró.')

        except Exception as e:
            print(f'Ocurrió un error: {str(e)}')

        return contenido

