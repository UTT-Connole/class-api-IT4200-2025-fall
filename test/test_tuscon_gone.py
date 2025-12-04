def test_if_Tuscon_endpoint_is_gone(client):
    response = client.get('/Tuscon')
    assert response.status_code == 404
    assert b'Not Found' in response.data