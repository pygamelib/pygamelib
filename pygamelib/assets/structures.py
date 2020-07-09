"""
This module contains many "helpers" classes to populate your game with structures.
It contains many directly usable structures and some generic ones that can be turned
in anything you like.

.. autosummary::
   :toctree: .

   Wall
   Treasure
   Door
   GenericStructure
   GenericActionableStructure

"""
import pygamelib.base as base
import pygamelib.board_items as board_items


class Wall(board_items.Immovable):
    """
    A Wall is a specialized :class:`~pygamelib.board_items.Immovable` object that as
    unmodifiable characteristics:

    * It is not pickable (and cannot be).
    * It is not overlappable (and cannot be).
    * It is not restorable (and cannot be).

    As such it's an object that cannot be moved, cannot be picked up or modified by
    Player or NPC and block their ways. It is therefor advised to create one per board
    and reuse it in many places.

    :param model: The representation of the Wall on the Board.
    :type model: str
    :param name: The name of the Wall.
    :type name: str
    :param size: The size of the Wall. This parameter will probably be deprecated as
        size is only used for pickable objects.
    :type size: int
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "#"
        if "name" not in kwargs.keys():
            kwargs["name"] = "wall"
        if "size" not in kwargs.keys():
            kwargs["size"] = 1
        board_items.Immovable.__init__(self, **kwargs)

    def pickable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be pick-up by player or NPC.

        :return: False
        :rtype: bool

        Example::

            if mywall.pickable():
                print('Whoaa this wall is really light... and small...')
            else:
                print('Really? Trying to pick-up a wall?')
        """
        return False

    def overlappable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be overlapped by player or NPC.

        :return: False
        :rtype: bool
        """
        return False

    def restorable(self):
        """
        This represent the capacity for an :class:`~pygamelib.board_items.Immovable`
        :class:`~pygamelib.board_items.BoardItem`(in this case a Wall item) to be
        restored by the board if the item is overlappable and has been overlapped by
        another :class:`~pygamelib.board_items.Movable` item.
        A wall is not overlappable.

        :return: False
        :rtype: bool
        """
        return False


class GenericStructure(board_items.Immovable):
    """
    A GenericStructure is as the name suggest, a generic object to create all kind of
    structures.

    It can be tweaked with all the properties of
    :class:`~pygamelib.board_items.BoardItem`, :class:`~pygamelib.board_items.Immovable`
    and it can be made pickable, overlappable or restorable or any combination of these.

    If you need an action to be done when a Player and/or a NPC touch the structure
    please have a look at
    :class:`pygamelib.assets.structures.GenericActionableStructure`.

    :param pickable: Define if the structure can be picked-up by a Player or NPC.
    :type pickable: bool
    :param overlappable: Define if the structure can be overlapped by a Player or NPC.
    :type overlappable: bool
    :param restorable: Define if the structure can be restored by the Board after a
        Player or NPC passed through. For example, you want a door or an activator
        structure (see GenericActionableStructure for that) to remain on the board after
        it's been overlapped by a player. But you could also want to develop some kind
        of Space Invaders game were the protection block are overlappable but not
        restorable.
    :type restorable: bool

    On top of these, this object takes all parameters of
    :class:`~pygamelib.board_items.BoardItem` and
    :class:`~pygamelib.board_items.Immovable`

    .. important:: If you need a structure with a permission system please have a look
        at :class:`~pygamelib.assets.structures.GenericActionableStructure`. This class
        has a permission system for activation.

    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "#"
        if "name" not in kwargs.keys():
            kwargs["name"] = "structure"
        board_items.Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs["value"]
        if "pickable" in kwargs.keys():
            self.__is_pickable = kwargs["pickable"]
        else:
            self.__is_pickable = False
        if "overlappable" in kwargs.keys():
            self.__is_overlappable = kwargs["overlappable"]
        else:
            self.__is_overlappable = False

        if "restorable" in kwargs.keys():
            self.__is_restorable = kwargs["restorable"]
        else:
            self.__is_restorable = False

    def pickable(self):
        """This represent the capacity for a BoardItem to be picked-up by player or NPC.

        To set this value please use :meth:`~.set_pickable`

        :return: True or False
        :rtype: bool

        .. seealso:: :meth:`~.set_pickable`
        """
        return self.__is_pickable

    def set_pickable(self, val):
        """Make the structure pickable or not.

        :param val: True or False depending on the pickability of the structure.
        :type val: bool

        Example::

            myneatstructure.set_pickable(True)
        """
        if type(val) is bool:
            self.__is_pickable = val

    def overlappable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be overlapped by player or NPC.

        To set this value please use :meth:`~.set_overlappable`

        :return: False
        :rtype: bool

        .. seealso:: :meth:`~.set_overlappable`
        """
        return self.__is_overlappable

    def set_overlappable(self, val):
        """Make the structure overlappable or not.

        :param val: True or False depending on the fact that the structure can be
            overlapped (i.e that a Player or NPC can step on it) or not.
        :type val: bool

        Example::

            myneatstructure.set_overlappable(True)
        """
        if type(val) is bool:
            self.__is_overlappable = val

    def restorable(self):
        """
        This represent the capacity for an :class:`~pygamelib.board_items.Immovable`
        :class:`~pygamelib.board_items.BoardItem` (in this case a GenericStructure item)
        to be restored by the board if the item is overlappable and has been overlapped
        by another :class:`~pygamelib.board_items.Movable` item.

        The value of this property is set with :meth:`~.set_restorable`

        :return: False
        :rtype: bool

        .. seealso:: :meth:`~.set_restorable`
        """
        return self.__is_restorable

    def set_restorable(self, val):
        """Make the structure restorable or not.

        :param val: True or False depending on the restorability of the structure.
        :type val: bool

        Example::

            myneatstructure.set_restorable(True)
        """
        if type(val) is bool:
            self.__is_restorable = val
        else:
            raise base.HacInvalidTypeException(
                "set_restorable(bool) takes a boolean as paramater."
            )


class GenericActionableStructure(GenericStructure, board_items.Actionable):
    """
    A GenericActionableStructure is the combination of a
    :class:`~pygamelib.assets.structures.GenericStructure` and an
    :class:`~pygamelib.board_items.Actionable`.
    It is only a helper combination.

    Please see the documentation for
    :class:`~pygamelib.assets.structures.GenericStructure` and
    :class:`~pygamelib.board_items.Actionable` for more information.
    """

    def __init__(self, **kwargs):
        GenericStructure.__init__(self, **kwargs)
        board_items.Actionable.__init__(self, **kwargs)


class Treasure(board_items.Immovable):
    """
    A Treasure is an :class:`~pygamelib.board_items.Immovable` that is pickable and
    with a non zero value. It is an helper class that allows to focus on game design and
    mechanics instead of small building blocks.

    :param model: The model that will represent the treasure on the map
    :type model: str
    :param value: The value of the treasure, it is usually used to calculate the score.
    :type value: int
    :param inventory_space: The space occupied by the treasure. It is used by
        :class:`~pygamelib.game.Inventory` as a measure of space. If the treasure's
        size exceed the Inventory size (or the cumulated size of all items + the
        treasure exceed the inventory max_size()) the
        :class:`~pygamelib.base.Inventory` will refuse to add the treasure.
    :type inventory_space: int

    .. note:: All the options from :class:`~pygamelib.board_items.Immovable` are also
        available to this constructor.

    Example::

        money_bag = Treasure(model=Sprites.MONEY_BAG,value=100,inventory_space=2)
        print(f"This is a money bag {money_bag}")
        player.inventory.add_item(money_bag)
        print(f"The inventory value is {player.inventory.value()} and is at
            {player.inventory.size()}/{player.inventory.max_size}")
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "¤"
        board_items.Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 10
        else:
            self.value = kwargs["value"]
        if "inventory_space" not in kwargs.keys():
            self._inventory_space = 1
        else:
            self._inventory_space = kwargs["inventory_space"]

    def pickable(self):
        """ This represent the capacity for a Treasure to be picked-up by player or NPC.

        A treasure is obviously pickable by the player and potentially NPCs.
        :class:`~pygamelib.game.Board` puts the Treasure in the
        :class:`~pygamelib.game.Inventory` if the picker implements has_inventory()

        :return: True
        :rtype: bool
        """
        return True

    def overlappable(self):
        """ This represent the capacity for a Treasure to be overlapped by player or NPC.

        A treasure is not overlappable.

        :return: False
        :rtype: bool
        """
        return False

    def restorable(self):
        """ This represent the capacity for a Treasure to be restored after being overlapped.

        A treasure is not overlappable, therefor is not restorable.

        :return: False
        :rtype: bool
        """
        return False


class Door(GenericStructure):
    """
    A Door is a :class:`~pygamelib.assets.structures.GenericStructure` that is not
    pickable, overlappable and restorable. It has a value of 0 and a size of 1 by
    default. It is an helper class that allows to focus on game design and mechanics
    instead of small building blocks.

    :param model: The model that will represent the door on the map
    :type model: str
    :param value: The value of the door, it is useless in that case. The default value
        is 0.
    :type value: int
    :param inventory_space: The size of the door in the inventory. Unless you make the
        door pickable (I have no idea why you would do that...), this parameter is not
        used.
    :type inventory_space: int
    :param type: The type of the door. It is often used as a type identifier for your
        game main loop. For example: unlocked_door or locked_door.
    :type type: str
    :param pickable: Is this door pickable by the player? Default value is False.
    :type pickable: Boolean
    :param overlappable: Is this door overlappable by the player? Default value is True.
    :type overlappable: Boolean
    :param restorable: Is this door restorable after being overlapped? Default value is
        True.
    :type restorable: Boolean

    .. note:: All the options from
       :class:`~pygamelib.assets.structures.GenericStructure` are also available to
       this constructor.

    Example::

        door1 = Door(model=Sprites.DOOR,type='locked_door')
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "]"
        board_items.Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs["value"]
        if "inventory_space" not in kwargs.keys():
            self._inventory_space = 1
        else:
            self._inventory_space = kwargs["inventory_space"]
        if "name" not in kwargs.keys():
            self.name = "Door"
        else:
            self.name = kwargs["name"]
        if "type" not in kwargs.keys():
            self.type = "door"
        else:
            self.type = kwargs["type"]
        if "pickable" not in kwargs.keys():
            self.set_pickable(False)
        else:
            self.set_pickable(kwargs["pickable"])
        if "overlappable" not in kwargs.keys():
            self.set_overlappable(True)
        else:
            self.set_overlappable(kwargs["overlappable"])
        if "restorable" not in kwargs.keys():
            self.set_restorable(True)
        else:
            self.set_restorable(kwargs["restorable"])
