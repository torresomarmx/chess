from src.util.chess_constants import BLACK_COLOR
from .piece import Piece

class Knight(Piece):
    BLACK_SYMBOL = "♞"
    WHITE_SYMBOL = "♘"
    STARTER_Y_INDICES = (1, 6)

    POSITIONAL_MOVES = {(-2, 1), (-2, -1), (2, 1), (2, -1),
                        (-1, -2), (1, -2), (-1, 2), (1, 2)}

    def __init__(self, color):
        symbol = Knight.BLACK_SYMBOL if color == BLACK_COLOR else Knight.WHITE_SYMBOL
        Piece.__init__(self, color, symbol, None)

    @staticmethod
    def is_sliding_piece():
        return False

    def get_attacking_moves(self):
        return Knight.POSITIONAL_MOVES

    def get_conditional_attacking_moves(self):
        return None

    def get_positional_moves(self):
        return Knight.POSITIONAL_MOVES

    def switch_orientation(self):
        pass