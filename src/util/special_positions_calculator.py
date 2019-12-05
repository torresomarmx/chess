from src.pieces import Pawn
from src.util.chess_constants import BLACK_COLOR, NORTH_TO_SOUTH_ORIENTATION, SOUTH_TO_NORTH_ORIENTATION, PAWN_SIGNATURE

class SpecialPositionsCalculator:

    @classmethod
    def get_en_passant_position(cls, pawn, board):
        current_x_position, current_y_position = pawn.current_position
        # first check if pawn is in either 4th or 5th rank. These are the only ranks where en passant move is possible
        north_to_south_condition = pawn.orientation == NORTH_TO_SOUTH_ORIENTATION and current_x_position == 4
        south_to_north_condition = pawn.orientation == SOUTH_TO_NORTH_ORIENTATION and current_x_position == 3
        if north_to_south_condition or south_to_north_condition:
            if len(board.moves_tracker.all_moves) == 0:
                return None

            # get previous opponent move using MovesTracker from Board
            opponent_previous_move = None
            if pawn.color == BLACK_COLOR:
                opponent_previous_move = board.moves_tracker.white_moves[-1]
            else:
                opponent_previous_move = board.moves_tracker.black_moves[-1]

            # check if opponent moved pawn, and if opponent pawn moved 2 positions forward on first move
            piece_displacement = abs(opponent_previous_move.old_position[0] - opponent_previous_move.new_position[0])
            opponent_pawn_position = None
            if opponent_previous_move.piece_signature == PAWN_SIGNATURE and piece_displacement == 2:
                opponent_pawn_position = opponent_previous_move.new_position
            else:
                return None

            # check if pawn has an opponent pawn on either it's left or right side
            for special_move in pawn.get_special_moves():
                adjacent_piece = board.get_piece_on_grid_position((current_x_position, current_y_position + special_move[1]))
                if adjacent_piece is not None and adjacent_piece.current_position == opponent_pawn_position:
                    return (current_x_position + special_move[0], current_y_position + special_move[1])

        return None

    @classmethod
    def get_special_positions(cls, piece, position_type, board):
        if piece.get_signature() == PAWN_SIGNATURE:
            en_passant_position = cls.get_en_passant_position(piece, board)
            set_to_return = set()
            if en_passant_position is not None:
                set_to_return.add(en_passant_position)
            return set_to_return