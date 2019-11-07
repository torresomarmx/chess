from colorama import Fore, Back, Style
from src.board import Board

if __name__ == "__main__":
    # import os
    # n = os.system("clear")

    # print(Fore.RED + 'some red text')
    # print(Back.GREEN + 'and with a green background')
    # print(Style.DIM + 'and in dim text')
    board = Board()
    board.display()

    board2 = Board(True)
    board2.display()