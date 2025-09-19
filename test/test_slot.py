import pytest
from app import app, users

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset user balance before each test
        users['user1']['balance'] = 1000
        yield client

def test_slots_jackpot(client, monkeypatch):
    # Force all reels to match for jackpot
    monkeypatch.setattr('random.choice', lambda x: x[0])
    response = client.post('/slots', json={'username': 'user1', 'bet': 10})
    data = response.get_json()
    assert response.status_code == 200
    assert data['payout'] == 100
    assert data['balance'] == 1090
    assert "Jackpot" in data['message']

def test_slots_two_match(client, monkeypatch):
    # Force two reels to match, one different
    sequence = iter(['🍒', '🍒', '🍋'])
    monkeypatch.setattr('random.choice', lambda x: next(sequence))
    response = client.post('/slots', json={'username': 'user1', 'bet': 10})
    data = response.get_json()
    assert response.status_code == 200
    assert data['payout'] == 20
    assert data['balance'] == 1010
    assert "Small win" in data['message']

def test_slots_no_match(client, monkeypatch):
    # Force all reels to be different
    sequence = iter(['🍒', '🍋', '🔔'])
    monkeypatch.setattr('random.choice', lambda x: next(sequence))
    response = client.post('/slots', json={'username': 'user1', 'bet': 10})
    data = response.get_json()
    assert response.status_code == 200
    assert data['payout'] == 0
    assert data['balance'] == 990
    assert "No match" in data['message']

def test_slots_insufficient_balance(client):
    users['user1']['balance'] = 5
    response = client.post('/slots', json={'username': 'user1', 'bet': 10})
    data = response.get_json()
    assert response.status_code == 400
    assert "Insufficient balance" in data['error']

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_tucson_endpoint(client):
    response = client.get('/Tucson')
    assert response.status_code == 200
    data = response.get_json()
    assert data["Location"] == "Tucson, Arizona"
    assert data["Description"] == "We don't take about it"