possible_responses = [
    "It is certain",
    "Without a doubt",
    "Most likely",
    "Ask again later",
    "Can't predict now",
    "My sources say no",
    "Outlook not so good",
    "Don't count on it"
]

def test_magic8ball_returns_200(client):
    response = client.get('/magic8ball')
    assert response.status_code == 200

def test_magic8ball_correct_response(client):
    response = client.get('/magic8ball')
    assert response.text in possible_responses

def test_magic8ball_response_is_random(client):
    '''
    There is a non-zero chance that this test randomly fails,
    but it is a 1 in 8^5 (32768) chance. I'll take those odds.
    '''
    responses = [
        client.get('/magic8ball').text
        for _ in range(5)
    ]

    # If randomness works, the set should have >1 unique response
    assert len(set(responses)) > 1, f"All responses were identical: {responses}"
