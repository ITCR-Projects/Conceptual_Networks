import os
import io
import numpy as np
import matplotlib.pyplot as plt
import re
import Stemmer
import networkx as nx

from PIL import Image

from wordcloud import WordCloud
from collections import Counter

from Codigo.Model.DocxFile import DocxFile
from Codigo.Model.WebFile import WebFile
from Codigo.Model.TextFile import TextFile
from Codigo.Model.PDF_File import PDFFile
from Codigo.Model.StructureStemming import StructureStemming

import os

path = ""


def resource_path(relative_path):
    global path
    try:
        base_path = os.path.dirname(__file__)
        path = base_path
    except:
        base_path = os.path.abspath(".")
        path = base_path
    return os.path.join(base_path, relative_path)


class TextHandlerAdmin:
    def __init__(self):
        self.files = []
        self.text = ""
        self.ignore_words_added_list = []
        self.structure_stemming = StructureStemming()
        #self.graph = nx.DiGraph()
        self.graph = nx.Graph()
        self.roots_words = []

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

    def getUrls(self):

        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.text)
        return urls

    def replaceUrls(self):
        url_regex = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        # Reemplazar las URLs
        self.text = url_regex.sub("ñjklñjjgra", self.text)

    def relocateUrls(self, urls):
        parts = self.text.split('ñjklñjjgra')
        result = parts[0]
        for i in range(1, len(parts)):
            result += urls[i - 1] + parts[i]
        self.text = result

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

        # Para que no tome en cuenta las tildes:
        # translateTable = str.maketrans('áéíóúüÜñ', 'aeiouuun', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–•¡!¿?{}[]')

        translateTable = str.maketrans('', '', '0123456789.,;|—:#$%&-*+-/()=><«»\@º–•¡!¿?{}['
                                               '▼“”₡°©αβγδηθιρσελξουφψχζνμτκπϛɛɔɣ⟺2−]⋅↑↓ωª_"~§ϻͱϙϟͳϡþʃʝðʕçʦᾱᾳῃῳᾶ`\'␃␊⇔→⇒∃≡∧¬∨⊥÷∀⊨⊢⊕⊤⊻⊃↔ℕ∈ʔṭςɲ·◻⊬⟹˜ǀǀ≤⌝⌜⋆⊽⋄∄∴∵⊭⋄⊽⟡⟢⟣⟤⟥®≠≥⥽⌐●')
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

        # Obtén la carpeta de documentos del usuario actual
        ignore = ""
        user_documents_folder = os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks', 'Ignore.txt'))
        if not os.path.exists(user_documents_folder):
            path2 = resource_path("Ignore.txt")
            with open(path2, 'r', encoding='utf8') as f:
                ignore = f.read()
                # ignore = f.read().splitlines()
            # Si no existe, lo crea
            try:
                os.mkdir(os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks')))
                with open(user_documents_folder, 'w', encoding='utf8') as f2:
                    f2.write(ignore)
            except Exception as e:
                print(e)
        else:
            try:
                with open(user_documents_folder, 'r', encoding='utf8') as f3:
                    ignore = f3.read()
            except Exception as e:
                print(e)

        ignore = ignore.splitlines()

        # path2 = resource_path("Ignore.txt")
        # with io.open(path2, 'r', encoding='utf8') as f:
        #     ignore = f.read().splitlines()

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

        elif extension == ".pdf":
            file = PDFFile(name, filepath)
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

        wordFrequency = Counter(wordList)

        wordFrequencySorted = dict(sorted(wordFrequency.items(), key=lambda item: item[1], reverse=True))
        return wordFrequencySorted

    def lexical_analysis(self):
        '''Método que realiza el análisis léxico del documento de texto de la clase.
        Entradas: self
        Salidas: Lista de palabras limpia.
        Restricciones: N/A'''
        urls = self.getUrls()
        self.replaceUrls()
        self.text = self.text.lower()  # Estadariza el texto completo a minúsculas
        self.deleteRepeatedLines()  # Elimina líneas repetidas
        self.splitFileWords()  # Divide el texto en una lista de palabras
        self.cleanText()  # Limpia el texto, elimina números, cambia tildes,etc.
        self.ignoreWords()  # Ignora Palabras sin carga semántica
        self.text = " ".join(self.text)
        self.relocateUrls(urls)
        self.text = self.text.split()
        self.stemming()
        self.text = "\n".join(self.text)

        # path = "../../Txts/Result" + ".txt"
        path = "Result.txt"
        with open(path, 'w', encoding="utf8") as output_file:
            output_file.write(self.text)  # Escribe el contenido en el archivo de salida
        return self.text

    def statistics(self):
        # counteWordsDict = self.countWords()

        # return counteWordsDict
        return self.structure_stemming
        # self.makeWordCloud(counteWordsDict)  # Se crea la Nube de Palabras

    def stemming(self):
        'Metodo que utiliza el stemming por medio de la libreria de Stemmer'
        stemmer = Stemmer.Stemmer('spanish')
        self.structure_stemming.cleanStructure()

        for word in self.text:
            root_word = stemmer.stemWord(word)
            self.structure_stemming.add(root_word, word)
            self.roots_words.append(root_word)
        self.structure_stemming.sortStruture()
        # print(self.structure_stemming.getStemWords())
        # print(self.structure_stemming.count_words)

    def create_network(self):
        # self.graph.add_edges_from(self.roots_words)
        # Agregar nodos al grafo y asignarles un atributo 'weight'
        # nodes = ["hola", "jose", "arce", "gato"]
        # weights = [1, 2, 1, 1]

        nodes, weights = self.structure_stemming.get_nodes_and_weights()

        for node, weight in zip(nodes, weights):
            if not self.graph.has_node(node):
                self.graph.add_node(node, weight=weight)

        # self.graph.add_nodes_from(nodes, weights)

    def create_relation(self, step=1):
        index = 0
        amount_words = len(self.roots_words)
        for node in self.roots_words:
            if index + step < amount_words:
                u, v = node, self.roots_words[index + step]
                if self.graph.has_edge(u, v):
                    self.graph[u][v]['weight'] += 1.0
                else:
                    self.graph.add_edge(u, v, weight=1.0)
            index += 1

    def combine_nodes(self, root, roots):
        text = " ".join(self.roots_words)
        for i in roots:
            text = text.replace(i, root)
        self.roots_words = text.split()

    def get_graph(self):
        return self.graph

    def get_graph_by_node_grade(self, amount=100):

        degree_dict = dict(self.graph.degree())
        nodes_sorted_by_degree = sorted(degree_dict, key=lambda x: degree_dict[x], reverse=True)
        top_x_nodes = nodes_sorted_by_degree[:amount]
        new_graph = self.graph.subgraph(top_x_nodes).copy()

        return new_graph

    def get_graph_by_edge_weight(self, amount=5):
        weights = nx.get_node_attributes(self.graph, 'weight')
        filtered_nodes = [node for node, weight in weights.items() if weight > amount]
        new_graph = self.graph.subgraph(filtered_nodes)
        return new_graph

    def get_weight_of_heaviest_node(self):
        weights = nx.get_node_attributes(self.graph, 'weight')
        max_weight = max(weights.values())
        return max_weight

    def get_weight_of_heaviest_edge(self):
        weights = nx.get_edge_attributes(self.graph, 'weight')
        max_weight = max(weights.values())
        return max_weight

    def get_weight_of_heaviest_grade(self):
        degree_dict = dict(self.graph.degree())
        max_grade = max(degree_dict.values())
        return max_grade

    def print_network(self,show_lables):
        # for node, data in self.graph.nodes(data=True):
        #     print(f"{node}: Peso {data['weight']}")
        #
        # for u, v, data in self.graph.edges(data=True):
        #     print(f"{u} --> {v}: Peso {data['weight']}")
        #
        weights = nx.get_node_attributes(self.graph, 'weight')

        try:
            plt.figure(figsize=(16, 9))
            circular_pos = nx.spring_layout(self.graph, k=0.15)  # Utiliza un diseño circular
            node_sizes = [weight * 50 for node, weight in weights.items()]

            nx.draw_networkx_nodes(self.graph, circular_pos, node_size=node_sizes)

            # Dibujar las aristas con un grosor proporcional al peso y el mismo color que los nodos
            for edge in self.graph.edges(data=True):
                nx.draw_networkx_edges(self.graph, circular_pos, edgelist=[(edge[0], edge[1])],
                                       width=2 * edge[2]['weight'], arrows=False, edge_color='lightblue')

            # Dibujar las etiquetas de los nodos con un tamaño proporcional a sus pesos y color negro
            if show_lables == 1:
                for node, weight in weights.items():
                    nx.draw_networkx_labels(self.graph, circular_pos, labels={node: node}, font_size=weight * 3,
                                            font_color='k')  # Cambia 'w' a 'k' para etiquetas negras

            # Mostrar el gráfico

            plt.ioff()
            plt.show()
        except Exception as e:
            print(e)

    def indexing(self):

        return

    def setIgnoreWords(self, iwords):
        self.ignore_words_added_list = iwords

    def addwordstoignore(self, iwords):
        ignore = ""
        user_documents_folder = os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks', 'Ignore.txt'))
        if not os.path.exists(user_documents_folder):
            path2 = resource_path("Ignore.txt")
            with open(path2, 'r', encoding='utf8') as f:
                ignore = f.read()
                # ignore = f.read().splitlines()
            # Si no existe, lo crea
            try:
                os.mkdir(os.path.expanduser(os.path.join('~', 'Documents', 'ConceptualNetworks')))
                with open(user_documents_folder, 'w', encoding='utf8') as f2:
                    f2.write(ignore)
            except Exception as e:
                print(e)
        else:
            try:
                with open(user_documents_folder, 'r', encoding='utf8') as f3:
                    ignore = f3.read()
            except Exception as e:
                print(e)

        ignore = ignore.splitlines()

        with open(user_documents_folder, 'a', encoding='utf8') as f:
            for word in iwords:
                if word not in ignore:
                    f.write('\n' + word.lower())

    def combine_roots(self, roots):
        root = self.structure_stemming.mergeList(roots)
        self.combine_nodes(root, roots)

    def get_cloud_words(self):
        return self.structure_stemming.get_firts_word_and_weights()

    def alphabeticSort(self):
        self.structure_stemming.sortStruture()

    def weigthSort(self):
        self.structure_stemming.sortStrutureWeigth()

    def delete_graph(self):
        self.graph.clear()


#x = TextHandlerAdmin()
#x.roots_words = ["hola", "jose", "arce", "jose", "gato", "gato"]
# x.combine_nodes("jose", ["jose","gato"])
#x.create_network()
#x.create_relation()
#x.print_network(1)
#print("------------------------")
#print(x.get_weight_of_heaviest_edge())
#print(x.get_weight_of_heaviest_node())
#print(x.get_weight_of_heaviest_grade())
