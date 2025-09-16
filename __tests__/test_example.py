from sum import add
from app import create_app

def test_example():
    assert True


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200