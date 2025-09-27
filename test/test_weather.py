import pytest
from app import app

class TestWeatherEndpoint:
    def test_weather_condition(self):
        with app.test_client() as client:
            response = client.get('/random-weather')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data is not None
            assert "condition" in data
            
            valid_conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
            assert data["condition"] in valid_conditions

    def test_temperature_range(self):
        with app.test_client() as client:
            response = client.get('/random-weather')
            data = response.get_json()
            
            temperature_str = data["temperature"]
            # Remove 'C' and convert to integer
            temperature_value = int(temperature_str.rstrip('C'))
            assert -30 <= temperature_value <= 50

    def test_humidity_range(self):
        with app.test_client() as client:
            response = client.get('/random-weather')
            data = response.get_json()
            
            humidity_str = data["humidity"]
            # Remove '%' and convert to integer
            humidity_value = int(humidity_str.rstrip('%'))
            assert 10 <= humidity_value <= 100

    def test_response_structure(self):
        with app.test_client() as client:
            response = client.get('/random-weather')
            data = response.get_json()
            
            # Test that all expected keys are present
            expected_keys = ["condition", "temperature", "humidity"]
            for key in expected_keys:
                assert key in data