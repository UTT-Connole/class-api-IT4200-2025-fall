import pytest
from app import app

def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_hellhole_route(client):
    response = client.get('/hellhole')
    
    # Check response status code
    assert response.status_code == 200
    
    # Check response is JSON
    data = response.get_json()
    assert data is not None
    
    # Check main keys
    expected_keys = {"location", "description", "fact", "unlivable_homes", "timestamp"}
    assert expected_keys.issubset(data.keys())
    
    # Validate unlivable_homes
    unlivable_homes = data["unlivable_homes"]
    assert isinstance(unlivable_homes, list)
    assert 3 <= len(unlivable_homes) <= 6  # Based on your random range
    
    # Check keys inside each unlivable home
    for home in unlivable_homes:
        assert "location" in home
        assert "issue" in home
        assert "description" in home
