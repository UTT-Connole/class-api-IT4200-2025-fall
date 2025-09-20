def test_return_json(client):
    response = client.get("/api/mars/properties")
    assert response.content_type == 'application/json'


def test_structure(client):
    response = client.get("/api/mars/properties")
    data = response.get_json()
    assert 'message' in data
    assert 'properties' in data
    assert isinstance(data['properties'], list)



def test_get_chernobyl_properties_only_get_method(client):
    response = client.post('/api/mars/properties')
    assert response.status_code == 405
    
    response = client.put('/api/mars/properties')
    assert response.status_code == 405
    
    response = client.delete('/api/mars/properties')
    assert response.status_code == 405


def test_required_fields(client):
    response = client.get('/api/mars/properties')
    data = response.get_json()
   
    required_fields = ['id', 'address', 'price', 'oxygen_level',
                      'temperature', 'amenities', 'warnings']
   
    for property_item in data['properties']:
        for field in required_fields:
            assert field in property_item, f"Missing field: {field}"


def test_get_chernobyl_properties_full_response(client):
    """Test the complete response structure and content"""
    response = client.get('/api/mars/properties')
    data = response.get_json()
   
    expected_response = {
        "message": "Mars Realty - Out of this world properties!",
        "properties": [
            {
                "id": 1,
                "address": "Olympus Mons Base Camp",
                "price": 2000000,
                "oxygen_level": "0%",
                "temperature": "-80°C to 20°C",
                "amenities": ["Tallest mountain views", "Low gravity fun", "Dust storm entertainment"],
                "warnings": ["Bring your own atmosphere", "18-month commute", "No pizza delivery"]
            },
            {
                "id": 2,
                "address": "Valles Marineris Canyon Penthouse",
                "price": 1500000,
                "oxygen_level": "0%",
                "temperature": "-120°C",
                "amenities": ["Grand Canyon views (but bigger)", "Extreme sports opportunities", "Silence guarantee"],
                "warnings": ["Radiation exposure", "No neighbors for 35 million miles", "Elon Musk not included"]
            }
        ]
    }
   
    assert data == expected_response
