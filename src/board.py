from src.util import chess_constants

class Board:

    def __init__(self, rotated = False):
        # rotates boars 180 degrees, so that black pieces are at the bottom
        self.rotated = rotated
        self.board = self.__create()

    def __create(self):
        board = self.__create_empty_board()
        white_ranks = board[:2] if self.rotated else board[-2:]
        black_ranks = board[-2:] if self.rotated else board[:2]

        self.__populate_starter_ranks(white_ranks, chess_constants.WHITE_NAME)
        self.__populate_starter_ranks(black_ranks, chess_constants.BLACK_NAME)

        return board

    def __create_empty_board(self):
        return [[None for i in range(8)] for y in range(8)]

    def __populate_starter_ranks(self, starter_ranks, color):
        if color == chess_constants.WHITE_NAME:
            # if rotated then white pieces are on top
            if self.rotated:
                for i in range(len(starter_ranks[0])):
                    starter_ranks[0][i] = "SW"
                for i in range(len(starter_ranks[1])):
                    starter_ranks[1][i] = "PW"
            else:
                for i in range(len(starter_ranks[0])):
                    starter_ranks[0][i] = "PW"
                for i in range(len(starter_ranks[1])):
                    starter_ranks[1][i] = "SW"
        elif color == chess_constants.BLACK_NAME:
            if self.rotated:
                for i in range(len(starter_ranks[0])):
                    starter_ranks[0][i] = "PB"
                for i in range(len(starter_ranks[1])):
                    starter_ranks[1][i] = "SB"
            else:
                for i in range(len(starter_ranks[0])):
                    starter_ranks[0][i] = "SB"
                for i in range(len(starter_ranks[1])):
                    starter_ranks[1][i] = "PB"

    def display(self):
        print(self.board)





