"""This module contains the Board class.
It is the base class for all levels.
"""

from gamelib.Utils import warn
from gamelib.HacExceptions import (HacException,
                                   HacOutOfBoardBoundException,
                                   HacInvalidTypeException,
                                   HacObjectIsNotMovableException)
from gamelib.BoardItem import BoardItem, BoardItemVoid
from gamelib.Movable import Movable
from gamelib.Immovable import Immovable, Actionable
from gamelib.Characters import Player, NPC
import gamelib.Constants as Constants


class Board():
    """A class that represent a game board.

    The board is being represented by a square matrix.
    For the moment a board only support one player.

    The Board object is the base object to build a level :
        you create a Board and then you add BoardItems
        (or objects derived from BoardItem).

    :param name: the name of the Board
    :type name: str
    :param size: array [width,height] with width and height being int.
        The size of the board.
    :type size: list
    :param player_starting_position: array [row,column] with row and
        column being int. The coordinates at which Game will place the player
        on change_level().
    :type player_starting_position: list
    :param ui_borders: To set all the borders to the same value
    :type ui_borders: str
    :param ui_border_left: A string that represents the left border.
    :type ui_border_left: str
    :param ui_border_right: A string that represents the right border.
    :type ui_border_right: str
    :param ui_border_top: A string that represents the top border.
    :type ui_border_top: str
    :param ui_border_bottom: A string that represents the bottom border.
    :type ui_border_bottom: str
    :param ui_board_void_cell: A string that represents an empty cell. This
        option is going to be the model of the BoardItemVoid
        (see :class:`gamelib.BoardItem.BoardItemVoid`)
    :type ui_board_void_cell: str
    """

    def __init__(self, **kwargs):
        self.name = "Board"
        self.size = [10, 10]
        self.player_starting_position = [0, 0]
        self.ui_border_left = '|'
        self.ui_border_right = '|'
        self.ui_border_top = '-'
        self.ui_border_bottom = '-'
        self.ui_board_void_cell = ' '
        # Setting class parameters
        for item in ['name', 'size', 'ui_border_bottom', 'ui_border_top',
                     'ui_border_left', 'ui_border_right', 'ui_board_void_cell',
                     'player_starting_position']:
            if item in kwargs:
                setattr(self, item, kwargs[item])
        # if ui_borders is set then set all borders to that value
        if 'ui_borders' in kwargs.keys():
            for item in ['ui_border_bottom', 'ui_border_top', 'ui_border_left',
                         'ui_border_right']:
                setattr(self, item, kwargs['ui_borders'])
        # Now checking for board's data sanity
        try:
            self.check_sanity()
        except HacException as error:
            raise error

        # Init the list of movable and immovable objects
        self._movables = []
        self._immovables = []
        # If sanity check passed then, initialize the board
        self.init_board()

    def __str__(self):
        return (f"----------------\n"
                "Board name: {self.name}\n"
                "Board size: {self.size}\n"
                "Borders: '{self.ui_border_left}','{self.ui_border_right}','"
                "{self.ui_border_top}','{self.ui_border_bottom}',\n"
                "Board void cell: '{self.ui_board_void_cell}'\n"
                "Player starting position: {self.player_starting_position}\n"
                "----------------")

    def init_board(self):
        """
        Initialize the board with BoardItemVoid that uses ui_board_void_cell
        as model.

        Example::

            myboard.init_board()
        """

        self._matrix = [[BoardItemVoid(model=self.ui_board_void_cell)
                        for i in range(0, self.size[0], 1)]
                        for j in range(0, self.size[1], 1)]

    def init_cell(self, row, column):
        """
        Initialize a specific cell of the board with BoardItemVoid that
        uses ui_board_void_cell as model.

        :param row: the row coordinate.
        :type row: int
        :param column: the column coordinate.
        :type column: int

        Example::

            myboard.init_cell(2,3)
        """
        self._matrix[row][column] = BoardItemVoid(
            model=self.ui_board_void_cell)

    def check_sanity(self):
        """Check the board sanity.

        This is essentially an internal method called by the constructor.
        """
        sanity_check = 0
        if type(self.size) is list:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO', ("The 'size' parameter must"
                                                   " be a list."))
        if len(self.size) == 2:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO', ("The 'size' parameter must"
                                                   " be a list of 2 elements."))
        if type(self.size[0]) is int:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The first element of the "
                                "'size' list must be an integer."))
        if type(self.size[1]) is int:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The second element of the 'size' "
                                "list must be an integer."))
        if type(self.name) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               "The 'name' parameter must be a string.")
        if type(self.ui_border_bottom) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The 'ui_border_bottom' parameter "
                                "must be a string."))
        if type(self.ui_border_top) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The 'ui_border_top' parameter must "
                                "be a string."))
        if type(self.ui_border_left) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The 'ui_border_left' parameter must "
                                "be a string."))
        if type(self.ui_border_right) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The 'ui_border_right' parameter must "
                                "be a string."))
        if type(self.ui_board_void_cell) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',
                               ("The 'ui_board_void_cell' parameter must "
                                "be a string."))

        if self.size[0] > 80:
            warn((f"The first dimension of your board is {self.size[0]}. "
                  "It is a good practice to keep it at a maximum of 80 for "
                  "compatibility with older terminals."))

        if self.size[1] > 80:
            warn((f"The second dimension of your board is {self.size[1]}. "
                  "It is a good practice to keep it at a maximum of 80 for "
                  "compatibility with older terminals."))

        # If all sanity check clears return True else raise a general error.
        # I have no idea how the general error could ever occur but...
        # better safe than sorry!
        if sanity_check == 10:
            return True
        else:
            raise HacException('SANITY_CHECK_KO',
                               "The board data are not valid.")

    def display(self):
        """Display the board.

        This method display the Board (as in print()), taking care of
        displaying the boarders, and everything inside.

        It uses the __str__ method of the item, which by default is
        BoardItem.model. If you want to override this behavior you have
        to subclass BoardItem.
        """
        border_top = ''
        border_bottom = ''
        for x in self._matrix[0]:
            border_bottom += self.ui_border_bottom
            border_top += self.ui_border_top
        border_bottom += self.ui_border_bottom*2
        border_top += self.ui_border_top*2
        print(border_top+"\r")
        for x in self._matrix:
            print(self.ui_border_left, end='')
            for y in x:
                if (isinstance(y, BoardItemVoid)
                        and y.model != self.ui_board_void_cell):
                    y.model = self.ui_board_void_cell
                print(y, end='')
            print(self.ui_border_right + "\r")
        print(border_bottom + "\r")

    def item(self, row, column):
        """
        Return the item at the row, column position if within
        board's boundaries.

        :rtype: gamelib.BoardItem.BoardItem

        :raise HacOutOfBoardBoundException: if row or column are
            out of bound.
        """
        if row < self.size[0] and column < self.size[0]:
            return self._matrix[row][column]
        else:
            raise HacOutOfBoardBoundException(
                  (f"There is no item at coordinates [{row},{column}] "
                   "because it's out of the board boundaries "
                   "({self.size[0]}x{self.size[1]}).")
                  )

    def place_item(self, item, row, column):
        """
        Place an item at coordinates row and column.

        If row or column are our of the board boundaries,
        an HacOutOfBoardBoundException is raised.

        If the item is not a subclass of BoardItem, an HacInvalidTypeException

        .. warning:: Nothing prevents you from placing an object on top of
            another. Be sure to check that. This method will check for items that
            are both overlappable **and** restorable to save them, but that's
            the extend of it.
        """
        if row < self.size[1] and column < self.size[0]:
            if isinstance(item, BoardItem):
                # If we are about to place the item on a overlappable and
                # restorable we store it to be restored
                # when the Movable will move.
                if (isinstance(self._matrix[row][column], Immovable)
                        and self._matrix[row][column].restorable()
                        and self._matrix[row][column].overlappable()):
                    item._overlapping = self._matrix[row][column]
                self._matrix[row][column] = item
                item.store_position(row, column)
                if (isinstance(item, Movable)
                        and item not in self._movables):
                    self._movables.append(item)
                elif (isinstance(item, Immovable)
                        and item not in self._immovables):
                    self._immovables.append(item)
            else:
                raise HacInvalidTypeException(
                    "The item passed in argument is "
                    "not a subclass of BoardItem")
        else:
            raise HacOutOfBoardBoundException(
                f"There is no item at coordinates [{row},{column}] because "
                "it's out of the board boundaries "
                "({self.size[0]}x{self.size[1]}).")

    def move(self, item, direction, step):
        """
        Move an item in the specified direction for a number of steps.

        Example::

            board.move(player,Constants.UP,1)

        :param item: an item to move (it has to be a subclass of Movable)
        :type item: gamelib.Movable.Movable
        :param direction: a direction from :ref:`constants-module`
        :type direction: gamelib.Constants
        :param step: the number of steps to move the item.
        :type step: int

        If the number of steps is greater than the Board, the item will
        be move to the maximum possible position.

        If the item is not a subclass of Movable, an
        HacObjectIsNotMovableException exception (see
        :class:`gamelib.HacExceptions.HacObjectIsNotMovableException`).

        .. Important:: if the move is successfull, an empty BoardItemVoid
            (see :class:`gamelib.BoardItem.BoardItemVoid`) will be put at the
            departure position (unless the movable item is over an overlappable
            item). If the movable item is over an overlappable item, the
            overlapped item is restored.

        .. note:: It could be interesting here, instead of relying on storing
            the overlapping item in a property of a Movable
            (:class:`gamelib.Movable.Movable`) object, to have another dimension
            on the board matrix to push and pop objects on a cell. Only the first
            item would be rendered and it would avoid the complicated and error
            prone logic in this method. If anyone feel up to the challenge,
            `PR are welcome ;-)
            <https://github.com/arnauddupuis/hac-game-lib/pulls>`_.

        .. todo:: check all types!

        """
        if isinstance(item, Movable) and item.can_move():

            # if direction not in dir(Constants):
            #     raise HacInvalidTypeException('In Board.move(item, direction,
            # step), direction must be a direction contant from the
            # gamelib.Constants module')

            new_x = None
            new_y = None
            if direction == Constants.UP:
                new_x = item.pos[0] - step
                new_y = item.pos[1]
            elif direction == Constants.DOWN:
                new_x = item.pos[0] + step
                new_y = item.pos[1]
            elif direction == Constants.LEFT:
                new_x = item.pos[0]
                new_y = item.pos[1] - step
            elif direction == Constants.RIGHT:
                new_x = item.pos[0]
                new_y = item.pos[1] + step
            elif direction == Constants.DRUP:
                new_x = item.pos[0] - step
                new_y = item.pos[1] + step
            elif direction == Constants.DRDOWN:
                new_x = item.pos[0] + step
                new_y = item.pos[1] + step
            elif direction == Constants.DLUP:
                new_x = item.pos[0] - step
                new_y = item.pos[1] - step
            elif direction == Constants.DLDOWN:
                new_x = item.pos[0] + step
                new_y = item.pos[1] - step
            if (new_x is not None
                    and new_y is not None
                    and new_x >= 0
                    and new_y >= 0
                    and new_x < self.size[1]
                    and new_y < self.size[0]
                    and self._matrix[new_x][new_y].overlappable()):
                # If we are here, it means the cell we are going to already
                # has an overlappable item, so let's save it for
                # later restoration
                if (not isinstance(self._matrix[new_x][new_y], BoardItemVoid)
                        and isinstance(self._matrix[new_x][new_y], Immovable)
                        and self._matrix[new_x][new_y].restorable()):
                    if item._overlapping is None:
                        item._overlapping = self._matrix[new_x][new_y]
                    else:
                        item._overlapping_buffer = self._matrix[new_x][new_y]

                if isinstance(self._matrix[new_x][new_y], Actionable):
                    if ((isinstance(item, Player) and
                            ((self._matrix[new_x][new_y].perm ==
                                Constants.PLAYER_AUTHORIZED)
                                or (self._matrix[new_x][new_y].perm ==
                                    Constants.ALL_PLAYABLE_AUTHORIZED)))
                        or (isinstance(item, NPC) and
                            ((self._matrix[new_x][new_y].perm ==
                                Constants.NPC_AUTHORIZED)
                            or (self._matrix[new_x][new_y].perm ==
                                Constants.ALL_PLAYABLE_AUTHORIZED)))):
                        self._matrix[new_x][new_y].activate()
                        # Here instead of just placing a BoardItemVoid on
                        # the departure position we first make sure there
                        # is no _overlapping object to restore.
                        if (item._overlapping is not None
                                and isinstance(item._overlapping, Immovable)
                                and item._overlapping.restorable()
                                and (item._overlapping.pos[0] != new_x or
                                     item._overlapping.pos[1] != new_y)):
                            self.place_item(
                                item._overlapping,
                                item._overlapping.pos[0],
                                item._overlapping.pos[1]
                            )
                            if item._overlapping_buffer is not None:
                                item._overlapping = item._overlapping_buffer
                                item._overlapping_buffer = None
                            else:
                                item._overlapping = None
                        else:
                            self.place_item(
                                BoardItemVoid(model=self.ui_board_void_cell),
                                item.pos[0],
                                item.pos[1]
                            )
                        self.place_item(item, new_x, new_y)
                else:
                    # if there is an overlapped item, restore it.
                    # Else just move
                    if (item._overlapping is not None
                            and isinstance(item._overlapping, Immovable)
                            and item._overlapping.restorable()
                            and (item._overlapping.pos[0] != new_x
                                 or item._overlapping.pos[1] != new_y)):
                        self.place_item(
                            item._overlapping,
                            item._overlapping.pos[0],
                            item._overlapping.pos[1]
                        )
                        if item._overlapping_buffer is not None:
                            item._overlapping = item._overlapping_buffer
                            item._overlapping_buffer = None
                        else:
                            item._overlapping = None
                    else:
                        self.place_item(
                            BoardItemVoid(model=self.ui_board_void_cell),
                            item.pos[0],
                            item.pos[1]
                        )
                    self.place_item(item, new_x, new_y)
            elif (new_x is not None and new_y is not None
                    and new_x >= 0 and new_y >= 0 and new_x < self.size[1]
                    and new_y < self.size[0]
                    and self._matrix[new_x][new_y].pickable()):
                if isinstance(item, Movable) and item.has_inventory():
                    item.inventory.add_item(self._matrix[new_x][new_y])
                    # Here instead of just placing a BoardItemVoid on the
                    # departure position we first make sure there is no
                    # _overlapping object to restore.
                    if (item._overlapping is not None
                            and isinstance(item._overlapping, Immovable)
                            and item._overlapping.restorable()
                            and (item._overlapping.pos[0] != new_x
                                 or item._overlapping.pos[1] != new_y)):
                        self.place_item(
                            item._overlapping,
                            item._overlapping.pos[0],
                            item._overlapping.pos[1]
                        )
                        item._overlapping = None
                    else:
                        self.place_item(
                            BoardItemVoid(model=self.ui_board_void_cell),
                            item.pos[0],
                            item.pos[1]
                        )
                    self.place_item(item, new_x, new_y)
            elif (new_x is not None and new_y is not None
                    and new_x >= 0 and new_y >= 0
                    and new_x < self.size[1] and new_y < self.size[0]
                    and isinstance(self._matrix[new_x][new_y], Actionable)):
                if ((isinstance(item, Player)
                        and ((self._matrix[new_x][new_y].perm ==
                              Constants.PLAYER_AUTHORIZED)
                             or (self._matrix[new_x][new_y].perm ==
                                 Constants.ALL_PLAYABLE_AUTHORIZED)))
                    or (isinstance(item, NPC)
                        and ((self._matrix[new_x][new_y].perm ==
                              Constants.NPC_AUTHORIZED)
                             or (self._matrix[new_x][new_y].perm ==
                                 Constants.ALL_PLAYABLE_AUTHORIZED)))):
                    self._matrix[new_x][new_y].activate()
        else:
            raise HacObjectIsNotMovableException(
                (f"Item '{item.name}' at position [{item.pos[0]}, "
                 "{item.pos[1]}] is not a subclass of Movable, "
                 "therefor it cannot be moved.")
                )

    def clear_cell(self, row, column):
        """Clear cell (row, column)

        This method clears a cell, meaning it position a
        void_cell BoardItemVoid at these coordinates.

        :param row: The row of the item to remove
        :type row: int
        :param column: The column of the item to remove
        :type column: int

        Example::

            myboard.clear_cell(3,4)

        .. WARNING:: This method does not check the content before,
            it *will* overwrite the content.

        """
        if self._matrix[row][column] in self._movables:
            index = self._movables.index(self._matrix[row][column])
            del(self._movables[index])
        elif self._matrix[row][column] in self._immovables:
            index = self._immovables.index(self._matrix[row][column])
            del(self._immovables[index])
        self.place_item(
            BoardItemVoid(model=self.ui_board_void_cell, name='void_cell'),
            row,
            column
        )

    def get_movables(self, **kwargs):
        """Return a list of all the Movable objects in the Board.

        See :class:`gamelib.Movable.Movable` for more on a Movable object.

        :param ``**kwargs``: an optional dictionnary with keys matching
            Movables class members and value being something contained
            in that member.
        :return: A list of Movable items

        Example::

            for m in myboard.get_movables():
                print(m.name)

            # Get all the Movable objects that has a type that contains "foe"
            foes = myboard.get_movables(type="foe")
        """
        if kwargs:
            retvals = []
            for item in self._movables:
                counter = 0
                for (arg_key, arg_value) in kwargs.items():
                    if arg_value in getattr(item, arg_key):
                        counter += 1
                if counter == len(kwargs):
                    retvals.append(item)
            return retvals
        else:
            return self._movables

    def get_immovables(self, **kwargs):
        """Return a list of all the Immovable objects in the Board.

        See :class:`gamelib.Immovable.Immovable` for more on
            an Immovable object.

        :param ``**kwargs``: an optional dictionnary with keys matching
            Immovables class members and value being something
            **contained** in that member.
        :return: A list of Immovable items

        Example::

            for m in myboard.get_immovables():
                print(m.name)

            # Get all the Immovable objects that type contains "wall"
                AND name contains fire
            walls = myboard.get_immovables(type="wall",name="fire")

        """
        if kwargs:
            retvals = []
            for item in self._immovables:
                counter = 0
                for (arg_key, arg_value) in kwargs.items():
                    if arg_value in getattr(item, arg_key):
                        counter += 1
                if counter == len(kwargs):
                    retvals.append(item)
            return retvals
        else:
            return self._immovables
