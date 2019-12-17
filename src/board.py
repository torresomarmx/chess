from src.util.chess_constants import *
from colorama import Fore, Back, Style
from src.pieces import Pawn, Rook, Knight, Bishop, King, Queen
from src.util.special_positions_handler import SpecialPositionsHandler
from src.util.moves_tracker import MovesTracker
from src.util.move_played import MovePlayed
import copy
import yaml

class Board:

    def __init__(self, moves_tracker = None):
        self.__grid = self.__create_empty_grid()
        # x axis on grid is top to bottom
        self.__rank_to_xindex_mapping = self.__create_rank_to_xindex_mapping()
        # y axis on grid is left to right
        self.__file_to_yindex_mapping = self.__create_file_to_yindex_mapping()
        # flipped means black is on bottom, white is on top. Default is white on bottom, black on top
        self.__flipped = False
        if moves_tracker is None:
            self.__moves_tracker = MovesTracker()
        else:
            self.__moves_tracker = moves_tracker

    @classmethod
    def create_board_from_yaml_file(cls, file_name):
        board = None
        with open(file_name) as file:
            file_content = yaml.full_load(file)

            moves_tracker = MovesTracker()
            keys_for_moves_tracker = ["black_moves_tracker", "white_moves_tracker"]
            for key in keys_for_moves_tracker:
                color = BLACK_COLOR if key == "black_moves_tracker" else "white_moves_tracker"
                for move in file_content[key]:
                    moves_tracker.add_move(
                        MovePlayed(move["piece_signature"], move["old_position"], move["new_position"]),
                        color
                    )

            board = Board(moves_tracker)

            keys_for_pieces = ["black_pieces", "white_pieces"]
            for key in keys_for_pieces:
                color = BLACK_COLOR if key == "black_pieces" else WHITE_COLOR
                for notation_position, piece_signature in file_content[key].items():
                    grid_position = board.get_grid_position_from_notation_position(notation_position)
                    if piece_signature == BISHOP_SIGNATURE:
                        board.add_piece_to_board(Bishop(color), grid_position)
                    elif piece_signature == KING_SIGNATURE:
                        board.add_piece_to_board(King(color), grid_position)
                    elif piece_signature == KNIGHT_SIGNATURE:
                        board.add_piece_to_board(Knight(color), grid_position)
                    elif piece_signature == PAWN_SIGNATURE:
                        board.add_piece_to_board(Pawn(color), grid_position)
                    elif piece_signature == QUEEN_SIGNATURE:
                        board.add_piece_to_board(Queen(color), grid_position)
                    elif piece_signature == ROOK_SIGNATURE:
                        board.add_piece_to_board(Rook(color), grid_position)

            if file_content["is_board_flipped"]:
                board.flip_board()

        return board

    def is_valid_notation_position(self, notation_position):
        if len(notation_position) != 2:
            return False
        file = notation_position[0]
        rank = notation_position[1]
        if file not in self.__file_to_yindex_mapping or rank not in self.__rank_to_xindex_mapping:
            return False

        return True

    def get_grid_position_from_notation_position(self, notation_position):
        if self.is_valid_notation_position(notation_position.upper()):
            file = notation_position[0]
            rank = notation_position[1]
            return (self.__rank_to_xindex_mapping[rank], self.__file_to_yindex_mapping[file])
        return None

    def get_notation_position_from_grid_position(self, grid_position):
        if self.__is_position_on_board(grid_position):
            x_position, y_position = grid_position
            x_index_to_rank_mapping = {x_index : rank for rank, x_index in self.__rank_to_xindex_mapping.items()}
            y_index_to_file_mapping = {y_index : file for file, y_index in self.__file_to_yindex_mapping.items()}
            return (y_index_to_file_mapping[y_position], x_index_to_rank_mapping[x_position])
        return None

    def get_king(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_on_grid_position((x, y))
                if isinstance(piece, King) and piece.color == color:
                    return piece

        return None

    @property
    def moves_tracker(self):
        return copy.deepcopy(self.__moves_tracker)

    @property
    def grid(self):
        return copy.deepcopy(self.__grid)

    def move_piece_to_new_position(self, piece, new_position, add_to_moves_tracker = False, position_of_piece_to_take = None):
        current_x_position_for_piece, current_y_position_for_piece = piece.current_position
        self.__grid[current_x_position_for_piece][current_y_position_for_piece] = None
        if add_to_moves_tracker:
            current_notation_position = self.get_notation_position_from_grid_position(piece.current_position)
            new_notation_position = self.get_notation_position_from_grid_position(new_position)
            new_move = MovePlayed(piece.get_signature(), current_notation_position, new_notation_position)
            self.__moves_tracker.add_move(new_move, piece.color)
            piece.increment_number_of_moves()

        self.add_piece_to_board(piece, new_position)
        if position_of_piece_to_take is not None:
            self.__grid[position_of_piece_to_take[0]][position_of_piece_to_take[1]] = None

    def get_defending_positions_for_piece(self, piece):
        return self.__get_positions_for_piece(piece, DEFENDING_POSITION)

    def get_attacking_positions_for_piece(self, piece):
        return self.__get_positions_for_piece(piece, ATTACKING_POSITION)

    def get_available_positions_for_piece(self, piece):
        return self.__get_positions_for_piece(piece, AVAILABLE_POSITION)

    def get_defending_positions(self, color):
        return self.__get_positions_for_color(color, DEFENDING_POSITION)

    def get_attacking_positions(self, color):
        return self.__get_positions_for_color(color, ATTACKING_POSITION)

    def get_available_positions(self, color, is_in_check):
        if is_in_check:
            return self.__get_in_check_available_positions(color)
        else:
            return self.__get_positions_for_color(color, AVAILABLE_POSITION)

    def is_in_checkmate(self, color):
        return len(self.__get_in_check_available_positions(color)) == 0

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
                back_color_black = Back.LIGHTYELLOW_EX if position in positions_to_highlight else Back.MAGENTA
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

    def get_piece_on_grid_position(self, position):
        x_index, y_index = position
        return self.__grid[x_index][y_index]

    def get_available_positions_for_piece_after_simulation(self, piece, positions_to_simulate = None, king = None):
        king = self.get_king(piece.color) if king is None else king

        opposite_color = WHITE_COLOR if piece.color == BLACK_COLOR else BLACK_COLOR
        available_positions_after_simulation = set()
        piece_original_position = piece.current_position
        available_positions_for_piece = self.get_available_positions_for_piece(piece) if positions_to_simulate is None else positions_to_simulate
        for available_position in available_positions_for_piece:
            # temporarily move piece to available position
            piece_at_available_position = self.get_piece_on_grid_position(available_position)
            self.move_piece_to_new_position(piece, available_position, False)
            new_attacked_positions = self.get_attacking_positions(opposite_color)
            is_in_check = king.current_position in new_attacked_positions

            # move everything back
            self.move_piece_to_new_position(piece, piece_original_position, False)
            if piece_at_available_position is not None:
                self.add_piece_to_board(piece_at_available_position, available_position)

            if is_in_check:
                continue
            else:
                available_positions_after_simulation.add(available_position)
        return available_positions_after_simulation

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

    def __is_position_available_or_defended(self, piece, move, is_conditional_attacking_move, move_type, current_position = None):
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
            if move_type == DEFENDING_POSITION or move_type == ATTACKING_POSITION:
                return True
            elif move_type == AVAILABLE_POSITION:
                return False if is_conditional_attacking_move else True
        else:
            if move_type == DEFENDING_POSITION:
                return piece_at_potential_position.color == piece.color
            elif move_type == ATTACKING_POSITION:
                return piece_at_potential_position.color != piece.color
            elif move_type == AVAILABLE_POSITION:
                if piece.get_signature() == PAWN_SIGNATURE and not is_conditional_attacking_move:
                    return False
                else:
                    return piece_at_potential_position.color != piece.color

    def __get_positions_for_piece(self, piece, position_type):
        positions = set()
        current_x_position, current_y_position = piece.current_position
        moves_to_check = []
        conditional_attacking_moves = piece.get_conditional_attacking_moves()
        move_type = position_type

        moves_to_check.append((True, conditional_attacking_moves))
        if position_type == DEFENDING_POSITION or position_type == ATTACKING_POSITION:
            moves_to_check.append( (False, piece.get_attacking_moves()) )
        elif position_type == AVAILABLE_POSITION:
            moves_to_check.append( (False, piece.get_positional_moves()) )

        for are_conditional_attacking_moves, moves in moves_to_check:
            if moves is None: continue
            for move in moves:
                if self.__is_position_available_or_defended(piece, move, are_conditional_attacking_moves, move_type):
                    potential_x_position = current_x_position + move[0]
                    potential_y_position = current_y_position + move[1]
                    positions.add((potential_x_position, potential_y_position))

        # then check if piece is sliding piece
        if piece.is_sliding_piece():
            for are_conditional_attacking_moves, moves in moves_to_check:
                if moves is None: continue
                for move in moves:
                    x_pos, y_pos = piece.current_position
                    while self.__is_position_available_or_defended(piece, move, are_conditional_attacking_moves, move_type, (x_pos, y_pos)):
                        x_pos += move[0]
                        y_pos += move[1]
                        positions.add((x_pos, y_pos))

        if piece.has_special_moves() and position_type == AVAILABLE_POSITION:
            special_positions = SpecialPositionsHandler.get_special_positions(piece, position_type, self)
            positions = positions.union(special_positions)

        # if piece is King and looking for available positions, make sure none of the positions are under attack or being defended
        attacked_positions = set()
        if piece.get_signature() == KING_SIGNATURE and position_type == AVAILABLE_POSITION:
            opposite_color = BLACK_COLOR if piece.color == WHITE_COLOR else WHITE_COLOR
            attacked_positions = self.get_attacking_positions(opposite_color)
            attacked_positions = attacked_positions.union(self.get_defending_positions(opposite_color))

        return positions.difference(attacked_positions)

    def __get_positions_for_color(self, color, position_type):
        positions = set()
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_on_grid_position((x, y))
                if piece is not None and piece.color == color:
                    positions = positions.union(self.__get_positions_for_piece(piece, position_type))

        return positions

    def __get_in_check_available_positions(self, color):
        king = self.get_king(color)
        available_positions_for_king = self.get_available_positions_for_piece(king)
        in_check_available_positions = set()

        if len(available_positions_for_king) == 0:
            # begin simulating moves
            for x in range(8):
                for y in range(8):
                    piece = self.get_piece_on_grid_position((x, y))
                    # we won't look at King again
                    if (piece is not None) and (piece.get_signature != KING_SIGNATURE) and (piece.color == color):
                        in_check_available_positions = in_check_available_positions.union(
                            self.get_available_positions_for_piece_after_simulation(piece, None, king)
                        )

            return in_check_available_positions
        else:
            return available_positions_for_king







