class ShipCell:

    def __init__(self, hits_needed_to_destroy):
        self.hits_needed_to_destroy = hits_needed_to_destroy
        self.hits_taken = 0

    def take_hit(self):
        self.hits_taken += 1

    @property
    def is_destroyed(self):
        return self.hits_taken == self.hits_needed_to_destroy


class ShipType:
    ship_types = {
        'Q': 1,
        'P': 2,
    }

    def __init__(self, ship_type):
        if ship_type not in self.ship_types:
            raise ValueError('Ship type must be one of {types}'.format(types=list(self.ship_types.keys())))
        self.hits_needed_to_destroy_cell = self.ship_types[ship_type]


class Ship:

    def __init__(self, ship_type_name, width, height):
        self.ship_type = ShipType(ship_type_name)
        self.width = width
        self.height = height
        self.cells = [
            [
                ShipCell(hits_needed_to_destroy=self.ship_type.hits_needed_to_destroy_cell)
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]
