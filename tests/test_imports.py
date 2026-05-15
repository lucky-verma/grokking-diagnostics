"""Smoke tests for grokking_diag package."""


def test_import_metrics():
    from grokking_diag import metrics
    assert hasattr(metrics, "__name__")


def test_import_predictor():
    from grokking_diag import predictor
    assert hasattr(predictor, "__name__")


def test_import_cli():
    from grokking_diag import cli
    assert hasattr(cli, "__name__")


def test_package_version():
    import grokking_diag
    # __version__ is optional; if present, must be string
    if hasattr(grokking_diag, "__version__"):
        assert isinstance(grokking_diag.__version__, str)
