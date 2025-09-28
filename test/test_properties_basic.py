# import unittest
# try:
#     from app import create_app as _create_app
#     app = _create_app()
# except Exception:
#     from app import app  # type: ignore

# class TestPropertiesBasic(unittest.TestCase):
#     def setUp(self):
#         self.c = app.test_client()

#     def test_chernobyl_basic(self):
#         r = self.c.get("/api/chernobyl/properties")
#         self.assertEqual(r.status_code, 200)
#         data = r.get_json()
#         self.assertIn("message", data)
#         self.assertIsInstance(data.get("properties"), list)
#         self.assertGreaterEqual(len(data["properties"]), 2)

#     def test_mars_basic(self):
#         r = self.c.get("/api/mars/properties")
#         self.assertEqual(r.status_code, 200)
#         data = r.get_json()
#         self.assertIn("message", data)
#         self.assertIsInstance(data.get("properties"), list)
#         self.assertGreaterEqual(len(data["properties"]), 2)
