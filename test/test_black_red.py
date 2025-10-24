def test_color_endpoint_exists(client):
    
    resp = client.get("/color")
    assert resp.status_code == 404
