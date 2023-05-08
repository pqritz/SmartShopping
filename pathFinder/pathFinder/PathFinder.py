from typing import List, Tuple
from operator import itemgetter


class PathFinder:

    def __init__(self, graph, start, end, pass_through):
        self.graph = graph
        self.start = start
        self.end = end
        self.pass_through = pass_through

    def todoList(self):
        """
        Define a graph data structure that represents the network topology. The graph should consist of a set of nodes and a set of edges connecting the nodes. Each edge should have a weight, which represents the cost of traversing the edge.

        Implement a function that initializes the graph and sets the starting node as the current node.

        Define a set of must-visit nodes that the algorithm needs to include in the shortest path.

        Create an empty dictionary to store the tentative distance from the starting node to each node in the graph. Set the distance of the starting node to 0 and the distance of all other nodes to infinity.

        Create an empty set to store visited nodes.

        Create a priority queue to store nodes that need to be visited. Add the starting node to the queue with a priority of 0.

        While the priority queue is not empty, perform the following steps:
        a. Get the node with the highest priority from the priority queue.
        b. If the node is in the set of must-visit nodes, check if all other must-visit nodes have been visited. If not, continue to the next node with the highest priority in the queue.
        c. Mark the current node as visited and add it to the visited set.
        d. For each neighbor of the current node, calculate the tentative distance from the starting node to the neighbor by adding the weight of the edge connecting the nodes to the distance of the current node.
        e. If the tentative distance is less than the current distance for the neighbor, update the neighbor's distance and add it to the priority queue with a priority equal to its tentative distance.

        Once the priority queue is empty, the algorithm has found the shortest path from the starting node to all other nodes in the graph.

        To retrieve the shortest path from the starting node to the end node, backtrack from the end node to the starting node using the recorded distances and the graph data structure.

        Return the shortest path from the starting node to the end node.
        """

    def dijkstra(self, graph: List[List[Tuple[int, int]]], start: int, end: int, must_pass: List[int]) -> List[int]:
        current_node = start
        tent_dist = {}
        visited = []
        prio_que = [] #prio value is equals the shortest path that is currently found

        while len(prio_que) > 1:
            cur_node = prio_que.pop(prio_que.index((max(prio_que, key=itemgetter(1)))))


