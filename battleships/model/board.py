from .. import constants
from . import ship


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [self.width * [None] for _ in range(self.height)]
        self.ships = []

    def _check_ship_fits(self, new_ship, x, y):
        for ship_y in range(new_ship.height):
            for ship_x in range(new_ship.width):
                try:
                    if isinstance(self.cells[ship_y + y][ship_x + x], ship.ShipCell):
                        return False
                except IndexError:
                    return False
        return True

    def add_ship(self, ship_type, width, height, x, y):
        new_ship = ship.Ship(ship_type_name=ship_type, width=width, height=height)
        if not self._check_ship_fits(new_ship, x, y):
            raise ValueError('The new ship does not fit')
        for ship_y in range(new_ship.height):
            for ship_x in range(new_ship.width):
                self.cells[ship_y + y][ship_x + x] = new_ship.cells[ship_y][ship_x]
        self.ships.append(new_ship)

    def take_hit(self, x, y):
        try:
            cell = self.cells[y][x]
        except IndexError:
            return constants.OUT_OF_BOUNDS
        if cell is None:
            return constants.MISS
        cell.take_hit()
        return constants.HIT

    @property
    def remaining_ships(self):
        return len([remaining_ship for remaining_ship in self.ships if not remaining_ship.is_destroyed])

    def __str__(self):
        return f'Board {self.width}x{self.height} ({len(self.ships)} ships)'

    def __repr__(self):
        return self.__str__()

