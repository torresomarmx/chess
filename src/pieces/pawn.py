from .piece import Piece

class Pawn(Piece):
    BLACK_SYMBOL = "♟"
    WHITE_SYMBOL = "♙"

    TOP_TO_BOTTOM_NATURAL_MOVES = ()
    TOP_TO_BOTTOM_UNIQUE_ATTACKING_MOVES  = ()
    BOTTOM_TO_TOP_NATURAL_MOVES = ()
    BOTTOM_TO_TOP_UNIQUE_ATTACKING_MOVES = ()

    def __init__(self, x_position, y_position, color):
        Piece.__init__(self, x_position, y_position, color)

    def white_symbol(cls):
        return cls.WHITE_SYMBOL

    def black_symbol(cls):
        return cls.BLACK_SYMBOL

    def is_sliding_piece(cls):
        return False

    def unique_attacking_moves(cls):
        return cls.

    def potential_moves(self, orientation):






