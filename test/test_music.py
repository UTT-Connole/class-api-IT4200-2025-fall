import unittest
from app import app

GENRES = ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae', 'Psychedelic', 'Surf']


class MusicTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_single_genre(self):
        response = self.client.get('/music')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendation", data)
        self.assertIn(data["recommendation"], ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae', 'Psychedelic', "Surf"])

    def test_multiple_genres(self):
        response = self.client.get('/music?count=3')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendations", data)
        self.assertEqual(len(data["recommendations"]), 3)
        for genre in data["recommendations"]:
            self.assertIn(genre, ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae', 'Psychedelic', 'Surf'])

    def test_count_one(self):
        response = self.client.get('/music?count=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendation", data)
        self.assertIn(data["recommendation"], GENRES)

    def test_count_more_than_available(self):
        response = self.client.get('/music?count=20')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendations", data)
        self.assertEqual(set(data["recommendations"]), set(GENRES))

    def test_count_zero(self):
        response = self.client.get('/music?count=0')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recommendation", data)
        self.assertIn(data["recommendation"], GENRES)

    def test_valid_genre(self):
        response = self.client.get('/music?genre=Jazz')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["recommendation"], "Jazz")

    def test_invalid_genre(self):
        response = self.client.get('/music?genre=Blues')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)