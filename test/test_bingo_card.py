import unittest
from app import app
import random

class TestGenerateCard(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        response = self.client.get("/bingo")
        data = response.get_json()
        self.card = data["card"]

    def test_bingo_exists(self):
        response = self.client.get("/bingo")
        self.assertEqual(response.status_code, 200)

    def test_card_size(self):
        self.assertEqual(len(self.card), 25)

    def test_free_space(self):
        # index 12 is the center square
        self.assertEqual(self.card[12]["value"], "FREE")

    def test_no_duplicates(self):
        seen = set()
        for cell in self.card:
            val = cell["value"]
            if val == "FREE":
                continue
            self.assertNotIn(val, seen, f"Duplicate number {val} found")
            seen.add(val)

    def test_number_ranges(self):
        first = -14
        last = 1
        test_pass = True
        for i in range(len(self.card)):
            if i % 5 == 0:
                first += 15
                last += 15
            if i == 12 and self.card[i]["value"] == "FREE":
                continue
            if self.card[i]["value"] not in range(first, last + 1):
                test_pass = False
        self.assertEqual(test_pass, True)

    def test_marking_cells(self):
        # simulates 20 bingo pulls and marks card accordingly
        pulled_nums = random.sample(range(1,76),20)
        for i in pulled_nums:
            for cell in self.card:
                if i == cell["value"]:
                    cell["marked"] = True

        # tests if the right numbers are marked
        for cell in self.card:
            if cell["value"] == "FREE":
                self.assertTrue(cell["marked"],
                                f"Free space should always be marked")
                continue
            if cell["value"] in pulled_nums:
                self.assertTrue(cell["marked"],
                                f"Cell with value {cell['value']} should be marked True")
            else:
                self.assertFalse(cell["marked"],
                                f"Cell with value {cell['value']} should still be False")

