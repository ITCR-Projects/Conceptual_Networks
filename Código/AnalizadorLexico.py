#Proyecto de Ingeniería de Software TEC S2-2023
#Ronaldo Vindas Barboza

#Analizador Léxico

import io


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


# Pruebas
    
words = splitFileWords((openTextArchive("Prueba", "r")))
cleanwordList = cleanText(words)
stringPalabras = ' '.join(cleanwordList)
print(stringPalabras)


