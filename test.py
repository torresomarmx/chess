from colorama import Fore, Back, Style
from src.board import Board
from src.pieces import Pawn
from src.util.chess_constants import BLACK_COLOR

if __name__ == "__main__":
    # import os
    # n = os.system("clear")

    # print(Fore.RED + 'some red text')
    # print(Back.GREEN + 'and with a green background')
    # print(Style.DIM + 'and in dim text')
    # board = Board()
    # board.display()
    # pos = board.get_piece_on_position("A", "1")
    # print(pos)
    # board.flip_display_board()
    # board.display()
    # pos = board.get_piece_on_position("A", "1")
    # print(pos)
    # board.flip_display_board()
    # board.display()
    # # standard notation is file-first, so A1
    # pos = board.get_piece_on_position("A", "1")
    # print(pos)

    p = Pawn((1,0), BLACK_COLOR)
    board = Board()
    board.add_piece_on_position(p, 1, 0)
    board.display()
    print(board.get_available_positions_for_piece(p))
    board.flip_board()
    board.display()
    print(board.get_available_positions_for_piece(p))
    # player class
    # game class

