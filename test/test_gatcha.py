def test_gatcha(client):
    response = client.get('/gatcha')
    assert response.status_code == 200

    data = response.json
    # The app returns a dict with three top-level keys: pool, rarities, weights
    assert isinstance(data, dict)
    assert len(data) == 3

    assert 'pool' in data and 'rarities' in data and 'weights' in data

    expected_rarities = ['C', 'R', 'SR', 'SSR']
    expected_weights = [70, 20, 9, 1]

    # Validate the rarities and weights arrays
    assert data['rarities'] == expected_rarities
    assert data['weights'] == expected_weights

    # Validate each pool item has the expected shape
    pool = data['pool']
    assert isinstance(pool, list)
    for item in pool:
        assert isinstance(item, dict)
        assert 'name' in item and 'rarity' in item and 'weight' in item
        assert item['rarity'] in expected_rarities
        assert item['weight'] in expected_weights