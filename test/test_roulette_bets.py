import json
from app import app as flask_app

def _get(client, path):
    resp = client.get(path)
    return resp.status_code, json.loads(resp.data)

def test_roulette_base_shape():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette")
        assert code == 200
        assert "spin" in data and "color" in data and "parity" in data

def test_roulette_force_spin_and_color_mapping():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette?force_spin=0")
        assert code == 200
        assert data["spin"] == 0
        assert data["color"] == "green"
        assert data["parity"] == "none"

        code, data = _get(client, "/roulette?force_spin=1")
        assert code == 200
        assert data["spin"] == 1
        assert data["color"] in {"red", "black"}  
       
        assert data["parity"] == "odd"

def test_roulette_color_bet_win_red():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette?force_spin=1&bet=red&amount=10")
        assert code == 200
        assert data["spin"] == 1
        assert data["outcome"] == "win"
        assert data["payout"] == 20  

def test_roulette_color_bet_lose():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette?force_spin=2&bet=red&amount=10")
        assert code == 200
        assert data["outcome"] == "lose"
        assert data["payout"] == 0

def test_roulette_green_color_bet_win():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette?force_spin=0&bet=green&amount=5")
        assert code == 200
        assert data["outcome"] == "win"
        assert data["payout"] == 175  

def test_roulette_number_bet_win():
    with flask_app.test_client() as client:
        code, data = _get(client, "/roulette?force_spin=17&bet=17&amount=2")
        assert code == 200
        assert data["outcome"] == "win"
        assert data["payout"] == 70 
def test_roulette_invalid_amount_or_bet():
    with flask_app.test_client() as client:
        code, _ = _get(client, "/roulette?bet=red") 
        assert code == 400

        code, _ = _get(client, "/roulette?amount=10") 
        assert code == 400

        code, _ = _get(client, "/roulette?bet=notacolor&amount=10")
        assert code == 400

        code, _ = _get(client, "/roulette?bet=37&amount=10")
        assert code == 400

        code, _ = _get(client, "/roulette?bet=red&amount=-1")
        assert code == 400

def test_roulette_force_spin_range():
    with flask_app.test_client() as client:
        code, _ = _get(client, "/roulette?force_spin=99")
        assert code == 400
