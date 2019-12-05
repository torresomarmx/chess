import unittest
from src.board import Board
from src.util.chess_constants import BLACK_COLOR

class TestNewGameBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.set_up_board_for_new_game()
        self.grid = self.board.grid

    def test_top_ranks_are_black_by_default(self):
        num_black_pieces = 0
        top_ranks = self.grid[:2]
        for rank in top_ranks:
            for piece in rank:
                if piece.color == BLACK_COLOR:
                    num_black_pieces += 1

        self.assertEqual(num_black_pieces, 16)

    def test_bottom_ranks_are_white_by_default(self):
        num_white_pieces = 0
        bottom_ranks = self.grid[-2:]
        for rank in bottom_ranks:
            for piece in rank:
                if piece.color == BLACK_COLOR:
                    num_white_pieces += 1

        self.assertEqual(num_white_pieces, 16)

    def test_pawn_are_in_place(self):
        pass

    def test_rooks_are_in_place(self):
        pass

    def test_knights_are_in_place(self):
        pass

    def test_bishops_are_in_place(self):
        pass

    def test_kings_are_in_place(self):
        pass

    def test_queens_are_in_place(self):
        pass

    def test_center_ranks_are_free(self):
        pass
