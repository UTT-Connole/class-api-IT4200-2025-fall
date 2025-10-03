from app import app



def test_coin_flip_response():
    tester = app.test_client()
    response = tester.get('/clint')
    
    assert response.status_code == 200
    assert response.data.decode() in ["Heads", "Tails"]

def test_coin_flip_randomness():
    tester = app.test_client()
    results = set()

    for _ in range(20):  # Run multiple times
        response = tester.get('/clint')
        results.add(response.data.decode())

    assert "Heads" in results
    assert "Tails" in results

def test_coin_flip_type():
    tester = app.test_client()
    response = tester.get('/clint')
    
    assert isinstance(response.data.decode(), str)

