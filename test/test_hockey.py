# test /hockey endpoint
import unittest
import json
import sys

# not sure how other people are able to run their tests in this directory without appending '..' to get to app.py

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

    def test_returning_json(self):
        #check that output is json
        response = self.client.get('/api/hockey')
        self.assertEqual(response.content_type, 'application/json')

    def test_random_game_result_is_valid(self):
        #check that randomly returned game is in the list
        response = self.client.get('/api/hockey')
        data = json.loads(response.data)
        result = data.get("game_result")
        self.assertIn(result, self.valid_results)

    def test_api_hockey_status(self):
       #check that the page is returning 200
       response = self.client.get('/api/hockey')
       self.assertEqual(response.status_code, 200)
    
    def test_api_hockey_multiple_requests(self):
        #test 100 requests
        for n in range(100):
            response = self.client.get('/api/hockey')
            self.assertEqual(response.status_code, 200)

    def test_hockey_page_html(self):
        #check that html is working and configrued properly and check that '/hockey' is also returning 200
        response = self.client.get('/hockey')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn(b"<html", response.data)
        self.assertIn(b"Hockey", response.data)

