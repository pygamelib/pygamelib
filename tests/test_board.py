from gamelib.Board import Board
from gamelib.BoardItem import BoardItem, BoardItemVoid
from gamelib.HacExceptions import HacOutOfBoardBoundException
import unittest

class TestBoard(unittest.TestCase):
    def test_create_board(self):
        self.board = Board(name='test_board',size=[10,10],player_starting_position=[5,5])
        self.assertEqual(self.board.name,'test_board')

    def test_item(self):
        self.board = Board(name='test_board',size=[10,10],player_starting_postiion=[5,5])
        self.placed_item = BoardItem()

        self.board.place_item(item=self.placed_item,row=1,column=1)
        self.returned_item = self.board.item(1,1)
        self.assertEqual(self.placed_item, self.returned_item)

        with self.assertRaises(HacOutOfBoardBoundException) as excinfo:
            self.board.item(15,15)
        self.assertTrue("out of the board boundaries" in str(excinfo.exception))

    def test_clear_cell(self):
        self.board = Board(name='test_board',size=[10,10],player_starting_postiion=[5,5])
        self.placed_item = BoardItem()
        self.board.place_item(item=self.placed_item,row=1,column=1)
        self.assertIsInstance(self.board.item(1,1), BoardItem)

        self.board.clear_cell(1,1)
        self.assertIsInstance(self.board.item(1,1), BoardItemVoid)


if __name__ == '__main__':
    unittest.main()
