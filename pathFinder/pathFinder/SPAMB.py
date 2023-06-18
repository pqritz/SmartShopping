from typing import List, Tuple


class SPAMB:
    def __init__(self, graph: List[List[Tuple[int, int]]], start: int, end: int, must_pass: List[int]):
        "self running logic in here"
        self.graph = graph
        self.start = start
        self.end = end
        self.must_pass = must_pass

        list = ['A', 'B' ,'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        path = self.SPAMB(graph, start, end, must_pass)

        for i in path:
            print(list[i])

    def write_start_tent(self, graph, start, path):
        if path:
            tent_dist = {i: [float("inf")] for i in range(0, len(graph))}
            tent_dist[start] = [0]
        else:
            tent_dist = {i: float("inf") for i in range(0, len(graph))}
            tent_dist[start] = 0

        return tent_dist

    def get_neighbours(self, graph, nodeIndex):
        node = graph[nodeIndex]
        nodes = []
        dist = []

        for i in node:
            if i[1] != 0:
                nodes.append(i[0])
                dist.append(i[1])

        return nodes, dist

    def calc_tent(self, graph, start):
        # (previous node, weight)
        shortest_paths = {start: (None, 0)}
        cur_node = start
        visited = []

        while len(graph) > len(visited):
            visited.append(cur_node)
            weight_to_current = shortest_paths[cur_node][1]
            neighbours, distances = self.get_neighbours(graph, cur_node)
            for i, next_node in enumerate(neighbours):
                dist = distances[i]
                new_weight = weight_to_current + dist
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (cur_node, new_weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > new_weight:
                        shortest_paths[next_node] = (cur_node, new_weight)
            if all(node in visited for node in neighbours):
                next_destinations = {node: shortest_paths[node] for node in shortest_paths}
            else:
                next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            cur_node = min(next_destinations, key=lambda k: next_destinations[k][1])

            # Work back through destinations in shortest path
        return shortest_paths

    def dijkstra(self, graph, start, end):
        shortest_paths = self.calc_tent(graph, start)
        print(shortest_paths)
        cur_node = end
        path = []
        while cur_node is not None:
            path.append(cur_node)
            next_node = shortest_paths[cur_node][0]
            cur_node = next_node
        # Reverse path
        path = path[::-1]
        return path

    def SPAMB(self, graph, start, end, must_pass):
        paths = [start]
        cur_node = start
        visited = []
        outer_must_pass = must_pass.copy()

        while cur_node != end:
            visited.append(cur_node)
            tent_dist = self.calc_tent(graph, start)
            if must_pass:
                for i in list(tent_dist):
                    if not i in must_pass:
                        del tent_dist[i]
            else:
                for i in list(tent_dist):
                    if not i is end:
                        del tent_dist[i]

            next_node = min(tent_dist, key=lambda k: tent_dist[k][1])
            path_to_next = self.dijkstra(graph, cur_node, next_node)
            del path_to_next[0]

            paths.extend(path_to_next)

            if next_node in must_pass:
                must_pass.pop(must_pass.index(next_node))

            cur_node = next_node

        return paths