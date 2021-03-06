from src.util.chess_constants import BLACK_COLOR, ROOK_SIGNATURE
from .piece import Piece

class Rook(Piece):
    SIGNATURE = ROOK_SIGNATURE

    BLACK_SYMBOL = "♜"
    WHITE_SYMBOL = "♖"
    STARTER_Y_INDICES = (0, 7)

    POSITIONAL_MOVES = {(-1, 0), (1, 0), (0, 1), (0, -1)}

    def __init__(self, color):
        symbol = Rook.BLACK_SYMBOL if color == BLACK_COLOR else Rook.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def get_signature():
        return Rook.SIGNATURE

    @staticmethod
    def is_sliding_piece():
        return True

    @staticmethod
    def has_special_moves():
        return False

    def get_attacking_moves(self):
        return Rook.POSITIONAL_MOVES

    def get_conditional_attacking_moves(self):
        return None

    def get_positional_moves(self):
        return Rook.POSITIONAL_MOVES

    def switch_orientation(self):
        pass

