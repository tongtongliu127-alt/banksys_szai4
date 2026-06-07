"""Offline training script for bank marketing subscription prediction.

Usage:
    python -m app.ml.train          # skip if model exists
    python -m app.ml.train --force  # overwrite existing model
"""

import argparse
import logging
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from app.models.data_loader import EXPECTED_FEATURES, TARGET_COLUMN, load_train_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"
RANDOM_STATE = 42

CATEGORICAL_FEATURES = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]


def preprocess(df: pd.DataFrame, encoders: dict | None = None) -> tuple[pd.DataFrame, dict]:
    df = df.copy()
    if encoders is None:
        encoders = {}
        for col in CATEGORICAL_FEATURES:
            le = LabelEncoder()
            df[col] = df[col].fillna("missing")
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    else:
        for col in CATEGORICAL_FEATURES:
            le = encoders[col]
            df[col] = df[col].fillna("missing")
            known = set(le.classes_)
            df[col] = df[col].astype(str).apply(lambda x: x if x in known else le.classes_[0])
            df[col] = le.transform(df[col])
    df[EXPECTED_FEATURES[-1]] = df[EXPECTED_FEATURES[-1]].fillna(0)
    return df, encoders


def train(force: bool = False) -> dict:
    if MODEL_PATH.exists() and not force:
        logger.info("Model already exists at %s. Use --force to overwrite.", MODEL_PATH)
        return {"status": "skipped", "reason": "model exists"}

    logger.info("Loading training data...")
    df = load_train_data()

    logger.info("Preprocessing...")
    df, encoders = preprocess(df)

    X = df[EXPECTED_FEATURES]
    y = LabelEncoder().fit_transform(df[TARGET_COLUMN])

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    logger.info("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_proba)

    logger.info("Validation metrics:")
    logger.info("  Accuracy:  %.4f", acc)
    logger.info("  AUC:       %.4f", auc)
    logger.info(
        "Classification report:\n%s",
        classification_report(y_val, y_pred, target_names=["no", "yes"]),
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {"model": model, "encoders": encoders, "features": EXPECTED_FEATURES}
    joblib.dump(artifact, MODEL_PATH)
    logger.info("Model saved to %s", MODEL_PATH)

    return {"status": "trained", "accuracy": acc, "auc": auc, "model_path": str(MODEL_PATH)}


def main():
    parser = argparse.ArgumentParser(description="Train bank marketing prediction model")
    parser.add_argument("--force", action="store_true", help="Overwrite existing model")
    args = parser.parse_args()

    result = train(force=args.force)
    if result["status"] == "skipped":
        sys.exit(0)
    elif result["status"] == "trained":
        logger.info("Training complete. AUC=%.4f, Accuracy=%.4f", result["auc"], result["accuracy"])
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
