# import unittest
# try:
#     from app import create_app as _create_app
#     app = _create_app()
# except Exception:
#     from app import app  # type: ignore

# class TestPropertiesLimit(unittest.TestCase):
#     def setUp(self):
#         self.c = app.test_client()

#     def test_chernobyl_limit_1(self):
#         r = self.c.get("/api/chernobyl/properties?limit=1")
#         self.assertEqual(r.status_code, 200)
#         props = r.get_json()["properties"]
#         self.assertEqual(len(props), 1)

#     def test_mars_limit_too_big_clamps(self):
#         r = self.c.get("/api/mars/properties?limit=99")
#         self.assertEqual(r.status_code, 200)
#         props = r.get_json()["properties"]
#         self.assertGreaterEqual(len(props), 1)
#         self.assertLessEqual(len(props), 2)  # list has only 2 in sample

#     def test_chernobyl_limit_bad_type(self):
#         r = self.c.get("/api/chernobyl/properties?limit=abc")
#         self.assertEqual(r.status_code, 400)
#         self.assertIn("error", r.get_json())
