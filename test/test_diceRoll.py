''' 
DISCLAIMER: This isn't using the conftest.py because 
that one doesnt test for the /roll/<sides> endpoint
therefore I had to create a fixture for this one.
'''

import pytest
from app import app as flask_app 

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

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

