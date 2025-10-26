import unittest
from app import app
import random

class TestDoubleOrNothing(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_endpoint_exists(self):
        response = self.client.get("/double_or_nothing?amount=50")
        self.assertEqual(response.status_code, 200)

    def test_missing_amount_returns_400(self):
        response = self.client.get("/double_or_nothing")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_negative_amount_returns_400(self):
        response = self.client.get("/double_or_nothing?amount=-10")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_double_or_nothing_win(self):
        random.seed(1) 
        response = self.client.get("/double_or_nothing?amount=100")
        data = response.get_json()
        self.assertIn(data["outcome"], ["win", "lose"])
        if data["outcome"] == "win":
            self.assertEqual(data["new_balance"], 200.0)
        else:
            self.assertEqual(data["new_balance"], 0.0)

    def test_double_or_nothing_lose(self):
        random.seed(5)
        response = self.client.get("/double_or_nothing?amount=100")
        data = response.get_json()
        self.assertEqual(data["outcome"], "lose")
        self.assertEqual(data["new_balance"], 0.0)
        self.assertEqual(data["bet"], 100.0)
        self.assertIn("message", data)

    def test_response_format(self):
        random.seed(2)
        response = self.client.get("/double_or_nothing?amount=75")
        data = response.get_json()
        for key in ["bet", "outcome", "new_balance", "message"]:
            self.assertIn(key, data)

    def test_bet_value_echoed_back(self):
        random.seed(3)
        response = self.client.get("/double_or_nothing?amount=25")
        data = response.get_json()
        self.assertEqual(data["bet"], 25.0)