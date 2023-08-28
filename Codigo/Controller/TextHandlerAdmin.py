import os
import io
import re


from Codigo.Model.DocxFile import DocxFile
from Codigo.Model.WebFile import WebFile


class TextHandlerAdmin:
    def __init__(self):
        self.files = []
        self.document = ""

    #----Métodos Privados ----


    def splitFileWords(text):
        '''Función que divide un texto en una lista de palabras.
        Entradas: Archivo de texto.
        Salidas: Lista de palabras.
        Restricciones: N/A'''
        words = []
        words = text.split()
        return words


    #-Limpiar texto  
    def cleanText(wordList):
        '''Función que limpia una lista de palabras. Elimina números,acentuación, signos de puntuación, etc.
        Entradas: Lista de palabras
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''
        
        translateTable= str.maketrans('áéíóúüÜñ', 'aeiouuun', '0123456789.,;|—:#$%&-*+-/()=><«»\@')
    
        newCleanWordList =[]
        for word in wordList:
            if not word.isdigit():
                newCleanWordList.append(word.translate(translateTable))
        return newCleanWordList

    def IgnoreWords(text):
            '''Método que elimina palabras no singnificativas.
            Entradas: Texto a procesar.
            Salidas: Documento con texto limpio.
            Restricciones: N/A '''

            #En vez de el codigo de leer el archivo para ignorar las palabras se puede usar Ignore = ["este", "un"]

            with io.open('Ignore.txt', 'r', encoding='utf8') as f:
                Ignore = f.read().splitlines()
            #
            for word in Ignore:
                text = re.sub(r'\b' + word + r'\b', '', text)

            with io.open('Ignore.txt', 'r', encoding='utf8') as f:
                Ignore = f.read().splitlines()
            #
            for word in Ignore:
                text = re.sub(r'\b' + word + r'\b', '', text)
            print(text)





















    # ---- Métodos Públicos ----

    def add_files(self, files):
        '''Método que añade archivos de la lista al documento a procesar.
        Entradas: nombre del archivo, self.
        Salidas: Documento con texto de la lista de archivos.
        Restricciones: Archivos deven tener extensión ".docx", ".html" '''
    
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
        '''Método que realiza el análisis léxico del documento de texto de la clase.
        Entradas: self
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''

        text = self.document.lower()                                            #Estadariza todo el texto a minúsculas
        wordList = self.splitFileWords(text)                                    #Divide el texto en una lista de palabras
        cleanwordList = self.cleanText(wordList)                                #Limpia el texto, elimina números, cambia tildes,etc.
        IgnoredWords = self.IgnoreWords(cleanwordList)                          #Ignora Palabras sin carga semántica


        return IgnoredWords


    def stop_words(self):

        return

    def stemming(self):

        return

    def indexing(self):
        
        return
