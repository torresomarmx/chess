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

    def is_color_in_check(self, color):
        # get available positions for all pieces of opposite color. These will the attacked positions
        # get the position of the king for color in question
        # check to see if king position is in attacked positions
        pass

    def get_king(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.__grid[x][y]
                if isinstance(piece, King) and piece.color == color:
                    return piece

        return None

    def is_color_in_checkmate(self, color):
        king = self.get_king(color)
        available_moves_for_king = self.get_available_positions_for_piece(king, False)

        if len(available_moves_for_king) == 0:
            # begin simulating moves
            simulation_board = Board()
            pieces_to_simulate_moves = []
            for x in range(8):
                for y in range(8):
                    piece = self.__grid[x][y]
                    if piece is not None:
                        piece_color = piece.color
                        simulation_piece = None
                        if isinstance(piece, Pawn):
                            simulation_piece = Pawn(piece_color)
                        elif isinstance(piece, Bishop):
                            simulation_piece = Bishop([piece_color])
                        elif isinstance(piece, King):
                            simulation_piece = King(piece_color)
                        elif isinstance(piece, Knight):
                            simulation_piece = Knight(piece_color)
                        elif isinstance(piece, Queen):
                            simulation_piece = Queen(piece_color)
                        elif isinstance(piece, Rook):
                            simulation_piece = Rook(piece_color)
                        else:
                            continue
                        simulation_board.add_piece_to_board(simulation_piece, piece.current_position)
                        if simulation_piece.color == color: pieces_to_simulate_moves.append(simulation_piece)

            for piece in pieces_to_simulate_moves:
                # get all the available positions
                    # store current position
                    # temporarily move piece to available position
                    # see if king is still in check

        else:
            return False

    def get_attacking_positions(self, color):
        attacking_positions = set()

        for x in range(8):
            for y in range(8):
                piece = self.__grid[x][y]
                if piece is not None and piece.color == color:
                    attacking_positions.add(self.get_available_positions_for_piece(piece))

        return attacking_positions

    def add_piece_to_board(self, piece, position):
        x_position = position[0]
        y_position = position[1]
        self.__grid[x_position][y_position] = piece
        piece.current_position = (x_position, y_position)

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

    def is_potential_move_valid(self, piece, move, is_unique_attacking_move, current_position = None):
        current_x_position = piece.current_position[0] if current_position is None else current_position[0]
        current_y_position = piece.current_position[1] if current_position is None else current_position[1]
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
        if piece_at_potential_position is None:
            return False if is_unique_attacking_move else True
        else:
            return piece_at_potential_position.color != piece.color

    def get_available_positions_for_piece(self, piece, skip_king_safety_check = True):
        # TODO: check if piece has a current position. This is only the case if piece is on board
        available_positions = set()
        attacked_positions = set()
        current_x_position = piece.current_position[0]
        current_y_position = piece.current_position[1]

        # if piece is King, we have to make sure none of the available_positions are under attack
        if isinstance(piece, King) and not skip_king_safety_check:
            opposite_color = BLACK_COLOR if piece.color == WHITE_COLOR else WHITE_COLOR
            attacked_positions = self.get_attacking_positions(opposite_color)

        moves_to_check = [(False, piece.get_one_step_moves())]
        unique_attacking_moves = piece.get_unique_attacking_moves()
        if unique_attacking_moves is not None:
            moves_to_check.append((True, unique_attacking_moves))

        for are_unique_attacking_moves, moves in moves_to_check:
            for move in moves:
                if self.is_potential_move_valid(piece, move, are_unique_attacking_moves):
                    potential_x_position = current_x_position + move[0]
                    potential_y_position = current_y_position + move[1]
                    available_positions.add( (potential_x_position, potential_y_position) )

        # then check if piece is sliding piece
        if piece.is_sliding_piece():
            for are_unique_attacking_moves, moves in moves_to_check:
                for move in moves:
                    x_pos = piece.current_position[0]
                    y_pos = piece.current_position[1]
                    while self.is_potential_move_valid(piece, move, are_unique_attacking_moves, (x_pos, y_pos)):
                        potential_x_position = x_pos + move[0]
                        potential_y_position = y_pos + move[1]
                        available_positions.add((potential_x_position, potential_y_position))
                        x_pos = potential_x_position
                        y_pos = potential_y_position

        return available_positions.difference(attacked_positions)

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

    def get_piece_on_position(self, file, rank):
        x_index = self.__rank_to_xindex_mapping[rank]
        y_index = self.__file_to_yindex_mapping[file]
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






