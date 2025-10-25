import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_jukebox(client):
    response = client.get("/jukebox")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert "song" in data
    assert "title" in data["song"]
    assert "artist" in data["song"]

def test_jukebox_year_type(client):
    response = client.get("/jukebox")
    song = response.get_json()["song"]
    assert isinstance(song["year"], int)