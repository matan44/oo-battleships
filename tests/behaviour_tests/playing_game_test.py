from unittest import TestCase, mock

from battleships import game
from battleships import constants


@mock.patch.object(game.Game, '_output')
class GameInputsTestCase(TestCase):

    @mock.patch.object(game.Game, '_input', side_effect=['5 E', '2', 'Q 1 1 A1'])
    def test_game_setup_too_few_ships(self, _input, _output):
        test_game = game.Game()
        with self.assertRaisesRegex(ValueError, 'Number of ships provided much match game settings'):
            test_game.play()

    @mock.patch.object(game.Game, '_input', side_effect=['5 E', '2', 'Q 1 1 A1 P 1 1 A1'])
    def test_game_setup_ships_do_not_fit(self, _input, _output):
        test_game = game.Game()
        with self.assertRaisesRegex(ValueError, 'The new ship does not fit'):
            test_game.play()

    @mock.patch.object(game.Game, '_input', side_effect=[
        '5 E',
        '2',
        'Q 1 1 A1 P 1 1 B2',
        'Q 1 1 A1 P 1 1 B2',
        'A1',
        'A1',
        'B2',
    ])
    def test_game_one_turn_victory(self, _input, _output):
        test_game = game.Game()
        test_game.play()
        self.assertEqual(test_game.game_status, constants.VICTORY)
        self.assertEqual(test_game.opposite_player.remaining_missiles, 99)

    @mock.patch.object(game.Game, '_input', side_effect=[
        '5 E', '2', 'Q 1 1 A1 P 1 1 B2', 'Q 1 1 A1 P 1 1 B2',
    ] + (['C1'] * 99) + (['D1'] * 99))
    def test_game_draw(self, _input, _output):
        test_game = game.Game()
        test_game.play()
        self.assertEqual(test_game.game_status, constants.DRAW)
