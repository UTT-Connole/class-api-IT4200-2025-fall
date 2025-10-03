
def test_blackjack_endpoint_accepts_post(client):
    """Test that POST /blackjack endpoint exists"""
    resp = client.post('/blackjack', json={'bet_amount': 10, 'username': 'alice'})
    # Just check it doesn't return 405 Method Not Allowed
    assert resp.status_code != 405

def test_blackjack_get_content_type(client):
    """Test that GET returns HTML content type"""
    resp = client.get('/blackjack')
    assert 'text/html' in resp.content_type