from gamelib.Board import Board
from gamelib.HacExceptions import HacException
import unittest

class TestBoard(unittest.TestCase):
    def test_create_board(self):
        self.board = Board(name='test_board',size=[10,10],player_starting_position=[5,5])
        self.assertEqual(self.board.name,'test_board')

    def test_sanity_size_is_list(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name='test_board',size="bad",player_starting_position=[5,5])

        self.assertTrue('must be a list.' in str(context.exception))

    def test_sanity_size_has_two_elements(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name='test_board',size=["one"],player_starting_position=[5,5])

        self.assertTrue('must be a list of 2 elements' in str(context.exception))

    def test_sanity_size_element_one_int(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name='test_board',size=["one", "two"],player_starting_position=[5,5])

        self.assertTrue('first element of the' in str(context.exception))

    def test_sanity_size_element_two_int(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name='test_board',size=[10, "two"],player_starting_position=[5,5])

        self.assertTrue('second element of the' in str(context.exception))

    def test_sanity_name_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],player_starting_position=[5,5])

        self.assertTrue('must be a string' in str(context.exception))

    def test_sanity_ui_border_bottom_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],ui_border_bottom=[])

        self.assertTrue('must be a string' in str(context.exception))

    def test_sanity_ui_border_top_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],ui_border_top=[])

        self.assertTrue('must be a string' in str(context.exception))

    def test_sanity_ui_border_left_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],ui_border_left=[])

        self.assertTrue('must be a string' in str(context.exception))

    def test_sanity_ui_border_right_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],ui_border_right=[])

        self.assertTrue('must be a string' in str(context.exception))

    def test_sanity_ui_board_void_cell_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100,size=[10, 10],ui_board_void_cell=[])

        self.assertTrue('must be a string' in str(context.exception))

if __name__ == '__main__':
    unittest.main()