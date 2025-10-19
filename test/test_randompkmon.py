def test_randompkmon_redirect(client):
    response = client.get("/randompkmon")
    assert response.status_code == 404

def test_random_pokemon_works(client):
    response = client.get("/random_pokemon")
    assert response.status_code == 404