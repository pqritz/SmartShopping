import SPAMB as pf
import Graph

graph = Graph.Graph(True)

node_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

graph_data = graph.to_adjacency_list()
finder = pf.SPAMB(graph_data, 1, 4, [0])

x = True
while x:
    s = input("What number to convert into Alphabet?")
    if s == "stop":
        x = False
        break
    print(node_list[int(s)])

