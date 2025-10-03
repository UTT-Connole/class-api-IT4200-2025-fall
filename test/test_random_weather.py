def test_status_code(client):
    response = client.get("/random-weather")
    assert response.status_code == 200

def test_has_expected_keys(client):
    response = client.get("/random-weather")
    data = response.get_json()
    for key in ["condition", "temperature", "humidity"]:
        assert key in data
        
def test_condition_value(client):
    """Condition must be one of the allowed"""
    response = client.get("/random-weather")
    data = response.get_json()
    valid_conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
    assert data["condition"] in valid_conditions

def test_humidity_value(client):
    """Humidity must be 10–100%"""
    response = client.get("/random-weather")
    data = response.get_json()
    humidity_val = int(data["humidity"].rstrip("%"))
    assert 10 <= humidity_val <= 100

