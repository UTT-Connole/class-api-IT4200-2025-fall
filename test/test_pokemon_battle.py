# test_pokemon_battle.py

def test_pokemon_battle_get_page(client):
    """Test that the Pokemon battle page loads correctly"""
    response = client.get('/pokemon-ranked')
    assert response.status_code == 200
    assert b'Pokemon Battles' in response.data
    assert b'Enter your Pokemon of choice' in response.data

def test_pokemon_battle_existing_pokemon(client):
    """Test battle with an existing Pokemon"""
    response = client.post('/pokemon-ranked', data={'pokemon': 'Charizard'})
    assert response.status_code == 200
    
    # Should contain battle results
    assert b'Battle Results!' in response.data
    assert b'Charizard' in response.data
    assert b'points' in response.data
    
    # Should have winner announcement
    assert (b'You win!' in response.data or 
            b'Computer wins!' in response.data or 
            b"It's a tie!" in response.data)

def test_pokemon_battle_case_insensitive(client):
    """Test that Pokemon names are case insensitive"""
    response = client.post('/pokemon-ranked', data={'pokemon': 'MEWTWO'})
    assert response.status_code == 200
    assert b'Battle Results!' in response.data
    assert b'Mewtwo' in response.data

def test_pokemon_battle_unknown_pokemon_no_power(client):
    """Test entering unknown Pokemon without power rating"""
    response = client.post('/pokemon-ranked', data={'pokemon': 'Pikachu'})
    assert response.status_code == 200
    assert b'not in the list' in response.data
    assert b'add its power level' in response.data
    assert b'Pikachu' in response.data

def test_pokemon_battle_add_new_pokemon(client):
    """Test adding a new Pokemon with valid power rating"""
    response = client.post('/pokemon-ranked', data={
        'pokemon': 'Pikachu',
        'power_rating': '60'
    })
    assert response.status_code == 200
    assert b'Battle Results!' in response.data
    assert b'Pikachu' in response.data

def test_pokemon_battle_duplicate_power_score(client):
    """Test that duplicate power scores are rejected"""
    # First add a Pokemon with score 50
    client.post('/pokemon-ranked', data={
        'pokemon': 'TestPokemon1',
        'power_rating': '50'
    })
    
    # Try to add another Pokemon with same score
    response = client.post('/pokemon-ranked', data={
        'pokemon': 'TestPokemon2', 
        'power_rating': '50'
    })
    assert response.status_code == 200
    assert b'already taken' in response.data

def test_pokemon_battle_invalid_power_rating_non_numeric(client):
    """Test invalid power rating (non-numeric)"""
    response = client.post('/pokemon-ranked', data={
        'pokemon': 'Bulbasaur',
        'power_rating': 'invalid'
    })
    assert response.status_code == 200
    assert b'must be a valid number' in response.data

def test_pokemon_battle_invalid_power_rating_out_of_range(client):
    """Test invalid power rating (out of range)"""
    # Test too high
    response = client.post('/pokemon-ranked', data={
        'pokemon': 'Squirtle',
        'power_rating': '101'
    })
    assert response.status_code == 200
    assert b'must be between 1 and 100' in response.data
    
    # Test too low
    response = client.post('/pokemon-ranked', data={
        'pokemon': 'Wartortle',
        'power_rating': '0'
    })
    assert response.status_code == 200
    assert b'must be between 1 and 100' in response.data

def test_pokemon_battle_empty_pokemon_name(client):
    """Test submitting empty Pokemon name"""
    response = client.post('/pokemon-ranked', data={'pokemon': ''})
    assert response.status_code == 200
    assert b'Please enter a Pokemon name!' in response.data

def test_pokemon_battle_whitespace_pokemon_name(client):
    """Test submitting Pokemon name with only whitespace"""
    response = client.post('/pokemon-ranked', data={'pokemon': '   '})
    assert response.status_code == 200
    assert b'Please enter a Pokemon name!' in response.data

def test_pokemon_battle_result_structure(client):
    """Test that battle results contain all expected elements"""
    response = client.post('/pokemon-ranked', data={'pokemon': 'Mewtwo'})
    assert response.status_code == 200
    
    # Check for battle result elements
    response_text = response.get_data(as_text=True)
    assert 'Battle Results!' in response_text
    assert 'points' in response_text
    assert ('You win!' in response_text or 
            'Computer wins!' in response_text or 
            "It's a tie!" in response_text)