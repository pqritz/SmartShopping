import SPAMB as pf
import Graph

graph = Graph.Graph(False)

graph_data = graph.to_adjacency_list()

finder = pf.SPAMB(graph_data, 1, 4, [0, 6])
