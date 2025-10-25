def test_coinflip_json_response(client):
    res = client.post("/api/coinflip", json={"choice": "heads", "bet": 5})
    data = res.get_json()
    assert res.status_code == 200
    assert data["choice"] in ["heads", "tails"]
    assert data["result"] in ["heads", "tails"]
    assert data["outcome"] in ["win", "lose"]
