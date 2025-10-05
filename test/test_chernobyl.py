def test_return_json(client):
    response = client.get("/api/chernobyl/properties")
    assert response.content_type == 'application/json'


def test_structure(client):
    response = client.get("/api/chernobyl/properties")
    data = response.get_json()
    assert 'message' in data
    assert 'properties' in data
    assert isinstance(data['properties'], list)


def test_required_fields(client):
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
   
    required_fields = ['id', 'address', 'price', 'radiation_level',
                      'distance_from_reactor', 'amenities', 'warnings']
   
    for property_item in data['properties']:
        for field in required_fields:
            assert field in property_item, f"Missing field: {field}"




def test_property_ids_are_unique(client):
    """Test all property IDs are unique"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
    
    property_ids = [prop['id'] for prop in data['properties']]
    assert len(property_ids) == len(set(property_ids)), "Duplicate property IDs found"


def test_property_ids_are_positive(client):
    """Test all property IDs are positive integers"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
    
    for prop in data['properties']:
        assert prop['id'] > 0, f"Property ID must be positive, got {prop['id']}"

def test_warnings_exist(client):
    """Test all properties have at least one warning"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
    
    for prop in data['properties']:
        assert len(prop['warnings']) > 0, f"Property {prop['id']} has no warnings"

def test_amenities_exist(client):
    """Test all properties have at least one amenity"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
    
    for prop in data['properties']:
        assert len(prop['amenities']) > 0, f"Property {prop['id']} has no amenities"

def test_addresses_not_empty(client):
    """Test all property addresses are non-empty strings"""
    response = client.get('/api/chernobyl/properties')
    data = response.get_json()
    
    for prop in data['properties']:
        assert len(prop['address'].strip()) > 0, f"Property {prop['id']} has empty address"
