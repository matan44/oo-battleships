class ShipCell:

    def __init__(self, parent_ship, hits_needed_to_destroy):
        self.parent_ship = parent_ship
        self.hits_needed_to_destroy = hits_needed_to_destroy
        self.hits_taken = 0

    def take_hit(self):
        self.hits_taken += 1

    @property
    def is_destroyed(self):
        return self.hits_taken == self.hits_needed_to_destroy


class ShipType:
    ship_types = {
        'P': 1,
        'Q': 2,
    }

    def __init__(self, ship_type):
        if ship_type not in self.ship_types:
            raise ValueError('Ship type must be one of {types}'.format(types=list(self.ship_types.keys())))
        self.name = ship_type
        self.hits_needed_to_destroy_cell = self.ship_types[ship_type]


class Ship:

    def __init__(self, ship_type_name, width, height):
        self.ship_type = ShipType(ship_type_name)
        self.width = width
        self.height = height
        self.cells = [
            [
                ShipCell(parent_ship=self, hits_needed_to_destroy=self.ship_type.hits_needed_to_destroy_cell)
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

    @property
    def is_destroyed(self):
        return all([cell.is_destroyed for row in self.cells for cell in row])

    def __str__(self):
        return f'Ship {self.ship_type.name}({self.width},{self.height})'

    def __repr__(self):
        return self.__str__()