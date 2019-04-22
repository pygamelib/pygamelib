from gamelib.Board import Board
import unittest

class TestBoard(unittest.TestCase):
    def test_create_board(self):
        self.board = Board(name='test_board',size=[10,10],player_starting_position=[5,5])
        self.assertEqual(self.board.name,'test_board')


if __name__ == '__main__':
    unittest.main()