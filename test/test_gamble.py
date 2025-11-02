import types
import json
from app import create_app

def test_gamble_function_exists():
    from app import create_app
    app = create_app()
    assert "gamble" in app.view_functions

def test_invalid_bet(client):
    response = client.post("/api/gamble", json={"bet": 0})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_valid_bet(client):
    response = client.post("/api/gamble", json={"bet": 5})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "result" in data
    assert data["original_bet"] == 5
    assert "winnings" in data
    assert data["result"] in ["win", "lose"]

def test_force_win(client, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: True)
    response = client.post("/api/gamble", json={"bet": 10})
    data = json.loads(response.data)
    assert data["result"] == "win"
    assert data["winnings"] == 20

def test_force_lose(client, monkeypatch):
    monkeypatch.setattr("random.choice", lambda x: False)
    response = client.post("/api/gamble", json={"bet": 10})
    data = json.loads(response.data)
    assert data["result"] == "lose"
    assert data["winnings"] == 0
    
def test_custom_multiplier_and_forced_win(client):
    payload = {"bet": 10, "payout_multiplier": 3, "force_result": "win"}
    resp = client.post("/api/gamble", json=payload)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["result"] == "win"
    assert data["original_bet"] == 10
    assert data["multiplier"] == 3
    assert data["winnings"] == 30

