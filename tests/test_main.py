def test_import_app():
    import app
    import app.models
    import app.ml
    import app.utils
    assert app is not None


def test_import_main():
    from app.main import st

    assert st is not None
