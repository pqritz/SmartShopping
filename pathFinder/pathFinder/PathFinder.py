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
        Start by initializing the distances of all nodes to infinity, except for the start node, which is set to 0.

        Create a priority queue to store the nodes that we need to visit next. Add the start node to the priority queue.

        Create a dictionary to store the shortest path to each node, which initially contains only the start node.

        Create a set to store the set of specified nodes that we need to pass through.

        Create a dictionary to store the shortest paths that pass through all specified nodes, which initially contains no paths.

        While the priority queue is not empty, do the following:

        a. Pop the node with the smallest distance from the priority queue.

        b. If the popped node is the end node and we have passed through all specified nodes, then we have found a path that satisfies the condition. Add this path to the dictionary of shortest paths that pass through all specified nodes.

        c. If the popped node is not the end node, then consider its neighbors. For each neighbor, calculate the distance to that neighbor as the sum of the distance to the current node and the weight of the edge between them.

        d. If the distance to the neighbor is less than its current distance, update the distance and add the neighbor to the priority queue.

        e. If the neighbor is one of the specified nodes, remove it from the set of specified nodes.

        f. If the set of specified nodes is empty, then we have passed through all specified nodes. Add the current node to the list of nodes on the current path that passes through all specified nodes, and continue exploring its neighbors.

        Once the priority queue is empty, return the shortest path from the dictionary of shortest paths that pass through all specified nodes.
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
        path = {}

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

            if cur_node == end and len(must_pass) == 0:
                path[len(path) - 1] = end

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


