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
        # flipped means black is on bottom, white is on top. Default is white on bottom, black on top
        self.__flipped = False

    def move_piece_to_new_position(self, piece, new_position):
        current_x_position_for_piece, current_y_position_for_piece = piece.current_position
        self.__grid[current_x_position_for_piece][current_y_position_for_piece] = None
        self.add_piece_to_board(piece, new_position)

    def get_king(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_on_grid_position((x, y))
                if isinstance(piece, King) and piece.color == color:
                    return piece

        return None

    def get_defending_positions_for_piece(self, piece):
        return self.__get_positions_for_piece(piece, "DEFENDING")

    def get_attacking_positions_for_piece(self, piece):
        return self.__get_positions_for_piece(piece, "ATTACKING")

    def get_available_positions_for_piece(self, piece):
        available_positions = self.__get_positions_for_piece(piece, "AVAILABLE")
        attacked_positions = set()

        # if piece is King, we have to make sure none of the available_positions are under attack or being defended
        if isinstance(piece, King):
            opposite_color = BLACK_COLOR if piece.color == WHITE_COLOR else WHITE_COLOR
            attacked_positions = self.get_attacking_positions(opposite_color)
            attacked_positions = attacked_positions.union(self.get_defending_positions(opposite_color))

        return available_positions.difference(attacked_positions)

    def get_defending_positions(self, color):
        return self.__get_positions_for_color(color, "DEFENDING")

    def get_attacking_positions(self, color):
        return self.__get_positions_for_color(color, "ATTACKING")

    def get_available_positions(self, color):
        return self.__get_positions_for_color(color, "AVAILABLE")

    def is_in_checkmate(self, color):
        king = self.get_king(color)
        available_moves_for_king = self.get_available_positions_for_piece(king)

        if len(available_moves_for_king) == 0:
            # begin simulating moves
            opposite_color = WHITE_COLOR if color == BLACK_COLOR else BLACK_COLOR

            for x in range(8):
                for y in range(8):
                    piece = self.get_piece_on_grid_position((x, y))
                    # we won't look at King again
                    if (piece is not None) and (not isinstance(piece, King)) and (piece.color == color):
                        piece_original_position = piece.current_position
                        available_positions_for_piece = self.get_available_positions_for_piece(piece)
                        for available_position in available_positions_for_piece:
                            # temporarily move piece to available position
                            piece_at_available_position = self.get_piece_on_grid_position(available_position)
                            self.move_piece_to_new_position(piece, available_position)

                            new_attacked_positions = self.get_attacking_positions(opposite_color)
                            is_in_check = king.current_position in new_attacked_positions

                            # move everything back
                            self.move_piece_to_new_position(piece, piece_original_position)
                            if piece_at_available_position is not None:
                                self.add_piece_to_board(piece_at_available_position, available_position)

                            if is_in_check:
                                continue
                            else:
                                return False
            return True
        else:
            return False

    def add_piece_to_board(self, piece, position):
        x_position, y_position = position
        self.__grid[x_position][y_position] = piece
        piece.current_position = position

    def set_up_board_for_new_game(self, flip_board = False):
        self.__grid = self.__create_empty_grid()

        for color in (WHITE_COLOR, BLACK_COLOR):
            pawn_rank_index = 6 if color == WHITE_COLOR else 1
            major_pieces_rank_index = 7 if color == WHITE_COLOR else 0

            # first create pawns
            for y in range(8):
                pawn = Pawn(color)
                self.add_piece_to_board(pawn, (pawn_rank_index, y))

            # then create major pieces
            for y in range(8):
                if y in Rook.STARTER_Y_INDICES:
                    rook = Rook(color)
                    self.add_piece_to_board(rook, (major_pieces_rank_index, y))
                elif y in Knight.STARTER_Y_INDICES:
                    knight = Knight(color)
                    self.add_piece_to_board(knight, (major_pieces_rank_index, y))
                elif y in Bishop.STARTER_Y_INDICES:
                    bishop = Bishop(color)
                    self.add_piece_to_board(bishop, (major_pieces_rank_index, y))
                elif y == King.DEFAULT_STARTER_Y_INDEX:
                    king = King(color)
                    self.add_piece_to_board(king, (major_pieces_rank_index, y))
                elif y == Queen.DEFAULT_STARTER_Y_INDEX:
                    queen = Queen(color)
                    self.add_piece_to_board(queen, (major_pieces_rank_index, y))

        # if flip_board rotate 180 degrees, so that black is at the bottom. Default is white on bottom, black on top
        if flip_board:
            self.flip_board()

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
        index_to_ranks_mapping = {index : rank for rank, index in self.__rank_to_xindex_mapping.items()}
        index_to_files_mapping = {index : file for file, index in self.__file_to_yindex_mapping.items()}

        for rank_index, rank in enumerate(self.__grid):
            # print rank number
            print(Fore.WHITE + index_to_ranks_mapping.get(rank_index) + " ", end="")
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
        for index in range(8):
            print(" {} ".format(Fore.WHITE + index_to_files_mapping.get(index)), end="")
        print()

    def get_piece_on_notation_position(self, position):
        file, rank = position
        x_index = self.__rank_to_xindex_mapping[rank]
        y_index = self.__file_to_yindex_mapping[file]
        return self.__grid[x_index][y_index]

    def get_piece_on_grid_position(self, position):
        x_index, y_index = position
        return self.__grid[x_index][y_index]

    def __create_empty_grid(self):
        return [[None for x in range(8)] for y in range(8)]

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

    def __is_position_on_board(self, position):
        x_position, y_position = position

        if (x_position > 7) or (y_position > 7):
            return False
        if (x_position < 0) or (y_position < 0):
            return False

        return True

    def __is_move_available_or_defended(self, piece, move, is_conditional_attacking_move, move_type, current_position = None):
        current_x_position, current_y_position = piece.current_position if current_position is None else current_position
        potential_x_position, potential_y_position = (current_x_position + move[0], current_y_position + move[1])

        # first check to see that current_position is valid (not stepping on any other piece)
        piece_at_current_position = self.get_piece_on_grid_position((current_x_position, current_y_position))
        if piece_at_current_position is not None and piece_at_current_position is not piece:
            return False

        # then check if potential position is out of bounds
        if not self.__is_position_on_board((potential_x_position, potential_y_position)):
            return False

        piece_at_potential_position = self.get_piece_on_grid_position((potential_x_position, potential_y_position))

        if piece_at_potential_position is None:
            if move_type == "DEFENDING" or move_type == "ATTACKING":
                return True
            elif move_type == "AVAILABLE":
                return False if is_conditional_attacking_move else True
        else:
            if move_type == "DEFENDING":
                return piece_at_potential_position.color == piece.color
            elif move_type == "AVAILABLE" or move_type == "ATTACKING":
                return piece_at_potential_position.color != piece.color

    def __get_positions_for_piece(self, piece, position_type):
        positions = set()
        current_x_position, current_y_position = piece.current_position
        moves_to_check = []
        conditional_attacking_moves = piece.get_conditional_attacking_moves()
        move_type = position_type

        if conditional_attacking_moves is not None:
            moves_to_check.append((True, conditional_attacking_moves))

        if position_type == "DEFENDING" or position_type == "ATTACKING":
            moves = piece.get_attacking_moves()
            if moves is not None: moves_to_check.append( (False, moves) )
        elif position_type == "AVAILABLE":
            moves = piece.get_positional_moves()
            if moves is not None: moves_to_check.append( (False, moves) )

        for are_conditional_attacking_moves, moves in moves_to_check:
            if moves is None:
                continue
            for move in moves:
                if self.__is_move_available_or_defended(piece, move, are_conditional_attacking_moves, move_type):
                    potential_x_position = current_x_position + move[0]
                    potential_y_position = current_y_position + move[1]
                    positions.add((potential_x_position, potential_y_position))

        # then check if piece is sliding piece
        if piece.is_sliding_piece():
            for are_conditional_attacking_moves, moves in moves_to_check:
                for move in moves:
                    x_pos, y_pos = piece.current_position
                    while self.__is_move_available_or_defended(piece, move, are_conditional_attacking_moves, move_type, (x_pos, y_pos)):
                        x_pos += move[0]
                        y_pos += move[1]
                        positions.add((x_pos, y_pos))

        return positions

    def __get_positions_for_color(self, color, position_type):
        positions = set()
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_on_grid_position((x, y))
                if piece is not None and piece.color == color:
                    if position_type == "AVAILABLE":
                        positions = positions.union(self.get_available_positions_for_piece(piece))
                    else:
                        positions = positions.union(self.__get_positions_for_piece(piece, position_type))

        return positions







