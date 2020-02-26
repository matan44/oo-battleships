from .model import board, player
from . import constants


class Game:

    def __init__(self):
        self.current_player = None
        self.opposite_player = None
        self.ships_no = 0
        self.game_status = constants.IN_PROGRESS

    @staticmethod
    def _input(message=None):
        return input(message).strip()

    @staticmethod
    def _output(message):
        return print(message)

    def _input_coordinates(self, message=None):
        s = self._input(message).lower()
        x = int(s[1]) - 1
        y = ord(s[0]) - 97
        return x, y

    def _input_board_dimensions(self):
        s = self._input('Board dimensions: (Format X Y, e.g. 3 C): ').split()
        x = int(s[0])
        y = ord(s[1].lower()) - 96
        return x, y

    def _set_up_game(self):
        height, width = self._input_board_dimensions()
        self.current_player = player.Player(
            name='1',
            remaining_missiles=99,
            board=board.Board(width=width, height=height)
        )
        self.opposite_player = player.Player(
            name='2',
            remaining_missiles=99,
            board=board.Board(width=width, height=height)
        )
        self._input_ship_no()
        self._input_player_ships(target_player=self.current_player)
        self._input_player_ships(target_player=self.opposite_player)

    def _get_game_status(self):
        if self.opposite_player.board.remaining_ships == 0:
            return constants.VICTORY

        if self.current_player.remaining_missiles == 0 and self.opposite_player.remaining_missiles == 0:
            return constants.DRAW

        return constants.IN_PROGRESS

    def _end_turn(self, result):
        if result == constants.MISS and not self.opposite_player.remaining_missiles == 0:
            self.current_player, self.opposite_player = self.opposite_player, self.current_player

    def _input_ship_no(self):
        s = self._input('Number of ships per player: ')
        self.ships_no = int(s)

    def _input_player_ships(self, target_player):
        s = self._input('Ships coordinates: (Format TYPE LENGTH HEIGHT XY, e.g. Q 1 1 A1): ')
        split_input_s = s.split()
        if len(split_input_s) % 4 != 0:
            raise ValueError('Must input groups of 4 space separated inputs')
        if len(split_input_s) / 4 != self.ships_no:
            raise ValueError('Number of ships provided much match game settings')
        for i in range(0, len(split_input_s), 4):
            ship_inputs = split_input_s[i:i + 4]
            try:
                width = int(ship_inputs[1])
                height = int(ship_inputs[2])
                y = ord(ship_inputs[3][0].lower()) - 97
                x = int(ship_inputs[3][1]) - 1
            except (ValueError, IndexError):
                raise ValueError('Ships input much match format')
            target_player.board.add_ship(
                ship_type=ship_inputs[0],
                width=width,
                height=height,
                x=x,
                y=y
            )

    def _end_game(self):
        if self.game_status == constants.DRAW:
            self._output('Draw')
        self._output(f'Player {self.current_player.name} wins')

    def _hit_opposite_player(self):
        while True:
            x, y = self._input_coordinates(
                f'Player {self.current_player.name} target coordinates (Format XY, e.g. A4): '
            )
            result = self.opposite_player.board.take_hit(x, y)
            if result == constants.OUT_OF_BOUNDS:
                continue
            self.current_player.remaining_missiles -= 1
            return result

    def play(self):
        self._set_up_game()

        while True:
            self._output('Player {name}\'s turn'.format(name=self.current_player.name))
            result = self._hit_opposite_player()
            self._output(f'Result: {result}')
            self.game_status = self._get_game_status()
            if self.game_status != constants.IN_PROGRESS:
                break
            self._end_turn(result)
        self._end_game()

