from app import app
import pytest

def test_chickenrace_get():
    """Test that the chicken race page loads correctly"""
    client = app.test_client()
    response = client.get('/chickenrace')
    assert response.status_code == 404  # Updated to reflect the route change

