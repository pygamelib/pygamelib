import examples_includes  # noqa: F401
from pygamelib import engine, base, constants
from pygamelib.gfx import core
from pygamelib.board_items import Treasure
from pygamelib.assets import graphics

print(
    base.Text(
        "\n\nPlease note that this example is supposed to finish by raising an "
        "exception.\n",
        core.Color(0, 255, 0),
        style=constants.BOLD + constants.UNDERLINE,
    )
)
print(
    base.Text(
        "It is not a bug, it is a feature!\n(hit any key to continue).\n\n",
        core.Color(0, 255, 0),
        style=constants.BOLD,
    )
)
engine.Game.get_key()


# In version 1.3.0, the Inventory class was revamped. It is now a PglBaseObject and uses
# the new observer pattern to notify observers when an item is added or removed.
# So let's create a Notifier class that will be notified when an item or a constraint is
# added or removed.
# IMPORTANT: This is completely optional, you can use the inventory in its most simple
# form, by just adding and removing items.
class Notifier(base.PglBaseObject):
    # The only job of this class is to implement the observer pattern and print
    # something when an event occurs in the inventory.
    # We could do stuff like play a sound or display a message on the screen instead.
    def handle_notification(self, subject, attribute=None, value=None):
        print(
            f"NOTIFICATION: subject={type(subject)} attribute={attribute} value={value}"
        )


# Create an inventory and attach a notifier to it.
inv = engine.Inventory()
inv.attach(Notifier())

# Add some items to the inventory.
for _ in range(5):
    inv.add_item(
        Treasure(
            inventory_space=1,
            name="Money Bag",
            item_type="currency",
            value=10,
            model=graphics.Models.MONEY_BAG,
        )
    )
    inv.add_item(
        Treasure(
            inventory_space=1,
            name="Gold Coin",
            item_type="currency",
            value=1,
            model=graphics.Models.COIN,
        )
    )

# Print the inventory.
print(inv)
print(f"Inventory size: {inv.size()}")
print(f"List of objects in the inventory (by names): {inv.items_name()}")
print(f"Inventory value: {inv.value()}")
print(f"List of items matching the search for 'Money Bag':{inv.search('Money Bag')}")
# This prints the first item that matches the parameter.
print(f"Retrieving item named 'Gold Coin': {inv.get_item('Gold Coin')}")
# The inventory is serializable if you so wish.
# print(inv.serialize())

# This deletes the first item that matches the parameter.
inv.delete_item("Gold Coin")
# Let's print the inventory again.
print(inv)
# This deletes ALL items that matches the parameter.
inv.delete_items("Gold Coin")
# Let's print the inventory again.
print(inv)

# Now let's see how constraints work.
# First, let's add constraints.
inv.add_constraint("max_money_bag", item_name="Money Bag", max_number=5)
print(f"Active constraintes: {len(inv.constraints)}")
inv.add_constraint("max_gold_coin", item_name="Gold Coin", max_number=5)
print(f"Active constraintes: {len(inv.constraints)}")

# Then remove constraints.
inv.remove_constraint("max_gold_coin")
print(f"Active constraintes: {len(inv.constraints)}")

# And clear all of the constraints.
inv.clear_constraints()
print(f"Active constraintes: {len(inv.constraints)}")

# Now add a constraint that will not allow you to add more than one gold coin.
inv.add_constraint("max_gold_coin", item_name="Gold Coin", max_number=1)
print(f"Active constraintes: {len(inv.constraints)}")
# The first item is added to the inventory, the constraint is not violated.
inv.add_item(
    Treasure(
        inventory_space=1,
        name="Gold Coin",
        item_type="currency",
        value=1,
        model=graphics.Models.COIN,
    )
)
# The second gold coin is not added to the inventory, the constraint is violated.
# An exception is raised.
inv.add_item(
    Treasure(
        inventory_space=1,
        name="Gold Coin",
        item_type="currency",
        value=1,
        model=graphics.Models.COIN,
    )
)
