from colorama import Fore, Back, Style
from src.board import Board
from src.pieces import Pawn, Bishop, King, Queen, Rook, Knight
from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR

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

    p = King(BLACK_COLOR)
    p2 = Queen(WHITE_COLOR)
    p3 = Pawn(WHITE_COLOR)
    p4 = Rook(WHITE_COLOR)
    board = Board()
    # board.set_up_board_for_new_game()
    # board.display()
    # p = board.get_piece_on_position("A", "2")
    board.add_piece_to_board(p, (0, 0))
    board.add_piece_to_board(p2, (7, 7))
    board.add_piece_to_board(p3, (1, 1))
    board.add_piece_to_board(p4, (7, 0))
    positions = board.get_available_positions_for_piece(p)
    # positions = board.get_defending_positions_for_piece(p2)
    # positions = board.get_attacking_positions_for_piece(p2)
    # positions = board.get_defending_positions(WHITE_COLOR)
    # positions = board.get_attacking_positions(WHITE_COLOR)
    board.display(positions)
    # print(board.is_in_checkmate(BLACK_COLOR))
    # board.flip_board()
    # positions = board.get_available_positions_for_piece(p)
    # board.display(positions)
    # positions2 = board.get_available_positions_for_piece(p)
    # board.display(positions2)
    # player class
    # game class

