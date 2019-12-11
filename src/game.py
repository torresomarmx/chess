from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from src.util.moves_tracker import MovesTracker

class Game:

    def __init__(self, board):
        self.board = board(MovesTracker())
        self.player_to_move = WHITE_COLOR

    def __handle_new_move_for_player(self, color, available_positions):
        while True:
            position_of_piece = input("Select a piece to move: ")
            piece = self.board.get_piece_on_notation_position((position_of_piece[0]), position_of_piece[1])
            if piece is None:
                print("No piece at given positions!")
                continue
            elif piece.color != color:
                print("Piece belongs to opposite color")
                continue

            available_positions_for_piece = set(position for position in self.board.get_available_positions_for_piece(piece) if position in available_positions)
            while True:
                chosen_position = input("Where would you like to move the selected piece? ")
                # TODO: convert from notation to grid
                if (chosen_position[0], chosen_position[1]) not in available_positions_for_piece:
                    print("Invalid move")
                    continue
                else:
                    

            break

    def start(self):
        self.board.set_up_board_for_new_game()
        while True:
            self.board.display()
            opposite_color = BLACK_COLOR if self.player_to_move == WHITE_COLOR else BLACK_COLOR
            attacked_positions = self.board.get_attacking_positions(opposite_color)
            king = self.board.get_king(self.player_to_move.color)
            if king.current_position in attacked_positions:
                in_check_available_positions = self.board.get_available_positions(self.player_to_move.color, True)
                if len(in_check_available_positions) == 0:
                    print("Game over. Checkmate!")
                    break
                else:
                    self.__handle_new_move_for_player(self.player_to_move.color, in_check_available_positions)
            else:
                available_positions = self.board.get_available_positions(self.player_to_move.color, False)
                if len(available_positions) == 0:
                    print("Game over. Stalemate!")
                    break
                else:
                    self.__handle_new_move_for_player(self.player_to_move.color, available_positions)

            # switch player, flip board
            self.player_to_move = BLACK_COLOR if self.player_to_move == WHITE_COLOR else BLACK_COLOR
            self.board.flip_board()





