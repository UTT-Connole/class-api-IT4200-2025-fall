import unittest
import json
import sys


sys.path.append('..')
from app import app


class TestHockeyAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.valid_results = [
            "Flames 3 - 2 Canuks",
            "Panthers 1 - 4 Mammoth",
            "Sharks 6 - 5 Penguins",
            "Wild 2 - 0 Maple Leafs",
            "Jets 6 - 3 Blues",
            "Oilers 5 - 2 Canuks",
            "Avalanche 1 - 4 Senators",
            "Bruins 6 - 2 Penguins",
            "Islanders 2 - 3 Rangers",
            "Jets 0 - 3 Stars"
        ]
    def test_hockey_lists_exist(self):
        import app  
        self.assertTrue(hasattr(app, "hockey_results1"))
        self.assertTrue(hasattr(app, "hockey_results2"))
        self.assertGreater(len(app.hockey_results1), 0)
        self.assertGreater(len(app.hockey_results2), 0)

    def test_returning_json(self):
        response = self.client.get('/hockey_matchup')
        self.assertEqual(response.content_type, 'application/json')

    def test_random_game_result_is_valid(self):
        response = self.client.get('/hockey_matchup')
        data = json.loads(response.data)

        team1 = data.get("team1")
        score1 = data.get("score1")
        score2 = data.get("score2")
        team2 = data.get("team2")

        result = f"{team1} {score1} - {score2} {team2}"
        self.assertIn(result, self.valid_results)
    
    def test_api_hockey_status(self):
       response = self.client.get('/hockey_matchup')
       self.assertEqual(response.status_code, 200)
    
    def test_hockey_page_html(self):
        response = self.client.get('/hockey')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn(b"<html", response.data)
        self.assertIn(b"Hockey", response.data)

    def test_hockey_response_keys(self):
        response = self.client.get('/hockey_matchup')
        data = json.loads(response.data)
        expected_keys = {"team1", "score1", "score2", "team2"}
        self.assertTrue(expected_keys.issubset(data.keys()), f'Missing keys in response: /hockey_matchup not returning {"team1", "score1", "score2", "team2"}')

    def test_api_hockey(self):
        response = self.client.get('/api/hockey')
        self.assertEqual(response.status_code, 404)

