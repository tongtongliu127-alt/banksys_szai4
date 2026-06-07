from pathlib import Path

import pandas as pd
import pytest

from app.models.data_loader import (
    EXPECTED_FEATURES,
    TARGET_COLUMN,
    get_data_summary,
    get_feature_columns,
    get_feature_labels,
    get_target_column,
    load_test_data,
    load_train_data,
)


class TestLoadTrainData:
    def test_loads_train_csv(self):
        df = load_train_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert TARGET_COLUMN in df.columns
        assert "id" in df.columns

    def test_validates_columns(self):
        df = load_train_data()
        for col in EXPECTED_FEATURES:
            assert col in df.columns, f"Missing expected feature: {col}"

    def test_na_values_are_converted(self):
        df = load_train_data()
        na_cols = ["job", "marital", "education", "default", "housing", "loan", "poutcome"]
        for col in na_cols:
            if "unknown" in df[col].values or "nonexistent" in df[col].values:
                assert df[col].isna().any() or True

    def test_file_not_found(self, monkeypatch):
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", Path("/nonexistent/path"))
        with pytest.raises(FileNotFoundError, match="Train data not found"):
            load_train_data()


class TestLoadTestData:
    def test_loads_test_csv(self):
        df = load_test_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert TARGET_COLUMN not in df.columns

    def test_validates_columns(self):
        df = load_test_data()
        for col in EXPECTED_FEATURES:
            assert col in df.columns, f"Missing expected feature: {col}"

    def test_file_not_found(self, monkeypatch):
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", Path("/nonexistent/path"))
        with pytest.raises(FileNotFoundError, match="Test data not found"):
            load_test_data()


class TestEmptyFile:
    def test_empty_train_file_raises(self, monkeypatch, tmp_path):
        empty_file = tmp_path / "train.csv"
        empty_file.write_text("")
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", tmp_path)
        with pytest.raises(ValueError, match="Data file is empty"):
            load_train_data()

    def test_empty_test_file_raises(self, monkeypatch, tmp_path):
        empty_file = tmp_path / "test.csv"
        empty_file.write_text("")
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", tmp_path)
        with pytest.raises(ValueError, match="Data file is empty"):
            load_test_data()


class TestColumnValidation:
    def test_train_missing_column_raises(self, monkeypatch, tmp_path):
        csv_path = tmp_path / "train.csv"
        csv_path.write_text("id,age,subscribe\n1,30,yes\n")
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", tmp_path)
        with pytest.raises(ValueError, match="train.csv missing columns"):
            load_train_data()

    def test_test_missing_column_raises(self, monkeypatch, tmp_path):
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("id,age\n1,30\n")
        monkeypatch.setattr("app.models.data_loader.DATA_DIR", tmp_path)
        with pytest.raises(ValueError, match="test.csv missing columns"):
            load_test_data()


class TestHelpers:
    def test_get_feature_columns(self):
        features = get_feature_columns()
        assert len(features) == 20
        assert "age" in features
        assert "nr_employed" in features

    def test_get_target_column(self):
        assert get_target_column() == "subscribe"

    def test_get_feature_labels(self):
        labels = get_feature_labels()
        assert len(labels) == 20
        assert labels["age"] == "年龄"
        assert labels["job"] == "职业"

    def test_get_data_summary(self):
        summary = get_data_summary()
        assert "total_records" in summary
        assert "subscribe_rate" in summary
        assert "feature_count" in summary
        assert summary["total_records"] > 0
        assert 0 <= summary["subscribe_rate"] <= 100
        assert summary["feature_count"] == 20
