import PathFinder as pf
import Graph


graph = Graph.Graph(True)
finder = pf.PathFinder(None, None, None, None)


for i in graph.to_adjacency_matrix():
    print(i)