import unittest
from src.board import Board

class TestBoard(unittest.TestCase):

    def test_board_is_empty_by_default(self):
        board = Board()
        pieces = []
        for piece in board.grid:
            if piece is not None:
                pieces.append(piece)

        self.assertEqual(len(pieces), 0)








