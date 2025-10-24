def test_nowizard(client):
    response = client.get('/wizard')
    assert response.status_code == 404