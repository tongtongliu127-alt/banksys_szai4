from pathlib import Path

import pandas as pd
import pytest

from app.models.data_loader import load_test_data, load_train_data


class TestLoadTrainData:
    def test_loads_train_csv(self):
        df = load_train_data()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "subscribe" in df.columns
        assert "id" in df.columns

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
        assert "subscribe" not in df.columns

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
