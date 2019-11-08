from src.util import chess_constants

class Board:

    def __init__(self, rotated = False):
        # rotates boars 180 degrees, so that black pieces are at the bottom
        self.rotated = rotated
        self.board = self.__create()
        self.rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        self.file_to_yindex_mapping = self.__create_file_to_yindex_mapping()

    def __create(self):
        board = self.__create_empty_grid()
        white_ranks = board[:2] if self.rotated else board[-2:]
        black_ranks = board[-2:] if self.rotated else board[:2]

        self.__populate_starter_ranks(white_ranks, chess_constants.WHITE_NAME)
        self.__populate_starter_ranks(black_ranks, chess_constants.BLACK_NAME)

        return board

    def __create_empty_grid(self):
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

    def __create_rank_to_xindex_mapping(self):
        # this maps a chess rank position (A, B, C, etc..) to a X position on the 8x8 grid
        ranks = [chr(i).upper() for i in range(97, 105)]
        if self.rotated:
            return {rank: index for index, rank in enumerate(ranks[::-1])}
        else:
            return {rank: index for index, rank in enumerate(ranks)}

    def __create_file_to_yindex_mapping(self):
        # this maps a chess file position (1, 2, 3, et..) to a Y position on the 8x8 grid
        files = [str(i) for i in range(1, 9)]
        if self.rotated:
            return {file: index for index, file in enumerate(files[::-1])}
        else:
            return {file: index for index, file in enumerate(files)}

    def display(self):
        for rank in self.board:
            print(rank)





