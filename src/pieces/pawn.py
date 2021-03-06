from .piece import Piece
from src.util.chess_constants import BLACK_COLOR, NORTH_TO_SOUTH_ORIENTATION, SOUTH_TO_NORTH_ORIENTATION, PAWN_SIGNATURE
import copy

class Pawn(Piece):
    SIGNATURE = PAWN_SIGNATURE

    BLACK_SYMBOL = "♟"
    WHITE_SYMBOL = "♙"

    NORTH_TO_SOUTH_POSITIONAL_MOVES = {(1, 0)}
    NORTH_TO_SOUTH_LEGAL_FIRST_MOVE = (2, 0)
    NORTH_TO_SOUTH_CONDITIONAL_ATTACKING_MOVES = {(1, -1), (1, 1)}
    NORTH_TO_SOUTH_STARTER_RANK = 1

    SOUTH_TO_NORTH_POSITIONAL_MOVES = {(-1, 0)}
    SOUTH_TO_NORTH_LEGAL_FIRST_MOVE = (-2, 0)
    SOUTH_TO_NORTH_CONDITIONAL_ATTACKING_MOVES = {(-1, 1), (-1, -1)}
    SOUTH_TO_NORTH_STARTER_RANK = 6

    def __init__(self, color):
        symbol = Pawn.BLACK_SYMBOL if color == BLACK_COLOR else Pawn.WHITE_SYMBOL
        orientation = NORTH_TO_SOUTH_ORIENTATION if color == BLACK_COLOR else SOUTH_TO_NORTH_ORIENTATION
        Piece.__init__(self, color, symbol, orientation)

    @staticmethod
    def get_signature():
        return Pawn.SIGNATURE

    @staticmethod
    def is_sliding_piece():
        return False

    @staticmethod
    def has_special_moves():
        return True

    def get_attacking_moves(self):
        return None

    def get_conditional_attacking_moves(self):
        if self.orientation == NORTH_TO_SOUTH_ORIENTATION:
            return Pawn.NORTH_TO_SOUTH_CONDITIONAL_ATTACKING_MOVES

        return Pawn.SOUTH_TO_NORTH_CONDITIONAL_ATTACKING_MOVES

    def get_positional_moves(self):
        if self.orientation == NORTH_TO_SOUTH_ORIENTATION:
            one_step_moves = copy.deepcopy(Pawn.NORTH_TO_SOUTH_POSITIONAL_MOVES)
            if not self.__made_first_move():
                one_step_moves.add(Pawn.NORTH_TO_SOUTH_LEGAL_FIRST_MOVE)

            return one_step_moves
        else:
            one_step_moves = copy.deepcopy(Pawn.SOUTH_TO_NORTH_POSITIONAL_MOVES)
            if not self.__made_first_move():
                one_step_moves.add(Pawn.SOUTH_TO_NORTH_LEGAL_FIRST_MOVE)

            return one_step_moves

    def switch_orientation(self):
        north = NORTH_TO_SOUTH_ORIENTATION
        south = SOUTH_TO_NORTH_ORIENTATION
        self.orientation = north if self.orientation == south else south

    def __made_first_move(self):
        current_rank = self.current_position[0]
        if self.orientation == NORTH_TO_SOUTH_ORIENTATION:
            return current_rank != Pawn.NORTH_TO_SOUTH_STARTER_RANK and self.number_of_moves == 0
        else:
            return current_rank != Pawn.SOUTH_TO_NORTH_STARTER_RANK and self.number_of_moves == 0







