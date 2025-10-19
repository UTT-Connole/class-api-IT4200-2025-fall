import unittest
from app import app 

class TestBingoCheck(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def get_generated_card(self):
        resp = self.client.get("/bingo")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        return data["card"]

    def make_card(self, marked_indexes):
        card = self.get_generated_card()
        for i in marked_indexes:
            if 0 <= i < len(card):
                card[i]["marked"] = True
        return card

    def test_first_row_bingo(self):
        card = self.make_card([0,1,2,3,4]) 
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertTrue(resp.get_json()["bingo"])

    def test_no_row_bingo(self):
        card = self.make_card([0,1,2,3])  
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertFalse(resp.get_json()["bingo"])

    def test_first_column_bingo(self):
        card = self.make_card([0,5,10,15,20])
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertTrue(resp.get_json()["bingo"])

    def test_no_column_bingo(self):
        card = self.make_card([0,5,10,15]) 
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertFalse(resp.get_json()["bingo"])

    def test_downward_diagonal_bingo(self):
        card = self.make_card([0,6,12,18,24])
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertTrue(resp.get_json()["bingo"])

    def test_upward_diagonal_bingo(self):
        card = self.make_card([4,8,12,16,20])
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertTrue(resp.get_json()["bingo"])

    def test_no_diagonal_bingo(self):
        card = self.make_card([0,6,12,18])  
        resp = self.client.post("/bingo/check", json={"card": card})
        self.assertFalse(resp.get_json()["bingo"])

    def test_invalid_card_length(self):
        resp = self.client.post("/bingo/check", json={"card": [{"value": 1, "marked": True}]})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

if __name__ == "__main__":
    unittest.main()
