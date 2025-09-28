# import pytest
# from app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_breakfest_status_code(client):
#     response = client.get('/breakfest')
#     assert response.status_code == 200

# def test_breakfest_key_in_response(client):
#     response = client.get('/breakfest')
#     data = response.get_json()
#     assert "breakfest" in data

# def test_breakfest_value_is_valid_option(client):
#     valid_options = [
#         "Pancakes", "Waffles", "Omelette", "Cereal", "Fruit Salad", "Yogurt Parfait",
#         "Avocado Toast", "Breakfast Burrito", "French Toast", "Bagel with Cream Cheese"
#     ]
#     response = client.get('/breakfest')
#     data = response.get_json()
#     assert data["breakfest"] in valid_options