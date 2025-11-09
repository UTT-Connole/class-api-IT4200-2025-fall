def test_gatcha(client):
    response = client.get('/gatcha')
    assert response.status_code == 200

    data = response.json
    assert isinstance(data, dict)
    assert len(data) == 4

    assert 'pool' in data and 'rarities' in data and 'weights' in data and 'last_pull' in data

    expected_rarities = ['C', 'R', 'SR', 'SSR']
    expected_weights = [70, 20, 9, 1]

    assert data['rarities'] == expected_rarities
    assert data['weights'] == expected_weights

    pool = data['pool']
    assert isinstance(pool, list)
    for item in pool:
        assert isinstance(item, dict)
        assert 'name' in item and 'rarity' in item and 'weight' in item
        assert item['rarity'] in expected_rarities
        assert item['weight'] in expected_weights
    
    last_pull = data['last_pull']
    assert isinstance(last_pull, dict)
    assert 'name' in last_pull and 'rarity' in last_pull and 'weight' in last_pull
    assert last_pull['rarity'] in expected_rarities
    assert last_pull['weight'] in expected_weights