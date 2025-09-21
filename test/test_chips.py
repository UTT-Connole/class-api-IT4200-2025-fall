def test_chips_get(client):
    # Test that the chips page loads correctly
    response = client.get('/chips')
    assert response.status_code == 200
    assert b'Enter amount' in response.data

def test_chips_post(client):
    # Test even distribution with amount 341
    response = client.post('/chips', data={'amount': '341'})
    assert response.status_code == 200
    assert b'$100' in response.data
    assert b'$25' in response.data
    assert b'$10' in response.data
    assert b'$5' in response.data
    assert b'$1' in response.data

def test_chips_invalid_input(client):
    # Test with invalid input (negative number)
    response = client.post('/chips', data={'amount': '-100'})
    assert response.status_code == 200
    
def test_chips_zero_amount(client):
    # Test with zero amount
    response = client.post('/chips', data={'amount': '0'})
    assert response.status_code == 200

def test_chips_large_amount(client):
    # Test with a large amount
    response = client.post('/chips', data={'amount': '999'})
    assert response.status_code == 200
    assert b'$100' in response.data
