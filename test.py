from colorama import Fore, Back, Style
from src.board import Board

if __name__ == "__main__":
    # import os
    # n = os.system("clear")

    # print(Fore.RED + 'some red text')
    # print(Back.GREEN + 'and with a green background')
    # print(Style.DIM + 'and in dim text')
    board = Board(True)
    board.display()
    # standard notation is file-first, so A1
    pos = board.get_piece_on_position("A", "1")
    print(pos)