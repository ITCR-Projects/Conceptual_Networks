# PyQt6 dependencies
import networkx as nx
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib import pyplot as plt


# Class that create a thread to process the files
class NetworkThread(QThread):

    finished = pyqtSignal()
    def __init__(self, main_controller, show_lables, type_graph, nodeSize, edgeWeight, nodeGrade,  relation, type_word):
        super().__init__()
        self.main_controller = main_controller
        self.show_lables = show_lables
        self.type_graph = type_graph
        self.nodeSize = nodeSize
        self.edgeWeight = edgeWeight
        self.nodeGrade = nodeGrade
        self.relation = relation
        self.type_word = type_word

    def run(self):
        self.main_controller.set_network_data()
        self.main_controller.create_network()
        self.main_controller.create_relation(self.relation)

        graph= nx.Graph()
        #print("Aquí voyyyyyyyyy <<<<<<<<<<<<<<")
        try:

            graph = self.main_controller.get_graph_by_filters(self.nodeSize,self.edgeWeight,self.nodeGrade, self.type_word)
            # if self.type_graph == 1:
            #     graph = self.main_controller.get_graph_by_node_weight(0)# all in general
            #    #graph = self.main_controller.get_graph()  # all in general
            #
            # elif self.type_graph == 2:
            #     graph = self.main_controller.get_graph_by_node_weight(self.nodeSize)  # cantidad de lo nodos que tiene mas grados
            #
            # elif self.type_graph == 3:
            #     graph = self.main_controller.get_graph_by_edge_weight(self.edgeWeight)  # por tamaño de la arista
            #
            # elif self.type_graph == 4:
            #     graph = self.main_controller.get_graph_by_node_grade(self.nodeGrade)  # por tamaño de la arista

            try:
                weights = nx.get_node_attributes(graph, 'weight')
                max_node_weight = max(weights.values())
                print("CACA1.2")
            except Exception as e:
                max_node_weight = 1
                print(e)
            try:
                edge_weights = [data['weight'] for u, v, data in graph.edges(data=True)]
                max_edge_weight = max(edge_weights)
            except Exception as e:
                max_edge_weight = 1
                print(e)



            #print(str(max_node_weight))
            #print(str(max_edge_weight))
            plt.figure(num=2,figsize=(16, 9))
            circular_pos = nx.spring_layout(graph, k=0.30)  # Utiliza un diseño circular
            node_sizes = [(weight / max_node_weight) * 400 for node, weight in weights.items()]

            nx.draw_networkx_nodes(graph, circular_pos, node_size=node_sizes)
            # Dibujar las aristas con un grosor proporcional al peso y el mismo color que los nodos
            for edge in graph.edges(data=True):

                num_relations = edge[2]['weight']
                normalized_weight = (num_relations / max_edge_weight) * 20

                nx.draw_networkx_edges(graph, circular_pos, edgelist=[(edge[0], edge[1])],
                                       width=normalized_weight, arrows=False, edge_color='lightblue')

            # Dibujar las etiquetas de los nodos con un tamaño proporcional a sus pesos y color negro
            if self.show_lables == 0:
                for node, weight in weights.items():

                    normalized_weight = (weight / max_node_weight) * 40

                    nx.draw_networkx_labels(graph, circular_pos, labels={node: node}, font_size=normalized_weight,
                                            font_color='k')  # Cambia 'w' a 'k' para etiquetas negras

            # Mostrar el gráfico

            plt.subplots_adjust(left=0, right=1, top=1, bottom=0) #posible solucion tengo mis dudas

            #plt.show()
            #plt.savefig("network.png", bbox_inches='tight', pad_inches=0, transparent=True)
        except Exception as e:
            print(e)
        self.finished.emit()