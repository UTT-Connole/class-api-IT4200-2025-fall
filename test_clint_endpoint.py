import unittest
from unittest.mock import patch
from app import spin_wheel, get_payout  

class TestRouletteGame(unittest.TestCase):

    def test_spin_wheel_output_range(self):
        """Test that spin_wheel returns a number between 0 and 36 and a valid color."""
        for _ in range(100):
            number, color = spin_wheel()
            self.assertIn(number, range(0, 37))
            self.assertIn(color, ['Red', 'Black', 'Green'])

    def test_payout_number_win(self):
        """Test correct payout for winning number bet."""
        result = get_payout('number', 17, 17, 'Red')
        self.assertEqual(result, 35)

    def test_payout_number_loss(self):
        """Test payout for losing number bet."""
        result = get_payout('number', 5, 17, 'Black')
        self.assertEqual(result, -1)

    def test_payout_color_win(self):
        """Test correct payout for winning color bet."""
        result = get_payout('color', 'Red', 2, 'Red')
        self.assertEqual(result, 1)

    def test_payout_color_loss(self):
        """Test payout for losing color bet."""
        result = get_payout('color', 'Black', 2, 'Red')
        self.assertEqual(result, -1)

    def test_edge_case_zero_green(self):
        """Test that betting on color loses when wheel lands on green (0)."""
        result = get_payout('color', 'Red', 0, 'Green')
        self.assertEqual(result, -1)

if __name__ == '__main__':
    unittest.main()


