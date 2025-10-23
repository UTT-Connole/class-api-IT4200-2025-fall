# ...existing code...
import random

def _make_randint(seq):
    it = iter(seq)
    def _randint(a, b):
        return next(it)
    return _randint

def test_yatzee_status(client):
    resp = client.get('/yatzy')
    assert resp.status_code == 200

def test_yatzee_yatzee(monkeypatch, client):
    # All five equal -> Yatzy
    seq = [3, 3, 3, 3, 3]
    monkeypatch.setattr(random, "randint", _make_randint(seq))
    resp = client.get('/yatzee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stats"]["dice_rolls"] == seq
    assert data["summary"] == "Yatzee! All five dice match."

def test_yatzy_full_house(monkeypatch, client):
    # Three of one value and two of another -> Full House
    seq = [2, 2, 2, 5, 5]
    monkeypatch.setattr(random, "randint", _make_randint(seq))
    resp = client.get('/yatzee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stats"]["dice_rolls"] == seq
    assert data["summary"] == "Full House! Three of a kind and a pair."

def test_yatzee_three_of_a_kind(monkeypatch, client):
    # Three same, two other different -> len(set) == 3
    seq = [4, 4, 4, 2, 3]
    monkeypatch.setattr(random, "randint", _make_randint(seq))
    resp = client.get('/yatzee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stats"]["dice_rolls"] == seq
    assert data["summary"] == "Three of a kind!"

def test_yatzee_one_pair(monkeypatch, client):
    # One pair -> len(set) == 4
    seq = [1, 1, 2, 3, 4]
    monkeypatch.setattr(random, "randint", _make_randint(seq))
    resp = client.get('/yatzee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stats"]["dice_rolls"] == seq
    assert data["summary"] == "One pair!"

def test_yatzee_no_special(monkeypatch, client):
    # All different -> len(set) == 5
    seq = [1, 2, 3, 4, 5]
    monkeypatch.setattr(random, "randint", _make_randint(seq))
    resp = client.get('/yatzee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stats"]["dice_rolls"] == seq
    assert data["summary"] == "No special combination."


def test_yatzee_max_roll(client):
    resp = client.get('/yatzee')
    data = resp.get_json()
    assert data["stats"]["max_roll"]

