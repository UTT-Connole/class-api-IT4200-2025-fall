def test_dallin_delete(client):
    response = client.post('/dallin', json={"confirm": "yes"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Deleting the internet... Goodbye world"
    assert data["status"] == "deleted"

def test_dallin_cancel(client):
    response = client.post('/dallin', json={"confirm": "no"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Operation canceled. For now."
    assert data["status"] == "canceled"

def test_dallin_missing_confirm(client):
    response = client.post('/dallin', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Operation canceled. For now."
    assert data["status"] == "canceled"