import os
import pathlib
import pytest

# Remove repository banking.db if present so tests start with a clean database
ROOT = pathlib.Path(__file__).resolve().parents[1]
db_file = ROOT / "banking.db"
if db_file.exists():
    try:
        db_file.unlink()
    except Exception:
        # best-effort; if unlink fails tests may still pass if they override DB
        pass

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()