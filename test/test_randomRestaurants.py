from unittest.mock import patch
from random import choice

possible_responses = [
    "Red Fort Cuisine Of India",
    "Painted Pony Restaurant",
    "Sakura Japanese Steakhouse",
    "Rusty Crab Daddy",
    "Mixed Greens",
    "Cliffside Restaurant",
    "Aubergine Kitchen"
]

def test_randomRestaurant_returns_200(client):
    response = client.get('/randomRestaurant')
    assert response.status_code == 200

def test_randomRestaurant_returns_405_bad_method(client):
    response = client.post('/randomRestaurant')
    assert response.status_code == 405

def test_randomRestaurant_correct_response(client):
    response = client.get('/randomRestaurant')
    assert response.text in possible_responses

@patch('random.choice')
def test_randomRestaurant_response_uses_random_choice(mock_choice, client):
    expected = choice(possible_responses)
    mock_choice.return_value = expected
    response = client.get('/randomRestaurant').text
    assert response == expected

