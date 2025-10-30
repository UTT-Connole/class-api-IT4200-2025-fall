def test_if_fav_quote_endpoint_is_gone(client):
    response = client.get('/fav_quote')
    assert response.status_code == 404