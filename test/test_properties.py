import unittest

try:
    from app import create_app as _create_app
    app = _create_app()
except Exception:
    from app import app  

class TestProperties(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_chernobyl_properties(self):
        r = self.client.get("/api/chernobyl/properties")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("message", data)
        self.assertIn("properties", data)
        self.assertIsInstance(data["properties"], list)
        self.assertGreaterEqual(len(data["properties"]), 2)
        first = data["properties"][0]
        for k in ("id", "address", "price", "radiation_level", "amenities", "warnings"):
            self.assertIn(k, first)

    def test_mars_properties(self):
        r = self.client.get("/api/mars/properties")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("message", data)
        self.assertIn("properties", data)
        self.assertIsInstance(data["properties"], list)
        self.assertGreaterEqual(len(data["properties"]), 2)
        first = data["properties"][0]
        for k in ("id", "address", "price", "oxygen_level", "amenities", "warnings"):
            self.assertIn(k, first)
