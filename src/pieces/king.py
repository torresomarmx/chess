from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class King(Piece):
    BLACK_SYMBOL = "♚"
    WHITE_SYMBOL = "♔"
    DEFAULT_STARTER_Y_INDEX = 4

    ONE_STEP_MOVES = {(-1, 1), (-1, -1), (1, 1), (1, -1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)}

    def __init__(self, color):
        symbol = King.BLACK_SYMBOL if color == BLACK_COLOR else King.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return False

    def get_unique_attacking_moves(self):
        return None

    def get_one_step_moves(self):
        return King.ONE_STEP_MOVES

    def switch_orientation(self):
        pass