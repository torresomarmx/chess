from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from colorama import Fore, Back, Style
from src.pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Board:

    def __init__(self, flip_board = False):
        self.grid = self.__create_chess_grid()
        self.rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        self.file_to_yindex_mapping = self.__create_file_to_yindex_mapping()
        self.display_board = self.grid
        # flipped means black is on bottom, white is on top
        self.flipped = False

        # if flip_board rotate 180 degrees, so that black is at the bottom. Default is white on bottom, black on top
        if flip_board:
            self.flip_display_board()

    def __create_chess_grid(self):
        board = self.__create_empty_grid()

        board[-2:] = self.__create_starter_ranks(WHITE_COLOR)
        board[:2] = self.__create_starter_ranks(BLACK_COLOR)

        return board

    def flip_display_board(self):
        new_display_board = [[] for y in range(8)]
        for index, rank in enumerate(self.display_board):
            new_display_board[index] = rank[::-1]

        new_display_board = new_display_board[::-1]

        self.flipped = False if self.flipped else True
        self.display_board = new_display_board

    def __create_empty_grid(self):
        return [[None for x in range(8)] for y in range(8)]

    def __create_starter_ranks(self, color):
        starter_ranks = [[None for x in range(8)] for y in range(2)]
        pawn_rank_index = 0 if color == WHITE_COLOR else 1
        major_pieces_rank_index = 1 if color == WHITE_COLOR else 0

        # first create pawns
        for i in range(8):
            starter_ranks[pawn_rank_index][i] = Pawn(pawn_rank_index, i, color)

        # then create major pieces
        for i in range(len(starter_ranks[major_pieces_rank_index])):
            # rooks
            if i in Rook.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][i] = Rook(major_pieces_rank_index, i, color)
            # knights
            elif i in Knight.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][i] = Knight(major_pieces_rank_index, i, color)
            # bishops
            elif i in Bishop.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][i] = Bishop(major_pieces_rank_index, i, color)
            # king
            elif i == King.DEFAULT_STARTER_Y_INDEX:
                starter_ranks[major_pieces_rank_index][i] = King(major_pieces_rank_index, i, color)
            # queen
            elif i == Queen.DEFAULT_STARTER_Y_INDEX:
                starter_ranks[major_pieces_rank_index][i] = Queen(major_pieces_rank_index, i, color)

        return starter_ranks

    def __create_rank_to_xindex_mapping(self):
        # this maps a chess rank position (1, 2, 3, et..) to a X position on the 8x8 grid
        ranks = [str(i) for i in range(1, 9)]
        return {rank: index for index, rank in enumerate(ranks[::-1])}

    def __create_file_to_yindex_mapping(self):
        # this maps a chess file position (A, B, C, etc..) to a Y position on the 8x8 grid
        files = [chr(i).upper() for i in range(97, 105)]
        return {file: index for index, file in enumerate(files)}

    def display(self):
        ranks = list(self.rank_to_xindex_mapping.keys())
        files = list(self.file_to_yindex_mapping.keys())
        if self.flipped:
            ranks = ranks[::-1]
            files = files[::-1]

        for rank_index, rank in enumerate(self.display_board):
            # print rank number
            print(Fore.WHITE + ranks[rank_index] + " ", end="")
            for file_index, file in enumerate(rank):
                piece = self.display_board[rank_index][file_index]
                symbol = "   " if piece is None else " {} ".format(Fore.BLACK + piece.symbol)
                if rank_index % 2 == 0:
                    print(Back.WHITE + symbol, end="") if file_index % 2 == 0 else print(Back.RED + symbol, end="")
                else:
                    print(Back.RED + symbol, end="") if file_index % 2 == 0 else print(Back.WHITE + symbol, end="")
            # starting new rank, so reset Back
            print(Back.RESET)

        # print files
        print("  ", end="")
        for file in files:
            print(" {} ".format(Fore.WHITE + file), end="")
        print()


    def get_piece_on_position(self, file, rank):
        x_index = self.rank_to_xindex_mapping[rank]
        y_index = self.file_to_yindex_mapping[file]
        return self.grid[x_index][y_index]






