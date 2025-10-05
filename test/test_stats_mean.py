import json
from app import app as flask_app

def test_stats_mean_ok():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean?vals=1,2,3,4")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["mean"] == 2.5

def test_stats_mean_missing():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean")
        assert resp.status_code == 400

def test_stats_mean_invalid():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean?vals=1,abc,3")
        assert resp.status_code == 400
