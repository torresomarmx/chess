import unittest
from src.board import Board

class TestBoard(unittest.TestCase):

    def test_en_passant_on_next_move(self):
        board = Board.create_board_from_yaml_file("./en_passant_on_next_move.yaml")
        available_positions = board.get_available_positions_for_piece(
            board.get_piece_on_grid_position((3, 3))
        )

        self.assertTrue(
            len(available_positions) == 2 and (2, 3) in available_positions and (2, 4) in available_positions,
            "En passant not possible on next move!"
        )

