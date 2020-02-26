from .model import board, player
from . import constants


class GameClient:

    def __init__(self):
        self.current_player = None
        self.opposite_player = None
        self.ships_no = 0
        self.game_status = constants.IN_PROGRESS

    @staticmethod
    def _input(message=None):
        return input(message)

    def _input_coordinates(self, message=None):
        s = self._input(message)
        x = int(s[1]) - 1
        y = ord(s[0]) - 97
        return x, y

    def _input_board_dimensions(self):
        return self._input_coordinates('Board dimensions: (Format X Y, e.g. A 4): ')

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
        self._input_player_ships(player=self.current_player)
        self._input_player_ships(player=self.opposite_player)

    def _get_game_status(self):
        if self.opposite_player.board.remaining_ships == 0:
            return constants.VICTORY

        if self.current_player.missiles_remaining == 0 and self.opposite_player.missiles_remaining == 0:
            return constants.DRAW

        return constants.IN_PROGRESS

    def _end_turn(self, result):
        if result == constants.MISS and self.opposite_player.remaining_missiles == 0:
            self.current_player, self.opposite_player = self.opposite_player, self.current_player

    def _input_ship_no(self):
        s = input('Number of ships')
        self.ships_no = int(s[1])

    def _input_player_ships(self, player):
        pass

    def _input_target_coordinates(self):
        return self._input_coordinates(
            f'Player {self.current_player.name} target coordinates (Format XY, e.g. A4): '
        )

    def _end_game(self):
        if self.game_status == constants.DRAW:
            print('Draw')
        print(f'Player {self.current_player.name} wins')

    def _hit_opposite_player(self):
        while True:
            x, y = self._input_target_coordinates()
            result = self.opposite_player.board.take_hit(x, y)
            if result == constants.OUT_OF_BOUNDS:
                continue
            return result

    def play(self):
        self._set_up_game()

        while True:
            print('Player {name}\'s turn'.format(name=self.current_player.name))
            result = self._hit_opposite_player()
            self.game_status = self._get_game_status()
            if self.game_status != constants.IN_PROGRESS:
                break
            self._end_turn(result)
        self._end_game()

