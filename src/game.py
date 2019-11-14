from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR

class Game:

    def __init__(self, board, player_1, player_2):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_to_move = player_1

    def start(self):
        while True:
            self.board.display()
            # here we first look at whether player_to_move is in check
            player_to_move_color = self.player_to_move.color
            opposite_color = WHITE_COLOR  if player_to_move_color == BLACK_COLOR else BLACK_COLOR
            attacked_positions = self.board.get_attacking_positions(opposite_color)
            king_position = self.board.get_king_position(player_to_move_color)
            if king_position in attacked_positions:
                # check to see if player_to_move is in check mate
                if self.board.is_in_checkmate(player_to_move_color, king_position):
                    # GAME OVER
                else:
                    # PROMPT

            else:
                # check to see if player_to_move is in stale mate
                if self.board.is_in_stalemate(player_to_move_color, king_position):
                    # GAME OVER
                else:
                    # PROMPT

            self.board.flip_display_board()







