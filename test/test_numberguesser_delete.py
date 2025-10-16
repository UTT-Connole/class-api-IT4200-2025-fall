from app import app

def test_random_weather_status_code():
    with app.test_client() as client:
        resp = client.get("/numberguesser")
        assert resp.status_code == 404, "endpoint exists? it shouldn't"
