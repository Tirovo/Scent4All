# similarity.py
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity_matrix(tfidf_matrix):
    """
    Compute cosine similarity between all perfumes using their TF-IDF vectors.

    Args:
        tfidf_matrix: Sparse matrix (TF-IDF encoded).

    Returns:
        ndarray: Cosine similarity matrix.
    """
    return cosine_similarity(tfidf_matrix)

