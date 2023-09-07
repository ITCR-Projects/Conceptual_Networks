import os
import io
import numpy as np
import matplotlib.pyplot as plt
import re

from PIL import Image
from wordcloud import WordCloud
from collections import Counter

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
    def getPhrases(self):
        '''Función que almacena las citas encontradas en un texto.
        Entradas: N/A.
        Salidas: Colección de Citas de un Texto.
        Restricciones: N/A'''

        phrases = re.findall(r'"(.*?)"', self.text)
        return phrases

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

        translateTable = str.maketrans('áéíóúüÜñ', 'aeiouuun', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–•¡!¿?{}[]')

        #Para que no tome en cuenta las tildes:
        #translateTable = str.maketrans('üÜñ', 'uun', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–•¡!¿?')

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

    def countWords(self):
        '''Método que realiza el conteo de palabras.
        Entradas: self
        Salidas: Diccionario con conteo de palabras.
        Restricciones: N/A'''


        wordList = self.text.split()
        #wordFrequency = []
        wordFrequency = {}
        wordFrequency = Counter(wordList)
        #for word in wordList:
            #wordFrequency[word] = float(wordList.count(word))


        wordFrequencySorted = dict(sorted(wordFrequency.items(), key=lambda item: item[1], reverse=True))#Usé el lambda para no tener que hacer un import de "operator", no sé si haya algún problema - Rony
        print(wordFrequencySorted)
        return wordFrequencySorted

        #return wordFrequency

    def makeWordCloud(self, text):
        '''print("Goku sj2")
        alice_mask = np.array(Image.open("nube.png"))

        wc = WordCloud(background_color="white", max_words=1000, mask=alice_mask)

        print("Goku sj3")
        # generate word cloud
        wc.generate_from_frequencies(text)


        # show
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()'''

        x, y = np.ogrid[:300, :300]

        mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
        mask = 255 * mask.astype(int)

        wc = WordCloud(background_color="white", repeat=True, mask=mask)
        wc.generate_from_frequencies(text)                          #El diccionario debe estar formado por llave tipo string y valor tipo float para generar la imagen, para generar la tabla, el valor se podría parsear devuelta a int

        plt.axis("off")                             #Genera escalas para mostrarlos por matplotlib, quizás sea bueno buscar otra forma de exportar, es posible exportar a png y svg mediante otras funciones
        plt.imshow(wc, interpolation="bilinear")
        plt.show()


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

    def Statistics(self):
        counteWordsDict = self.countWords()
        self.makeWordCloud(counteWordsDict)  # Se crea la Nube de Palabras


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
