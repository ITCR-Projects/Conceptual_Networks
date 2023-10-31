from Codigo.Controller.TextHandlerAdmin import TextHandlerAdmin


#HOLAMUNDO PRUEBA 5

class MainController:
    def __init__(self):
        self.textHandlerAdmin = TextHandlerAdmin()

    def addFiles(self, filepath):
        if filepath == "":
            return {
                'response': True,
                'message': "Ruta del archivo inválida",

            }
        return self.textHandlerAdmin.add_file(filepath)

    def textAnalysis(self):
        return self.textHandlerAdmin.lexical_analysis()

    def cleanText(self):
        self.textHandlerAdmin.setTextBlank()

    def setIgnoreWords(self, iwords):
        self.textHandlerAdmin.setIgnoreWords(iwords)

    def addwordstoignore(self, iwords):
        self.textHandlerAdmin.addwordstoignore(iwords)

    def getStatistics(self):
        return self.textHandlerAdmin.statistics()

    def combine_roots(self, roots):
        self.textHandlerAdmin.combine_roots(roots)

    def get_cloud_words(self, number):
        return self.textHandlerAdmin.get_cloud_words(number)

    def alphabeticSort(self):
        self.textHandlerAdmin.alphabeticSort()

    def weigthSort(self):
        self.textHandlerAdmin.weigthSort()

    def get_graph(self):
        return self.textHandlerAdmin.get_graph()

    def get_graph_by_filters(self, node_weight, edge_weight, node_grade, type_word):
        return self.textHandlerAdmin.get_graph_by_filters(node_weight, edge_weight, node_grade, type_word)

    def create_network(self):
        self.textHandlerAdmin.create_network()

    def create_relation(self,step=1):
        self.textHandlerAdmin.create_relation(step)

    #por tamaño de nodo !
    def get_graph_by_node_weight(self,amount=0):
        return self.textHandlerAdmin.get_graph_by_node_weight(amount)
    def get_weight_of_heaviest_node(self):
        return self.textHandlerAdmin.get_weight_of_heaviest_node()
    #por tamaño de arsita
    def get_graph_by_edge_weight(self, amount=5):
        return self.textHandlerAdmin.get_graph_by_edge_weight(amount)
    def get_weight_of_heaviest_edge(self):
        return self.textHandlerAdmin.get_weight_of_heaviest_edge()

    #por grado del nodo
    def get_graph_by_node_grade(self, amount):
        return self.textHandlerAdmin.get_graph_by_node_grade(amount)
    def get_weight_of_heaviest_grade(self):
        return self.textHandlerAdmin.get_weight_of_heaviest_grade()
    def delete_graph(self):
        self.textHandlerAdmin.delete_graph()

