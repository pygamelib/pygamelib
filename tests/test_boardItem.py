import pygamelib.board_items as pgl_board_items
import unittest


class TestBoard(unittest.TestCase):
    def test_create_default_boardItem(self):
        self.boardItem = pgl_board_items.BoardItem()
        self.assertEqual(self.boardItem.name, "Board item")
        self.assertEqual(self.boardItem.type, "item")
        self.assertEqual(self.boardItem.pos, [None, None])
        self.assertEqual(self.boardItem.model, "*")

    def test_create_custom_boardItem(self):
        self.boardItem = pgl_board_items.BoardItem(
            name="test_boardItem", type="test_type", pos=[10, 10], model="test_model"
        )
        self.assertEqual(self.boardItem.name, "test_boardItem")
        self.assertEqual(self.boardItem.type, "test_type")
        self.assertEqual(self.boardItem.pos, [10, 10])
        self.assertEqual(self.boardItem.model, "test_model")


if __name__ == "__main__":
    unittest.main()
