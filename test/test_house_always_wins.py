import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_house_always_wins(client):
    """Check that /house/<name> returns the correct message."""
    response = client.get('/house/Clint')
    assert response.status_code == 200
    assert b"Sorry, Clint. The house always wins!" in response.data

    