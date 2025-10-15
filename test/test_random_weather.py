from app import app

VALID_CONDITIONS = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]

def test_random_weather_status_code():
    with app.test_client() as client:
        resp = client.get("/random-weather")
        assert resp.status_code == 200, "Endpoint did not return 200 OK"

def test_random_weather_structure():
    with app.test_client() as client:
        resp = client.get("/random-weather")
        data = resp.get_json()
        assert data is not None and isinstance(data, dict), "Response is not a JSON object"
        for key in ("condition", "temperature", "humidity"):
            assert key in data, f"Missing key: {key}"

def test_condition_value():
    with app.test_client() as client:
        data = client.get("/random-weather").get_json()
        assert data["condition"] in VALID_CONDITIONS, "Condition is not one of the expected values"

def test_temperature_format_and_range():
    with app.test_client() as client:
        data = client.get("/random-weather").get_json()
        temp = data["temperature"]
        assert isinstance(temp, str) and temp.endswith("C"), "Temperature must be a string ending with 'C'"
        num_str = temp[:-1]
        try:
            temp_val = float(num_str)
        except (TypeError, ValueError):
            assert False, "Temperature numeric part is not numeric"
        assert -30 <= temp_val <= 50, "Temperature out of expected range (-30 to 50 C)"

def test_humidity_format_and_range():
    with app.test_client() as client:
        data = client.get("/random-weather").get_json()
        hum = data["humidity"]
        assert isinstance(hum, str) and hum.endswith("%"), "Humidity must be a string ending with '%'"
        hum_str = hum[:-1]
        try:
            hum_val = float(hum_str)
        except (TypeError, ValueError):
            assert False, "Humidity numeric part is not numeric"
        assert 10 <= hum_val <= 100, "Humidity out of expected range (10% to 100%)"