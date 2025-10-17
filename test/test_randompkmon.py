def test_randompkmon_redirect(client):
    response = client.get("/randompkmon")
    assert response.status_code == 404
