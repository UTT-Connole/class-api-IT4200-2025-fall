import os
import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "banking.db"
    monkeypatch.setenv("TEST_BANK_DB", str(db_path))

    from app import app as flask_app

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_bank_endpoints_create_and_add_remove(client):
    username = "pytest_user"

    r = client.get(f"/api/bank/{username}")
    assert r.status_code == 200
    data = r.get_json()
    assert data["username"] == username
    assert isinstance(data["balance"], int)
    initial_balance = data["balance"]

    r = client.post(f"/api/bank/{username}/add", json={"amount": 100})
    assert r.status_code == 200
    data = r.get_json()
    assert data["balance"] == initial_balance + 100
    assert data["last_gain"] == 100

    r = client.post(f"/api/bank/{username}/remove", json={"amount": 30})
    assert r.status_code == 200
    data = r.get_json()
    assert data["last_loss"] == 30
    assert data["balance"] == initial_balance + 100 - 30

    r = client.post(f"/api/bank/{username}/remove", json={"amount": 1000000})
    assert r.status_code == 400


def test_bank_list_page(client):
    r = client.get("/bank")
    assert r.status_code == 200
    assert b"Bank Balances" in r.data
