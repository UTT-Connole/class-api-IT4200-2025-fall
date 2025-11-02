def test_chicken_stats(client):
    response = client.get("/race/stats")
    assert response.status_code == 200

def test_chicken_stats_rendered_html(client):
    response = client.get("/race/stats")
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "<h1>BARNYARD PERFORMANCE REPORT</h1>" in html
    assert "Top Speed:" in html
    assert "Top Stamina:" in html
    assert "Luckiest Chicken:" in html
    assert "Best Pay Out Chicken:" in html


def test_chicken_stats_predicted_winner(client):
    response = client.get("/race/stats")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Predicted Winner:" in html
    assert "Cluck Norris" in html 
