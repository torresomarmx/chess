from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Knight(Piece):
    BLACK_SYMBOL = "♞"
    WHITE_SYMBOL = "♘"
    STARTER_Y_INDICES = (1, 6)

    ONE_STEP_MOVES = {(-2, 1), (-2, -1), (2, 1), (2, -1),
                      (-1, -2), (1, -2), (-1, 2), (1, 2)}

    def __init__(self, color):
        symbol = Knight.BLACK_SYMBOL if color == BLACK_COLOR else Knight.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return False

    def get_unique_attacking_moves(self):
        return None

    def get_one_step_moves(self):
        return Knight.ONE_STEP_MOVES

    def switch_orientation(self):
        pass