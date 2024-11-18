import unittest
import numpy as np
from Board import Board

class TestHistoryValidation(unittest.TestCase):

    def setUp(self):
        cell_features = [("H", int), ("PP", int), ("D", int), ("VS", float)]
        self.board = Board(dimX=3, dimY=3, cell_features=cell_features, alpha=0.1, beta=0.5, gamma=0.2, init_random=False)

        # Initialize cells with a controlled state
        for x in range(3):
            for y in range(3):
                self.board.set_cell_feature(x, y, "H", 1)
                self.board.set_cell_feature(x, y, "PP", 2)
                self.board.set_cell_feature(x, y, "D", 3)
                self.board.set_cell_feature(x, y, "VS", 0.5)

    def test_history_updates_correctly(self):
        self.assertEqual(len(self.board.history), 0)

        for i in range(3):
            self.board.update()
            self.assertEqual(len(self.board.history), i + 1)
            np.testing.assert_array_equal(self.board.history[-1], self.board.cells)
            self.assertIsNot(self.board.history[-1], self.board.cells)

    def test_terminate_adds_final_state(self):
        self.board.update()
        self.board.terminate()
        self.assertEqual(len(self.board.history), 2)
        np.testing.assert_array_equal(self.board.history[-1], self.board.cells)

    def test_terminate_without_updates(self):
        self.board.terminate()
        self.assertEqual(len(self.board.history), 1)
        np.testing.assert_array_equal(self.board.history[-1], self.board.cells)

    def test_history_starts_empty_and_grows(self):
        self.assertEqual(len(self.board.history), 0)
        self.board.update()
        self.assertEqual(len(self.board.history), 1)
        self.board.update()
        self.assertEqual(len(self.board.history), 2)
        self.board.terminate()
        self.assertEqual(len(self.board.history), 3)


if __name__ == "__main__":
    unittest.main()
