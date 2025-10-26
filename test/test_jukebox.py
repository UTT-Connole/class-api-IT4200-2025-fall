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

def test_jukebox_genre_filter_success(client):
    response = client.get("/jukebox?genre=Surf rock")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["song"]["genre"] == "Surf rock"

def test_jukebox_genre_filter_not_found(client):
    response = client.get("/jukebox?genre=Jazz")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False

def test_jukebox_contains_vibrations(client):
    response = client.get("/jukebox")
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data
    assert isinstance(data["success"], bool)