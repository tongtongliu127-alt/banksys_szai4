def test_import_app():
    import app
    import app.ml
    import app.models
    import app.utils

    assert app is not None


def test_import_main_module():
    import app.main

    assert app.main is not None


def test_import_pages():
    from app.pages import data_analysis, prediction

    assert data_analysis is not None
    assert prediction is not None


def test_import_data_loader():
    from app.models.data_loader import load_test_data, load_train_data

    assert load_train_data is not None
    assert load_test_data is not None
