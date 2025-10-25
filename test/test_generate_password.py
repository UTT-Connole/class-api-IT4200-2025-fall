import unittest
from app import app

class TestGeneratePassword(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def get_password(self, length=None, complexity=None):
        # Build query parameters dynamically
        params = []
        if length is not None:
            params.append(f"Length={length}")
        if complexity is not None:
            params.append(f"Complexity={complexity}")
        query_string = "?" + "&".join(params) if params else ""
        resp = self.client.get(f"/generatePassword{query_string}")
        return resp

    def test_default_password(self):
        resp = self.get_password()
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("password", data)
        self.assertEqual(len(data["password"]), 12)

    def test_custom_length(self):
        resp = self.get_password(length=16)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data["password"]), 16)

    def test_invalid_length(self):
        resp = self.get_password(length="abc")
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Length must be an integer")

    def test_basic_complexity(self):
        resp = self.get_password(length=20, complexity="basic")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        password = data["password"]
        self.assertTrue(all(c.islower() for c in password))

    def test_simple_complexity(self):
        resp = self.get_password(length=20, complexity="simple")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        password = data["password"]
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c.islower() for c in password))

    def test_complex_complexity(self):
        resp = self.get_password(length=50, complexity="complex")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        password = data["password"]
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "~!@#$%^&*()-_=+[{]}|;:,<.>/?"
                            for c in password))

    def test_invalid_complexity(self):
        resp = self.get_password(complexity="ultra")
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Choose a valid option: basic, simple, or complex.")

if __name__ == "__main__":
    unittest.main()
