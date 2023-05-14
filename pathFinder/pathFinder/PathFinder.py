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
        Create a set called remaining_must_pass containing all the must_pass nodes.
        Initialize a dictionary called distances with the tentative distance to every point in the graph from the starting point. Set the distance to the starting point to 0 and the distance to all other points to infinity.
        Initialize a dictionary called prev to keep track of the previous node on the shortest path to each node. Set the previous node for the starting point to None.
        Initialize a list called visited to keep track of visited nodes. Add the starting node to the visited list.
        While remaining_must_pass is not empty:
        Find the must_pass node with the smallest tentative distance from the starting point. If there are multiple must_pass nodes with the same distance, choose one arbitrarily.
        Remove the chosen must_pass node from remaining_must_pass.
        Run Dijkstra's algorithm to find the shortest path from the starting point to the chosen must_pass node, using the distances and prev dictionaries as described in the algorithm.
        Add all nodes on the shortest path from the starting point to the chosen must_pass node (excluding the starting point) to the visited list.
        Run Dijkstra's algorithm to find the shortest path from the last chosen must_pass node to the end node, using the distances and prev dictionaries as described in the algorithm.
        Add all nodes on the shortest path from the last chosen must_pass node to the end node (including the end node) to the visited list.
        If the visited list contains all the must_pass nodes and the end node, return the list of visited nodes as the shortest path. Otherwise, return that there is no path that passes through all the must_pass nodes and ends at the end node.
        Here's a step-by-step list of actions you can take based on this algorithm:

        Initialize remaining_must_pass with all the must_pass nodes.
        Initialize distances with the tentative distance to every point in the graph from the starting point.
        Initialize prev with the previous node on the shortest path to each node.
        Initialize visited with the starting node.
        While remaining_must_pass is not empty:
        Find the must_pass node with the smallest tentative distance from the starting point. If there are multiple must_pass nodes with the same distance, choose one arbitrarily.
        Remove the chosen must_pass node from remaining_must_pass.
        Initialize distances and prev dictionaries for running Dijkstra's algorithm from the starting point to the chosen must_pass node.
        Run Dijkstra's algorithm to find the shortest path from the starting point to the chosen must_pass node.
        Update visited with all nodes on the shortest path from the starting point to the chosen must_pass node (excluding the starting point).
        Initialize distances and prev dictionaries for running Dijkstra's algorithm from the last chosen must_pass node to the end node.
        Run Dijkstra's algorithm to find the shortest path from the last chosen must_pass node to the end node.
        Update visited with all nodes on the shortest path from the last chosen must_pass node to the end node (including the end node).
        If visited contains all the must_pass nodes and the end node, return visited as the shortest path. Otherwise, return
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
        visited = []

        while cur_node != start:
            neighbours, distances = self.get_neighbours(graph, cur_node)
            min_dist = float("inf")
            next_node = None

            if all(node in visited for node in neighbours):
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
            else:
                for i, neighbour in enumerate(neighbours):
                    if neighbour in visited:
                        continue
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
            visited.append(cur_node)
            cur_node = next_node

        return path.reverse()