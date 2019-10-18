from gamelib.Board import Board
from gamelib.BoardItem import BoardItem, BoardItemVoid
from gamelib.HacExceptions import HacOutOfBoardBoundException
import unittest


class TestBoard(unittest.TestCase):
    def test_create_board(self):
        self.board = Board(
            name="test_board", size=[10, 10], player_starting_position=[5, 5]
        )
        self.assertEqual(self.board.name, "test_board")

    def test_sanity_size_is_list(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(
                name="test_board", size="bad", player_starting_position=[5, 5]
            )

        self.assertTrue("must be a list." in str(context.exception))

    def test_sanity_size_has_two_elements(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(
                name="test_board", size=["one"], player_starting_position=[5, 5]
            )

        self.assertTrue("must be a list of 2 elements" in str(context.exception))

    def test_sanity_size_element_one_int(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(
                name="test_board", size=["one", "two"], player_starting_position=[5, 5]
            )

        self.assertTrue("first element of the" in str(context.exception))

    def test_sanity_size_element_two_int(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(
                name="test_board", size=[10, "two"], player_starting_position=[5, 5]
            )

        self.assertTrue("second element of the" in str(context.exception))

    def test_sanity_name_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], player_starting_position=[5, 5])

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_bottom_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], ui_border_bottom=[])

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_top_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], ui_border_top=[])

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_left_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], ui_border_left=[])

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_border_right_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], ui_border_right=[])

        self.assertTrue("must be a string" in str(context.exception))

    def test_sanity_ui_board_void_cell_string(self):
        with self.assertRaises(Exception) as context:
            self.board = Board(name=100, size=[10, 10], ui_board_void_cell=[])

        self.assertTrue("must be a string" in str(context.exception))

    def test_item(self):
        self.board = Board(
            name="test_board", size=[10, 10], player_starting_position=[5, 5]
        )
        self.placed_item = BoardItem()

        self.board.place_item(self.placed_item, 1, 1)
        self.returned_item = self.board.item(1, 1)
        self.assertEqual(self.placed_item, self.returned_item)

        with self.assertRaises(HacOutOfBoardBoundException) as excinfo:
            self.board.item(15, 15)
        self.assertTrue("out of the board boundaries" in str(excinfo.exception))

    def test_clear_cell(self):
        self.board = Board(
            name="test_board", size=[10, 10], player_starting_position=[5, 5]
        )
        self.placed_item = BoardItem()
        self.board.place_item(item=self.placed_item, row=1, column=1)
        self.assertIsInstance(self.board.item(1, 1), BoardItem)

        self.board.clear_cell(1, 1)
        self.assertIsInstance(self.board.item(1, 1), BoardItemVoid)


if __name__ == "__main__":
    unittest.main()
