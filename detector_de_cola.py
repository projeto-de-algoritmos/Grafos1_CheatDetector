# text similarity related imports
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# plotting related imports
import matplotlib.pyplot as plt
import networkx as nx


class DetectorDeCola():
    """Cheat detector for written exams with multiple questions.

    Parameters
    ----------
    edge_color : tuple
        When the graph is plotted, this is the RGB color of the edge
        i.e (0, 0, 1).
    node_color : str
        When the graph is plotted, this is the color of the node i.e 'orange'.
    transformer_name : str
        Name of a sentence transformer from HuggingFace.

    Attributes
    ----------
    model : SentenceTransformer
        Sentence Transformer loaded from transformer_name.
    edge_color
    node_color
    transformer_name

    """

    def __init__(self, edge_color=(0, 0, 1), node_color='orange',
                 transformer_name='distiluse-base-multilingual-cased'):
        """Initialize this class.

        Parameters
        ----------
        edge_color : tuple
            RGB color i.e blue would be (0, 0, 1).
        node_color : str
            Color str i.e 'orange'.
        transformer_name : str
            Name of a sentence transformer from HuggingFace.

        """
        self.edge_color = edge_color
        self.node_color = node_color
        self.transformer_name = transformer_name
        self.model = SentenceTransformer(self.transformer_name)

    def predict_sim_matrix(self, answer_list):
        """Generate the embeddings, then the similarity matrix.

        Parameters
        ----------
        answer_list : list of str
            One string for the answer of each student.

        Returns
        -------
        numpy.ndarray
            Similarity matrix of shape (len(answer_list), len(answer_list)).

        """
        return cosine_similarity(self.model.encode(answer_list))

    def sim_to_rgba(self, similarity, threshold):
        """Convert similarity to RGBA.

        Parameters
        ----------
        similarity : float
            Similarity between two answers.

        Returns
        -------
        tuple i.e (0, 0, 1, 0.78)
            RGBA values i.e (R, G, B, A).

        """
        RGBA = (
            *self.edge_color, similarity
            # *self.edge_color, (similarity-threshold)*(1-threshold)
        )
        return RGBA

    def sim_to_length(self, similarity):
        """Convert similarity to edge length.

        Parameters
        ----------
        similarity : float
            Similarity between two answers.

        Returns
        -------
        float
            Value between 0 and 100 corresponding to the distance between
            two nodes.

        """
        return 100-(similarity*100)

    def sim_to_width(self, similarity):
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

    def sim_to_label(self, similarity):
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

    def sim_matrix_to_closest_answers(self, sim_matrix, threshold):
        """Analyzes the similarity matrix and returns a graph
        of the most similar answers.

        Parameters
        ----------
        numpy.ndarray
            Similarity matrix of shape (len(answer_list), len(answer_list)).

        Returns
        -------
        dict
            Graph of the closest answers.

        """
        graph = {}
        for i in range(sim_matrix.shape[0]):
            for j in range(sim_matrix.shape[1]):
                # consider only the upper triangle without the diagonal
                if j <= i:
                    continue
                similarity = max(0, min(1, sim_matrix[i][j]))
                # this threshold determines whether two nodes are connected
                if similarity <= threshold:
                    continue
                edge_attr = {
                    'color': self.sim_to_rgba(similarity, threshold),
                    'length': self.sim_to_length(similarity),
                    'width': self.sim_to_width(similarity),
                    'label': self.sim_to_label(similarity),
                }
                if i+1 not in graph:
                    graph[i+1] = {}
                if j+1 not in graph:
                    graph[j+1] = {}
                graph[i+1][j+1] = edge_attr
                graph[j+1][i+1] = edge_attr
        return graph

    def plot_closest_answers(self, graph):
        """Plot the closest answers graph.

        Parameters
        ----------
        graph : dict
            Closest answers graph.

        """
        graph_nx = nx.from_dict_of_dicts(graph)
        pos = nx.spring_layout(graph_nx)
        # get the label of each edge
        edge_labels = {}
        for i in graph.items():
            for j in i[1].items():
                edge_labels[(i[0], j[0])] = j[1]['label']
        # plot the graph
        nx.draw(
            graph_nx, pos,
            node_size=1000,
            edge_color=nx.get_edge_attributes(graph_nx, 'color').values(),
            width=list(nx.get_edge_attributes(graph_nx, 'width').values()),
            with_labels=True,
            node_color=self.node_color
        )
        nx.draw_networkx_edge_labels(
            graph_nx, pos, edge_labels=edge_labels
        )
        plt.show()
