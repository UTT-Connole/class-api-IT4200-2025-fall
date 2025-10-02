import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_create_user_and_get_balance(client):
    username = "pytestuser"
    # Ensure user does not exist yet
    resp = client.get(f"/api/bank/{username}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["username"] == username
    assert data["balance"] == 0

def test_add_value(client):
    username = "pytestuser"
    resp = client.post(f"/api/bank/{username}/add", json={"amount": 50})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["balance"] >= 50
    assert data["last_gain"] == 50
    assert data["total_gained"] >= 50

def test_remove_value(client):
    username = "pytestuser"
    # Add first to ensure sufficient balance
    client.post(f"/api/bank/{username}/add", json={"amount": 30})
    resp = client.post(f"/api/bank/{username}/remove", json={"amount": 20})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["last_loss"] == 20
    assert data["total_lost"] >= 20

def test_remove_too_much(client):
    username = "pytestuser"
    # Try to remove more than available
    resp = client.post(f"/api/bank/{username}/remove", json={"amount": 100000})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Insufficient funds" in data["error"]

def test_add_invalid_amount(client):
    username = "pytestuser"
    resp = client.post(f"/api/bank/{username}/add", json={"amount": -10})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Amount must be positive" in data["error"]