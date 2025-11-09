import unittest
import json
import sys


sys.path.append('..')
from app import app


class TestHockey_TeamsAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_teams_endpoint_structure(self):
        response = self.client.get('/hockey_teams')
        data = json.loads(response.data)
        self.assertIn("teams", data)
        self.assertIsInstance(data["teams"], list)
        self.assertGreater(len(data["teams"]), 0)
        self.assertTrue(all(isinstance(team, str) for team in data["teams"]))
