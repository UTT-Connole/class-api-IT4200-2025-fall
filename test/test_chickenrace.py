from app import app
import pytest

def test_chickenrace_get():
    """Test that the chicken race page loads correctly"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert response.status_code == 200
    assert b'Barnyard Racing Exchange' in response.data

def test_chickenrace_post_valid_bet():
    """Test placing a valid bet"""
    client = app.test_client()
    data = {
        'chicken': "Colonel Sanders' Revenge",
        'bet': '100'
    }
    response = client.post('/chickenrace', data=data)
    json_data = response.get_json()
    assert 'winner' in json_data
    assert 'message' in json_data
    assert 'winnings' in json_data

def test_chickenrace_post_invalid_bet():
    """Test placing an invalid bet amount"""
    client = app.test_client()
    data = {
        'chicken': "Colonel Sanders' Revenge",     # The HTML handles the bet being larger than 0 so this 
        'bet': '0'                                 # test just ensures server handles it gracefully
    }
    response = client.post('/chickenrace', data=data)
    assert response.status_code == 200

def test_chickenrace_odds():
    """Test that odds are correctly set"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert b'2.0' in response.data 
    assert b'10.0' in response.data 