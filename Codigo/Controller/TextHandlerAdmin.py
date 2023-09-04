import os
import io
import re

from Codigo.Model.DocxFile import DocxFile
from Codigo.Model.WebFile import WebFile
from Codigo.Model.TextFile import TextFile


class TextHandlerAdmin:
    def __init__(self):
        self.files = []
        self.text = ""
        self.ignore_words_added_list = []

    # ----Métodos Privados ----
    def setTextBlank(self):
        '''Función que limpia el buffer de texto.
        Entradas: N/A.
        Salidas: Buffer de Texto vacio.
        Restricciones: N/A'''

        self.text = ""
        return

    def deleteRepeatedLines(self):
        '''Función que elimina líneas repetidas seguidas.
        Entradas: Archivo de texto.
        Salidas: Texto sin líneas repetidas seguidas.
        Restricciones: N/A'''

        # self.text = '\n'.join([line for line in self.text.split('\n') if line.strip() != ''])
        # lines = self.text.split('\n')
        lines = [line for line in self.text.split('\n') if line.strip() != '']
        new_lines = [lines[i] for i in range(len(lines)) if i == 0 or lines[i] != lines[i - 1]]
        self.text = '\n'.join(new_lines)

        # return

    def splitFileWords(self):
        '''Función que divide un texto en una lista de palabras.
        Entradas: Archivo de texto.
        Salidas: Lista de palabras.
        Restricciones: N/A'''

        self.text = self.text.split()

        # return words

    # -Limpiar texto
    def cleanText(self):
        '''Función que limpia una lista de palabras. Elimina números,acentuación, signos de puntuación, etc.
        Entradas: Lista de palabras
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''

        translateTable = str.maketrans('áéíóúüÜñ', 'aeiouuun', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–•¡!¿?')
        newCleanWordList = []

        for word in self.text:
            if not word.isdigit():
                newCleanWordList.append(word.translate(translateTable))
        self.text = newCleanWordList

        # return

    def ignoreWords(self):
        '''Método que elimina palabras no singnificativas.
            Entradas: Texto a procesar.
            Salidas: Documento con texto limpio.
            Restricciones: N/A '''

        # En vez de el codigo de leer el archivo para ignorar las palabras se puede usar Ignore = ["este", "un"]

        # en vez de el codigo de leer el archivo para ignorar las palabras se
        # puede usar Ignore = ["este", "un"]
        with io.open('../Ignore.txt', 'r', encoding='utf8') as f:
            ignore = f.read().splitlines()

        #
        if self.ignore_words_added_list:
            ignore.extend(self.ignore_words_added_list)

        result = []
        for word in self.text:
            if word not in ignore:
                result.append(word)
        self.text = result
        # return

    # ---- Métodos Públicos ----

    def add_file(self, filepath):
        '''Método que añade archivos de la lista al documento a procesar.
        Entradas: nombre del archivo, self.
        Salidas: Documento con texto de la lista de archivos.
        Restricciones: Archivos deven tener extensión ".docx", ".html" '''

        name, extension = os.path.splitext(filepath)
        name = os.path.basename(name)
        if extension == ".docx":
            file = DocxFile(name, filepath)
            self.files.append(file)
            response = file.get_text()
            if response['response']:
                return response

            self.text = self.text + response['message']
            return response

        elif extension == ".txt":
            file = TextFile(name, filepath)
            self.files.append(file)
            response = file.get_text()
            if response['response']:
                return response

            self.text = self.text + response['message']
            return response

        else:
            file = WebFile(filepath, filepath)
            self.files.append(file)
            response = file.get_text()
            if response['response']:
                return response

            self.text = self.text + response['message']
            return response

    def lexical_analysis(self):
        '''Método que realiza el análisis léxico del documento de texto de la clase.
        Entradas: self
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''

        self.text = self.text.lower()                               # Estadariza el texto completo a minúsculas
        self.deleteRepeatedLines()                                  # Elimina líneas repetidas
        self.splitFileWords()                                       # Divide el texto en una lista de palabras
        self.cleanText()                                            # Limpia el texto, elimina números, cambia tildes,etc.
        self.ignoreWords()                                          # Ignora Palabras sin carga semántica
        self.text = '\n'.join(self.text)

        path = "../../Txts/Result" + ".txt"
        with open(path, 'w', encoding="utf8") as output_file:
            output_file.write(str(self.text))                       # Escribe el contenido en el archivo de salida

        return self.text



    def countWords(self):
        wordList = self.text.split()
        wordFrequency = []

        for word in wordList:
            wordFrequency.append(wordList.count(word))
        print(wordFrequency)

        #return
    def stemming(self):

        return

    def indexing(self):

        return

    def setIgnoreWords(self, iwords):
        self.ignore_words_added_list = iwords

    def addwordstoignore(self, iwords):
        with io.open('../Ignore.txt', 'r', encoding='utf8') as f:
            ignore = f.read().splitlines()

        with io.open('../Ignore.txt', 'a', encoding='utf8') as f:
            for word in iwords:
                if word not in ignore:
                    f.write('\n' + word.lower())
