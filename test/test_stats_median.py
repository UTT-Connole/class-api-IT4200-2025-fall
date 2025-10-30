import json
from app import app as flask_app

def test_stats_median_ok_odd():
    with flask_app.test_client() as client:
        resp = client.get("/stats/median?vals=1,9,3")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["median"] == 3.0

def test_stats_median_ok_even():
    with flask_app.test_client() as client:
        resp = client.get("/stats/median?vals=1,2,3,4")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["median"] == 2.5

def test_stats_median_missing():
    with flask_app.test_client() as client:
        resp = client.get("/stats/median")
        assert resp.status_code == 400

def test_stats_median_invalid():
    with flask_app.test_client() as client:
        resp = client.get("/stats/median?vals=1,a,3")
        assert resp.status_code == 400
