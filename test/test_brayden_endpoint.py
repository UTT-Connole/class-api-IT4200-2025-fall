
def test_home(client):
    response = client.get('/brayden')
    assert response.status_code == 200