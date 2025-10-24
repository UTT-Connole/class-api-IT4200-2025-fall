def test_random_restaurants_status_code(client):
    resp = client.get("/randomRestaurant")
    assert resp.status_code == 404, "This endpoint shouldn't exist"