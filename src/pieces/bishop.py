from src.util.chess_constants import BLACK_COLOR, BISHOP_SIGNATURE
from .piece import Piece

class Bishop(Piece):
    SIGNATURE = BISHOP_SIGNATURE

    BLACK_SYMBOL = "♝"
    WHITE_SYMBOL = "♗"
    STARTER_Y_INDICES = (2, 5)

    POSITIONAL_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1)}

    def __init__(self, color):
        symbol = Bishop.BLACK_SYMBOL if color == BLACK_COLOR else Bishop.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def get_signature():
        return Bishop.SIGNATURE

    @staticmethod
    def is_sliding_piece():
        return True

    @staticmethod
    def has_special_moves():
        return False

    def get_attacking_moves(self):
        return Bishop.POSITIONAL_MOVES

    def get_conditional_attacking_moves(self):
        return None

    def get_positional_moves(self):
        return Bishop.POSITIONAL_MOVES

    def switch_orientation(self):
        pass

