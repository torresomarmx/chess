from src.util import chess_constants
from colorama import Fore, Back, Style
from src.pieces.pawn import Pawn
from src.pieces.rook import Rook

class Board:

    def __init__(self, rotated = False):
        # rotates boars 180 degrees, so that black pieces are at the bottom
        self.rotated = rotated
        self.board = self.__create_chess_grid()
        self.rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        self.file_to_yindex_mapping = self.__create_file_to_yindex_mapping()

    def __create_chess_grid(self):
        board = self.__create_empty_grid()
        white_ranks = board[:2] if self.rotated else board[-2:]
        black_ranks = board[-2:] if self.rotated else board[:2]

        # TODO: write pure functions
        self.__populate_starter_ranks(white_ranks, chess_constants.WHITE_COLOR)
        self.__populate_starter_ranks(black_ranks, chess_constants.BLACK_COLOR)

        return board

    def __create_empty_grid(self):
        return [[None for i in range(8)] for y in range(8)]

    def __populate_starter_ranks(self, starter_ranks, color):
        # if rotated then
        top_rank_index = 0
        bottom_rank_index = 1
        for y in range(len(starter_ranks[top_rank_index])):
            # rooks
            if y in Rook.STARTER_Y_INDICES:
                starter_ranks[top_rank_index][y] = Rook(top_rank_index, y, color)
            # bishops
            if y in Bishop.STARTER_Y_INDICES:


        for i in range(len(starter_ranks[bottom_rank_index])):
            starter_ranks[bottom_rank_index][i] = Pawn(bottom_rank_index, i, color)

        # if self.rotated:
        # else:
        #     for i in range(len(starter_ranks[top_rank_index])):
        #         starter_ranks[top_rank_index][i] = Pawn(top_rank_index, i, color)
        #
        #     for i in range(len(starter_ranks[bottom_rank_index])):
        #         starter_ranks[bottom_rank_index][i] = "SW"

    def __create_rank_to_xindex_mapping(self):
        # this maps a chess rank position (1, 2, 3, et..) to a X position on the 8x8 grid
        ranks = [str(i) for i in range(1, 9)]
        if self.rotated:
            return {rank: index for index, rank in enumerate(ranks)}
        else:
            return {rank: index for index, rank in enumerate(ranks[::-1])}

    def __create_file_to_yindex_mapping(self):
        # this maps a chess file position (A, B, C, etc..) to a Y position on the 8x8 grid
        files = [chr(i).upper() for i in range(97, 105)]
        if self.rotated:
            return {file: index for index, file in enumerate(files[::-1])}
        else:
            return {file: index for index, file in enumerate(files)}

    def display(self):
        for rank_index, rank in enumerate(self.board):
            rank_index += 1
            for file_index, file in enumerate(rank):
                file_index += 1
                if rank_index % 2 == 0:
                    print(Back.WHITE + "   ", end="") if file_index % 2 == 0 else print(Back.RED + "   ", end="")
                else:
                    print(Back.RED + "   ", end="") if file_index % 2 == 0 else print(Back.WHITE + "   ", end="")
            print(Back.RESET)

    def get_piece_on_position(self, file, rank):
        x_index = self.rank_to_xindex_mapping[rank]
        y_index = self.file_to_yindex_mapping[file]
        return self.board[x_index][y_index]






