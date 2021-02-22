import matplotlib.pyplot as plt
import networkx as nx


def sim_to_rgba(similarity, edge_color):
    """Convert similarity to RGBA.

    Parameters
    ----------
    similarity : float
        Similarity between two answers.
    edge_color : tuple
        When the graph is plotted, this is the RGB color of the edge
        i.e (0, 0, 1).

    Returns
    -------
    tuple i.e (0, 0, 1, 0.78)
        RGBA values i.e (R, G, B, A).

    """
    RGBA = (
        *edge_color, similarity
    )
    return RGBA


# haven't figured out how to determine each edge length with networkx
# def sim_to_length(similarity):
#     """Convert similarity to edge length.
#
#     Parameters
#     ----------
#     similarity : float
#         Similarity between two answers.
#
#     Returns
#     -------
#     float
#         Value between 0 and 100 corresponding to the distance between
#         two nodes.
#
#     """
#     return 100-(similarity*100)


def sim_to_width(similarity):
    """Convert similarity to edge width.

    Parameters
    ----------
    similarity : float
        Similarity between two answers.

    Returns
    -------
    float
        Width of an edge.

    """
    return similarity*10


def sim_to_label(similarity):
    """Convert similarity to edge label.

    Parameters
    ----------
    similarity : float
        Similarity between two answers.

    Returns
    -------
    str
        Label of the edge. Similarity in percentage i.e 90%.

    """
    return str(round(similarity*100)) + '%'


def edge_with_plotting_attributes(edge, edge_color):
    """Add plotting attributes to the edge, such as the color and the width.

    Parameters
    ----------
    edge : dict
        Edge between two nodes i.e
        {'nodes': (1, 2), 'similarity': 0.97}
    edge_color : tuple
        RGB color of the edge i.e (0, 0, 1). What changes from edge to edge is
        the alpha of the RGBA color.

    Returns
    -------
    dict
        Edge between two nodes with the plotting attributes i.e
        {
         'nodes': (1, 2), 'similarity': 0.97,
         'color': (0, 0, 1, 0.97), 'width': 9.7, 'label': '97%'
        }

    """
    edge_to_plot = edge.copy()
    edge_to_plot['color'] = sim_to_rgba(edge_to_plot['similarity'], edge_color)
    # edge_to_plot['length'] = sim_to_length(edge_to_plot['similarity'])
    edge_to_plot['width'] = sim_to_width(edge_to_plot['similarity'])
    edge_to_plot['label'] = sim_to_label(edge_to_plot['similarity'])
    return edge_to_plot


def plot_edge_list(edge_list, node_color='orange', edge_color=(0, 0, 1)):
    """Plot a graph from the closest edges.

    Parameters
    ----------
    edge_list : list
        List of the graph edges. It's a list of dicts.
        i.e [{'nodes': (i1, j2), 'similarity': matrix[i1][j2]}, ...]
    node_color : str
        The node color is the same for all nodes. It should be passed as a
        color name i.e 'orange'.
    edge_color : tuple
        When the graph is plotted, this is the RGB color of all edges
        i.e (0, 0, 1). What changes from edge to edge is the alpha of the RGBA
        color.

    """
    graph_nx = nx.Graph()
    edge_colors = []
    edge_widths = []
    edge_labels = {}

    for edge in edge_list:
        edge_to_plot = edge_with_plotting_attributes(edge, edge_color)
        graph_nx.add_edge(edge_to_plot['nodes'][0], edge_to_plot['nodes'][1])
        edge_colors.append(edge_to_plot['color'])
        edge_widths.append(edge_to_plot['width'])
        edge_labels[edge_to_plot['nodes']] = edge_to_plot['label']

    pos = nx.spring_layout(graph_nx)
    # plot the graph
    nx.draw(
        graph_nx, pos,
        node_size=1000,
        edge_color=edge_colors,
        width=edge_widths,
        with_labels=True,
        node_color=node_color
    )
    nx.draw_networkx_edge_labels(
        graph_nx, pos, edge_labels=edge_labels
    )
    plt.show()
