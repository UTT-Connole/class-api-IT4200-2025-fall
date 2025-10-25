def test_chicken_stats(client):
    response = client.get("/race/stats")
    assert response.status_code == 200


def test_chicken_stats_content(client):
    response = client.get("/race/stats")
    data = response.get_json()
    assert "total_chickens" in data
    assert data["total_chickens"] == 8
    assert "average_speed" in data
    assert "top_speed" in data

def test_chicken_stats_rendered_html(client):
    response = client.get("/race/stats")
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "<h1>BARNYARD PERFORMANCE REPORT</h1>" in html
    assert "Total Chickens:" in html
    assert "Average Speed:" in html
    assert "Top Speed:" in html
    assert "Best Pay Out Chicken:" in html


