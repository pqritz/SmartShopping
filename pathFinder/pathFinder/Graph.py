import random
import networkx as nx
import plotly.graph_objs as go
import math


class Graph:

    def __init__(self, show_fig):
        self.node_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.show = show_fig
        self.fig = self.functionality()

        self.names, self.connected_x_coords, self.xCoords, self.yCoords = self.return_graph_values()

    def to_adjacency_list(self):
        rows = []
        for i in range(0, len(self.node_list)):
            column = []
            for j in range(0, len(self.node_list)):
                if self.is_connected(self.node_list[i], self.node_list[j]):
                    column.append((j, self.return_length(self.node_list[i], self.node_list[j])))
            rows.append(column)

        return rows

    def return_graph_values(self):
        return self.fig.data[1].pop("text"), self.fig.data[0].pop("x"), self.fig.data[1].pop("x"), self.fig.data[1].pop("y")

    def is_connected(self, name1, name2):

        if str(name1).lower() == str(name2).lower():
            return True

        i1 = self.names.index(name1)
        i2 = self.names.index(name2)

        p1x = float(self.xCoords[i1])
        p2x = float(self.xCoords[i2])

        for count, value in enumerate(self.connected_x_coords):
            if value == p1x:
                if self.connected_x_coords[count + 1] == p2x:
                    return True

                if count != 0:
                    if self.connected_x_coords[count - 1] == p2x:
                        return True

        return False

    def return_map(self):
        return self.fig.data

    def return_length(self, name1, name2):

        if str(name1).lower() == str(name2).lower():
            return 0

        i1 = self.names.index(name1)
        i2 = self.names.index(name2)

        p1 = (float(self.xCoords[i1]), float(self.yCoords[i1]))
        p2 = (float(self.xCoords[i2]), float(self.yCoords[i2]))

        distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


        return distance

    def draw_number(self, length):
        """determines a random index number for selection."""
        from_index = random.randint(0, length)
        to_index = random.randint(0, length)
        while from_index == to_index:
            to_index = random.randint(0, length)
        return from_index, to_index

    def functionality(self):

        from_list = []
        to_list = []
        counter = 50
        i = 0
        while i < counter:
            from_index, to_index = self.draw_number(len(self.node_list) - 1)
            if from_index == to_index:
                continue
            from_list.append(self.node_list[from_index])
            to_list.append(self.node_list[to_index])
            i += 1

        for i, value in enumerate(self.node_list):
            if value not in from_list and value not in to_list:

                from_list.append(self.node_list[i])
                if i == len(self.node_list) - 1:
                    to_list.append(self.node_list[0])
                else:
                    to_list.append(self.node_list[i - 1])

        G = nx.Graph()
        for i in range(len(self.node_list)):
            G.add_node(self.node_list[i])

        for i in range(len(from_list)):
            G.add_edges_from([(from_list[i], to_list[i])])

        pos = nx.spring_layout(G)
        for n, p in pos.items():
            G.nodes[n]['pos'] = p

        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                colorscale='pinkyl',
                reversescale=True,
                color=[],
                size=37,
                colorbar=dict(
                    thickness=1,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=0)))
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        for node, adjacencies in enumerate(G.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = adjacencies[0]
            node_trace['text'] += tuple([node_info])

        title = "Route"
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=title,
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=21, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Smart Shopping",
                                showarrow=False,
                                xref="paper", yref="paper")],
                            xaxis=dict(showgrid=False, zeroline=False,
                                       showticklabels=False, mirror=True),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True)))

        if self.show:
            fig.show()
        return fig
