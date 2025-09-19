def test_landing(client):
    response = client.get('/')
    assert response.status_code == 200

def test_404(client):
    response = client.get('/not-found')
    assert response.status_code == 404


