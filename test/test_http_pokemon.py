import pytest

@pytest.fixture
def client():
    from app import app   # adjust import if your main file is named differently
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_pokemon_endpoint_returns_json(client):
    """Test that /pokemon returns a JSON response with 'pokemon': 'Jigglypuff'"""
    response = client.get("/pokemon")
    
    # 1️⃣ Basic response status and type
    assert response.status_code == 200, "Expected 200 OK response"
    assert response.is_json, "Response should be JSON"

    # 2️⃣ Validate response content
    data = response.get_json()
    assert "pokemon" in data, "JSON should include key 'pokemon'"
    assert data["pokemon"] == "Jigglypuff", "Expected pokemon to be 'Jigglypuff'"
