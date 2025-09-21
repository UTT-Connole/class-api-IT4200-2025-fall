import types
import json
from app import create_app

# Test if function exists
def test_gamble_function_exists():
    from app import create_app
    app = create_app()
    assert "gamble" in app.view_functions

# Check bet <= 0 returns error
def test_invalid_bet(client):
    response = client.post("/api/gamble", json={"bet": 0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

# Check a valid bet returns fields
def test_valid_bet(client):
    response = client.post("/api/gamble", json={"bet": 5})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "result" in data
    assert data["original_bet"] == 5
    assert "winnings" in data
    assert data["result"] in ["win", "lose"]

# Check winning logic
def test_force_win(client, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: True)
    response = client.post("/api/gamble", json={"bet": 10})
    data = json.loads(response.data)
    assert data["result"] == "win"
    assert data["winnings"] == 20

# Test 6: Check losing logic
def test_force_lose(client, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: False)
    response = client.post("/api/gamble", json={"bet": 10})
    data = json.loads(response.data)
    assert data["result"] == "lose"
    assert data["winnings"] == 0
