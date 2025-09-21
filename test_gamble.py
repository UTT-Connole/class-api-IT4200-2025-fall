# test/test_gamble.py
import unittest
from unittest.mock import patch

try:
    from app import create_app as _create_app
    app = _create_app()
except Exception:
    from app import app  # type: ignore

class TestGamble(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_gamble_rejects_non_positive_bet(self):
        r = self.client.post("/api/gamble", json={"bet": 0})
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())

    @patch("app.random.choice", return_value=True)
    def test_gamble_win_path(self, _mock_choice):
        bet = 50
        r = self.client.post("/api/gamble", json={"bet": bet})
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["result"], "win")
        self.assertEqual(data["original_bet"], bet)
        self.assertEqual(data["winnings"], bet * 2)

    @patch("app.random.choice", return_value=False)
    def test_gamble_lose_path(self, _mock_choice):
        bet = 40
        r = self.client.post("/api/gamble", json={"bet": bet})
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["result"], "lose")
        self.assertEqual(data["original_bet"], bet)
        self.assertEqual(data["winnings"], 0)
