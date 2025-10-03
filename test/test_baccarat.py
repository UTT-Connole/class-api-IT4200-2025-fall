def test_baccarat_returns_200(client):
    response = client.get('/baccarat')
    assert response.status_code == 200
    assert response.data == b'Baccarat endpoint is working!'