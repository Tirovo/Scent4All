# utils.py
import pandas as pd
from sklearn.cluster import KMeans

def cluster_perfumes(tfidf_matrix, n_clusters: int = 10) -> list[int]:
    """
    Apply KMeans clustering to group perfumes based on their TF-IDF vectors.

    Args:
        tfidf_matrix: TF-IDF feature matrix.
        n_clusters (int): Number of clusters to create.

    Returns:
        list[int]: Cluster labels for each perfume.
    """
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    return model.fit_predict(tfidf_matrix)

def assign_clusters(df: pd.DataFrame, labels: list[int]) -> pd.DataFrame:
    """
    Assign cluster labels to the DataFrame.

    Args:
        df (pd.DataFrame): Perfume dataset.
        labels (list[int]): Cluster labels.

    Returns:
        pd.DataFrame: Updated DataFrame with a new 'Cluster' column.
    """
    df["Cluster"] = labels
    return df
