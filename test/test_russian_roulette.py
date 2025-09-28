import unittest
from app import app

class TestRussianRoulette(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_endpoint_works(self):
        resp = self.client.get("/russian-roulette")
        self.assertEqual(resp.status_code, 200)

    def test_has_expected_keys(self):
        resp = self.client.get("/russian-roulette")
        data = resp.get_json()
        self.assertIn("chambers", data)
        self.assertIn("fired_chamber", data)
        self.assertIn("bullet_chamber", data)
        self.assertIn("outcome", data)
        self.assertIn("survived", data)

if __name__ == "__main__":
    unittest.main()
