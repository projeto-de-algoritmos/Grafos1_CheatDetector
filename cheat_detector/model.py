from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityModel(object):
    """Class to compare texts.

    Parameters
    ----------
    transformer_name : str
        Name of a sentence transformer from HuggingFace.

    Attributes
    ----------
    model : SentenceTransformer
        Sentence Transformer loaded from transformer_name.
    transformer_name

    """

    def __init__(self, transformer_name='distiluse-base-multilingual-cased'):
        """Initialize this class.

        Parameters
        ----------
        transformer_name : str
            Name of a sentence transformer from HuggingFace.

        """
        self.transformer_name = transformer_name
        self.model = SentenceTransformer(self.transformer_name)
        # sklearn.metrics.pairwise.cosine_similarity
        self.pairwise_cosine_similarity = cosine_similarity

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
        return self.pairwise_cosine_similarity(
            self.generate_embeddings(answer_list)
        )

    def generate_embeddings(self, text):
        """Generate the embeddings, then the similarity matrix.

        Parameters
        ----------
        text : str or list of str
            One string for the answer of each student.

        Returns
        -------
        numpy.ndarray
            Embeddings of shape (512, ) or (len(text), len(text)*512, ).

        """
        return self.model.encode(text)
