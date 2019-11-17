from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Queen(Piece):
    BLACK_SYMBOL = "♛"
    WHITE_SYMBOL = "♕"
    DEFAULT_STARTER_Y_INDEX = 3

    ONE_STEP_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)}

    def __init__(self, color):
        symbol = Queen.BLACK_SYMBOL if color == BLACK_COLOR else Queen.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return True

    def get_unique_attacking_moves(self):
        return None

    def get_one_step_moves(self):
        return Queen.ONE_STEP_MOVES

    def switch_orientation(self):
        pass
