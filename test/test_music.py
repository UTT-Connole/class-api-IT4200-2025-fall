# import unittest
# from app import app

# class MusicTestCase(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()

#     def test_single_genre(self):
#         response = self.client.get('/music')
#         self.assertEqual(response.status_code, 200)
#         data = response.get_json()
#         self.assertIn("recommendation", data)
#         self.assertIn(data["recommendation"], ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae'])

#     def test_multiple_genres(self):
#         response = self.client.get('/music?count=3')
#         self.assertEqual(response.status_code, 200)
#         data = response.get_json()
#         self.assertIn("recommendations", data)
#         self.assertEqual(len(data["recommendations"]), 3)
#         for genre in data["recommendations"]:
#             self.assertIn(genre, ['Rock', 'Jazz', 'Indie', 'Hip-Hop', 'Funk', 'Reggae'])