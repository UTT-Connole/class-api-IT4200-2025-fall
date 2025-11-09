import unittest
import json
import sys


sys.path.append('..')
from app import app


class Testgill(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
   
    def test_gill_endpoint_does_not_exist(self):
       response = self.client.get('/gill')
       self.assertEqual(response.status_code, 404)

