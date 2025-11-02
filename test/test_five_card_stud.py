import json
from unittest.mock import patch


def test_five_card_stud_endpoint_exists(client):
    """Test that the /five_card_stud endpoint exists and returns JSON"""
    response = client.get('/five_card_stud')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


@patch('random.sample')
def test_royal_flush(mock_sample, client):
    """Test Royal Flush: A, K, Q, J, 10 all same suit"""
    # Suit 0 (spades): 10, J, Q, K, A
    mock_sample.return_value = [(0, 9), (0, 10), (0, 11), (0, 12), (0, 0)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Royal Flush"


@patch('random.sample')
def test_straight_flush(mock_sample, client):
    """Test Straight Flush: 5 consecutive cards same suit"""
    # Suit 1 (hearts): 5, 6, 7, 8, 9
    mock_sample.return_value = [(1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Straight Flush"


@patch('random.sample')
def test_four_of_a_kind(mock_sample, client):
    """Test Four of a Kind: 4 cards same rank"""
    # Four 7s and a 2
    mock_sample.return_value = [(0, 7), (1, 7), (2, 7), (3, 7), (0, 2)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Four of a Kind"


@patch('random.sample')
def test_full_house(mock_sample, client):
    """Test Full House: 3 of a kind + pair"""
    # Three 9s and two 4s
    mock_sample.return_value = [(0, 9), (1, 9), (2, 9), (0, 4), (1, 4)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Full House"


@patch('random.sample')
def test_flush(mock_sample, client):
    """Test Flush: 5 cards same suit, not consecutive"""
    # All diamonds, not consecutive
    mock_sample.return_value = [(2, 2), (2, 5), (2, 8), (2, 10), (2, 12)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Flush"


@patch('random.sample')
def test_straight(mock_sample, client):
    """Test Straight: 5 consecutive cards, different suits"""
    # 4, 5, 6, 7, 8 different suits
    mock_sample.return_value = [(0, 4), (1, 5), (2, 6), (3, 7), (0, 8)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Straight"


@patch('random.sample')
def test_straight_ace_high(mock_sample, client):
    """Test Straight with Ace high: 10, J, Q, K, A different suits"""
    # 10, J, Q, K, A different suits
    mock_sample.return_value = [(0, 9), (1, 10), (2, 11), (3, 12), (1, 0)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Straight"


@patch('random.sample')
def test_three_of_a_kind(mock_sample, client):
    """Test Three of a Kind: 3 cards same rank"""
    # Three 6s, a 2 and a 9
    mock_sample.return_value = [(0, 6), (1, 6), (2, 6), (0, 2), (1, 9)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Three of a Kind"


@patch('random.sample')
def test_two_pair(mock_sample, client):
    """Test Two Pair: 2 different pairs"""
    # Two 8s, two 3s, and a King
    mock_sample.return_value = [(0, 8), (1, 8), (2, 3), (3, 3), (0, 12)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Two Pair"


@patch('random.sample')
def test_pair(mock_sample, client):
    """Test Pair: 2 cards same rank"""
    # Two Jacks and three random cards
    mock_sample.return_value = [(0, 10), (1, 10), (2, 3), (3, 7), (0, 1)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Pair"


@patch('random.sample')
def test_high_card(mock_sample, client):
    """Test High Card: no matches or sequences"""
    # Random cards with no matches
    mock_sample.return_value = [(0, 2), (1, 5), (2, 8), (3, 10), (0, 12)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "High Card"


@patch('random.sample')
def test_flush_beats_straight_detection(mock_sample, client):
    """Test that flush is correctly identified even with near-straight"""
    # All spades: 3, 5, 7, 9, 11 (flush but not straight)
    mock_sample.return_value = [(0, 3), (0, 5), (0, 7), (0, 9), (0, 11)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Flush"


@patch('random.sample')
def test_straight_different_suits(mock_sample, client):
    """Test straight with mixed suits to ensure it's not misidentified as flush"""
    # 2, 3, 4, 5, 6 all different suits
    mock_sample.return_value = [(0, 2), (1, 3), (2, 4), (3, 5), (0, 6)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Straight"


@patch('random.sample')
def test_full_house_not_misidentified(mock_sample, client):
    """Test full house is correctly identified over three of a kind or pair"""
    # Three Aces and two Kings
    mock_sample.return_value = [(0, 0), (1, 0), (2, 0), (0, 12), (1, 12)]

    response = client.get('/five_card_stud')
    data = json.loads(response.data)

    assert data == "Full House"