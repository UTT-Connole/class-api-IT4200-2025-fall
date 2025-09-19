def test_add_chips(client):
    response = client.get('/add_chips')
    assert response.status_code == 200

    data = response.json
    assert isinstance(data, list)
    assert len(data) == 3

    expected_chips = {'Gold': 100, 'Silver': 50, 'Bronze': 25}
    for chip in data:
        assert 'type' in chip and 'value' in chip
        assert chip['type'] in expected_chips
        assert chip['value'] == expected_chips[chip['type']]