import logging
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd

from app.models.data_loader import EXPECTED_FEATURES

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "model" / "model.pkl"


def _load_artifact() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run `python -m app.ml.train` first."
        )
    return joblib.load(MODEL_PATH)


def get_feature_options() -> Dict[str, list]:
    """Return allowed values for each categorical feature based on encoder classes."""
    try:
        artifact = _load_artifact()
    except FileNotFoundError:
        return {}
    encoders = artifact["encoders"]
    options = {}
    for col, encoder in encoders.items():
        options[col] = sorted([v for v in encoder.classes_ if v != "missing"])
    return options


def predict(features: Dict[str, object]) -> dict:
    artifact = _load_artifact()
    model = artifact["model"]
    encoders = artifact["encoders"]

    df = pd.DataFrame([features])

    for col in EXPECTED_FEATURES:
        if col not in df.columns:
            df[col] = 0

    for col, encoder in encoders.items():
        if col in df.columns:
            val = str(df[col].iloc[0]) if df[col].notna().iloc[0] else "missing"
            known = set(encoder.classes_)
            if val not in known:
                val = encoder.classes_[0]
            df[col] = encoder.transform([val])[0]

    df = df[EXPECTED_FEATURES]
    df = df.fillna(0)

    proba = float(model.predict_proba(df)[0, 1])
    prediction = bool(proba >= 0.5)

    if proba >= 0.8:
        confidence = "高"
    elif proba >= 0.5:
        confidence = "中"
    else:
        confidence = "低"

    return {"subscribe": prediction, "probability": round(proba, 4), "confidence": confidence}
