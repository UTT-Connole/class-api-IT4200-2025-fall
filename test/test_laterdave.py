def test_bydave(client):
    response = client.get('/dave')
    assert response.status_code == 404