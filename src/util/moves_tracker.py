from src.util.chess_constants import BLACK_COLOR

class MovesTracker:
    def __init__(self):
        self.__all_moves = []
        self.__black_moves = []
        self.__white_moves = []

    @property
    def black_moves(self):
        return self.__black_moves

    @property
    def white_moves(self):
        return self.__white_moves

    @property
    def all_moves(self):
        return self.__all_moves

    def add_move(self, move, color):
        if color == BLACK_COLOR:
            self.__black_moves.append(move)
        else:
            self.__white_moves.append(move)
        self.__all_moves.append(move)



