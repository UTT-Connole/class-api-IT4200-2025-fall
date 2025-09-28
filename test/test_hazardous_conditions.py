from app import app
import pytest   

class TestHazardousConditionsEndpoint:
    def test_response_status_and_structure(self):
        with app.test_client() as client:
            response = client.get('/hazardous-conditions')
            assert response.status_code == 200

            data = response.get_json()
            assert data is not None

            expected_keys = [
                "condition",             # changed from "weather_condition"
                "temperature",
                "humidity",
                "hazardous_condition",
                "severity"
            ]
            for key in expected_keys:
                assert key in data

    def test_condition_validity(self):
        with app.test_client() as client:
            response = client.get('/hazardous-conditions')
            data = response.get_json()

            valid_conditions = ["Sunny", "Rainy", "Windy", "Cloudy", "Snowy"]
            assert data["condition"] in valid_conditions

    def test_temperature_format_and_range(self):
        with app.test_client() as client:
            response = client.get('/hazardous-conditions')
            data = response.get_json()

            temp_str = data["temperature"]
            assert temp_str.endswith('C')
            temp_value = int(temp_str.rstrip('C'))
            assert -30 <= temp_value <= 50

    def test_humidity_format_and_range(self):
        with app.test_client() as client:
            response = client.get('/hazardous-conditions')
            data = response.get_json()

            humidity_str = data["humidity"]
            assert humidity_str.endswith('%')
            humidity_value = int(humidity_str.rstrip('%'))
            assert 10 <= humidity_value <= 100

    def test_hazardous_condition_and_severity_values(self):
        with app.test_client() as client:
            response = client.get('/hazardous-conditions')
            data = response.get_json()

            valid_hazards = [
                "Blizzard Warning",
                "Flood Advisory",
                "Extreme Heat Warning",
                "Wind Chill Advisory",
                "Heat Advisory",
                "No Hazardous Conditions"
            ]
            valid_severities = ["Severe", "High", "None"]

            assert data["hazardous_condition"] in valid_hazards
            assert data["severity"] in valid_severities
