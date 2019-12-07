from src.util.chess_constants import BLACK_COLOR, KING_SIGNATURE
from .piece import Piece

class King(Piece):
    SIGNATURE = KING_SIGNATURE

    BLACK_SYMBOL = "♚"
    WHITE_SYMBOL = "♔"
    DEFAULT_STARTER_Y_INDEX = 4

    POSITIONAL_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1),
                        (-1, 0), (1, 0), (0, -1), (0, 1)}

    def __init__(self, color):
        symbol = King.BLACK_SYMBOL if color == BLACK_COLOR else King.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def get_signature():
        return King.SIGNATURE

    @staticmethod
    def is_sliding_piece():
        return False

    @staticmethod
    def has_special_moves():
        return True

    def get_attacking_moves(self):
        return King.POSITIONAL_MOVES

    def get_conditional_attacking_moves(self):
        return None

    def get_positional_moves(self):
        return King.POSITIONAL_MOVES

    def switch_orientation(self):
        pass