from unittest.mock import patch
from random import choice

possible_responses = [
    "It is certain",
    "Without a doubt",
    "Most likely",
    "Ask again later",
    "Can't predict now",
    "My sources say no",
    "Outlook not so good",
    "Don't count on it"
]

def test_magic8ball_returns_200(client):
    response = client.get('/magic8ball')
    assert response.status_code == 200

def test_magic8ball_returns_405_bad_method(client):
    response = client.post('/magic8ball')
    assert response.status_code == 405

def test_magic8ball_correct_response(client):
    response = client.get('/magic8ball')
    assert response.text in possible_responses

@patch('random.choice')
def test_magic8ball_response_uses_random_choice(mock_choice, client):
    expected = choice(possible_responses)
    mock_choice.return_value = expected
    response = client.get('/magic8ball').text
    assert response == expected

