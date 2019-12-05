from src.util.chess_constants import BLACK_COLOR, QUEEN_SIGNATURE
from .piece import Piece

class Queen(Piece):
    SIGNATURE = QUEEN_SIGNATURE

    BLACK_SYMBOL = "♛"
    WHITE_SYMBOL = "♕"
    DEFAULT_STARTER_Y_INDEX = 3

    POSITIONAL_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1),
                        (-1, 0), (1, 0), (0, -1), (0, 1)}

    def __init__(self, color):
        symbol = Queen.BLACK_SYMBOL if color == BLACK_COLOR else Queen.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def get_signature():
        return Queen.SIGNATURE

    @staticmethod
    def is_sliding_piece():
        return True

    def get_attacking_moves(self):
        return Queen.POSITIONAL_MOVES

    def get_conditional_attacking_moves(self):
        return None

    def get_positional_moves(self):
        return Queen.POSITIONAL_MOVES

    def switch_orientation(self):
        pass

    def get_special_moves(self):
        return None
