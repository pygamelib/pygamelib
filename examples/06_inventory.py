import examples_includes  # noqa: F401
from gamelib.Inventory import Inventory
from gamelib.Structures import Treasure

inv = Inventory(max_size=5)
print("Inventory size:" + str(inv.size()))
print("Adding a new item to inventory")
inv.add_item(Treasure(name="money"))
print("Inventory size:" + str(inv.size()))
print("Adding a new item to inventory")
inv.add_item(Treasure(name="money"))
print("Inventory size:" + str(inv.size()))
print("Adding a new item to inventory")
inv.add_item(Treasure(name="money"))
print("Inventory size:" + str(inv.size()))
print("Adding a new item to inventory")
inv.add_item(Treasure(name="money"))
print("Inventory size:" + str(inv.size()))
print("Adding a new item to inventory")
inv.add_item(Treasure(name="money"))
print("Inventory size:" + str(inv.size()))

print(inv)
print("Inventory value:" + str(inv.value()))

print("Retrieving item named 'money':" + str(inv.get_item("money")))
print("Deleting this item from inventory")
inv.delete_item("money")
print("Inventory size:" + str(inv.size()))
print("Inventory value:" + str(inv.value()))
print(inv)
