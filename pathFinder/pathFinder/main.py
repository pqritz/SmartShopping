import PathFinder as pf
import Graph


graph = Graph.Graph(True)
finder = pf.PathFinder(None, None, None, None)

graph_data = graph.to_adjacency_list()

finder.find_shortest_with_must_pass(graph_data, 1, 2, [4])
