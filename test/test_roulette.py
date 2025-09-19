import unittest
import json
from app import app

class RouletteTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()

    def test_roulette_status_code(self):
        """Test that the /roulette endpoint returns a 200 OK status"""
        response = self.client.get('/roulette')
        self.assertEqual(response.status_code, 200)

    def test_roulette_json_structure(self):
        """Test that the response contains the correct keys"""
        response = self.client.get('/roulette')
        data = json.loads(response.data)

        self.assertIn('spin', data)
        self.assertIn('color', data)
        self.assertIn('parity', data)

    def test_roulette_spin_range(self):
        """Test that the spin is between 0 and 36"""
        response = self.client.get('/roulette')
        data = json.loads(response.data)

        self.assertGreaterEqual(data['spin'], 0)
        self.assertLessEqual(data['spin'], 36)

    def test_roulette_color_valid(self):
        """Test that the color is one of red, black, or green"""
        response = self.client.get('/roulette')
        data = json.loads(response.data)

        self.assertIn(data['color'], ['red', 'black', 'green'])

    def test_roulette_parity_valid(self):
        """Test that the parity matches the spin result"""
        response = self.client.get('/roulette')
        data = json.loads(response.data)

        if data['spin'] == 0:
            self.assertEqual(data['parity'], 'none')
        elif data['spin'] % 2 == 0:
            self.assertEqual(data['parity'], 'even')
        else:
            self.assertEqual(data['parity'], 'odd')

if __name__ == '__main__':
    unittest.main()
