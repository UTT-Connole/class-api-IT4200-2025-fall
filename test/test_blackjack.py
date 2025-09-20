def test_blackjack_tie(client):
    """When the game is a tie, the route should return 'It's a Tie!'"""
    builtins.input = lambda prompt='': '10'
    resp = client.get('/blackjack')
    assert resp.status_code == 200
    # The view returns plain text
    assert resp.get_data(as_text=True) == "It's a Tie!"

def test_blackjack_invalid_input(client):
    """When the input is not a number, the route should return 'Invalid Input'"""
    builtins.input = lambda prompt='': 'abc'
    resp = client.get('/blackjack')
    assert resp.status_code == 200
    # The view returns plain text
    assert resp.get_data(as_text=True) == 'Invalid Input'
    
def test_blackjack_win(client):
    """When the player wins, the route should return 'You Win!'"""
    builtins.input = lambda prompt='': '21'
    resp = client.get('/blackjack')
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == 'You Win!'

def test_blackjack_lose(client):
    """When the player loses, the route should return 'You Lose!'"""
    builtins.input = lambda prompt='': '5'
    resp = client.get('/blackjack')
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == 'You Lose!'

def test_blackjack_bust(client):
    """When the player busts, the route should return 'Bust!'"""
    builtins.input = lambda prompt='': '22'
    resp = client.get('/blackjack')
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == 'Bust!'