import pytest
from app import app, generate_unlivable_home, hellhole_facts, locations, issues, descriptions
import json

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_generate_unlivable_home_returns_proper_keys():
    home = generate_unlivable_home()
    assert isinstance(home, dict)
    assert set(home.keys()) == {"location", "issue", "description"}

    assert home["location"] in locations
    assert home["issue"] in issues
    assert home["description"] in descriptions

def test_generate_unlivable_home_multiple_different_results():
    results = set()
    for _ in range(10):
        home = generate_unlivable_home()
        results.add(json.dumps(home, sort_keys=True))
    assert len(results) > 1 

def test_hellhole_route_status_code_and_content(client):
    response = client.get('/hellhole')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)

def test_hellhole_route_required_keys(client):
    response = client.get('/hellhole')
    data = response.get_json()

    expected_keys = {"location", "description", "fact", "unlivable_homes", "timestamp"}
    assert expected_keys.issubset(data.keys())

def test_hellhole_route_location_and_description(client):
    response = client.get('/hellhole')
    data = response.get_json()

    assert data["location"] == "Hellhole"
    assert "nightmares" in data["description"]

def test_hellhole_route_fact_in_hellhole_facts(client):
    response = client.get('/hellhole')
    data = response.get_json()
    assert data["fact"] in hellhole_facts

def test_hellhole_route_timestamp_format(client):
    response = client.get('/hellhole')
    data = response.get_json()

    assert data["timestamp"].endswith("Z")

def test_hellhole_route_unlivable_homes_type_and_count(client):
    response = client.get('/hellhole')
    data = response.get_json()

    homes = data["unlivable_homes"]
    assert isinstance(homes, list)
    assert 3 <= len(homes) <= 6

def test_hellhole_route_unlivable_homes_each_item(client):
    response = client.get('/hellhole')
    data = response.get_json()
    homes = data["unlivable_homes"]

    for home in homes:
        assert set(home.keys()) == {"location", "issue", "description"}
        assert home["location"] in locations
        assert home["issue"] in issues
        assert home["description"] in descriptions

def test_hellhole_route_multiple_calls_randomness(client):
    response1 = client.get('/hellhole').get_json()
    response2 = client.get('/hellhole').get_json()

    fact_differs = response1["fact"] != response2["fact"]
    homes_differs = response1["unlivable_homes"] != response2["unlivable_homes"]

    assert fact_differs or homes_differs