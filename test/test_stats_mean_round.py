import json
from app import app as flask_app

def test_stats_mean_round_noop():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean?vals=1,2,3&round=1")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["mean"] == 2.0  

def test_stats_mean_round_applied():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean?vals=1,2,3.3333&round=2")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["mean"] == 2.11

def test_stats_mean_round_out_of_range():
    with flask_app.test_client() as client:
        resp = client.get("/stats/mean?vals=1,2,3&round=99")
        assert resp.status_code == 400
