"""This module contains the Inventory class.
"""
from gamelib.BoardItem import BoardItem
from gamelib.HacExceptions import HacInvalidTypeException, HacInventoryException
import uuid


class Inventory:
    """A class that represent the Player (or NPC) inventory.

    This class is pretty straightforward: it is an object container, you can add, get
    and remove items and you can get a value from the objects in the inventory.

    The constructor takes only one parameter: the maximum size of the inventory. Each
    :class:`~gamelib.BoardItem.BoardItem` that is going to be put in the inventory has a
    size (default is 1), the total addition of all these size cannot exceed max_size.

    :param max_size: The maximum size of the inventory. Deafult value: 10.
    :type max_size: int

    .. note:: You can print() the inventory. This is mostly useful for debug as you want
        to have a better display in your game.

    .. warning:: The :class:`~gamelib.Game.Game` engine and
        :class:`~gamelib.Characters.Player` takes care to initiate an inventory for the
        player, you don't need to do it.

    """

    def __init__(self, max_size=10):
        self.max_size = max_size
        self.__items = {}

    def __str__(self):
        s = "=============\n"
        s += "= inventory =\n"
        s += "============="
        types = {}
        for k in self.__items.keys():
            if self.__items[k].type in types.keys():
                types[self.__items[k].type]["size"] += self.__items[k].size()
            else:
                types[self.__items[k].type] = {
                    "size": self.__items[k].size(),
                    "model": self.__items[k].model,
                }
        for k in types.keys():
            s += f"\n{types[k]['model']} : {types[k]['size']}"
        return s

    def add_item(self, item):
        """Add an item to the inventory.

        This method will add an item to the inventory unless:
         * it is not an instance of :class:`~gamelib.BoardItem.BoardItem`,
         * you try to add an item that is not pickable,
         * there is no more space left in the inventory (i.e: the cumulated size of the
            inventory + your item.size is greater than the inventory max_size)

        :param item: the item you want to add
        :type item: :class:`~gamelib.BoardItem.BoardItem`
        :raises: HacInventoryException, HacInvalidTypeException

        Example::

            item = Treasure(model=Sprites.MONEY_BAG,size=2,name='Money bag')
            try:
                mygame.player.inventory.add_item(item)
            expect HacInventoryException as e:
                if e.error == 'not_enough_space':
                    print(f"Impossible to add {item.name} to the inventory, there is no"
                    "space left in it!")
                    print(e.message)
                elif e.error == 'not_pickable':
                    print(e.message)

        .. warning:: if you try to add more than one item with the same name (or if the
            name is empty), this function will automatically change the name of the item
            by adding a UUID to it.

        """
        if isinstance(item, BoardItem):
            if item.pickable():
                if (
                    item.name is None
                    or item.name == ""
                    or item.name in self.__items.keys()
                ):
                    item.name += "_" + uuid.uuid4().hex
                if (
                    hasattr(item, "_size")
                    and self.max_size >= self.size() + item.size()
                ):
                    self.__items[item.name] = item
                else:
                    raise HacInventoryException(
                        "not_enough_space",
                        "There is not enough space left in the inventory. Max. size: "
                        + self.max_size
                        + ", current inventory size: "
                        + self.size()
                        + " and item size: "
                        + item.size(),
                    )
            else:
                raise HacInventoryException(
                    "not_pickable",
                    f"The item (name='{item.name}') is not pickable. Make sure to only "
                    "add pickable objects to the inventory.",
                )
        else:
            raise HacInvalidTypeException(
                "The item is not an instance of BoardItem. The item is of type: "
                + type(item)
            )

    def size(self):
        """
        Return the cumulated size of the inventory.
        It can be used in the UI to display the size compared to max_size for example.

        :return: size of inventory
        :rtype: int

        Example::

            print(f"Inventory: {mygame.player.inventory.size()}/"
            "{mygame.player.inventory.max_size}")
        """
        val = 0
        for k in self.__items.keys():
            if hasattr(self.__items[k], "size"):
                val += self.__items[k].size()
        return val

    def value(self):
        """
        Return the cumulated value of the inventory.
        It can be used for scoring for example.

        :return: value of inventory
        :rtype: int

        Example::

            if inventory,value() >= 10:
                print('Victory!')
                break
        """
        val = 0
        for k in self.__items.keys():
            if hasattr(self.__items[k], "value"):
                val += self.__items[k].value
        return val

    def items_name(self):
        """Return the list of all items names in the inventory.

        :return: a list of string representing the items names.
        :rtype: list

        """
        return self.__items.keys()

    def search(self, query):
        """Search for objects in the inventory.

        All objects that matches the query are going to be returned.
        :param query: the query that items in the inventory have to match to be returned
        :type name: str
        :returns: a table of BoardItems.
        :rtype: list

        Example::

            for item in game.player.inventory.search('mighty'):
                print(f"This is a mighty item: {item.name}")
        """
        return [item for key, item in self.__items.items() if query in key]

    def get_item(self, name):
        """Return the item corresponding to the name given in argument.

        :param name: the name of the item you want to get.
        :type name: str
        :return: An item.
        :rtype: :class:`~gamelib.BoardItem.BoardItem`
        :raises: HacInventoryException

        .. note:: in case an execpetion is raised, the error will be
            'no_item_by_that_name' and the message is giving the specifics.

        .. seealso:: :class:`gamelib.HacExceptions.HacInventoryException`.

        Example::

            life_container = mygame.player.inventory.get_item('heart_1')
            if isinstance(life_container,GenericActionableStructure):
                life_container.action(life_container.action_parameters)

        .. note:: Please note that the item object reference is returned but nothing is
            changed in the inventory. The item hasn't been removed.

        """
        if name in self.__items.keys():
            return self.__items[name]
        else:
            raise HacInventoryException(
                "no_item_by_that_name",
                f'There is no item named "{name}" in the inventory.',
            )

    def delete_item(self, name):
        """Delete the item corresponding to the name given in argument.

        :param name: the name of the item you want to delete.
        :type name: str

        .. note:: in case an execpetion is raised, the error will be
            'no_item_by_that_name' and the message is giving the specifics.

        .. seealso:: :class:`gamelib.HacExceptions.HacInventoryException`.

        Example::

            life_container = mygame.player.inventory.get_item('heart_1')
            if isinstance(life_container,GenericActionableStructure):
                life_container.action(life_container.action_parameters)
                mygame.player.inventory.delete_item('heart_1')

        """
        if name in self.__items.keys():
            del self.__items[name]
        else:
            raise HacInventoryException(
                "no_item_by_that_name",
                f'There is no item named "{name}" in the inventory.',
            )
