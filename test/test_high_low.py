def client():
    from app import app
    with app.test_client() as client:
        yield client


def test_high_low_higher_win(client, monkeypatch):
    """
    Case: Player guesses 'higher' and wins.
    Mock random.choice to control card order.
    """
    seq = ["5", "K"]  
    monkeypatch.setattr("random.choice", lambda x: seq.pop(0))
    res = client.get("/high_low?guess=higher")
    data = res.get_json()

    assert res.status_code == 200
    assert data["guess"] == "higher"
    assert data["first_card"] == "5"
    assert data["second_card"] == "K"
    assert data["outcome"] == "win"


def test_high_low_lower_win(client, monkeypatch):
    """
    Case: Player guesses 'lower' and wins.
    """
    seq = ["Q", "4"]
    monkeypatch.setattr("random.choice", lambda x: seq.pop(0))
    res = client.get("/high_low?guess=lower")
    data = res.get_json()

    assert res.status_code == 200
    assert data["outcome"] == "win"
    assert data["first_card"] == "Q"
    assert data["second_card"] == "4"


def test_high_low_tie_results_in_lose(client, monkeypatch):
    """
    Case: Same card twice results in 'lose'.
    """
    seq = ["8", "8"]
    monkeypatch.setattr("random.choice", lambda x: seq.pop(0))
    res = client.get("/high_low?guess=higher")
    data = res.get_json()

    assert res.status_code == 200
    assert data["outcome"] == "lose"
    assert data["first_card"] == data["second_card"]


def test_high_low_invalid_guess(client):
    """
    Case: Invalid guess string triggers 400 error.
    """
    res = client.get("/high_low?guess=sideways")
    data = res.get_json()
    assert res.status_code == 400
    assert "error" in data
    assert "Guess must be" in data["error"]


def test_high_low_missing_guess(client):
    """
    Case: Missing 'guess' parameter triggers 400 error.
    """
    res = client.get("/high_low")
    data = res.get_json()
    assert res.status_code == 400
    assert "error" in data


def test_high_low_case_insensitive_guess(client, monkeypatch):
    """
    Case: Guess works even if passed in uppercase.
    """
    seq = ["4", "9"]
    monkeypatch.setattr("random.choice", lambda x: seq.pop(0))
    res = client.get("/high_low?guess=HIGHER")
    data = res.get_json()

    assert res.status_code == 200
    assert data["outcome"] == "win"