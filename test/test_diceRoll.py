def test_roll(client):
    resp = client.get("/roll/6")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "result" in data
    assert 1 <= data["result"] <= 6

def test_nonInteger(client):
    resp = client.get("/roll/abc")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Silly goose, the number of sides must be a number!" in data["error"]

def test_notEnoughSides(client):
    resp = client.get("/roll/1")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Dice should have more than one side goober." in data["error"]

