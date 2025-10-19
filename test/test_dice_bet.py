def test_dice_bet_valid(client):
    response = client.post("/api/dice/bet", json={"choice": 3, "bet": 10})
    assert response.status_code == 200
    data = response.get_json()
    assert "rolled" in data
    assert "result" in data
    assert "winnings" in data

def test_dice_bet_invalid_choice(client):
    response = client.post("/api/dice/bet", json={"choice": 8, "bet": 10})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_dice_bet_invalid_json(client):
    response = client.post("/api/dice/bet", data="not json")
    assert response.status_code == 400
