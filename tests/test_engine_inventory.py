from pygamelib import engine
from pygamelib.board_items import Treasure, Wall
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.inv = engine.Inventory()

    def test_add_item(self):
        self.inv.add_item(Treasure(inventory_space=9, name="test", value=10))
        self.assertEqual(self.inv.value(), 10)
        self.assertEqual(self.inv.get_item("test").inventory_space, 9)
        with self.assertRaises(engine.base.PglInventoryException):
            self.inv.add_item(Treasure(inventory_space=9, name=None))
        with self.assertRaises(engine.base.PglInvalidTypeException):
            self.inv.add_item(1)
        with self.assertRaises(engine.base.PglInventoryException):
            self.inv.add_item(Wall())

    def test_empty(self):
        self.inv.empty()
        self.assertEqual(self.inv.value(), 0)
        self.assertEqual(len(self.inv.items_name()), 0)

    def test_search_get_delete(self):
        self.inv.add_item(Treasure(inventory_space=0.5, name="test", value=10))
        self.assertEqual(len(self.inv.search("test")), 1)
        self.assertEqual(self.inv.get_item("test").name, "test")
        with self.assertRaises(engine.base.PglInventoryException) as e:
            self.inv.get_item("crash")
            self.assertEqual(e.error, "no_item_by_that_name")
        self.assertIsNone(self.inv.delete_item("test"))
        with self.assertRaises(engine.base.PglInventoryException) as e:
            self.inv.delete_item("test")
            self.assertEqual(e.error, "no_item_by_that_name")

    def test_str(self):
        self.inv.empty()
        self.assertEqual(
            self.inv.__str__(), "=============\n= inventory =\n============="
        )
        self.inv.add_item(
            Treasure(inventory_space=0.5, name="test", value=10, model="$")
        )
        self.inv.add_item(
            Treasure(inventory_space=0.5, name="test", value=10, model="$")
        )
        self.assertEqual(
            self.inv.__str__(), "=============\n= inventory =\n=============\n$ : 1.0"
        )


if __name__ == "__main__":
    unittest.main()
