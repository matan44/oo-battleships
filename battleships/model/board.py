from .. import constants


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [self.width * [None] for _ in range(self.height)]

    def add_ship(self, type, x, y):
        pass

    def take_hit(self, x, y):
        return constants.MISS
