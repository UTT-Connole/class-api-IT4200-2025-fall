import pytest
from app import app  # assuming your Flask file is named app.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_sports_status_code(client):
    response = client.get("/sports")
    assert response.status_code == 200

def test_sports_returns_json(client):
    response = client.get("/sports")
    assert response.is_json

def test_sports_has_required_keys(client):
    response = client.get("/sports")
    data = response.get_json()
    assert "matchup" in data
    assert "winner" in data
    assert "won_bet" in data

def test_winner_in_matchup(client):
    response = client.get("/sports")
    data = response.get_json()
    matchup = data["matchup"]
    assert data["winner"] in matchup
