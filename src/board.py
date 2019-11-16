from src.util.chess_constants import BLACK_COLOR, WHITE_COLOR
from colorama import Fore, Back, Style
from src.pieces import Pawn, Rook, Knight, Bishop, King, Queen

class Board:

    def __init__(self):
        self.__grid = self.__create_empty_grid()
        # x axis on grid is top to bottom
        self.__rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        # y axis on grid is left to right
        self.__file_to_yindex_mapping = self.__create_file_to_yindex_mapping()
        self.__flipped = False

    def add_piece_on_position(self, piece, x_position, y_position):
        self.__grid[x_position][y_position] = piece

    def set_up_board_for_new_game(self, flip_board = False):
        self.__grid = self.__create_grid_for_new_game()
        # flipped means black is on bottom, white is on top
        # if flip_board rotate 180 degrees, so that black is at the bottom. Default is white on bottom, black on top
        if flip_board:
            self.flip_board()

    def is_potential_move_valid(self, piece, current_position, move):
        current_x_position = current_position[0]
        current_y_position = current_position[1]
        potential_x_position = current_x_position + move[0]
        potential_y_position = current_y_position + move[1]

        # first check to see that current_position is valid (not stepping on any other piece)
        piece_at_current_position = self.__grid[current_x_position][current_y_position]
        if piece_at_current_position is not None and piece_at_current_position is not piece:
            return False

        # then check if potential position is out of bounds
        if (potential_x_position > 7) or (potential_y_position > 7):
            return False
        if (potential_x_position < 0) or (potential_y_position < 0):
            return False

        piece_at_potential_position = self.__grid[potential_x_position][potential_y_position]
        # then check to see if there is a piece to take at that position
        if piece_at_potential_position is not None:
            return piece_at_potential_position.color != piece.color
        else:
            return True

    def get_available_positions_for_piece(self, piece):
        available_positions = set()
        current_x_position = piece.current_position[0]
        current_y_position = piece.current_position[1]

        moves_to_check = piece.get_one_step_moves()
        unique_attacking_moves = piece.get_unique_attacking_moves()
        if len(unique_attacking_moves) != 0:
            moves_to_check.union(unique_attacking_moves)

        for move in moves_to_check:
            if self.is_potential_move_valid(piece, piece.current_position, move):
                potential_x_position = current_x_position + move[0]
                potential_y_position = current_y_position + move[1]
                available_positions.add( (potential_x_position, potential_y_position) )

        # then check if piece is sliding piece
        if piece.is_sliding_piece():
            for move in moves_to_check:
                while self.is_potential_move_valid(piece, (current_x_position, current_y_position), move):
                    potential_x_position = current_x_position + move[0]
                    potential_y_position = current_y_position + move[1]
                    available_positions.add((potential_x_position, potential_y_position))
                    current_x_position = potential_x_position
                    current_y_position = potential_y_position

        return available_positions

    def flip_board(self):
        new_board = [[] for y in range(8)]
        for index, rank in enumerate(self.__grid):
            new_board[index] = rank[::-1]

        new_board = new_board[::-1]

        for rank_index, rank in enumerate(new_board):
            for file_index, file in enumerate(rank):
                piece = new_board[rank_index][file_index]
                if piece is not None:
                    piece.current_position = (rank_index, file_index)
                    piece.switch_orientation()

        self.__grid = new_board
        self.__flipped = False if self.__flipped else True
        self.__rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping(self.__flipped)
        self.__file_to_yindex_mapping = self.__create_file_to_yindex_mapping(self.__flipped)

    def display(self, positions_to_highlight = None):
        positions_to_highlight = {} if positions_to_highlight is None else positions_to_highlight
        ranks = list(self.__rank_to_xindex_mapping.keys())
        files = list(self.__file_to_yindex_mapping.keys())
        if self.__flipped:
            ranks = ranks[::-1]
            files = files[::-1]

        for rank_index, rank in enumerate(self.__grid):
            # print rank number
            print(Fore.WHITE + ranks[rank_index] + " ", end="")
            for file_index, file in enumerate(rank):
                position = (rank_index, file_index)
                piece = self.__grid[rank_index][file_index]
                symbol = "   " if piece is None else " {} ".format(Fore.BLACK + piece.symbol)
                back_color_white = Back.LIGHTYELLOW_EX if position in positions_to_highlight else Back.WHITE
                back_color_black = Back.LIGHTYELLOW_EX if position in positions_to_highlight else Back.RED
                if rank_index % 2 == 0:
                    if file_index % 2 == 0:
                        print(back_color_white + symbol, end="")
                    else:
                        print(back_color_black + symbol, end="")
                else:
                    if file_index % 2 == 0:
                        print(back_color_black + symbol, end="")
                    else:
                        print(back_color_white + symbol, end="")
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

    def __create_grid_for_new_game(self):
        grid = self.__create_empty_grid()

        grid[:2] = self.__create_starter_ranks(BLACK_COLOR)
        grid[-2:] = self.__create_starter_ranks(WHITE_COLOR)

        return grid

    def __create_empty_grid(self):
        return [[None for x in range(8)] for y in range(8)]

    def __create_starter_ranks(self, color):
        starter_ranks = [[None for x in range(8)] for y in range(2)]
        pawn_rank_index = 0 if color == WHITE_COLOR else 1
        major_pieces_rank_index = 1 if color == WHITE_COLOR else 0

        # first create pawns
        for y in range(8):
            starter_ranks[pawn_rank_index][y] = Pawn((pawn_rank_index, y), color)

        # then create major pieces
        for y in range(8):
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

    def __create_rank_to_xindex_mapping(self, flipped = False):
        # this maps a chess rank position (1, 2, 3, et..) to a X position on the 8x8 grid
        ranks = [str(i) for i in range(1, 9)]

        if flipped:
            return {rank : index for index, rank in enumerate(ranks)}

        return {rank: index for index, rank in enumerate(ranks[::-1])}

    def __create_file_to_yindex_mapping(self, flipped = False):
        # this maps a chess file position (A, B, C, etc..) to a Y position on the 8x8 grid
        files = [chr(i).upper() for i in range(97, 105)]

        if flipped:
            return {file : index for index, file in enumerate(files[::-1])}

        return {file: index for index, file in enumerate(files)}






