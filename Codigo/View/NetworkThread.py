# PyQt6 dependencies
import networkx as nx
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib import pyplot as plt


# Class that create a thread to process the files
class NetworkThread(QThread):

    finished = pyqtSignal()
    def __init__(self, main_controller, show_lables, type_graph, nodeSize, edgeWeight, relation):
        super().__init__()
        self.main_controller = main_controller
        self.show_lables = show_lables
        self.type_graph = type_graph
        self.nodeSize = nodeSize
        self.edgeWeight = edgeWeight
        self.relation = relation

    def run(self):
        self.main_controller.create_network()
        self.main_controller.create_relation(self.relation)

        if self.type_graph == 1:
            graph = self.main_controller.get_graph()  # todo en general
        elif self.type_graph == 2:
            graph = self.main_controller.get_graph_by_node_grade(self.nodeSize)  # cantidad de lo nodos que tiene mas grados
        elif self.type_graph == 3:
            graph = self.main_controller.get_graph_by_edge_weight(self.edgeWeight)  # por tamaño de la arista

        weights = nx.get_node_attributes(graph, 'weight')
        max_node_weight = max(weights.values())
        edge_weights = [data['weight'] for u, v, data in graph.edges(data=True)]
        max_edge_weight = max(edge_weights)

        try:

            print(str(max_node_weight))
            print(str(max_edge_weight))
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
                    normalized_weight = (weight / max_node_weight) * 30

                    nx.draw_networkx_labels(graph, circular_pos, labels={node: node}, font_size=normalized_weight,
                                            font_color='k')  # Cambia 'w' a 'k' para etiquetas negras

            # Mostrar el gráfico
            #plt.show()
            #plt.savefig("network.png", bbox_inches='tight', pad_inches=0, transparent=True)
        except Exception as e:
            print(e)
        self.finished.emit()