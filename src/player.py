class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color