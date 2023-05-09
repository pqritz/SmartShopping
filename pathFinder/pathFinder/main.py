import PathFinder as pf
import Graph

test = [(0, 1), (2, 0)]
print(1 in test[0])
if 1 in test[0]:
    del test[test[0].index(1)]
print(test)
graph = Graph.Graph(False)
finder = pf.PathFinder(None, None, None, None)

graph_data = graph.to_adjacency_list()
graph = {}
for i in range(len(graph_data)):
    node_edges = {}
    for j in range(1, len(graph_data[i])):
        dest_node, weight = graph_data[i][j]
        node_edges[dest_node] = weight
    graph[graph_data[i][0]] = node_edges

finder.get_neighbours(graph_data, 2)
finder.dijkstra(graph_data, 2, 4, [2])
