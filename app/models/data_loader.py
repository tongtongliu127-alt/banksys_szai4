from pathlib import Path
from typing import Dict, List

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

NA_VALUES = ["unknown", "nonexistent"]

TARGET_COLUMN = "subscribe"

EXPECTED_FEATURES = [
    "age",
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]

FEATURE_LABELS: Dict[str, str] = {
    "age": "年龄",
    "job": "职业",
    "marital": "婚姻状况",
    "education": "教育水平",
    "default": "是否有违约",
    "housing": "是否有房贷",
    "loan": "是否有个人贷款",
    "contact": "联系方式",
    "month": "最后联系月份",
    "day_of_week": "最后联系星期",
    "duration": "通话时长(秒)",
    "campaign": "营销活动联系次数",
    "pdays": "上次联系距今(天)",
    "previous": "之前联系次数",
    "poutcome": "之前营销结果",
    "emp_var_rate": "就业变化率",
    "cons_price_index": "消费价格指数",
    "cons_conf_index": "消费信心指数",
    "lending_rate3m": "3个月贷款利率",
    "nr_employed": "雇员人数",
}


def get_feature_columns() -> List[str]:
    return list(EXPECTED_FEATURES)


def get_target_column() -> str:
    return TARGET_COLUMN


def get_feature_labels() -> Dict[str, str]:
    return dict(FEATURE_LABELS)


def _read_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, na_values=NA_VALUES)
    except pd.errors.EmptyDataError:
        raise ValueError(f"Data file is empty: {path}")


def _validate_columns(df: pd.DataFrame, required_cols: List[str], label: str) -> None:
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")


def load_train_data() -> pd.DataFrame:
    path = DATA_DIR / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"Train data not found at: {path}")
    df = _read_csv(path)
    if df.empty:
        raise ValueError("Train data file is empty")
    required = ["id"] + EXPECTED_FEATURES + [TARGET_COLUMN]
    _validate_columns(df, required, "train.csv")
    return df


def load_test_data() -> pd.DataFrame:
    path = DATA_DIR / "test.csv"
    if not path.exists():
        raise FileNotFoundError(f"Test data not found at: {path}")
    df = _read_csv(path)
    if df.empty:
        raise ValueError("Test data file is empty")
    required = ["id"] + EXPECTED_FEATURES
    _validate_columns(df, required, "test.csv")
    return df


def get_data_summary() -> dict:
    df = load_train_data()
    total = len(df)
    subscribed = int(df[TARGET_COLUMN].eq("yes").sum())
    not_subscribed = total - subscribed
    subscribe_rate = round(subscribed / total * 100, 2) if total > 0 else 0.0
    return {
        "total_records": total,
        "feature_count": len(EXPECTED_FEATURES),
        "subscribed": subscribed,
        "not_subscribed": not_subscribed,
        "subscribe_rate": subscribe_rate,
    }
