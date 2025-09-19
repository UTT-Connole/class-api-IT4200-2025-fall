import unittest
from app import generate_wizard_name

class TestWizardNameGenerator(unittest.TestCase):

    def test_returns_string(self):
        """Test that the output is a string."""
        name = generate_wizard_name()
        self.assertIsInstance(name, str)

    def test_contains_title_and_name(self):
        """Test that the name has two parts: title and name."""
        name = generate_wizard_name()
        parts = name.split()
        self.assertEqual(len(parts), 2)

    def test_title_is_valid(self):
        """Test that the title is one of the expected wizard titles."""
        valid_titles = ['Archmage', 'Sorcerer', 'Seer', 'Mystic', 'Enchanter', 'Spellbinder']
        title = generate_wizard_name().split()[0]
        self.assertIn(title, valid_titles)

    def test_name_is_capitalized(self):
        """Test that the wizard name part starts with a capital letter."""
        wizard_name = generate_wizard_name().split()[1]
        self.assertTrue(wizard_name[0].isupper())

    def test_multiple_names_are_different(self):
        """Test that two generated names are not identical."""
        name1 = generate_wizard_name()
        name2 = generate_wizard_name()
        self.assertNotEqual(name1, name2)

if __name__ == '__main__':
    unittest.main()



