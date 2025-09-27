import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_place_plant_bet_success(client):
    response = client.post('/plants/match', json={
        'username': 'alice',
        'plant_id': 1,
        'amount': 20
    })
    assert response.status_code == 200
    assert 'remaining_balance' in response.json

def test_place_plant_bet_user_not_found(client):
    response = client.post('/plants/match', json={
        'username': 'charlie',
        'plant_id': 1,
        'amount': 20
    })
    assert response.status_code == 404
    assert 'error' in response.json

def test_place_plant_bet_insufficient_balance(client):
    response = client.post('/plants/match', json={
        'username': 'bob',
        'plant_id': 1,
        'amount': 1000
    })
    assert response.status_code == 400
    assert 'error' in response.json
