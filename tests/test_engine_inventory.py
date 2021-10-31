from pygamelib import engine
from pygamelib.board_items import Treasure, Wall
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class SuperTreasure(Treasure):
    def __init__(self, value=10, **kwargs):
        super().__init__(value=value, **kwargs)


class SuperTreasureBork(Treasure):
    def __init__(self, value=10, **kwargs):
        super().__init__(value=value, **kwargs)

    @classmethod
    def load(cls, data):
        raise Exception()


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
        self.assertEqual(e.exception.error, "no_item_by_that_name")
        self.assertIsNone(self.inv.delete_item("test"))
        with self.assertRaises(engine.base.PglInventoryException) as e:
            self.inv.delete_item("test")
        self.assertEqual(e.exception.error, "no_item_by_that_name")

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

    def test_serialization(self):
        inv = engine.Inventory()
        inv.add_item(SuperTreasure(name="Super Treasure"))
        inv.add_item(Treasure(name="Normal Treasure"))
        data = inv.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["max_size"], inv.max_size)
        invl = engine.Inventory.load(data)
        self.assertEqual(inv.size(), invl.size())
        inv.add_item(SuperTreasureBork(name="Super Bork"))
        data = inv.serialize()
        with self.assertRaises(Exception):
            engine.Inventory.load(data)


if __name__ == "__main__":
    unittest.main()
