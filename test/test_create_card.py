import unittest
from app import app, generate_bingo_card


class TestCreateCard(unittest.TestCase):
    def setUp(self):
        self.card = generate_bingo_card()

    def test_create_card_exists(self):
        self.assertEqual(set(self.card.keys()), {"B", "I", "N", "G", "O"})

    def test_column_lengths(self):
        for nums in self.card.values():
            self.assertEqual(len(nums), 5)

    def test_free_space(self):
        self.assertEqual(self.card["N"][2], "FREE")

    def test_no_duplicates(self):
        for col, nums in self.card.items():
            filtered = [n for n in nums if n != "FREE"]
            self.assertEqual(len(filtered), len(set(filtered)))

    def test_numberranges(self):
        ranges = {
            "B": range(1, 16),
            "I": range(16, 31),
            "N": range(31, 46),
            "G": range(46, 61),
            "O": range(61, 76)
        }
        for col, nums in self.card.items():
            for i, num in enumerate(nums):
                if col == "N" and i == 2:
                    continue
            self.assertIn(num, ranges[col])