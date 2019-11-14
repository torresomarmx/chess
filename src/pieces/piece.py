from abc import ABC, abstractmethod
from src.util.chess_constants import BLACK_COLOR

class Piece(ABC):

    def __init__(self, x_position, y_position, color):
        self.current_position = (x_position, y_position)
        self.__color = color
        self.__symbol = Piece.white_symbol() if color == BLACK_COLOR else Piece.black_symbol()

    @property
    def color(self):
        return self.__color

    @property
    def current_position(self):
        return self.__current_position

    @current_position.setter
    def current_position(self, new_position):
        self.__current_position = new_position

    @property
    def symbol(self):
        return self.__symbol

    @classmethod
    @abstractmethod
    def white_symbol(cls):
        pass

    @classmethod
    @abstractmethod
    def black_symbol(cls):
        pass

    @classmethod
    @abstractmethod
    def unique_attacking_moves(cls):
        pass

    @classmethod
    @abstractmethod
    def is_sliding_piece(cls):
        pass

    @abstractmethod
    def potential_moves(self, orientation):
        pass

