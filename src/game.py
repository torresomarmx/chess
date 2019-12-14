from src.util.chess_constants import *
from src.util.moves_tracker import MovesTracker
from src.util.special_positions_handler import SpecialPositionsHandler
from src.board import Board

class Game:

    def __init__(self, board = None, color_to_move = None):
        if board is None:
            self.board = Board(MovesTracker())
            self.board.set_up_board_for_new_game()
            self.color_to_move = WHITE_COLOR
        else:
            self.board = board
            self.color_to_move = color_to_move

    def start(self):
        while True:
            self.board.display()
            opposite_color = BLACK_COLOR if self.color_to_move == WHITE_COLOR else WHITE_COLOR
            attacked_positions = self.board.get_attacking_positions(opposite_color)
            king = self.board.get_king(self.color_to_move)
            if king.current_position in attacked_positions:
                in_check_available_positions = self.board.get_available_positions(self.color_to_move, True)
                if len(in_check_available_positions) == 0:
                    print("Game over. Checkmate!")
                    break
                else:
                    print(self.color_to_move + " is in check")
                    self.__handle_new_move_for_player(self.color_to_move, in_check_available_positions)
            else:
                available_positions = self.board.get_available_positions(self.color_to_move, False)
                if len(available_positions) == 0:
                    print("Game over. Stalemate!")
                    break
                else:
                    self.__handle_new_move_for_player(self.color_to_move, available_positions)

            # switch player, flip board
            self.color_to_move = BLACK_COLOR if self.color_to_move == WHITE_COLOR else WHITE_COLOR
            self.board.flip_board()

    def __handle_new_move_for_player(self, color, available_positions):
        while True:
            print(color)
            position_of_piece = input("Select a piece to move: ")
            if self.board.is_valid_notation_position(position_of_piece.upper()):
                position_of_piece = self.board.get_grid_position_from_notation_position(position_of_piece.upper())
            else:
                print("Invalid notation!")
                continue

            piece = self.board.get_piece_on_grid_position(position_of_piece)
            if piece is None:
                print("No piece at given position!")
                continue
            elif piece.color != color:
                print("Piece belongs to opposite color")
                continue

            available_positions_for_piece = set(position for position in self.board.get_available_positions_for_piece(piece) if position in available_positions)
            available_positions_for_piece_after_simulation = self.board.get_available_positions_for_piece_after_simulation(piece, available_positions_for_piece)
            if len(available_positions_for_piece_after_simulation) == 0:
                print("Piece has no available positions! Select a different piece")
                continue

            self.board.display(available_positions_for_piece_after_simulation)
            while True:
                chosen_position = input("Where would you like to move the selected piece? ")
                if self.board.is_valid_notation_position(chosen_position.upper()):
                    chosen_position = self.board.get_grid_position_from_notation_position(chosen_position.upper())
                else:
                    print("Invalid notation!")
                    continue

                if chosen_position not in available_positions_for_piece_after_simulation:
                    print("Invalid move")
                    continue
                else:
                    if piece.get_signature() == PAWN_SIGNATURE:
                        en_passant_position = SpecialPositionsHandler.get_en_passant_position(piece, self.board)
                        if chosen_position == en_passant_position:
                            position_of_pawn_to_take = (piece.current_position[0], en_passant_position[1])
                            self.board.move_piece_to_new_position(piece, chosen_position, True, position_of_pawn_to_take)
                        elif SpecialPositionsHandler.is_pawn_ready_for_promotion(piece, chosen_position):
                            new_promotion_piece = SpecialPositionsHandler.get_promotion_piece(piece.color)
                            self.board.move_piece_to_new_position(piece, chosen_position, True)
                            self.board.add_piece_to_board(new_promotion_piece, chosen_position)
                        else:
                            self.board.move_piece_to_new_position(piece, chosen_position, True)
                    elif piece.get_signature() == KING_SIGNATURE:
                        left_castling_position = SpecialPositionsHandler.get_castling_position(piece, LEFT_SIDE, self.board)
                        right_castling_position = SpecialPositionsHandler.get_castling_position(piece, RIGHT_SIDE, self.board)
                        if chosen_position == left_castling_position:
                            new_position_for_left_rook = (piece.current_position[0], piece.current_position[1] - 1)
                            left_rook = self.board.get_piece_on_grid_position((piece.current_position[0], 0))
                            self.board.move_piece_to_new_position(piece, chosen_position, True)
                            self.board.move_piece_to_new_position(left_rook, new_position_for_left_rook, False)
                        elif chosen_position == right_castling_position:
                            new_position_for_right_rook = (piece.current_position[0], piece.current_position[1] + 1)
                            right_rook = self.board.get_piece_on_grid_position((piece.current_position[0], 7))
                            self.board.move_piece_to_new_position(piece, chosen_position, True)
                            self.board.move_piece_to_new_position(right_rook, new_position_for_right_rook, False)
                        else:
                            self.board.move_piece_to_new_position(piece, chosen_position, True)
                    else:
                        self.board.move_piece_to_new_position(piece, chosen_position, True)
                    # break while loop
                    break
            break





