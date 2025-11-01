import random
from unittest.mock import patch

def test_drawCard(client):
    response = client.get('/drawCard')
    assert response.status_code == 200

    data = response.json
    assert 'rank' in data
    assert 'suit' in data

@patch('random.choice')
def test_drawCard_uses_randomChoice(mock_choice, client):
    expected = "Hearts"
    mock_choice.return_value = expected
    response = client.get('/drawCard').json
    print("TESTING THING", response, expected)
    assert response['rank'] == "Hearts"