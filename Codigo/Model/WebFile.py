from abc import ABC
from Codigo.Model.File import File
import requests
from bs4 import BeautifulSoup


class WebFile(File, ABC):
    def __init__(self, name, url_file):
        super().__init__(name, url_file)

    def get_text(self):
        # Se obtiene la pagina web
        response = requests.get(self.name)
        soup = BeautifulSoup(response.content, 'html.parser')

        name_txt = soup.title.string.replace(' ', '_')
        self.url_file = name_txt + ".txt"
        text = soup.body.get_text()

        # Se crea el archivo .txt y se guarda con la infoamción de la página
        with open(self.path + self.url_file, "w", encoding="utf-8") as f:
            f.write(text)
        return text
