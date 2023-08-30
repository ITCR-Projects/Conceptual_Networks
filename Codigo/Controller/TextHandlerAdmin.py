import os
import io
import re


from Codigo.Model.DocxFile import DocxFile
from Codigo.Model.WebFile import WebFile
from Codigo.Model.TextFile import TextFile


class TextHandlerAdmin:
    def __init__(self):
        self.files = []
        self.document = ""

    #----Métodos Privados ----

    def splitFileWords(self,text):
        '''Función que divide un texto en una lista de palabras.
        Entradas: Archivo de texto.
        Salidas: Lista de palabras.
        Restricciones: N/A'''
        words = text.split()
        return words


    #-Limpiar texto  
    def cleanText(self,wordList):
        '''Función que limpia una lista de palabras. Elimina números,acentuación, signos de puntuación, etc.
        Entradas: Lista de palabras
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''
        
        translateTable= str.maketrans('áéíóúüÜñ', 'aeiouuun', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–')
    
        newCleanWordList =[]
        for word in wordList:
            if not word.isdigit():
                newCleanWordList.append(word.translate(translateTable))
        return newCleanWordList

    def IgnoreWords(self,wordList):
            '''Método que elimina palabras no singnificativas.
            Entradas: Texto a procesar.
            Salidas: Documento con texto limpio.
            Restricciones: N/A '''

            #En vez de el codigo de leer el archivo para ignorar las palabras se puede usar Ignore = ["este", "un"]

            # en ves de el codigo de ler el archibo para ignorar las palabras se
            # puede usar Ignore = ["este", "un"]
            with io.open('../Ignore.txt', 'r', encoding='utf8') as f:
                Ignore = f.read().splitlines()
            #
            print("goku")
            for word in Ignore:
                while word in wordList:
                    wordList.remove(word)
            return wordList

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

            self.document = self.document + response['message']
            return response

        elif extension == ".txt":
            file = TextFile(name, filepath)
            self.files.append(file)
            response = file.get_text()
            if response['response']:
                return response

            self.document = self.document + response['message']
            return response

        else:
            file = WebFile(filepath, filepath)
            self.files.append(file)
            response = file.get_text()
            if response['response']:
                return response

            self.document = self.document + response['message']
            return response

    def lexical_analysis(self):
        '''Método que realiza el análisis léxico del documento de texto de la clase.
        Entradas: self
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''

        texts = self.document.lower()                         #Estadariza todo el texto a minúsculas
        text = texts.replace('\n', ' ')                       #Elimina espacios de más y saltos de página de un texto.
        print("Nuevo Goku")
        
        wordList = self.splitFileWords(text)                  #Divide el texto en una lista de palabras
         
        cleanwordList = self.cleanText(wordList)              #Limpia el texto, elimina números, cambia tildes,etc.
       
        IgnoredWords = self.IgnoreWords(cleanwordList)        #Ignora Palabras sin carga semántica

        print (IgnoredWords)
        return IgnoredWords


    def stop_words(self):

        return

    def stemming(self):

        return

    def indexing(self):
        
        return
