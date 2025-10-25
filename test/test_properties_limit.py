def test_chernobyl_returns_all(client):
    """Should return all 4 Chernobyl properties regardless of limit param"""
    r = client.get("/api/chernobyl/properties?limit=1")
    assert r.status_code == 200
    data = r.get_json()
    assert "properties" in data
    props = data["properties"]
    assert isinstance(props, list)
    assert len(props) == 4  


def test_mars_limit_too_big_clamps(client):
    r = client.get("/api/mars/properties?limit=99")
    assert r.status_code == 200
    data = r.get_json()
    props = data["properties"]
    assert isinstance(props, list)
    assert len(props) >= 1  # list has at least one sample property


def test_chernobyl_limit_bad_type(client):
    r = client.get("/api/chernobyl/properties?limit=abc")
    assert r.status_code == 200  
    data = r.get_json()
    assert "properties" in data
    props = data["properties"]
    assert isinstance(props, list)
    assert len(props) == 4 
