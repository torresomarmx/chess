# maybe ArtifactMove
class MovePlayed:
    def __init__(self, piece_signature, old_position, new_position):
        # copy piece, or turn piece into string
        self.__piece_signature = piece_signature
        self.__old_position = old_position
        self.__new_position = new_position

    @property
    def piece_signature(self):
        return self.__piece_signature

    @property
    def old_position(self):
        return self.__old_position

    @property
    def new_position(self):
        return self.__new_position
