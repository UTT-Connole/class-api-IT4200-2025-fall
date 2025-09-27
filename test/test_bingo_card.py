import unittest
from app import app, generate_bingo_card


class TestCreateCard(unittest.TestCase):
    def setUp(self):
        self.card = generate_bingo_card()

    def test_columns_exist(self):
        expected = {"B", "I", "N", "G", "O"}
        self.assertEqual(set(self.card.keys()), expected)

    def test_column_lengths(self):
        for column in self.card.values():
            self.assertEqual(len(column), 5)

    def test_free_space(self):
        self.assertEqual(self.card["N"][2], "FREE")

    def test_no_duplicates(self):
        for values in self.card.values():
            seen = []
            for num in values:
                if num == "FREE":
                    continue
                self.assertNotIn(num, seen, f"Duplicate number {num} found")
                seen.append(num)

    def test_number_ranges(self):
        ranges = {
            "B": (1, 15),
            "I": (16, 30),
            "N": (31, 45),
            "G": (46, 60),
            "O": (61, 75)
        }

        for col in "BINGO":
            start, end = ranges[col]
            for num in self.card[col]:
                if num == "FREE":
                    continue
                self.assertTrue(start <= num <= end)