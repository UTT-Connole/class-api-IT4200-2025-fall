import json
from unittest.mock import patch

def test_craps_endpoint_exists(client):
    """Test that the /craps endpoint exists and returns JSON"""
    response = client.get('/craps')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_craps_returns_valid_result(client):
    """Test that the endpoint returns a valid result (0 or 1)"""
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert 'result' in data
    assert data['result'] in [0, 1]


@patch('random.randint')
def test_craps_immediate_win_7(mock_randint, client):
    """Test immediate win with roll of 7"""
    mock_randint.return_value = 3  # 3 + 3 = 6, but we need 7
    mock_randint.side_effect = [3, 4]  # 3 + 4 = 7
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 1


@patch('random.randint')
def test_craps_immediate_win_11(mock_randint, client):
    """Test immediate win with roll of 11"""
    mock_randint.side_effect = [5, 6]  # 5 + 6 = 11
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 1


@patch('random.randint')
def test_craps_immediate_loss_2(mock_randint, client):
    """Test immediate loss with roll of 2"""
    mock_randint.side_effect = [1, 1]  # 1 + 1 = 2
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 0


@patch('random.randint')
def test_craps_immediate_loss_3(mock_randint, client):
    """Test immediate loss with roll of 3"""
    mock_randint.side_effect = [1, 2]  # 1 + 2 = 3
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 0


@patch('random.randint')
def test_craps_immediate_loss_12(mock_randint, client):
    """Test immediate loss with roll of 12"""
    mock_randint.side_effect = [6, 6]  # 6 + 6 = 12
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 0


@patch('random.randint')
def test_craps_point_win(mock_randint, client):
    """Test winning by hitting the point"""
    # First roll: 8 (point), second roll: 8 (win)
    mock_randint.side_effect = [4, 4, 3, 5]  # 8, then 8 again
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 1


@patch('random.randint')
def test_craps_point_loss(mock_randint, client):
    """Test losing by rolling 7 before hitting point"""
    # First roll: 8 (point), second roll: 7 (loss)
    mock_randint.side_effect = [4, 4, 3, 4]  # 8, then 7
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 0


@patch('random.randint')
def test_craps_multiple_point_rolls(mock_randint, client):
    """Test multiple rolls before resolution"""
    # Point: 6, then roll 5, 9, 10, 6 (win)
    mock_randint.side_effect = [
        3, 3,  # First roll: 6 (point)
        2, 3,  # Second roll: 5 (continue)
        4, 5,  # Third roll: 9 (continue)
        4, 6,  # Fourth roll: 10 (continue)
        2, 4   # Fifth roll: 6 (win!)
    ]
    
    response = client.get('/craps')
    data = json.loads(response.data)
    
    assert data['result'] == 1