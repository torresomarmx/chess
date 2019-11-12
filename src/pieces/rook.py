from src.util.chess_constants import BLACK_COLOR

class Rook:
    BLACK_SYMBOL = "♜"
    WHITE_SYMBOL = "♖"
    STARTER_Y_INDICES = (0, 7)

    def __init__(self, x_position, y_position, color):
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.__symbol = Rook.BLACK_SYMBOL if self.color == BLACK_COLOR else Rook.WHITE_SYMBOL

    @property
    def symbol(self):
        return self.__symbol


