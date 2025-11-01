import unittest
import json
from app import app, generate_minesweeper_grid

class TestMinesweeper(unittest.TestCase):

    def count_mines(self, grid):
        return sum(cell == -1 for row in grid for cell in row)

    def test_beginner_grid_dimensions_and_mines(self):
        grid = generate_minesweeper_grid('beginner')
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
        self.assertEqual(self.count_mines(grid), 10)

    def test_intermediate_grid_dimensions_and_mines(self):
        grid = generate_minesweeper_grid('intermediate')
        self.assertEqual(len(grid), 16)
        self.assertEqual(len(grid[0]), 16)
        self.assertEqual(self.count_mines(grid), 40)

    def test_expert_grid_dimensions_and_mines(self):
        grid = generate_minesweeper_grid('expert')
        self.assertEqual(len(grid), 16)
        self.assertEqual(len(grid[0]), 30)
        self.assertEqual(self.count_mines(grid), 99)

    def test_invalid_difficulty_returns_error(self):
        result = generate_minesweeper_grid('invalid')
        self.assertIn('Error', result)

    def test_cell_values_valid(self):
        grid = generate_minesweeper_grid('beginner')
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                self.assertTrue(cell == -1 or 0 <= cell <= 8)

    def test_cell_numbers_match_mines(self):
        grid = generate_minesweeper_grid('beginner')
        rows, cols = len(grid), len(grid[0])

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == -1:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == -1:
                            count += 1

                self.assertEqual(grid[r][c], count)

    def test_flask_endpoint_returns_json(self):
        tester = app.test_client()
        response = tester.get('/minesweeper?difficulty=beginner')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('grid', data)
        self.assertEqual(len(data['grid']), 9)
