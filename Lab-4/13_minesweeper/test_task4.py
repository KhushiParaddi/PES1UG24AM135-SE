import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path

# Use the patched game.py in this solution folder and the project's board.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(1, str(Path(__file__).resolve().parent.parent))

from board import Board
from game import Minesweeper


class TestTask4Feedback(unittest.TestCase):
    def make_game(self, mines):
        game = Minesweeper("easy")
        game.board = Board(6, 6, len(mines))
        game.board.mines = set(mines)
        return game

    def run_commands(self, game, *commands):
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), \
             patch.object(game, "display"), \
             redirect_stdout(output):
            game.run()
        return output.getvalue()

    def test_normal_safe_reveal_feedback(self):
        game = self.make_game({(0, 0), (5, 5)})
        output = self.run_commands(game, "r 1 2", "q")
        self.assertIn("Safe cell revealed. Adjacent mines: 1.", output)

    def test_flood_fill_has_one_feedback_message(self):
        game = self.make_game({(0, 5), (5, 5)})
        # Keep one safe cell flagged so this test exercises flood-fill
        # without ending the game in a win.
        game.board.flags.add((5, 0))
        output = self.run_commands(game, "r 3 3", "q")
        self.assertIn("Flood-fill expanded to", output)
        self.assertEqual(output.count("Empty cell revealed."), 1)
        self.assertEqual(output.count("Flood-fill expanded to"), 1)
        self.assertGreater(len(game.board.revealed), 1)

    def test_mine_hit_feedback(self):
        game = self.make_game({(0, 0), (5, 5)})
        output = self.run_commands(game, "r 1 1")
        self.assertIn("BOOM! You hit a mine.", output)
        self.assertNotIn("Safe cell revealed.", output)

    def test_invalid_coordinates_feedback_and_state(self):
        game = self.make_game({(0, 0), (5, 5)})
        output = self.run_commands(game, "r 7 1", "q")
        self.assertIn("Outside the board.", output)
        self.assertEqual(game.board.revealed, set())
        self.assertEqual(game.board.flags, set())

    def test_flagged_cell_cannot_be_revealed(self):
        game = self.make_game({(0, 0), (5, 5)})
        output = self.run_commands(game, "f 1 2", "r 1 2", "q")
        self.assertIn("Cell is flagged. Unflag it before revealing.", output)
        self.assertNotIn((0, 1), game.board.revealed)
        self.assertIn((0, 1), game.board.flags)

    def test_repeated_reveal_feedback(self):
        game = self.make_game({(0, 0), (5, 5)})
        output = self.run_commands(game, "r 1 2", "r 1 2", "q")
        self.assertIn("Cell already revealed.", output)
        self.assertEqual(output.count("Safe cell revealed."), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
