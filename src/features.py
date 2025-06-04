# features.py
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas import DataFrame, Series

def merge_features(row: Series) -> str:
    """
    Merge key perfume attributes into a single string for feature extraction.

    Args:
        row (Series): A row of the DataFrame containing perfume details.

    Returns:
        str: Concatenated and cleaned feature string.
    """
    fields = [
        row["mainaccord1"], row["mainaccord2"], row["mainaccord3"],
        row["mainaccord4"], row["mainaccord5"],
        row["Top"], row["Middle"], row["Base"]
    ]
    return " ".join(
        str(f).lower().strip().replace(",", " ") for f in fields if f
    )

def extract_features(df: DataFrame) -> tuple[DataFrame, any, TfidfVectorizer]:
    """
    Generate TF-IDF features from merged perfume attributes.

    Args:
        df (DataFrame): Perfume dataset.

    Returns:
        tuple: (DataFrame with new 'features_text' column,
                TF-IDF sparse matrix,
                fitted TfidfVectorizer)
    """
    df["features_text"] = df.apply(merge_features, axis=1)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["features_text"])
    return df, tfidf_matrix, vectorizer
