from copy import deepcopy


def matrix_to_edge_list(matrix, n):
    """Keep only the upper triangle of the adjacency matrix without its
    diagonal. Probably, should only be used in the case of an undirected graph.

    Parameters
    ----------
    matrix : list of a list
        Square adjacency matrix of an undirected graph.
    n : int
        The shape of the matrix should be (n, n, ).

    Returns
    -------
    list
        List of the graph edges. It's a list of dicts.
        i.e [{'nodes': (i1, j2), 'similarity': matrix[i1][j2]}, ...]

    """
    edge_list = []
    for i in range(n):
        for j in range(n):
            # consider only the upper triangle without the diagonal
            if j <= i:
                continue
            edge_list.append({
                'nodes': (i, j),
                'similarity': max(0, min(1, matrix[i][j]))
            })
    return edge_list


def closest_edges(edge_list, threshold):
    """Threshold the edge_list considering only the similarity.

    Parameters
    ----------
    edge_list : list
        List of the graph edges. It's a list of dicts.
        i.e [{'nodes': (i1, j2), 'similarity': matrix[i1][j2]}, ...]

    Returns
    -------
    list
        List of the graph edges. It's a list of dicts.
        i.e [{'nodes': (i1, j2), 'similarity': matrix[i1][j2]}, ...]

    """
    # the threshold determines whether two nodes are connected
    return [edge for edge in edge_list if edge['similarity'] > threshold]


# slow due to Python for loops
def calc_mean_edge_list(list_of_edge_lists):
    """Suppose you have two edge lists and you want to know the mean between
    them. In the case of this cheat detector, you would calculate the mean
    similarity between each edge of the edge lists (the pairwise mean). That's
    what this function does.

    Parameters
    ----------
    list_of_edge_lists : list
        edge_list list

    Returns
    -------
    list
        Mean edge list.

    """
    mean_edge_list = deepcopy(list_of_edge_lists[0])
    for edge_list in list_of_edge_lists[1:]:
        for mean_edge, edge in zip(mean_edge_list, edge_list):
            mean_edge['similarity'] += edge['similarity']
    n = len(list_of_edge_lists)
    for edge in mean_edge_list:
        edge['similarity'] /= n
    return mean_edge_list
