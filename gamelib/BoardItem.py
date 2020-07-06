"""This module contains the basic board items classes (regular and void items).

.. autosummary::
   :toctree: .

   BoardItem
   BoardItemVoid
"""
from gamelib.GFX import Core
from gamelib.HacExceptions import HacOutOfBoardBoundException, HacInvalidTypeException
import gamelib.Utils


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
    :param parent: The parent object of the board item. Usually a Board or Game object.

    ..important:: Starting with version 1.2.0 and introduction of complex items,
       BoardItems have a dimension. That dimension **CANNOT** be set. It is always 1x1.
       This is because a BoardItem always takes 1 cell, whatever it's actual number of
       characters. Python does not really provide a way to prevent changing that member
       but if you do, you'll break rendering. You have been warned.
    """

    def __init__(self, **kwargs):
        self.name = "Board item"
        self.type = "item"
        self.pos = [None, None]
        self.model = "*"
        self.animation = None
        self.parent = None
        self.sprixel = None
        self.dimension = [1, 1]
        # Setting class parameters
        for item in ["name", "type", "pos", "model", "parent", "sprixel"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])

    def __str__(self):
        if self.sprixel is not None:
            return self.sprixel.__repr__()
        else:
            return self.model

    def __repr__(self):
        return self.__str__()

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

    def position_as_vector(self):
        """Returns the current item position as a Vector2D

        :returns: The position as a 2D vector
        :rtype: :class:`~gamelib.GFX.Core.Vector2D`

        Example::

            gravity = Vector2D(9.81, 0)
            next_position = item.position_as_vector() + gravity.unit()
        """
        return Core.Vector2D(self.pos[0], self.pos[1])

    def row(self):
        """Convenience method to get the current stored row of the item.

        This is absolutely equivalent to access to item.pos[0].

        :return: The row coordinate
        :rtype: int

        Example::

            if item.row() != item.pos[0]:
                print('Something extremely unlikely just happened...')
        """
        return self.pos[0]

    def column(self):
        """Convenience method to get the current stored column of the item.

        This is absolutely equivalent to access to item.pos[1].

        :return: The column coordinate
        :rtype: int

        Example::

            if item.column() != item.pos[1]:
                print('Something extremely unlikely just happened...')
        """
        return self.pos[1]

    def width(self):
        """Convenience method to get the width of the item.

        This is absolutely equivalent to access to item.dimension[0].

        :return: The width
        :rtype: int

        Example::

            if item.width() > board.width():
                print('The item is too big for the board.')
        """
        return self.dimension[0]

    def height(self):
        """Convenience method to get the height of the item.

        This is absolutely equivalent to access to item.dimension[1].

        :return: The height
        :rtype: int

        Example::

            if item.height() > board.height():
                print('The item is too big for the board.')
        """
        return self.dimension[1]

    def collides_with(self, other):
        """Tells if this item collides with another item.

        :param other: The item you want to check for collision.
        :type other: :class:`~gamelib.BoardItem.BoardItem`
        :rtype: bool

        Example::

            if projectile.collides_with(game.player):
                game.player.hp -= 5
        """
        if isinstance(other, BoardItem):
            return gamelib.Utils.intersect(
                self.pos[0],
                self.pos[1],
                self.dimension[0],
                self.dimension[1],
                other.pos[0],
                other.pos[1],
                other.dimension[0],
                other.dimension[1],
            )
        else:
            raise HacInvalidTypeException(
                "BoardItem.collides_with require a BoardItem as parameter."
            )

    def distance_to(self, other):
        """Calculates the distance with an item.

        :param other: The item you want to calculate the distance to.
        :type other: :class:`~gamelib.BoardItem.BoardItem`
        :return: The distance between this item and the other.
        :rtype: float

        Example::

            if npc.distance_to(game.player) <= 2.0:
                npc.seek_and_destroy = True
        """
        if isinstance(other, BoardItem):
            return gamelib.Utils.distance(
                self.pos[0], self.pos[1], other.pos[0], other.pos[1],
            )
        else:
            raise HacInvalidTypeException(
                "BoardItem.distance_to require a BoardItem as parameter."
            )

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


class BoardItemComplexComponent(BoardItem):
    """The default component of a complex item.

    It is literrally just a BoardItem but is subclassed for easier identification.

    It is however scanning its parent for the item's basic properties (overlappable,
    restorable, etc.)

    A component can never be pickable by itself.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, "parent") and self.parent is not None:
            if hasattr(self.parent, "restorable") and callable(self.parent.restorable):
                self.__restorable = self.parent.restorable
            else:
                self.__restorable = False
            if hasattr(self.parent, "overlappable") and callable(
                self.parent.overlappable
            ):
                self.__overlappable = self.parent.overlappable
            else:
                self.__overlappable = False
            if hasattr(self.parent, "can_move") and callable(self.parent.can_move):
                self.__can_move = self.parent.can_move
            else:
                self.__can_move = False
        else:
            self.__restorable = False
            self.__overlappable = False
            self.__can_move = False
        self.__pickable = False

    def restorable(self):
        return self.__restorable

    def overlappable(self):
        return self.__overlappable

    def can_move(self):
        return self.__can_move

    def pickable(self):
        return self.__pickable


class BoardComplexItem(BoardItem):
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.name = "Board Multi Item"
        self.type = "multi_item"
        super().__init__(**kwargs)
        self.sprite = Core.Sprite()
        self.null_sprixel = None
        self.dimension = None
        self._item_matrix = []
        # Not sure about that one
        self.hit_box = []
        self.base_item_type = BoardItemComplexComponent
        for item in ["sprite", "dimension", "null_sprixel", "base_item_type"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])
        # Size is used for something else in BoardItem. Let's use dimension
        if self.dimension is None:
            self.dimension = self.sprite.dimension()
        self.update_sprite()

    def update_sprite(self):
        self._item_matrix = []
        for row in range(0, self.dimension[1]):
            self._item_matrix.append([])
            for col in range(0, self.dimension[0]):
                if (
                    self.null_sprixel is not None
                    and self.sprite.sprixel(row, col) == self.null_sprixel
                ):
                    self._item_matrix[row].append(BoardItemVoid())
                else:
                    self._item_matrix[row].append(self.base_item_type(**self.__kwargs))
                    self._item_matrix[row][col].name = f"{self.name}_{row}_{col}"
                    self._item_matrix[row][col].model = self.sprite.sprixel(
                        row, col
                    ).model
                    self._item_matrix[row][col].sprixel = self.sprite.sprixel(row, col)
                    self._item_matrix[row][col].parent = self

    def item(self, row, column):
        """
        Return the item at the row, column position if within
        sprite's boundaries.

        :rtype: gamelib.BoardItem.BoardItem

        :raise HacOutOfBoardBoundException: if row or column are
            out of bound.
        """
        if row < self.dimension[1] and column < self.dimension[0]:
            return self._item_matrix[row][column]
        else:
            raise HacOutOfBoardBoundException(
                (
                    f"There is no item at coordinates [{row},{column}] "
                    "because it's out of the board multi item boundaries "
                    f"({self.size[0]}x{self.size[1]})."
                )
            )
