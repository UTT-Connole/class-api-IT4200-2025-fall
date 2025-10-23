from unittest.mock import patch
from random import choice

possible_responses = [
    "Red Fort Cuisine Of India",
    "Painted Pony Restaurant",
    "Sakura Japanese Steakhouse",
    "Rusty Crab Daddy",
    "Mixed Greens",
    "Cliffside Restaurant",
    "Aubergine Kitchen",
    "Panda Express",
    "Del Taco",
    "Chic-fil-a"
]

def test_randomRestaurant_returns_200(client):
    response = client.get('/randomRestaurant')
    assert response.status_code == 200

def test_randomRestaurant_returns_405_bad_method(client):
    response = client.post('/randomRestaurant')
    assert response.status_code == 405

def test_random_restaurant_all_possible_responses(client):
    expected_restaurants = [
        "Red Fort Cuisine Of India",
        "Painted Pony Restaurant", 
        "Sakura Japanese Steakhouse", 
        "Rusty Crab Daddy", 
        "Mixed Greens", 
        "Cliffside Restaurant", 
        "Aubergine Kitchen",
        "Panda Express",
        "Del Taco",
        "Chic-fil-a"
    ]

    # test each restaurant deterministically by mocking random.choice
    for restaurant in expected_restaurants:
        with patch("random.choice", return_value=restaurant):
            response = client.get("/randomRestaurant")
            assert response.status_code == 200
            assert response.get_json() == restaurant


@patch('random.choice')
def test_randomRestaurant_response_uses_random_choice(mock_choice, client):
    expected = choice(possible_responses)
    mock_choice.return_value = expected
    response = client.get('/randomRestaurant')
    assert response.get_json() == expected

