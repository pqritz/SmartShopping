import PathFinder as pf
import Graph

graph = Graph.Graph(True)
finder = pf.PathFinder(None, None, None, None)

graph_data = graph.to_adjacency_list()
graph = {}
for i in range(len(graph_data)):
    node_edges = {}
    for j in range(1, len(graph_data[i])):
        dest_node, weight = graph_data[i][j]
        node_edges[dest_node] = weight
    graph[graph_data[i][0]] = node_edges

print(graph_data)
print(finder.dijkstra(graph, 0, 4, [2]))
