class Game:

    def __init__(self, board, player_1, player_2):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2


    def start(self):
        self.board.setup()

