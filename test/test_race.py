def test_race_get(client):
    response = client.get('/race')
    assert response.status_code == 200   

def test_race_post_valid_bet(client):
    data = {
        'chicken': "Hen Solo",
        'bet': '10'
    }
    response = client.post('/race', data=data)
    json_data = response.get_json()
    assert 'winner' in json_data
    assert 'message' in json_data
    assert 'winnings' in json_data
    assert 'odds' in json_data
    assert 'fun_fact' in json_data
    assert isinstance(json_data['fun_fact'], str)
    assert isinstance(json_data['odds'], str)

def test_race_post_invalid_bet(client):
    data = {
        'chicken': "Colonel Sanders Revenge",     # The HTML handles the bet being larger than 0 so this 
        'bet': '0'                                 # test just ensures server handles it gracefully
    }
    response = client.post('/race', data=data)
    assert response.status_code == 200

def test_race_odds(client):
    response = client.get('/race')
    assert b'5/10' in response.data 
    assert b'6/10' in response.data
    assert b'4/10' in response.data
    assert b'3/10' in response.data

def test_race_get_chicken_stats_in_dropdown(client):
    response = client.get('/race')
    assert b'Hen Solo' in response.data
    assert b'Odds:' in response.data
    assert b'Speed:' in response.data
    assert b'Stamina:' in response.data
    assert b'Luck:' in response.data


def test_race_form_elements(client):
    response = client.get("/race")
    html = response.data.decode("utf-8")
    assert '<form' in html
    assert 'type="submit"' in html
    assert 'name="bet"' in html  # check if input or select for betting exists