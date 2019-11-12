from src.util.chess_constants import BLACK_COLOR

class King:
    BLACK_SYMBOL = "♚"
    WHITE_SYMBOL = "♔"
    STARTER_Y_INDEX = 4

    def __init__(self, x_position, y_position, color):
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.symbol = King.BLACK_SYMBOL if self.color == BLACK_COLOR else King.WHITE_SYMBOL