from colorama import Fore, Back, Style
from src.board import Board
from src.pieces import Pawn, Bishop, King, Queen, Rook, Knight
from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from src.util.moves_tracker import MovesTracker

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
    p5 = Pawn(WHITE_COLOR)
    p6 = Bishop(WHITE_COLOR)
    p7 = Bishop(WHITE_COLOR)
    p8 = Bishop(BLACK_COLOR)
    p9 = Pawn(BLACK_COLOR)

    moves_tracker = MovesTracker()
    board = Board(moves_tracker)
    # board.set_up_board_for_new_game()
    # board.display()
    # p = board.get_piece_on_position("A", "2")
    board.add_piece_to_board(p, (0, 0))
    # board.add_piece_to_board(p2, (7, 7))
    board.add_piece_to_board(p3, (6, 1))
    board.add_piece_to_board(p4, (7, 0))
    # board.add_piece_to_board(p5, (1, 2))
    # board.add_piece_to_board(p6, (6, 7))
    # board.add_piece_to_board(p7, (7, 6))
    board.add_piece_to_board(p9, (4, 2))
    board.move_piece_to_new_position(p3, (4, 1), True)
    # board.move_piece_to_new_position(p4, (7,1), True)
    # positions = board.get_available_positions_for_piece(p)
    positions = board.get_available_positions(BLACK_COLOR, True)
    # positions = board.get_defending_positions_for_piece(p5)
    # positions = board.get_attacking_positions_for_piece(p5)
    # board.flip_board()
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

