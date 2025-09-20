def test_return_json(client):
    response = client.get("/api/chernobyl/properties")
    assert response.content_type == 'application/json'


def test_structure(client):
    response = client.get("/api/chernobyl/properties")
    data = response.get_json()
    assert 'message' in data
    assert 'properties' in data
    assert isinstance(data['properties'], list)



def test_chernobyl_get_method(client):
    response = client.post('/api/chernobyl/properties')
    assert response.status_code == 405
    
    response = client.put('/api/chernobyl/properties')
    assert response.status_code == 405
    
    response = client.delete('/api/chernobyl/properties')
    assert response.status_code == 405


def test_required_fields(client):
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
   
    required_fields = ['id', 'address', 'price', 'radiation_level',
                      'distance_from_reactor', 'amenities', 'warnings']
   
    for property_item in data['properties']:
        for field in required_fields:
            assert field in property_item, f"Missing field: {field}"


def test_get_chernobyl_properties_full_response(client):
    """Test the complete response structure and content"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
   
    expected_response = {
        "message": "Chernobyl Real Estate - Where your problems glow away!",
        "properties": [
            {
                "id": 1,
                "address": "Pripyat Central Square, Apartment Block #1",
                "price": 0,
                "radiation_level": "15,000 mSv/year",
                "distance_from_reactor": "3 km",
                "amenities": ["Ferris wheel view", "Glow-in-the-dark features", "No electricity needed"],
                "warnings": ["Protective gear required", "May cause mutations"]
            },
            {
                "id": 2,
                "address": "Reactor 4 Penthouse Suite",
                "price": -1000000,
                "radiation_level": "Over 9000 mSv/year",
                "distance_from_reactor": "0 km",
                "amenities": ["360° views", "Built-in sarcophagus", "Unlimited energy"],
                "warnings": ["Immediate death likely", "GPS stops working"]
            }
        ]
    }
   
    assert data == expected_response

