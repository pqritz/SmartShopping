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
        <DONE UNTIL THIS POINT> a. Get the node with the highest priority from the priority queue.
        <DONE UNTIL THIS POINT> b. If the node is in the set of must-visit nodes, check if all other must-visit nodes have been visited. If not, continue to the next node with the highest priority in the queue.
        <DONE UNTIL THIS POINT> c. Mark the current node as visited and add it to the visited set.
        <DONE UNTIL THIS POINT> d. For each neighbor of the current node, calculate the tentative distance from the starting node to the neighbor by adding the weight of the edge connecting the nodes to the distance of the current node.
        <DONE UNTIL THIS POINT> e. If the tentative distance is less than the current distance for the neighbor, update the neighbor's distance and add it to the priority queue with a priority equal to its tentative distance.

        <DONE UNTIL THIS POINT> Once the priority queue is empty, the algorithm has found the shortest path from the starting node to all other nodes in the graph.

        To retrieve the shortest path from the starting node to the end node, backtrack from the end node to the starting node using the recorded distances and the graph data structure.

        Return the shortest path from the starting node to the end node.
        """

        #[(0, inf), (1, 0), (2, inf), (3, inf), (4, inf), (5, inf), (6, inf), (7, inf), (8, inf)]

    def get_neighbours(self, graph, nodeIndex):
        node = graph[nodeIndex]
        nodes = []
        dist = []

        for i in node:
            if i[1] != 0:
                nodes.append(i[0])
                dist.append(i[1])

        return nodes, dist

    def dijkstra(self, graph: List[List[Tuple[int, int]]], start: int, end: int, must_pass: List[int]) -> List[int]:
        tent_dist = {}
        visited = []
        prio_que = [] #prio value is equals the shortest path that is currently found
        unedited_must_pass = must_pass

        for i in range(0, len(graph)):
            if i == start:
                tent_dist[i] = 0
                continue
            tent_dist[i] = float("inf")

        prio_que.append((start, 0))

        while len(prio_que) > 1:
            #step a
            cur_node = prio_que.pop(prio_que.index((min(prio_que, key=itemgetter(1)))))
            #step c
            visited.append(cur_node)

            #step b
            if cur_node in must_pass:
                must_pass.remove(cur_node)

            #step d
            cur_node_tent = tent_dist[cur_node[0]]
            neighbours, distances = self.get_neighbours(graph, cur_node[0])

            for i, neighbour in enumerate(neighbours):
                dist = distances[i]
                new_tent = cur_node_tent + dist
                if new_tent < tent_dist[neighbour]:
                    tent_dist[neighbour] = new_tent

                    if neighbour not in [item[0] for item in prio_que]:
                        prio_que.append((neighbour, new_tent))
                    else:
                        for i, item in enumerate(prio_que):
                            if item[0] == neighbour:
                                prio_que[i] = (neighbour, new_tent)
                                break


            #at the end (step b)
            if len(must_pass) <= 0:
                break

        return self.backtrack(graph, start, end, unedited_must_pass, tent_dist)

    def backtrack(self, graph, start, end, must_pass, tent_dist):
        path = [end]
        cur_node = end

        while cur_node != start:
            neighbours, distances = self.get_neighbours(graph, cur_node)
            min_dist = float("inf")
            next_node = None

            for i, neighbour in enumerate(neighbours):
                if tent_dist[neighbour] + distances[i] == tent_dist[cur_node]:
                    if neighbour in must_pass:
                        if tent_dist[neighbour] < min_dist:
                            min_dist = tent_dist[neighbour]
                            next_node = neighbour
                    else:

                        if distances[i] < min_dist:
                            min_dist = distances[i]
                            next_node = neighbour
            path.append(next_node)
            cur_node = next_node

        return path.reverse()
