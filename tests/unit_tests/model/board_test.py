from unittest import TestCase, mock

from battleships.model import board
from battleships.model import ship
from battleships import constants


class BoardBaseTestCase(TestCase):

    @staticmethod
    def get_mock_cell():
        mock_cell = mock.create_autospec(ship.ShipCell)
        return mock_cell

    def get_mock_ship(self):
        mock_ship = mock.create_autospec(ship.Ship)
        mock_ship.height = 1
        mock_ship.width = 1
        mock_ship.cells = [[self.get_mock_cell]]
        return mock_ship


class BoardTestCaseInit(BoardBaseTestCase):

    def test_init(self):
        width = 5
        height = 2
        test_board = board.Board(width=width, height=height)
        self.assertEqual(test_board.width, width)
        self.assertEqual(test_board.height, height)
        self.assertEqual(len(test_board.cells), height)
        self.assertListEqual([len(row) for row in test_board.cells], [width] * height)


class BoardTestCaseCheckShipFits(BoardBaseTestCase):

    def test_check_ship_fits_out_of_range(self):
        test_board = board.Board(width=1, height=1)
        mock_ship = self.get_mock_ship()
        mock_ship.height = 2
        mock_ship.width = 3
        self.assertFalse(test_board._check_ship_fits(mock_ship, 1, 1))

    def test_check_ship_fits_cell_taken(self):
        test_board = board.Board(width=1, height=1)
        mock_ship = self.get_mock_ship()
        mock_ship.height = 1
        mock_ship.width = 1
        test_board.cells[0][0] = self.get_mock_cell()
        self.assertFalse(test_board._check_ship_fits(mock_ship, 0, 0))

    def test_check_ship_fits(self):
        test_board = board.Board(width=1, height=1)
        mock_ship = self.get_mock_ship()
        mock_ship.height = 1
        mock_ship.width = 1
        self.assertTrue(test_board._check_ship_fits(mock_ship, 0, 0))


@mock.patch.object(board.Board, '_check_ship_fits')
@mock.patch('battleships.model.ship.Ship', autospec=True)
class BoardTestCaseAddShip(BoardBaseTestCase):

    def test_add_ship_adds_ship(self, mock_ship_class, mock_check_ship_fits):
        mock_ship = self.get_mock_ship()
        mock_ship_class.return_value = mock_ship
        mock_check_ship_fits.return_value = True
        test_board = board.Board(width=1, height=1)
        test_board.add_ship('XX', 3, 4, 0, 0)
        self.assertListEqual(test_board.ships, [mock_ship])

    def test_add_ship_checks_ship_fits(self, mock_ship_class, mock_check_ship_fits):
        mock_ship = self.get_mock_ship()
        mock_ship_class.return_value = mock_ship
        mock_check_ship_fits.return_value = True
        test_board = board.Board(width=1, height=1)
        test_board.add_ship('XX', 3, 4, 0, 0)
        mock_check_ship_fits.assert_called_with(mock_ship, 0, 0)

    def test_add_ship_ship_does_not_fit(self, mock_ship_class, mock_check_ship_fits):
        mock_ship = self.get_mock_ship()
        mock_ship_class.return_value = mock_ship
        mock_check_ship_fits.return_value = False
        test_board = board.Board(width=1, height=1)
        with self.assertRaisesRegex(ValueError, 'The new ship does not fit'):
            test_board.add_ship('XX', 3, 4, 1, 0)
        self.assertListEqual(test_board.ships, [])


class BoardTestCaseTakeHit(BoardBaseTestCase):

    def test_take_hit_out_of_bounds(self):
        test_board = board.Board(width=1, height=1)
        result = test_board.take_hit(3, 3)
        self.assertEqual(result, constants.OUT_OF_BOUNDS)

    def test_take_hit_miss(self):
        test_board = board.Board(width=1, height=1)
        result = test_board.take_hit(0, 0)
        self.assertEqual(result, constants.MISS)

    def test_take_hit_hit(self):
        test_board = board.Board(width=1, height=1)
        test_board.cells = [[self.get_mock_cell()]]
        result = test_board.take_hit(0, 0)
        self.assertEqual(result, constants.HIT)

    def test_take_hit_hits_cell(self):
        test_board = board.Board(width=1, height=1)
        test_board.cells = [[self.get_mock_cell()]]
        test_board.take_hit(0, 0)
        test_board.cells[0][0].take_hit.assert_called_once()

    def test_take_hit_hits_only_right_cell(self):
        test_board = board.Board(width=2, height=1)
        test_board.cells = [[self.get_mock_cell(), self.get_mock_cell()]]
        test_board.take_hit(0, 0)
        test_board.cells[0][1].take_hit.assert_not_called()


class BoardTestCaseRemainingShips(BoardBaseTestCase):

    def test_remaining_ships_no_ships(self):
        test_board = board.Board(width=1, height=1)
        self.assertEqual(test_board.remaining_ships, 0)

    def test_remaining_ships_destroyed(self):
        test_board = board.Board(width=1, height=1)
        mock_ship = self.get_mock_ship()
        mock_ship.is_destroyed = True
        test_board.ships = [mock_ship]
        self.assertEqual(test_board.remaining_ships, 0)

    def test_remaining_ships_one_remaining(self):
        test_board = board.Board(width=1, height=1)
        mock_ship = self.get_mock_ship()
        mock_ship.is_destroyed = True
        mock_ship2 = self.get_mock_ship()
        mock_ship2.is_destroyed = False
        test_board.ships = [mock_ship, mock_ship2]
        self.assertEqual(test_board.remaining_ships, 1)


class BoardTestCaseStr(BoardBaseTestCase):

    def test_str(self):
        test_board = board.Board(width=1, height=1)
        self.assertEqual(str(test_board), 'Board 1x1 (0 ships)')

    def test_str_with_ships(self):
        test_board = board.Board(width=4, height=11)
        mock_ship = self.get_mock_ship()
        mock_ship.is_destroyed = True
        mock_ship2 = self.get_mock_ship()
        mock_ship2.is_destroyed = False
        test_board.ships = [mock_ship, mock_ship2]
        self.assertEqual(str(test_board), 'Board 4x11 (2 ships)')
