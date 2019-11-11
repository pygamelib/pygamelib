"""This module contains the basic board items classes (regular and void items).
"""


class BoardItem:
    """
    Base class for any item that will be placed on a Board.

    :param type: A type you want to give your item. It can be any string. You can then
        use the type for sorting or grouping for example.
    :type type: str
    :param name: A name for this item. For identification purpose.
    :type name: str
    :param pos: the position of this item. When the item is managed by the Board and
        Game engine this member hold the last updated position of the item. It is not
        updated if you manually move the item. It must be an array of
        2 integers [row,column]
    :type pos: array
    :param model: The model to use to display this item on the Board. Be mindful of the
        space it will require. Default value is '*'.
    :type model: str
    """

    def __init__(self, **kwargs):
        self.name = "Board item"
        self.type = "item"
        self.pos = [None, None]
        self.model = "*"
        self.animation = None
        # Setting class parameters
        for item in ["name", "type", "pos", "model"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])

    def __str__(self):
        return self.model

    def __repr__(self):
        return self.model

    def display(self):
        """
        Print the model WITHOUT carriage return.
        """
        print(self.model, end="")

    def debug_info(self):
        """
        Return a string with the list of the attributes and their current value.

        :rtype: str
        """
        string = "attrs: \n"
        for key in vars(self):
            if type(getattr(self, key)) is list:
                string += (
                    f"'{key}' = '"
                    + "".join(str(e) + " " for e in getattr(self, key))
                    + "'\n"
                )
            else:
                string += f"'{key}' = '" + getattr(self, key) + "'\n"
        return string

    def store_position(self, row, column):
        """Store the BoardItem position for self access.

        The stored position is used for consistency and quick access to the self
        postion. It is a redundant information and might not be synchronized.

        :param row: the row of the item in the :class:`~gamelib.Board.Board`.
        :type row: int
        :param column: the column of the item in the :class:`~gamelib.Board.Board`.
        :type column: int

        Example::

            item.store_position(3,4)
        """
        self.pos = [row, column]

    def can_move(self):
        """
        This is a virtual method that must be implemented in deriving classes.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be moved by the Board.
        """
        raise NotImplementedError()

    def pickable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be pick-up by player or NPC.
        """
        raise NotImplementedError()

    def overlappable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be overlapped by another
        BoardItem.
        """
        raise NotImplementedError()

    def size(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return an integer.
        This represent the size of the BoardItem. It is used for example to evaluate
        the space taken in the inventory.
        """
        raise NotImplementedError()


class BoardItemVoid(BoardItem):
    """
    A class that represent a void cell.
    """

    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        self.name = "void_cell"

    def pickable(self):
        """
        A BoardItemVoid is not pickable, therefor this method return false.

        :return: False
        """
        return False

    def overlappable(self):
        """
        A BoardItemVoid is obviously overlappable (so player and NPC can walk over).

        :return: True
        """
        return True
