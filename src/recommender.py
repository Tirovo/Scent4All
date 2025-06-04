# recommender.py
import pandas as pd
from data_loader import load_dataset
from features import extract_features
from similarities import compute_similarity_matrix
from utils import cluster_perfumes, assign_clusters

def get_recommendations(
    df: pd.DataFrame,
    sim_matrix,
    perfume_name: str,
    top_n: int = 5
) -> pd.DataFrame:
    """
    Return the top N most similar perfumes to the selected one.

    Args:
        df (pd.DataFrame): Full perfume dataset.
        sim_matrix: Cosine similarity matrix.
        perfume_name (str): Reference perfume name.
        top_n (int): Number of similar perfumes to return.

    Returns:
        pd.DataFrame: Top N recommended perfumes.
    """
    if perfume_name not in df["Perfume"].values:
        return pd.DataFrame()

    index = df[df["Perfume"] == perfume_name].index[0]
    similarity_scores = list(enumerate(sim_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in similarity_scores[1:top_n + 1]]

    return df.iloc[top_indices][[
        "Perfume", "Brand", "mainaccord1", "mainaccord2", "mainaccord3",
        "Top", "Middle", "Base", "Rating Value"
    ]]

def run_pipeline(
    csv_path: str,
    perfume_name: str,
    top_n: int = 5
) -> pd.DataFrame:
    """
    Full perfume recommendation pipeline.

    Args:
        csv_path (str): Path to the perfume CSV dataset.
        perfume_name (str): Target perfume to find similar ones.
        top_n (int): Number of recommendations to return.

    Returns:
        pd.DataFrame: Top N perfume recommendations.
    """
    df = load_dataset(csv_path)
    df, tfidf_matrix, _ = extract_features(df)
    sim_matrix = compute_similarity_matrix(tfidf_matrix)
    labels = cluster_perfumes(tfidf_matrix)
    df = assign_clusters(df, labels)

    return get_recommendations(df, sim_matrix, perfume_name, top_n)
