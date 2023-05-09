import PathFinder as pf
import Graph


graph = Graph.Graph(True)
finder = pf.PathFinder(None, None, None, None)

graph_data = graph.to_adjacency_list()
print(finder.dijkstra(graph_data, 0, 4, [2]))
