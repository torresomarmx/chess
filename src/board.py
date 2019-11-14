from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from colorama import Fore, Back, Style
from src.pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Board:

    def __init__(self, flip_board = False):
        self.__grid = self.__create_chess_grid()
        self.__rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        self.__file_to_yindex_mapping = self.__create_file_to_yindex_mapping()
        self.__display_board = self.__grid
        # flipped means black is on bottom, white is on top
        self.__flipped = False

        # if flip_board rotate 180 degrees, so that black is at the bottom. Default is white on bottom, black on top
        if flip_board:
            self.flip_display_board()

    def is_potential_move_valid(self, piece, move, is_unique_attacking_move = False):
        piece_color = piece.color
        current_x_position = piece.current_position[0]
        current_y_position = piece.current_position[1]
        potential_x_position = current_x_position + move[0]
        potential_y_position = current_y_position + move[1]
        # first check if potential position is out of bounds
        if (potential_x_position) > 7 or (potential_x_position) < 0:
            return False
        if (potential_y_position) > 7 or (potential_y_position) < 0:
            return False
        # if not out of bounds then FIRST check to see if move is_unique_attacking_move.
        # If it is, then check to see if there is a piece to attack
        piece_at_potential_position = self.__grid[potential_x_position][potential_y_position]
        if is_unique_attacking_move and piece_at_potential_position.color != piece_color:
            return True
        # else check to see that there is nothing blocking the move
        if piece_at_potential_position is None or piece_at_potential_position.color != piece_color:
            return True

    def get_available_positions_for_piece(self, piece):
        available_positions = set()
        current_x_position = piece.current_position[0]
        current_y_position = piece.current_position[1]

        for move in piece.legal_moves:
            if self.is_potential_move_valid(piece, move):
                potential_x_position = current_x_position + move[0]
                potential_y_position = current_y_position + move[1]
                available_positions.add((potential_x_position, potential_y_position))

        # then check to see if piece, like the Pawn, has unique attacking moves
        unique_attacking_moves = piece.get_unique_attacking_moves
        if len(unique_attacking_moves) != 0:
            for move in unique_attacking_moves:
                if self.is_potential_move_valid(piece, move, True):
                    potential_x_position = current_x_position + move[0]
                    potential_y_position = current_y_position + move[1]
                    available_positions.add((potential_x_position, potential_y_position))

        return available_positions

    def get_flipped_board(self):
        new_display_board = [[] for y in range(8)]
        for index, rank in enumerate(self.__display_board):
            new_display_board[index] = rank[::-1]

        new_display_board = new_display_board[::-1]
        return new_display_board

    def flip_display_board(self):
        new_display_board = self.get_flipped_board()

        self.__flipped = False if self.__flipped else True
        self.__display_board = new_display_board

    def display(self):
        ranks = list(self.__rank_to_xindex_mapping.keys())
        files = list(self.__file_to_yindex_mapping.keys())
        if self.__flipped:
            ranks = ranks[::-1]
            files = files[::-1]

        for rank_index, rank in enumerate(self.__display_board):
            # print rank number
            print(Fore.WHITE + ranks[rank_index] + " ", end="")
            for file_index, file in enumerate(rank):
                piece = self.__display_board[rank_index][file_index]
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
        x_index = self.__rank_to_xindex_mapping[rank]
        y_index = self.__file_to_yindex_mapping[file]
        return self.__grid[x_index][y_index]

    def __create_chess_grid(self):
        grid = self.__create_empty_grid()

        grid[-2:] = self.__create_starter_ranks(WHITE_COLOR)
        grid[:2] = self.__create_starter_ranks(BLACK_COLOR)

        return grid

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






