from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Bishop(Piece):
    BLACK_SYMBOL = "♝"
    WHITE_SYMBOL = "♗"
    STARTER_Y_INDICES = (2, 5)

    ONE_STEP_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1)}

    def __init__(self, color):
        symbol = Bishop.BLACK_SYMBOL if color == BLACK_COLOR else Bishop.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return True

    def get_unique_attacking_moves(self):
        return None

    def get_one_step_moves(self):
        return Bishop.ONE_STEP_MOVES

    def switch_orientation(self):
        pass

