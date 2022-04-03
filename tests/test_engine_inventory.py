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
        self.assertEqual(len(self.inv.items), 0)

    def test_search_get_delete(self):
        self.inv.add_item(Treasure(inventory_space=0.5, name="test", value=10))
        self.assertEqual(len(self.inv.search("test")), 1)
        self.assertEqual(self.inv.get_item("test").name, "test")
        self.assertIsNone(self.inv.delete_item("test"))
        self.assertEqual(self.inv.search(None), [])

    def test_get_items(self):
        inv = engine.Inventory()
        for _ in range(5):
            inv.add_item(
                Treasure(
                    inventory_space=1,
                    name="Money Bag",
                    item_type="currency",
                    value=10,
                    model="O",
                )
            )
            inv.add_item(
                Treasure(
                    inventory_space=1,
                    name="Gold Coin",
                    item_type="currency",
                    value=1,
                    model="o",
                )
            )
        self.assertEqual(len(inv.items), 10)
        self.assertEqual(len(inv.get_items("Money Bag")), 5)
        self.assertEqual(len(inv.get_items("Gold Coin")), 5)

    def test_delete_items(self):
        inv = engine.Inventory()
        for _ in range(5):
            inv.add_item(
                Treasure(
                    inventory_space=1,
                    name="Money Bag",
                    item_type="currency",
                    value=10,
                    model="O",
                )
            )
            inv.add_item(
                Treasure(
                    inventory_space=1,
                    name="Gold Coin",
                    item_type="currency",
                    value=1,
                    model="o",
                )
            )
        self.assertEqual(len(inv.items), 10)
        inv.delete_items("Money Bag")
        self.assertEqual(len(inv.items), 5)

    def test_constraints(self):
        inv = engine.Inventory()
        inv.add_constraint("max_gold_coin", item_name="Gold Coin", max_number=1)
        self.assertEqual(len(inv.constraints), 1)
        inv.add_constraint("max_money_bag", item_name="Money Bag", max_number=5)
        self.assertEqual(len(inv.constraints), 2)
        inv.remove_constraint("max_money_bag")
        self.assertEqual(len(inv.constraints), 1)
        # Ok
        inv.add_item(
            Treasure(
                inventory_space=1,
                name="Gold Coin",
                item_type="currency",
                value=1,
                model="o",
            )
        )
        self.assertEqual(len(inv.items), 1)
        # # KO
        with self.assertRaises(engine.base.PglInventoryException):
            inv.add_item(
                Treasure(
                    inventory_space=1,
                    name="Gold Coin",
                    item_type="currency",
                    value=1,
                    model="o",
                )
            )
        inv.clear_constraints()
        self.assertEqual(len(inv.constraints), 0)
        with self.assertRaises(engine.base.PglInventoryException) as context:
            inv.add_constraint("fail")
        self.assertEqual(context.exception.args[0], "invalid_constraint")
        with self.assertRaises(engine.base.PglInventoryException) as context:
            inv.add_constraint("", item_name="fail")
        self.assertEqual(context.exception.args[0], "invalid_constraint")

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
