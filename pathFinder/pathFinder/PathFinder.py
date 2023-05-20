from typing import List, Tuple
from operator import itemgetter


class PathFinder:

    def __init__(self, graph, start, end, pass_through):
        self.graph = graph
        self.start = start
        self.end = end
        self.pass_through = pass_through

    def get_neighbours(self, graph, nodeIndex):
        node = graph[nodeIndex]
        nodes = []
        dist = []

        for i in node:
            if i[1] != 0:
                nodes.append(i[0])
                dist.append(i[1])

        return nodes, dist

    def write_tent(self, graph, start):
        tent_dist = {i: [float('inf')] for i in range(0, len(graph))}
        tent_dist[start] = [0]
        return tent_dist

    def find_shortest_with_must_pass(self, graph, start, end, must_pass: List[int]):
        path = []
        cur_node = start
        must_pass_nodes = must_pass

        while cur_node != end:
            if not must_pass_nodes:
                shortest_path = self.calc_tent_with_path(graph, cur_node, end)
                for i in shortest_path:
                    path.append(i)
                break

            tent = self.calc_tent(graph, cur_node)
            changable_tent = tent.copy()
            for key in list(changable_tent.keys()):

                if not key in must_pass_nodes:
                    del changable_tent[key]

            next_node = min(changable_tent, key=changable_tent.get)
            shortest_path = self.calc_tent_with_path(graph, cur_node, next_node)

            for i in shortest_path:
                path.append(i)

            cur_node = next_node
            must_pass_nodes.remove(cur_node)

        return path

    def calc_tent(self, graph: List[List[Tuple[int, int]]], start: int):
        tent_dist = self.write_tent(graph, start)
        visited = []
        prio_que = [] #prio value is equals the shortest path that is currently found
        prio_que.append((start, 0))

        while len(prio_que) > 0:
            #step a
            cur_node = prio_que.pop(prio_que.index((min(prio_que, key=itemgetter(1)))))
            #step c
            visited.append(cur_node)

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

        return tent_dist

    def calc_tent_with_path(self, graph, start, end):
        path = [start]
        visited = []
        tent_dist = self.write_tent(start)
        cur_node = start

        while cur_node != end:
            visited.append(cur_node)
            neighbours, distances = self.get_neighbours(graph, cur_node)
            next_node = None
            min_dist = float("inf")

            for i, neighbour in enumerate(neighbours):
                distance = distances[i]
                if neighbour == cur_node and len(neighbours) > 1:
                    continue

                if tent_dist[cur_node][0] + distance < tent_dist[neighbour][0]:
                    tent_dist[neighbour][0] = tent_dist[cur_node][0] + distance
                    for i in path:
                        tent_dist[neighbour].append(i)
                if distance < min_dist:
                    if all(item in neighbours for item in visited):
                        next_node = neighbour
                    else:
                        if not neighbour in visited:
                            next_node = neighbour

            path.append(next_node)
            cur_node = next_node

        del tent_dist[end][0]
        print(tent_dist[end])
        return tent_dist[end]

    """
    def backtrack(self, graph, start, end, must_pass, tent_dist):
        path = [end]
        cur_node = end
        visited = []
        print(cur_node)

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
            print(next_node)
            cur_node = next_node

        return path.reverse()
    """