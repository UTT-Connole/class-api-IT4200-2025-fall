from app import app

def test_ping_ok():
    client = app.test_client()
    resp = client.get("/api/ping")
    assert resp.status_code == 200
    assert resp.is_json
    data = resp.get_json()
    assert data["status"] == "ok"
    assert isinstance(data["uptime_ms"], int)
    assert data["uptime_ms"] >= 0
