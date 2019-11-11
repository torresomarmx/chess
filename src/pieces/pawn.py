from src.util.chess_constants import BLACK_COLOR

class Pawn:
    BLACK_SYMBOL = "♟"
    WHITE_SYMBOL = "♙"

    def __init__(self, x_position, y_position, color):
        self.x_position = x_position
        self.y_position = y_position
        self.position_tuple = (x_position, y_position)
        self.color = color
        self.symbol = Pawn.BLACK_SYMBOL if self.color == BLACK_COLOR else Pawn.WHITE_SYMBOL




