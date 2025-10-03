import unittest
from app import app

class TestPlantBattle(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_defaults_work(self):
        resp = self.client.get("/plant-battle")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("chosen_plant", data)
        self.assertIn("winner", data)
        self.assertIn("winnings", data)

    def test_invalid_bet_returns_error(self):
        resp = self.client.get("/plant-battle?bet=0&plant=Cactus")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_plant_returns_error(self):
        resp = self.client.get("/plant-battle?bet=10&plant=OakTree")
        self.assertEqual(resp.status_code, 400)

    def test_valid_request_returns_result(self):
        resp = self.client.get("/plant-battle?bet=10&plant=Cactus")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("winner", data)
        self.assertIn("result", data)
        self.assertIn("winnings", data)

    def test_outcome_is_win_or_lose(self):
        resp = self.client.get("/plant-battle?bet=5&plant=Venus%20Flytrap")
        data = resp.get_json()
        self.assertIn(data["result"], ["win", "lose"])

if __name__ == "__main__":
    unittest.main()
