import time

import pytest

from app.ml.train import train as train_model
from app.models.predictor import get_feature_options, predict


def _train_and_redirect(monkeypatch, tmp_path):
    """Train a model in tmp_path and redirect predictor to use it."""
    model_path = tmp_path / "model.pkl"
    monkeypatch.setattr("app.ml.train.MODEL_DIR", tmp_path)
    monkeypatch.setattr("app.ml.train.MODEL_PATH", model_path)
    monkeypatch.setattr("app.models.predictor.MODEL_PATH", model_path)
    train_model(force=True)
    return model_path


class TestPredict:
    def test_predict_returns_valid_result(self, monkeypatch, tmp_path):
        _train_and_redirect(monkeypatch, tmp_path)
        features = {
            "age": 40,
            "job": "admin.",
            "marital": "married",
            "education": "high.school",
            "default": "no",
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "month": "may",
            "day_of_week": "mon",
            "duration": 300,
            "campaign": 2,
            "pdays": 999,
            "previous": 0,
            "poutcome": "nonexistent",
            "emp_var_rate": 0.0,
            "cons_price_index": 94.0,
            "cons_conf_index": -40.0,
            "lending_rate3m": 2.0,
            "nr_employed": 5100.0,
        }
        result = predict(features)
        assert "subscribe" in result
        assert "probability" in result
        assert "confidence" in result
        assert isinstance(result["subscribe"], bool)
        assert 0.0 <= result["probability"] <= 1.0
        assert result["confidence"] in ("高", "中", "低")

    def test_predict_response_time(self, monkeypatch, tmp_path):
        _train_and_redirect(monkeypatch, tmp_path)
        features = {
            "age": 40,
            "job": "technician",
            "marital": "single",
            "education": "university.degree",
            "default": "no",
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "month": "aug",
            "day_of_week": "tue",
            "duration": 200,
            "campaign": 1,
            "pdays": 999,
            "previous": 0,
            "poutcome": "nonexistent",
            "emp_var_rate": -1.0,
            "cons_price_index": 93.0,
            "cons_conf_index": -42.0,
            "lending_rate3m": 3.0,
            "nr_employed": 5000.0,
        }
        start = time.perf_counter()
        predict(features)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Prediction took {elapsed:.3f}s"

    def test_model_not_found_raises(self, monkeypatch, tmp_path):
        monkeypatch.setattr("app.models.predictor.MODEL_PATH", tmp_path / "nonexistent.pkl")
        with pytest.raises(FileNotFoundError, match="Model not found"):
            predict({"age": 30})

    def test_get_feature_options(self, monkeypatch, tmp_path):
        _train_and_redirect(monkeypatch, tmp_path)
        opts = get_feature_options()
        assert "job" in opts
        assert "marital" in opts
        assert len(opts["job"]) > 0
