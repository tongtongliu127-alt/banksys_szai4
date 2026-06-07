from app.ml.train import preprocess, train


def _setup(monkeypatch, tmp_path):
    """Redirect MODEL_DIR and MODEL_PATH to a temp directory."""
    p = tmp_path / "model.pkl"
    monkeypatch.setattr("app.ml.train.MODEL_DIR", tmp_path)
    monkeypatch.setattr("app.ml.train.MODEL_PATH", p)
    if p.exists():
        p.unlink()
    return p


class TestTrain:
    def test_train_creates_model_file(self, monkeypatch, tmp_path):
        model_path = _setup(monkeypatch, tmp_path)
        result = train(force=False)
        assert result["status"] == "trained"
        assert result["accuracy"] > 0.5
        assert result["auc"] > 0.5
        assert model_path.exists()

    def test_train_reproducibility(self, monkeypatch, tmp_path):
        _setup(monkeypatch, tmp_path)
        result1 = train(force=True)
        result2 = train(force=True)
        assert result1["auc"] == result2["auc"]
        assert result1["accuracy"] == result2["accuracy"]

    def test_force_overwrite(self, monkeypatch, tmp_path):
        model_path = _setup(monkeypatch, tmp_path)
        train(force=False)
        mtime_before = model_path.stat().st_mtime
        train(force=True)
        mtime_after = model_path.stat().st_mtime
        assert mtime_after >= mtime_before

    def test_skip_if_exists(self, monkeypatch, tmp_path):
        _setup(monkeypatch, tmp_path)
        train(force=False)
        result = train(force=False)
        assert result["status"] == "skipped"

    def test_preprocess_handles_missing(self, sample_df_for_viz):
        df, encoders = preprocess(sample_df_for_viz)
        assert len(encoders) > 0
        assert not df.isna().any().any()
