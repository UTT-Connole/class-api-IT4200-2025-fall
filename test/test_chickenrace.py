from app import app
import pytest

def test_chickenrace_get():
    """Test that the chicken race page loads correctly"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert response.status_code == 200
    assert b'Barnyard Racing Exchange' in response.data

def test_chickenrace_post_valid_bet():
    """Test placing a valid bet returns all expected chicken stats and fun fact"""
    client = app.test_client()
    data = {
        'chicken': "Hen Solo",
        'bet': '10'
    }
    response = client.post('/chickenrace', data=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'winner' in json_data
    assert 'message' in json_data
    assert 'winnings' in json_data
    assert 'odds' in json_data
    assert 'fun_fact' in json_data
    assert isinstance(json_data['fun_fact'], str)
    assert isinstance(json_data['odds'], str)

def test_chickenrace_post_invalid_bet():
    """Test placing an invalid bet amount"""
    client = app.test_client()
    data = {
        'chicken': "Colonel Sanders Revenge",     # The HTML handles the bet being larger than 0 so this 
        'bet': '0'                                 # test just ensures server handles it gracefully
    }
    response = client.post('/chickenrace', data=data)
    assert response.status_code == 200











def test_chickenrace_odds():
    """Test that odds are correctly set"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert b'5/10' in response.data 
    assert b'6/10' in response.data
    assert b'4/10' in response.data
    assert b'7/10' in response.data
    assert b'3/10' in response.data

def test_chickenrace_get_chicken_stats_in_dropdown():
    """Test that chicken stats appear in the dropdown on GET"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert b'Hen Solo' in response.data
    assert b'Odds:' in response.data
    assert b'Speed:' in response.data
    assert b'Stamina:' in response.data
    assert b'Luck:' in response.data


def test_chickenrace_form_elements():
    """Check that the form elements exist on the page"""
    client = app.test_client()
    response = client.get("/chickenrace")
    html = response.data.decode("utf-8")
    assert '<form' in html
    assert 'type="submit"' in html
    assert 'name="bet"' in html  # check if input or select for betting exists
