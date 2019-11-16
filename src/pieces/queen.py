from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Queen(Piece):
    BLACK_SYMBOL = "♛"
    WHITE_SYMBOL = "♕"
    DEFAULT_STARTER_Y_INDEX = 3

    def __init__(self, color):
        symbol = Queen.BLACK_SYMBOL if color == BLACK_COLOR else Queen.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return False

    def get_unique_attacking_moves(self):
        return {}

    def get_one_step_moves(self):
        return {}

    def switch_orientation(self):
        pass
