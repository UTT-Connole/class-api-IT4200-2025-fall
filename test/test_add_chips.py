def test_add_chips(client):
    response = client.get("/add_chips")
    assert response.status_code == 200