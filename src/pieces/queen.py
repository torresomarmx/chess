from src.util.chess_constants import BLACK_COLOR

class Queen:
    BLACK_SYMBOL = "♛"
    WHITE_SYMBOL = "♕"
    DEFAULT_STARTER_Y_INDEX = 3

    def __init__(self, x_position, y_position, color):
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.symbol = Queen.BLACK_SYMBOL if self.color == BLACK_COLOR else Queen.WHITE_SYMBOL