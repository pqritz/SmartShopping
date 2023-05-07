import random
import networkx as nx
import plotly.graph_objs as go
import math

node_list = ["A","B","C","D","E","F","G","H","E"]

"""
def is_connected(name1, name2):
    names = fig.data[1].pop("text")
    namedCoords = fig.data[1].pop("x")
    connectedCoords = fig.data[0].pop("x")

    i1 = names.index(name1)
    i2 = names.index(name2)

    p1x = float(namedCoords[i1])
    p2x = float(namedCoords[i2])

    for count, value in enumerate(connectedCoords):
        print(type(count), type(len(connectedCoords)))
        if value == p1x:
            if connectedCoords[count + 1] == p2x:
                return True

            if count != 0:
                if connectedCoords[count - 1] == p2x:
                    return True

    return False
"""


def return_map():
    return fig.data


def return_length(name1, name2):
    names = fig.data[1].pop("text")
    xCoords = fig.data[1].pop("x")
    yCoords = fig.data[1].pop("y")

    i1 = names.index(name1)
    i2 = names.index(name2)

    p1 = (float(xCoords[i1]), float(yCoords[i1]))
    p2 = (float(xCoords[i2]), float(yCoords[i2]))

    distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

    return distance


def draw_number(length):
    """determines a random index number for selection."""
    from_index = random.randint(0, length)
    to_index = random.randint(0, length)
    return from_index, to_index


from_list = []
to_list = []
counter = 20
i = 0
while i < counter:
    from_index, to_index = draw_number(len(node_list)-1)
    if from_index == to_index:
        continue
    from_list.append(node_list[from_index])
    to_list.append(node_list[to_index])
    i += 1


G = nx.Graph()
for i in range(len(node_list)):
    G.add_node(node_list[i])
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

fig.show()
