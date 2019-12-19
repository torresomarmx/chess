from colorama import Fore, Back, Style
from src.board import Board
from src.pieces import Pawn, Bishop, King, Queen, Rook, Knight
from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from src.util.moves_tracker import MovesTracker
from src.game import Game

if __name__ == "__main__":
    test_board = Board.create_board_from_yaml_file("pawn_promotion_on_next_move.yaml")
    game = Game(test_board, BLACK_COLOR if test_board.is_flipped else WHITE_COLOR)
    # game = Game()
    game.start()



