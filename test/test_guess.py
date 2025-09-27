import random

def test_numberpick_correct(monkeypatch, client):
    # Force secret to 5
    monkeypatch.setattr(random, "randint", lambda a, b: 5)
    resp = client.get("/guess?user_guess=5")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] == "Correct!"
    assert data["secret"] == 5

def test_numberpick_wrong(monkeypatch, client):
    # Force secret to 7
    monkeypatch.setattr(random, "randint", lambda a, b: 7)
    resp = client.get("/guess?user_guess=3")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] == "Wrong!"
    assert data["secret"] == 7

def test_numberpick_out_of_range(client):
    resp = client.get("/guess?user_guess=15")
    # Should reject with 400 status code
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data
    assert data["error"] == "Guess must be between 1 and 10"

    


