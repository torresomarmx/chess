import unittest
from src.board import Board
from src.util.chess_constants import BLACK_COLOR

class TestCheckmateInOneMove(unittest.TestCase):

    def test_checkmate_in_one_move(self):
        board = Board.create_board_from_yaml_file("./checkmate_on_next_move.yaml", True)
        queen = board.get_piece_on_grid_position((2,5))
        board.move_piece_to_new_position(queen,(1,6))
        self.assertTrue(
            board.is_in_checkmate(BLACK_COLOR),
            "Black is not in checkmate, when it should be "
        )