import io
import re



#esta funcion elimina las palabras no significatibas de un string 
def IgnoreWords(text):
    # Leer el texto desde un archivo txt
   # with io.open('prueba.txt', 'r', encoding='utf8') as f:
    #    text = f.read().lower()
     #   f.close()
    

    #en ves de el codigo de ler el archibo para ignorar las palabras se
    #puede usar Ignore = ["este", "un"]
    with io.open('Ignore.txt', 'r', encoding='utf8') as f:
        Ignore = f.read().splitlines()
    #
    for word in Ignore:
        text = re.sub(r'\b' + word + r'\b', '', text)

    print(text)

#esta funcion elimina las palabras no significatibas de una lista de palabras
def IgnoreWords2(wordList):
   
    #en ves de el codigo de ler el archibo para ignorar las palabras se
    #puede usar Ignore = ["este", "un"]
    with io.open('Ignore.txt', 'r', encoding='utf8') as f:
        Ignore = f.read().splitlines()
    #
    for word in Ignore:
        while word in wordList:
            wordList.remove(word)

        

    print(wordList)

def addwordstoignore():
    words = []
    ignore = input("escriba las palabras que desea ignorar: ")
    words = ignore.split()
    
    with io.open('Ignore.txt', 'a', encoding='utf8') as f:
        for word in words:
            f.write(word+ '\n')

#Proyecto de Ingeniería de Software TEC S2-2023
#Ronaldo Vindas Barboza

#Analizador Léxico



#1-Abrir archivo en .txt

def openTextArchive(archiveName, mode):
    '''Función que abre un archivo de texto y lo pasa a minúsculas.
    Entradas: nombre del archivo, modo de lectura/escritura
    Salidas: archivo abierto
    Restricciones: N/A'''

    with io.open(archiveName + '.txt',mode, encoding='utf8') as f:
        text = f.read().lower()
        f.close()
        return text

#2-Dividir texto    
def splitFileWords(text):
    '''Función que divide un texto en palabras.
    Entradas: Archivo de texto.
    Salidas: Lista de palabras.
    Restricciones: N/A'''
    words = []
    words = text.split()
    return words


#3-Dividir texto  
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

words = splitFileWords((openTextArchive("Prueba", "r")))
cleanwordList = cleanText(words)


IgnoreWords2(cleanwordList)
