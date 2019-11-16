from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Rook(Piece):
    BLACK_SYMBOL = "♜"
    WHITE_SYMBOL = "♖"
    STARTER_Y_INDICES = (0, 7)

    def __init__(self, color):
        symbol = Rook.BLACK_SYMBOL if color == BLACK_COLOR else Rook.WHITE_SYMBOL
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

