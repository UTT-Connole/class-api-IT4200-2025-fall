def test_gatcha(client):
    response = client.get('/gatcha')
    assert response.status_code == 200

    data = response.jason
    assert isinstance(data, list)
    assert len(data) == 3

    expected_rarities = ['C', 'R', 'SR', 'SSR']
    expected_weights = [70, 20, 9, 1]
    for item in data:
        assert 'name' in item and 'rarity' in item and 'weight' in item
        assert item['rarity'] in expected_rarities
        assert item['weight'] in expected_weights