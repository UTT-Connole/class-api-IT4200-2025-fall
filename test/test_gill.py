import unittest
import json
import sys

# not sure how other people are able to run their tests in this directory without appending '..' to get to app.py

sys.path.append('..')
from app import app


class Testgill(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
   
    def test_gill_endpoint_does_not_exist(self):
       #check that the page does not exist
       response = self.client.get('/gill')
       self.assertEqual(response.status_code, 404)

