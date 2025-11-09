import json


def test_list_endpoints_structure(client):
    """Ensure `/__endpoints` returns a JSON with count and endpoints list."""
    resp = client.get("/__endpoints")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert "count" in data and isinstance(data["count"], int)
    assert "endpoints" in data and isinstance(data["endpoints"], list)

    rules = [r.get("rule") for r in data["endpoints"]]
    assert "/" in rules
    assert "/__endpoints" in rules
