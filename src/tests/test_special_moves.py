import unittest
from src.board import Board
from src.util.special_positions_handler import SpecialPositionsHandler

class TestBoard(unittest.TestCase):

    def test_en_passant_on_next_move(self):
        board = Board.create_board_from_yaml_file("./en_passant_on_next_move.yaml", True)
        available_positions = board.get_available_positions_for_piece(
            board.get_piece_on_grid_position((3, 3))
        )

        self.assertTrue(
            len(available_positions) == 2 and (2, 3) in available_positions and (2, 4) in available_positions,
            "En passant not possible on next move!"
        )

    def test_en_passant_no_longer_available(self):
        board = Board.create_board_from_yaml_file("./en_passant_no_longer_available.yaml", True)
        available_positions = board.get_available_positions_for_piece(
            board.get_piece_on_grid_position((3, 3))
        )

        self.assertTrue(
            len(available_positions) == 1 and (2, 3) in available_positions,
            "Pawn should only have 1 available move"
        )

    def test_pawn_promotion_on_next_move(self):
        board = Board.create_board_from_yaml_file("./checkmate_on_next_move.yaml", True)
        pawn = board.get_piece_on_grid_position((1,0))
        self.assertTrue(SpecialPositionsHandler.is_pawn_ready_for_promotion(pawn), "Pawn is not ready for promotion")

    def test_castling_moves_available_on_both_sides(self):
        board = Board.create_board_from_yaml_file("./checkmate_on_next_move.yaml", True)
        king = board.get_piece_on_grid_position((7, 4))
        available_positions = board.get_available_positions_for_piece(king)
        self.assertTrue(
            (7, 2) in available_positions and (7, 6) in available_positions,
            "Castling position not available 1 or more sides"
        )



