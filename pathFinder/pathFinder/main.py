import PathFinder as pf
import Graph


graph = Graph.Graph(False)
finder = pf.PathFinder(None, None, None, None)

graph_data = graph.to_adjacency_list()
print(finder.dijkstra(graph_data, 0, 4, [1]))

print(graph.node_list[0], graph.node_list[4])
