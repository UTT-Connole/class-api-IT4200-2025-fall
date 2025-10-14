
def test_chips_gone_baby(client):
    response = client.get("/chips")
    assert response.status_code == 404
