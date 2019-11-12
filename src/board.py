from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from colorama import Fore, Back, Style
from src.pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Board:

    def __init__(self, flip_board = False):
        self.grid = self.__create_chess_grid()
        self.display_board = self.grid
        self.rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        self.file_to_yindex_mapping = self.__create_file_to_yindex_mapping()
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

        self.flipped = True if not self.flipped else False
        self.display_board = new_display_board

    def __create_empty_grid(self):
        return [[None for i in range(8)] for y in range(8)]

    def __create_starter_ranks(self, color):
        starter_ranks = [[None for i in range(8)] for y in range(2)]
        pawn_rank_index = 0 if color == WHITE_COLOR else 1
        major_pieces_rank_index = 1 if color == WHITE_COLOR else 0

        # first create pawns
        for y in range(len(starter_ranks[pawn_rank_index])):
            starter_ranks[pawn_rank_index][y] = Pawn(pawn_rank_index, y, color)

        # then create major pieces
        for y in range(len(starter_ranks[major_pieces_rank_index])):
            # rooks
            if y in Rook.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][y] = Rook(major_pieces_rank_index, y, color)
            # knights
            elif y in Knight.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][y] = Knight(major_pieces_rank_index, y, color)
            # bishops
            elif y in Bishop.STARTER_Y_INDICES:
                starter_ranks[major_pieces_rank_index][y] = Bishop(major_pieces_rank_index, y, color)
            # king
            elif y == King.DEFAULT_STARTER_Y_INDEX:
                starter_ranks[major_pieces_rank_index][y] = King(major_pieces_rank_index, y, color)
            # queen
            elif y == Queen.DEFAULT_STARTER_Y_INDEX:
                starter_ranks[major_pieces_rank_index][y] = Queen(major_pieces_rank_index, y, color)

        return starter_ranks

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
        for rank_index, rank in enumerate(self.display_board):
            for file_index, file in enumerate(rank):
                piece = self.display_board[rank_index][file_index]
                symbol = "   " if piece is None else " {} ".format(Fore.BLACK + piece.symbol)
                if rank_index % 2 == 0:
                    print(Back.WHITE + symbol, end="") if file_index % 2 == 0 else print(Back.RED + symbol, end="")
                else:
                    print(Back.RED + symbol, end="") if file_index % 2 == 0 else print(Back.WHITE + symbol, end="")
            # starting new rank, so reset Back
            print(Back.RESET)

    def get_piece_on_position(self, file, rank):
        x_index = self.rank_to_xindex_mapping[rank]
        y_index = self.file_to_yindex_mapping[file]
        return self.grid[x_index][y_index]






