# import unittest
# from app import app

# class TestRollDice(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()

#     def test_valid_roll(self):
#         resp = self.client.get("/roll/6")
#         self.assertEqual(resp.status_code, 200)
#         data = resp.get_json()
#         self.assertEqual(data["sides"], 6)
#         self.assertTrue(1 <= data["result"] <= 6)

#     def test_large_sides_roll(self):
#         resp = self.client.get("/roll/20")
#         data = resp.get_json()
#         self.assertEqual(data["sides"], 20)
#         self.assertTrue(1 <= data["result"] <= 20)

#     def test_invalid_sides(self):
#         resp = self.client.get("/roll/1")
#         self.assertEqual(resp.status_code, 400)
#         self.assertIn("error", resp.get_json())

# # Tests for updated API code 
#     def test_roll_message_and_even_flag(self):
#         resp = self.client.get("/roll/6")
#         data = resp.get_json()
#         self.assertIn("message", data)
#         self.assertIn("is_even", data)
#         self.assertEqual(data["is_even"], data["result"] % 2 == 0)

#     def test_critical_fail_message(self):
#         # force sides=1 should hit invalid branch, so test sides=2 and catch result=1
#         resp = self.client.get("/roll/2")
#         data = resp.get_json()
#         if data["result"] == 1:
#             self.assertEqual(data["message"], "Critical Fail!")
#         else:
#             self.assertNotEqual(data["message"], "Critical Fail!")

#     def test_critical_success_message(self):
#         resp = self.client.get("/roll/2")
#         data = resp.get_json()
#         if data["result"] == 2:
#             self.assertEqual(data["message"], "Critical Success!")
#         else:
#             self.assertNotEqual(data["message"], "Critical Success!")


