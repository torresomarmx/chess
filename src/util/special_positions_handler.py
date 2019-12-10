from src.pieces import Pawn, Queen
from src.util.chess_constants import *

class SpecialPositionsHandler:

    @classmethod
    def get_castling_position(cls, king, side, board):
        if king.get_signature() == KING_SIGNATURE:
            # TODO: also check that king is in first rank and that it is in one of two legal positions for king
            if king.number_of_moves == 0:
                attacked_positions = board.get_attacking_positions(BLACK_COLOR if king.color == WHITE_COLOR else WHITE_COLOR)
                if king.current_position in attacked_positions:
                    return None
                current_x, current_y = king.current_position
                rook_y_position = 0 if side == LEFT_SIDE else 7
                y_incrementer = -1 if side == LEFT_SIDE else 1
                search_y = current_y + y_incrementer
                positions_between_king_and_rook = {(current_x, search_y)}
                while search_y != rook_y_position and board.get_piece_on_grid_position((current_x, search_y)) is None:
                    search_y += y_incrementer
                    positions_between_king_and_rook.add((current_x, search_y))

                found_piece = board.get_piece_on_grid_position((current_x, search_y))
                if (search_y == rook_y_position and found_piece is not None and found_piece.get_signature() == ROOK_SIGNATURE
                        and found_piece.number_of_moves == 0 and all(pos not in attacked_positions for pos in positions_between_king_and_rook)):
                    return (current_x, current_y + (2 * y_incrementer))

        return None

    @classmethod
    def get_castling_positions(cls, king, board):
        castling_positions = set()
        if king.get_signature() == KING_SIGNATURE:
            sides = [LEFT_SIDE, RIGHT_SIDE]
            for side in sides:
                position = SpecialPositionsHandler.get_castling_position(king, side, board)
                if position is not None:
                    castling_positions.add(position)

        return castling_positions

    @classmethod
    def is_pawn_ready_for_promotion(cls, pawn, new_position):
        return (pawn.orientation == NORTH_TO_SOUTH_ORIENTATION and new_position[0] == 7) or \
            (pawn.orientation == SOUTH_TO_NORTH_ORIENTATION and new_position[0] == 0)

    @classmethod
    def get_promotion_piece(cls, color):
        return Queen(color)

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
            for special_move in pawn.get_conditional_attacking_moves():
                adjacent_piece = board.get_piece_on_grid_position((current_x_position, current_y_position + special_move[1]))
                if adjacent_piece is not None and adjacent_piece.current_position == opponent_pawn_position:
                    return (current_x_position + special_move[0], current_y_position + special_move[1])

        return None

    @classmethod
    def get_special_positions(cls, piece, position_type, board):
        if piece.get_signature() == PAWN_SIGNATURE:
            set_to_return = set()
            en_passant_position = cls.get_en_passant_position(piece, board)
            if en_passant_position is not None:
                set_to_return.add(en_passant_position)
            return set_to_return
        elif piece.get_signature() == KING_SIGNATURE:
            return cls.get_castling_positions(piece, board)