from app import app

client = app.test_client()
response = client.get('/real-weather')

def test_meteo_API(client):
    assert response.status_code == 200, "API did not respond with status 200, is Meteo OK?"

def test_datetime_format():
    with app.test_client() as client:
        data = response.get_json()
        current_data = data[0]
        daily_data = data[1]
        time = current_data["time"]
        sunrise = daily_data["sunrise"]
        sunset = daily_data["sunset"]
        if isinstance(sunrise, list):
            sunrise = sunrise[0]
        if isinstance(sunset, list):
            sunset = sunset[0]
        for dt in [time, sunrise, sunset]:
            assert isinstance(dt, str), f"{dt} is not a string"
            assert len(dt) == 16, f"{dt} does not have length 16"
            assert dt[4] == '-' and dt[7] == '-' and dt[10] == 'T' and dt[13] == ':', f"{dt} does not match format YYYY-MM-DDTHH:MM"

def test_temperature_ranges():
    with app.test_client() as client:
        data = response.get_json()
        temperature = data[0]["temperature"]
        min_temp = data[1]["temperature_min"]
        max_temp = data[1]["temperature_max"]
        if isinstance(min_temp, list):
            min_temp = min_temp[0]
        if isinstance(max_temp, list):
            max_temp = max_temp[0]
        # Test current temperature range
        assert isinstance(temperature, (int, float)) and 0 <= temperature <= 130, "Current temperature is out of expected range (0 to 130 F)"
        # Test minimum temperature range
        assert isinstance(min_temp, (int, float)) and -100 <= min_temp <= 130, "Minimum temperature is out of expected range (-100 to 130 F)"
        # Test maximum temperature range
        assert isinstance(max_temp, (int, float)) and -100 <= max_temp <= 130, "Maximum temperature is out of expected range (-100 to 130 F)"
        # Ensure min is not greater than max
        assert min_temp <= max_temp, "Minimum temperature is greater than maximum temperature"

def test_current_humidity_range():
    with app.test_client() as client:
        data = response.get_json()
        humidity = data[0]["humidity"]
        assert isinstance(humidity, (int, float)) and 0 <= humidity <= 100, "Humidity is out of expected range (0 to 100%)"

def test_wind_speed_range():
    with app.test_client() as client:
        data = response.get_json()
        windspeed = data[0]["windspeed"]
        assert isinstance(windspeed, (int, float)) and 0 <= windspeed <= 150, "Wind speed is out of expected range (0 to 150 mph)"

def test_wind_direction_range():
    with app.test_client() as client:
        data = response.get_json()
        winddirection = data[0]["winddirection"]
        assert isinstance(winddirection, (int, float)) and 0 <= winddirection <= 360, "Wind direction is out of expected range (0 to 360 degrees)"

def test_precipitation_probability_range():
    with app.test_client() as client:
        data = response.get_json()
        precipitation_probability = data[1]["precipitation_probability"]
        if isinstance(precipitation_probability, list):
            precipitation_probability = precipitation_probability[0]
        assert isinstance(precipitation_probability, (int, float)) and 0 <= precipitation_probability <= 100, "Precipitation probability is out of expected range (0 to 100%)"