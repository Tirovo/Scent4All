# data_loader.py
import pandas as pd

def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the perfume dataset from a CSV file and clean it.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, sep=";", encoding="ISO-8859-1")

    df["Rating Value"] = pd.to_numeric(df["Rating Value"], errors="coerce")
    df["Rating Count"] = pd.to_numeric(df["Rating Count"], errors="coerce")
    df.fillna("", inplace=True)

    return df
