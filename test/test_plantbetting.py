def test_place_plant_bet_invalid_amount(client):
    """When an invalid bet amount is placed, the route should return an error message."""
    builtins.input = lambda prompt='': '-5'  # Simulating an invalid bet of -5
    resp = client.post('/place_plant_bet')
    assert resp.status_code == 400
    assert resp.get_data(as_text=True) == 'Invalid bet amount!'

def test_place_plant_bet_zero_amount(client):
    """When a bet of zero is placed, the route should return an error message."""
    builtins.input = lambda prompt='': '0'  # Simulating a bet of 0
    resp = client.post('/place_plant_bet')
    assert resp.status_code == 400
    assert resp.get_data(as_text=True) == 'Invalid bet amount!'
def test_place_plant_bet_valid_amount(client):
    """When a valid bet amount is placed, the route should return a success message."""
    builtins.input = lambda prompt='': '10'  # Simulating a valid bet of 10
    resp = client.post('/place_plant_bet')
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == 'Bet placed successfully!'