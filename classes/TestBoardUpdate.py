import unittest
import numpy as np
from unittest.mock import patch
from Board import Board

class TestBoardUpdate(unittest.TestCase):

    def setUp(self):
        # Define the structure of cell features and initialize the Board
        cell_features = [("H", int), ("PP", int), ("D", int), ("VS", float)]
        self.board = Board(dimX=3, dimY=3, cell_features=cell_features, alpha=0.1, beta=0.5, gamma=0.2, init_random=False)
        # Manually set the initial state of the board for testing
        self.board.cells = np.array([
            [(1, 1, 1, 0.5), (0, 2, 2, 0.8), (1, 3, 3, 0.2)],
            [(0, 2, 1, 0.7), (1, 4, 2, 0.3), (0, 3, 3, 0.1)],
            [(1, 1, 0, 0.9), (0, 2, 1, 0.4), (1, 5, 3, 0.6)],
        ], dtype=self.board.cell_features)

    def test_update_history(self):
        self.board.update()
        self.assertEqual(len(self.board.history), 1)
        # Validate the update process without assuming changes
        for x in range(self.board.dimX):
            for y in range(self.board.dimY):
                original_cell = self.board.history[0][x, y]
                updated_cell = self.board.cells[x, y]
                self.assertEqual(original_cell["H"], updated_cell["H"])  # Income level should stay the same
                self.assertGreaterEqual(updated_cell["PP"], original_cell["PP"])  # PP should not decrease
                self.assertGreaterEqual(updated_cell["D"], 0)
                self.assertLessEqual(updated_cell["D"], 3)

    @patch.object(Board, 'property_price_update')
    @patch.object(Board, 'desirability_update')
    @patch.object(Board, 'vacancy_update')
    def test_cell_updates(self, mock_vacancy_update, mock_desirability_update, mock_property_price_update):
        # Adjust mocks for structured arrays
        mock_property_price_update.side_effect = lambda cell, n: np.array(
            (cell["H"], cell["PP"] + 1, cell["D"], cell["VS"]),
            dtype=self.board.cell_features
        )
        mock_desirability_update.side_effect = lambda cell, n: np.array(
            (cell["H"], cell["PP"], cell["D"] + 1, cell["VS"]),
            dtype=self.board.cell_features
        )
        mock_vacancy_update.side_effect = lambda cell, n: np.array(
            (cell["H"], cell["PP"], cell["D"], 1.0),
            dtype=self.board.cell_features
        )

        self.board.update()
        for x in range(self.board.dimX):
            for y in range(self.board.dimY):
                cell = self.board.get_cell(x, y)
                self.assertEqual(cell["PP"], self.board.history[0][x, y]["PP"] + 1)
                self.assertEqual(cell["D"], self.board.history[0][x, y]["D"] + 1)
                self.assertEqual(cell["VS"], 1.0)

    def test_neighborhood_logic(self):
        neighborhood = self.board.get_neighborhood(1, 1)
        expected_neighborhood = np.array([
            [(1, 1, 1, 0.5), (0, 2, 2, 0.8), (1, 3, 3, 0.2)],
            [(0, 2, 1, 0.7), (1, 4, 2, 0.3), (0, 3, 3, 0.1)],
            [(1, 1, 0, 0.9), (0, 2, 1, 0.4), (1, 5, 3, 0.6)],
        ], dtype=self.board.cell_features)
        np.testing.assert_array_equal(neighborhood, expected_neighborhood)

    def test_cells_update_properly(self):
        self.board.update()
        for x in range(self.board.dimX):
            for y in range(self.board.dimY):
                updated_cell = self.board.get_cell(x, y)
                original_cell = self.board.history[0][x, y]

                self.assertGreaterEqual(updated_cell["PP"], original_cell["PP"])
                self.assertGreaterEqual(updated_cell["D"], 0)
                self.assertLessEqual(updated_cell["D"], 3)
                self.assertGreaterEqual(updated_cell["VS"], 0.0)
                self.assertLessEqual(updated_cell["VS"], 1.0)
