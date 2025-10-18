from app import app

def test_bet_rps_invalid_params():
    client = app.test_client()
    resp = client.get("/bet_rps?player=spock&amount=10")
    assert resp.status_code == 400

def test_bet_rps_win(monkeypatch):
    # Force computer to choose scissors so rock wins
    monkeypatch.setattr("random.choice", lambda seq: "scissors")
    client = app.test_client()
    resp = client.get("/bet_rps?player=rock&amount=10")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["computer"] == "scissors"
    assert data["result"] == "win"
    assert data["payout"] == 20

def test_bet_rps_tie(monkeypatch):
    monkeypatch.setattr("random.choice", lambda seq: "paper")
    client = app.test_client()
    resp = client.get("/bet_rps?player=paper&amount=7")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] == "tie"
    assert data["payout"] == 7

def test_bet_rps_lose(monkeypatch):
    monkeypatch.setattr("random.choice", lambda seq: "paper")
    client = app.test_client()
    resp = client.get("/bet_rps?player=rock&amount=9")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] == "lose"
    assert data["payout"] == 0
