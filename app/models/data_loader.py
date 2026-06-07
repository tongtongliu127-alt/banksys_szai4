from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

NA_VALUES = ["unknown", "nonexistent"]


def _read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, na_values=NA_VALUES)
    except pd.errors.EmptyDataError:
        raise ValueError(f"Data file is empty: {path}")


def load_train_data() -> pd.DataFrame:
    path = DATA_DIR / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Train data not found at: {path}")
    df = _read_csv(path)
    if df.empty:
        raise ValueError("Train data file is empty")
    return df


def load_test_data() -> pd.DataFrame:
    path = DATA_DIR / "test.csv"
    if not path.exists():
        raise FileNotFoundError(f"Test data not found at: {path}")
    df = _read_csv(path)
    if df.empty:
        raise ValueError("Test data file is empty")
    return df
