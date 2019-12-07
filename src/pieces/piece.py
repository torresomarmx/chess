from abc import ABC, abstractmethod

class Piece(ABC):

    def __init__(self, color, symbol, orientation):
        self.__color = color
        self.__symbol = symbol
        self.__orientation = orientation
        self.current_position = None

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

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, orientation):
        self.__orientation = orientation

    @staticmethod
    @abstractmethod
    def is_sliding_piece():
        pass

    @staticmethod
    @abstractmethod
    def has_special_moves():
        pass

    @staticmethod
    @abstractmethod
    def get_signature():
        pass

    @abstractmethod
    def get_attacking_moves(self):
        pass

    @abstractmethod
    def get_conditional_attacking_moves(self):
        # moves that are activated only if there is a piece to attack
        pass

    @abstractmethod
    def get_positional_moves(self):
        pass

    @abstractmethod
    def switch_orientation(self):
        pass
