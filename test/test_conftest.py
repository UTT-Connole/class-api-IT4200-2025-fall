import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.testing = True
    return flask_app.test_client()
