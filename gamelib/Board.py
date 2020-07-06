"""This module contains the Board class.
It is the base class for all levels.
"""

from gamelib.Utils import warn
from gamelib.HacExceptions import (
    HacException,
    HacOutOfBoardBoundException,
    HacInvalidTypeException,
    HacObjectIsNotMovableException,
)
from gamelib.BoardItem import BoardItem, BoardItemVoid, BoardComplexItem
from gamelib.Movable import Movable
from gamelib.Immovable import Immovable, Actionable
from gamelib.Characters import Player, NPC
from gamelib.GFX import Core
import gamelib.Constants as Constants


class Board:
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
    :param parent: The parent object (usually the Game object).
    :type parent: :class:`~gamelib.Game.Game`
    :param DISPLAY_SIZE_WARNINGS: A boolean to show or hide the warning about boards
        bigger than 80 rows and columns.
    :type DISPLAY_SIZE_WARNINGS: bool
    """

    def __init__(self, **kwargs):
        self.name = "Board"
        self.size = [10, 10]
        self.player_starting_position = [0, 0]
        self.ui_border_left = "|"
        self.ui_border_right = "|"
        self.ui_border_top = "-"
        self.ui_border_bottom = "-"
        self.ui_board_void_cell = " "
        self.ui_board_void_cell_sprixel = None
        self.DISPLAY_SIZE_WARNINGS = True
        self.parent = None
        # The overlapped matrix is used as an invisible layer were overlapped
        # restorable items are parked momentarily (until the cell they were on
        # is free again).
        self._overlapped_matrix = []
        # Setting class parameters
        for item in [
            "name",
            "size",
            "ui_border_bottom",
            "ui_border_top",
            "ui_border_left",
            "ui_border_right",
            "ui_board_void_cell",
            "ui_board_void_cell_sprixel",
            "player_starting_position",
            "DISPLAY_SIZE_WARNINGS",
            "parent",
        ]:
            if item in kwargs:
                setattr(self, item, kwargs[item])
        # if ui_borders is set then set all borders to that value
        if "ui_borders" in kwargs.keys():
            for item in [
                "ui_border_bottom",
                "ui_border_top",
                "ui_border_left",
                "ui_border_right",
            ]:
                setattr(self, item, kwargs["ui_borders"])
        # Now checking for board's data sanity
        try:
            self.check_sanity()
        except HacException as error:
            raise error

        # Init the list of movable and immovable objects
        self._movables = set()
        self._immovables = set()
        # If sanity check passed then, initialize the board
        self.init_board()

    def __str__(self):
        return (
            "----------------\n"
            f"Board name: {self.name}\n"
            f"Board size: {self.size}\n"
            f"Borders: '{self.ui_border_left}','{self.ui_border_right}','"
            f"{self.ui_border_top}','{self.ui_border_bottom}',\n"
            f"Board void cell: '{self.ui_board_void_cell}'\n"
            f"Player starting position: {self.player_starting_position}\n"
            "----------------"
        )

    def init_board(self):
        """
        Initialize the board with BoardItemVoid that uses ui_board_void_cell
        as model.

        Example::

            myboard.init_board()
        """
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell_sprixel, Core.Sprixel
        ):
            self._matrix = [
                [
                    BoardItemVoid(sprixel=self.ui_board_void_cell_sprixel, parent=self)
                    for i in range(0, self.size[0], 1)
                ]
                for j in range(0, self.size[1], 1)
            ]
        else:
            self._matrix = [
                [
                    BoardItemVoid(model=self.ui_board_void_cell, parent=self)
                    for i in range(0, self.size[0], 1)
                ]
                for j in range(0, self.size[1], 1)
            ]
        self._overlapped_matrix = [
            [None for i in range(0, self.size[0], 1)] for j in range(0, self.size[1], 1)
        ]

    def generate_void_cell(self):
        """This method return a void cell.

        If ui_board_void_cell_sprixel is defined it uses it, otherwise use
        ui_board_void_cell to generate the void item.

        :return: A void board item
        :rtype: :class:`~gamelib.BoardItem.BoardItemVoid`

        Example::

            board.generate_void_cell()
        """
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell_sprixel, Core.Sprixel
        ):
            return BoardItemVoid(
                sprixel=self.ui_board_void_cell_sprixel,
                model=self.ui_board_void_cell_sprixel.model,
                parent=self,
            )
        else:
            return BoardItemVoid(model=self.ui_board_void_cell, parent=self)

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
        self._matrix[row][column] = self.generate_void_cell()

    def check_sanity(self):
        """Check the board sanity.

        This is essentially an internal method called by the constructor.
        """
        sanity_check = 0
        if type(self.size) is list:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO", ("The 'size' parameter must be a list.")
            )
        if len(self.size) == 2:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO",
                ("The 'size' parameter must be a list of 2 elements."),
            )
        if type(self.size[0]) is int:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO",
                ("The first element of the 'size' list must be an integer."),
            )
        if type(self.size[1]) is int:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO",
                ("The second element of the 'size' list must be an integer."),
            )
        if type(self.name) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO", "The 'name' parameter must be a string."
            )
        if type(self.ui_border_bottom) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO",
                ("The 'ui_border_bottom' parameter must be a string."),
            )
        if type(self.ui_border_top) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO", ("The 'ui_border_top' parameter must be a string.")
            )
        if type(self.ui_border_left) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO", ("The 'ui_border_left' parameter must be a string.")
            )
        if type(self.ui_border_right) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO", ("The 'ui_border_right' parameter must be a string.")
            )
        if type(self.ui_board_void_cell) is str:
            sanity_check += 1
        else:
            raise HacException(
                "SANITY_CHECK_KO",
                ("The 'ui_board_void_cell' parameter must be a string."),
            )
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell, Core.Sprixel
        ):
            sanity_check += 1
        elif self.ui_board_void_cell_sprixel is not None and not isinstance(
            self.ui_board_void_cell_sprixel, Core.Sprixel
        ):
            raise HacException(
                "SANITY_CHECK_KO",
                ("The 'ui_board_void_cell_sprixel' parameter must be a Sprixel."),
            )
        else:
            sanity_check += 1
        if self.size[0] > 80:
            if self.DISPLAY_SIZE_WARNINGS:
                warn(
                    (
                        f"The first dimension of your board is {self.size[0]}. "
                        "It is a good practice to keep it at a maximum of 80 for "
                        "compatibility with older terminals."
                    )
                )

        if self.size[1] > 80:
            if self.DISPLAY_SIZE_WARNINGS:
                warn(
                    (
                        f"The second dimension of your board is {self.size[1]}. "
                        "It is a good practice to keep it at a maximum of 80 for "
                        "compatibility with older terminals."
                    )
                )

        # If all sanity check clears return True else raise a general error.
        # I have no idea how the general error could ever occur but...
        # better safe than sorry!
        if sanity_check == 11:
            return True
        else:
            raise HacException("SANITY_CHECK_KO", "The board data are not valid.")

    def width(self):
        """A convenience method to get the width of the Board.

        It is absolutely equivalent to access to board.size[0].

        :return: The width of the board.
        :rtype: int

        Example::

            if board.size[0] != board.width():
                print('Houston, we have a problem...')
        """
        return self.size[0]

    def height(self):
        """A convenience method to get the height of the Board.

        It is absolutely equivalent to access to board.size[1].

        :return: The height of the board.
        :rtype: int

        Example::

            if board.size[1] != board.height():
                print('Houston, we have a problem...')
        """
        return self.size[1]

    def display_around(self, object, row_radius, column_radius):
        """Display only a part of the board.

        This method behaves like display() but only display a part of the board around
        an object (usually the player).
        Example::

            # This will display only a total of 30 cells vertically and
            # 60 cells horizontally.
            board.display_around(player, 15, 30)

        :param object: an item to center the view on (it has to be a subclass
            of BoardItem)
        :type object: :class:`~gamelib.BoardItem.BoardItem`
        :param row_radius: The radius of display in number of rows showed. Remember that
            it is a radius not a diameter...
        :type row_radius: int
        :param column_radius: The radius of display in number of columns showed.
            Remember that... Well, same thing.
        :type column_radius: int

        It uses the same display algorithm than the regular display() method.
        """
        # First let's take care of the type checking
        if not isinstance(object, BoardItem):
            raise HacInvalidTypeException(
                "Board.display_around: object needs to be a BoardItem."
            )
        if type(row_radius) is not int or type(column_radius) is not int:
            raise HacInvalidTypeException(
                "Board.display_around: both row_radius and"
                " column_radius needs to be int."
            )
        # Now if the viewport is greater or equal to the board size, well we just need
        # a regular display()
        if self.size[1] <= 2 * row_radius and self.size[0] <= 2 * column_radius:
            return self.display()
        if self.size[0] <= 2 * column_radius:
            column_radius = round(self.size[0] / 2)
        if self.size[1] <= 2 * row_radius:
            row_radius = round(self.size[1] / 2)
        row_min_bound = 0
        row_max_bound = self.size[1]
        column_min_bound = 0
        column_max_bound = self.size[0]
        # Here we account for the dimension of the complex item to center the viewport
        # on it.
        pos_row = object.pos[0]
        pos_col = object.pos[1]
        if isinstance(object, BoardComplexItem):
            pos_row = object.pos[0] + int(object.height() / 2)
            pos_col = object.pos[1] + int(object.width() / 2)
        # Row
        if pos_row - row_radius >= 0:
            row_min_bound = pos_row - row_radius
        if pos_row + row_radius < row_max_bound:
            row_max_bound = pos_row + row_radius
        # Columns
        if pos_col - column_radius >= 0:
            column_min_bound = pos_col - column_radius
        if pos_col + column_radius < column_max_bound:
            column_max_bound = pos_col + column_radius
        # Now adjust boundaries so it looks fine at min and max
        if column_min_bound <= 0:
            column_min_bound = 0
            column_max_bound = 2 * column_radius
        if column_max_bound >= self.size[0]:
            column_max_bound = self.size[0]
            if (self.size[0] - 2 * column_radius) >= 0:
                column_min_bound = self.size[0] - 2 * column_radius
        if row_min_bound <= 0:
            row_min_bound = 0
            row_max_bound = 2 * row_radius
        if row_max_bound >= self.size[1]:
            row_max_bound = self.size[1]
            if (self.size[1] - 2 * row_radius) >= 0:
                row_min_bound = self.size[1] - 2 * row_radius
        if row_min_bound == 0:
            bt_size = column_radius * 2
            if bt_size >= self.size[0]:
                bt_size = self.size[0]
                if pos_col - column_radius > 0:
                    bt_size = self.size[0] - (pos_col - column_radius)
            print(self.ui_border_top * bt_size, end="")
            if column_min_bound <= 0 and column_max_bound >= self.size[0]:
                print(self.ui_border_top * 2, end="")
            elif column_min_bound <= 0 or column_max_bound >= self.size[0]:
                print(self.ui_border_top, end="")
            print("\r")
        for row in self._matrix[row_min_bound:row_max_bound]:
            if column_min_bound == 0:
                print(self.ui_border_left, end="")
            for y in row[column_min_bound:column_max_bound]:
                if isinstance(y, BoardItemVoid) and y.model != self.ui_board_void_cell:
                    y.model = self.ui_board_void_cell
                    y.sprixel = self.ui_board_void_cell_sprixel
                print(y, end="")
            if column_max_bound >= self.size[0]:
                print(self.ui_border_right, end="")
            print("\r")
        if row_max_bound >= self.size[1]:
            bb_size = column_radius * 2
            if bb_size >= self.size[0]:
                bb_size = self.size[0]
                if pos_col - column_radius > 0:
                    bb_size = self.size[0] - (pos_col - column_radius)
            print(self.ui_border_bottom * bb_size, end="")
            if column_min_bound <= 0 and column_max_bound >= self.size[0]:
                print(self.ui_border_bottom * 2, end="")
            elif column_min_bound <= 0 or column_max_bound >= self.size[0]:
                print(self.ui_border_bottom, end="")
            print("\r")

    def display(self):
        """Display the entire board.

        This method display the Board (as in print()), taking care of
        displaying the borders, and everything inside.

        It uses the __str__ method of the item, which by default uses (in order)
        BoardItem.sprixel and (if no sprixel is defined) BoardItem.model. If you want to
        override this behavior you have to subclass BoardItem.
        """
        # # Debug: print the overlapped matrix
        # for row in self._overlapped_matrix:
        #     print(self.ui_border_left, end="")
        #     for column in row:
        #         if (
        #             isinstance(column, BoardItemVoid)
        #             and column.model != self.ui_board_void_cell
        #         ):
        #             column.model = self.ui_board_void_cell
        #         elif column is None:
        #             print(" ", end="")
        #         else:
        #             print(column, end="\x1b[0m")
        #     print(self.ui_border_right + "\x1b[0m\r")
        # print("\x1b[0m")
        # # eod
        print(
            "".join(
                [
                    self.ui_border_top * len(self._matrix[0]),
                    self.ui_border_top * 2,
                    "\r",
                ]
            )
        )
        for row in self._matrix:
            print(self.ui_border_left, end="")
            for column in row:
                if (
                    isinstance(column, BoardItemVoid)
                    and column.model != self.ui_board_void_cell
                ):
                    if isinstance(self.ui_board_void_cell, Core.Sprixel):
                        column.sprixel = self.ui_board_void_cell_sprixel
                        column.model = self.ui_board_void_cell_sprixel.model
                    else:
                        column.model = self.ui_board_void_cell
                print(column, end="")
            print(self.ui_border_right + "\r")
        print(
            "".join(
                [
                    self.ui_border_bottom * len(self._matrix[0]),
                    self.ui_border_bottom * 2,
                    "\r",
                ]
            )
        )

    def item(self, row, column):
        """
        Return the item at the row, column position if within
        board's boundaries.

        :rtype: gamelib.BoardItem.BoardItem

        :raise HacOutOfBoardBoundException: if row or column are
            out of bound.
        """
        if row < self.size[1] and column < self.size[0]:
            return self._matrix[row][column]
        else:
            raise HacOutOfBoardBoundException(
                (
                    f"There is no item at coordinates [{row},{column}] "
                    "because it's out of the board boundaries "
                    f"({self.size[0]}x{self.size[1]})."
                )
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
            if isinstance(item, BoardComplexItem):
                for ir in range(0, item.dimension[1]):
                    for ic in range(0, item.dimension[0]):
                        if not isinstance(item.item(ir, ic), BoardItemVoid):
                            self.place_item(item.item(ir, ic), row + ir, column + ic)
                item.store_position(row, column)
            elif isinstance(item, BoardItem):
                # If we are about to place the item on a overlappable and
                # restorable we store it to be restored
                # when the Movable will move.
                existing_item = self._matrix[row][column]
                if (
                    isinstance(existing_item, Immovable)
                    and existing_item.restorable()
                    and existing_item.overlappable()
                ):
                    # Let's save the item on the hidden layer
                    self._overlapped_matrix[row][column] = self._matrix[row][column]
                    if (
                        item.sprixel is not None
                        and self._overlapped_matrix[row][column].sprixel is not None
                        and item.sprixel.is_bg_transparent
                    ):
                        item.sprixel.bg_color = self._overlapped_matrix[row][
                            column
                        ].sprixel.bg_color
                # Place the item on the board
                self._matrix[row][column] = item
                # Take ownership of the item (if item doesn't have parent)
                if item.parent is None:
                    item.parent = self
                item.store_position(row, column)
                if isinstance(item, Movable):
                    if isinstance(item.parent, BoardComplexItem):
                        self._movables.add(item.parent)
                    else:
                        self._movables.add(item)
                elif isinstance(item, Immovable):
                    if isinstance(item.parent, BoardComplexItem):
                        self._immovables.add(item.parent)
                    else:
                        self._immovables.add(item)
            else:
                raise HacInvalidTypeException(
                    "The item passed in argument is not a subclass of BoardItem"
                )
        else:
            raise HacOutOfBoardBoundException(
                f"Cannot place item at coordinates [{row},{column}] because "
                f"it's out of the board boundaries ({self.size[0]}x{self.size[1]})."
            )

    def _move_complex(self, item, direction, step=1):
        if isinstance(item, Movable) and item.can_move():
            # If direction is not a vector, transform into one
            if not isinstance(direction, Core.Vector2D):
                direction = Core.Vector2D.from_direction(direction, step)

            projected_position = item.position_as_vector() + direction
            if (
                projected_position is not None
                and projected_position.row >= 0
                and projected_position.column >= 0
                and (projected_position.row + item.height() - 1) < self.size[1]
                and (projected_position.column + item.width() - 1) < self.size[0]
            ):
                can_draw = True
                for orow in range(0, item.dimension[1]):
                    for ocol in range(0, item.dimension[0]):
                        new_row = projected_position.row + orow
                        new_column = projected_position.column + ocol
                        # Check all items within the surface
                        if isinstance(self._matrix[new_row][new_column], Actionable):
                            if (
                                isinstance(item, Player)
                                and (
                                    (
                                        self._matrix[new_row][new_column].perm
                                        == Constants.PLAYER_AUTHORIZED
                                    )
                                    or (
                                        self._matrix[new_row][new_column].perm
                                        == Constants.ALL_CHARACTERS_AUTHORIZED
                                    )
                                )
                            ) or (
                                isinstance(item, NPC)
                                and (
                                    (
                                        self._matrix[new_row][new_column].perm
                                        == Constants.NPC_AUTHORIZED
                                    )
                                    or (
                                        self._matrix[new_row][new_column].perm
                                        == Constants.ALL_CHARACTERS_AUTHORIZED
                                    )
                                )
                                or (
                                    self._matrix[new_row][new_column].perm
                                    == Constants.ALL_MOVABLE_AUTHORIZED
                                )
                            ):
                                self._matrix[new_row][new_column].activate()
                        # Now I need to put the rest of the code here...
                        if (
                            not self._matrix[new_row][new_column].overlappable()
                            and self._matrix[new_row][new_column].pickable()
                            and isinstance(item, Movable)
                            and item.has_inventory()
                        ):
                            # Put the item in the inventory
                            item.inventory.add_item(self._matrix[new_row][new_column])
                            # And then clear the cell (this is usefull for the next one)
                            self.clear_cell(new_row, new_column)
                            # Finally we check if the destination is overlappable
                        if (
                            self._matrix[new_row][new_column].parent != item
                            and not self._matrix[new_row][new_column].overlappable()
                        ):
                            can_draw = False
                            break
                if can_draw:
                    for row in range(0, item.dimension[1], 1):
                        for col in range(0, item.dimension[0], 1):
                            if (
                                self._overlapped_matrix[item.pos[0] + row][
                                    item.pos[1] + col
                                ]
                                is not None
                            ):
                                self.place_item(
                                    self._overlapped_matrix[item.pos[0] + row][
                                        item.pos[1] + col
                                    ],
                                    item.pos[0] + row,
                                    item.pos[1] + col,
                                )
                                self._overlapped_matrix[item.pos[0] + row][
                                    item.pos[1] + col
                                ] = None
                            # else:
                            #     self.place_item(
                            #         self.generate_void_cell(),
                            #         item.pos[0] + row,
                            #         item.pos[1] + col,
                            #     )
                    self.place_item(
                        item, projected_position.row, projected_position.column,
                    )
        else:
            raise HacObjectIsNotMovableException(
                (
                    f"Item '{item.name}' at position [{item.pos[0]}, "
                    f"{item.pos[1]}] is not a subclass of Movable, "
                    f"therefor it cannot be moved."
                )
            )

    def move(self, item, direction, step=1):
        """
        Board.move() is a routing function. It does 2 things:

         1 - If the direction is a :class:`~gamelib.GFX.Core.Vector2D`, round the values
            to the nearest integer (as move works with entire board cells).
         2 - route toward the right moving function depending if the item is complex or
            not.
        Move an item in the specified direction for a number of steps.

        :param item: an item to move (it has to be a subclass of Movable)
        :type item: gamelib.Movable.Movable
        :param direction: a direction from :ref:`constants-module`
        :type direction: gamelib.Constants or :class:`~gamelib.GFX.Core.Vector2D`
        :param step: the number of steps to move the item.
        :type step: int

        If the number of steps is greater than the Board, the item will
        be move to the maximum possible position.

        If the item is not a subclass of Movable, an
        HacObjectIsNotMovableException exception (see
        :class:`gamelib.HacExceptions.HacObjectIsNotMovableException`).

        Example::

            board.move(player,Constants.UP,1)

        .. Important:: if the move is successfull, an empty BoardItemVoid
            (see :class:`gamelib.BoardItem.BoardItemVoid`) will be put at the
            departure position (unless the movable item is over an overlappable
            item). If the movable item is over an overlappable item, the
            overlapped item is restored.

        .. Important:: Also important: If the direction is a
           :class:`~gamelib.GFX.Core.Vector2D`, the values will be rounded to the
           nearest integer (as move works with entire board cells). It allows for
           movement accumulation before actually moving.

        .. todo:: check all types!
        """
        if isinstance(direction, Core.Vector2D):
            # If direction is a vector, round the numbers to the next integer.
            direction.row = round(direction.row)
            direction.column = round(direction.column)
        if isinstance(item, BoardComplexItem):
            return self._move_complex(item, direction, step)
        else:
            return self._move_simple(item, direction, step)

    def _move_simple(self, item, direction, step=1):
        if isinstance(item, Movable) and item.can_move():

            # if direction not in dir(Constants):
            #     raise HacInvalidTypeException('In Board.move(item, direction,
            # step), direction must be a direction contant from the
            # gamelib.Constants module')

            new_row = None
            new_column = None
            if isinstance(direction, Core.Vector2D):
                new_row = item.pos[0] + direction.row
                new_column = item.pos[1] + direction.column
            else:
                if direction == Constants.UP:
                    new_row = item.pos[0] - step
                    new_column = item.pos[1]
                elif direction == Constants.DOWN:
                    new_row = item.pos[0] + step
                    new_column = item.pos[1]
                elif direction == Constants.LEFT:
                    new_row = item.pos[0]
                    new_column = item.pos[1] - step
                elif direction == Constants.RIGHT:
                    new_row = item.pos[0]
                    new_column = item.pos[1] + step
                elif direction == Constants.DRUP:
                    new_row = item.pos[0] - step
                    new_column = item.pos[1] + step
                elif direction == Constants.DRDOWN:
                    new_row = item.pos[0] + step
                    new_column = item.pos[1] + step
                elif direction == Constants.DLUP:
                    new_row = item.pos[0] - step
                    new_column = item.pos[1] - step
                elif direction == Constants.DLDOWN:
                    new_row = item.pos[0] + step
                    new_column = item.pos[1] - step
            # First of all we check if the new coordinates are within the board
            if (
                new_row is not None
                and new_column is not None
                and new_row >= 0
                and new_column >= 0
                and new_row < self.size[1]
                and new_column < self.size[0]
            ):
                # Then, we check if the item is actionable and if so, if the item
                # is allowed to activate it.
                if isinstance(self._matrix[new_row][new_column], Actionable):
                    if (
                        isinstance(item, Player)
                        and (
                            (
                                self._matrix[new_row][new_column].perm
                                == Constants.PLAYER_AUTHORIZED
                            )
                            or (
                                self._matrix[new_row][new_column].perm
                                == Constants.ALL_CHARACTERS_AUTHORIZED
                            )
                        )
                    ) or (
                        isinstance(item, NPC)
                        and (
                            (
                                self._matrix[new_row][new_column].perm
                                == Constants.NPC_AUTHORIZED
                            )
                            or (
                                self._matrix[new_row][new_column].perm
                                == Constants.ALL_CHARACTERS_AUTHORIZED
                            )
                        )
                    ):
                        self._matrix[new_row][new_column].activate()
                # Now we check if the destination contains a pickable item.
                # Note: I'm not sure why I decided that pickables were not overlapable.
                if (
                    not self._matrix[new_row][new_column].overlappable()
                    and self._matrix[new_row][new_column].pickable()
                    and isinstance(item, Movable)
                    and item.has_inventory()
                ):
                    # Put the item in the inventory
                    item.inventory.add_item(self._matrix[new_row][new_column])
                    # And then clear the cell (this is usefull for the next one)
                    self.clear_cell(new_row, new_column)
                # Finally we check if the destination is overlappable
                if self._matrix[new_row][new_column].overlappable():
                    # And if it is, we check if the destination is restorable
                    if (
                        not isinstance(self._matrix[new_row][new_column], BoardItemVoid)
                        and isinstance(self._matrix[new_row][new_column], Immovable)
                        and self._matrix[new_row][new_column].restorable()
                    ):
                        # If so, we save the item on the hidden layer
                        self._overlapped_matrix[new_row][new_column] = self._matrix[
                            new_row
                        ][new_column]
                    if (
                        item.sprixel is not None
                        and self._matrix[new_row][new_column].sprixel is not None
                        and item.sprixel.is_bg_transparent
                    ):
                        item.sprixel.bg_color = self._matrix[new_row][
                            new_column
                        ].sprixel.bg_color
                    # Finally instead of just placing a BoardItemVoid on
                    # the departure position we first make sure there
                    # is no overlapping object to restore.
                    overlapped_item = self._overlapped_matrix[item.pos[0]][item.pos[1]]
                    if (
                        overlapped_item is not None
                        and isinstance(overlapped_item, Immovable)
                        and overlapped_item.restorable()
                        and (
                            overlapped_item.pos[0] != new_row
                            or overlapped_item.pos[1] != new_column
                        )
                    ):
                        self.place_item(
                            overlapped_item,
                            overlapped_item.pos[0],
                            overlapped_item.pos[1],
                        )
                        self._overlapped_matrix[item.pos[0]][item.pos[1]] = None
                    else:
                        self.place_item(
                            self.generate_void_cell(), item.pos[0], item.pos[1],
                        )
                    self.place_item(item, new_row, new_column)
        else:
            raise HacObjectIsNotMovableException(
                (
                    f"Item '{item.name}' at position [{item.pos[0]}, "
                    f"{item.pos[1]}] is not a subclass of Movable, "
                    f"therefor it cannot be moved."
                )
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

        .. Important:: This method test if something is left on the overlapped layer.
           If so, it restore what was overlapped instead of creating a new void item.

        """
        if self._matrix[row][column] in self._movables:
            self._movables.discard(self._matrix[row][column])
        elif self._matrix[row][column] in self._immovables:
            self._immovables.discard(self._matrix[row][column])
        self._matrix[row][column] = None
        # self.place_item(
        #     BoardItemVoid(model=self.ui_board_void_cell, name="void_cell"),
        #     row,
        #     column,
        # )
        if self._overlapped_matrix[row][column] is not None:
            self._matrix[row][column] = self._overlapped_matrix[row][column]
            self._overlapped_matrix[row][column] = None
        else:
            self.init_cell(row, column)

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
            return list(self._movables)

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
            return list(self._immovables)
