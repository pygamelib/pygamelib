__docformat__ = "restructuredtext"
"""
The game module contains the core classes for a game:

 * The Game object itself.
 * The Board object.
 * The Inventory object.

The Game object is what could be called the game engine.
It holds a lot of methods that helps taking care of some complex mechanics behind the
curtain.

The Board class is the base class for all levels.

.. autosummary::
   :toctree: .

   pygamelib.engine.Board
   pygamelib.engine.Game
   pygamelib.engine.Inventory
   pygamelib.engine.Screen

"""
from pygamelib import board_items, base, constants, actuators
from pygamelib.assets import graphics
from pygamelib.gfx import core, particles
from pygamelib.functions import pgl_isinstance
from blessed import Terminal
import random
import json
import sys
import time
import copy
import ast
import numpy as np

# We need to ignore that one as it is used by user to compare keys (i.e Utils.key.UP)
from readchar import readkey, key  # noqa: F401


class Board(base.PglBaseObject):
    """A class that represent a game board.

    The board object is a 2D matrix of board items. This means that you can visualize it
    as a chessboard for example. All board items are positioned on this chessboard-like
    object and can be moved around.

    The Board object is the base object to build a level. Once created to your liking
    you can add items from the :ref:`boarditem-module` module. You can also derived
    :class:`~pygamelib.board_items.BoardItem` to create your own board items, specific
    to your game.

    If you want a detailed introduction to the Board object, go the the pygamelib wiki
    and read the "`Getting started: the Board
    <https://github.com/pygamelib/pygamelib/wiki/Getting-started-Board>`_" article.

    .. role:: boldblue
    .. role:: blue


    .. Note:: In version 1.3.0 a new screen rendering stack was introduced. With this
       came the need for some object to hold more information about their state. This is
       the case for Board. To use partial display with the :class:`Screen` buffer system
       the board itself needs to hold the information about were to draw and on what to
       focus on. The existing code will still work as the :class:`Game` object takes
       care of forwarding the information to the Board. However, it is now possible to
       exploit the :class:`~pygamelib.board_items.Camera` object to create cut scenes
       and more interesting movements.

    .. Important:: Partial display related parameters are information used by the
       :func:`~pygamelib.engine.Board.display_around()` method and the :class:`Screen`
       object to either display directly the board (display_around) or render the Board
       in the frame buffer. **You have to make sure that the focus element's position
       is updated**. If you use the player, you have nothing to do but the Camera object
       needs to be manually updated for example.

    .. Warning:: in 1.3.0 the notion of layers was added to the Board object. Layers are
       used to better manage items overlapping. For the moment, layers are automatically
       managed to expand and shrink on demand (or on a need basis). You can use the
       layer system to add some depth to your game but you should be warned that you may
       experience some issues. If it is the case please report them on the
       `Github issues page <https://github.com/pygamelib/pygamelib/issues>`_.
       For existing code, the entire Board object behaves exactly like in version 1.2.x.

    """

    def __init__(
        self,
        name: str = "Board",
        size: list = None,
        ui_borders: str = None,
        ui_border_bottom: str = "-",
        ui_border_top: str = "-",
        ui_border_left: str = "|",
        ui_border_right: str = "|",
        ui_board_void_cell=" ",
        ui_board_void_cell_sprixel: core.Sprixel = None,
        player_starting_position: list = None,
        DISPLAY_SIZE_WARNINGS=False,
        parent=None,
        partial_display_viewport=None,
        partial_display_focus=None,
        enable_partial_display=False,
    ):
        """
        :param name: the name of the Board
        :type name: str
        :param size: array [width,height] with width and height being int.
           The size of the board. If layers is not specified it is set to 5.
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
           (see :class:`pygamelib.board_items.BoardItemVoid`)
        :type ui_board_void_cell: str
        :param parent: The parent object (usually the Game object).
        :type parent: :class:`~pygamelib.engine.Game`
        :param DISPLAY_SIZE_WARNINGS: A boolean to show or hide the warning about boards
           bigger than 80 rows and/or columns.
        :type DISPLAY_SIZE_WARNINGS: bool
        :param enable_partial_display: A boolean to tell the Board to enable or not
           partial display of boards. Default: False.
        :type enable_partial_display: bool
        :param partial_display_viewport: A 2 int elements array that gives the
           **radius** of the partial display in number of row and column. Please see
           :func:`~pygamelib.engine.Board.display_around()`.
        :type partial_display_viewport: list
        :param partial_display_focus: An item to focus (i.e center) the view on. When
           partial display is enabled the rendered view will be centered on this focus
           point/item. It can be an item or a vector.
        :type partial_display_focus: :class:`~pygamelib.board_items.BoardItem` or
           :class:`~pygamelib.base.Vector2D`

        """
        super().__init__()
        self.name = name
        if size is None:
            size = [10, 10]
        self.size = size
        if player_starting_position is None:
            player_starting_position = [0, 0, 0]
        self.player_starting_position = player_starting_position
        self.ui_border_left = ui_border_left
        self.ui_border_right = ui_border_right
        self.ui_border_top = ui_border_top
        self.ui_border_bottom = ui_border_bottom
        self.ui_board_void_cell = ui_board_void_cell
        self.ui_board_void_cell_sprixel = ui_board_void_cell_sprixel
        self.DISPLAY_SIZE_WARNINGS = DISPLAY_SIZE_WARNINGS
        self.parent = parent
        self.partial_display_viewport = partial_display_viewport
        self.partial_display_focus = partial_display_focus
        self.enable_partial_display = enable_partial_display
        self._matrix = None
        # self._matrix = np.array([])

        # if ui_borders is set then set all borders to that value
        if ui_borders is not None:
            for border in [
                "ui_border_bottom",
                "ui_border_top",
                "ui_border_left",
                "ui_border_right",
            ]:
                setattr(self, border, ui_borders)
        # Now checking for board's data sanity
        try:
            self.check_sanity()
        except base.PglException as error:
            raise error

        # Init the list of movable and immovable objects
        self._movables = set()
        self._immovables = set()
        # Init the list of particle emitters.
        self._particle_emitters = set()
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
            f"Board void sprixel: {self.ui_board_void_cell_sprixel}\n"
            f"Player starting position: {self.player_starting_position}\n"
            f"Partial display enabled: {self.enable_partial_display}\n"
            f"Partial display viewport: {self.partial_display_viewport}\n"
            f"Partial display focus: {self.partial_display_focus}\n"
            "----------------"
        )

    def init_board(self):
        """
        Initialize the board with BoardItemVoid that uses ui_board_void_cell_sprixel or
        ui_board_void_cell (in that order of preference) as model.

        **This method is automatically called by the Board's constructor**.

        Example::

            myboard.init_board()
        """
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell_sprixel, core.Sprixel
        ):
            # The deepcopy is a lot slower but it protects against a ton of unwanted
            # side effects
            self._matrix = np.array(
                [
                    [None for i in range(0, self.size[0], 1)]
                    for j in range(0, self.size[1], 1)
                ]
            )
            for r in range(self.size[1]):
                for c in range(self.size[0]):
                    self._matrix[r][c] = [
                        board_items.BoardItemVoid(
                            pos=[r, c, 0],
                            sprixel=copy.deepcopy(self.ui_board_void_cell_sprixel),
                            parent=self,
                        )
                    ]
        else:
            self._matrix = np.array(
                [
                    [None for i in range(0, self.size[0], 1)]
                    for j in range(0, self.size[1], 1)
                ]
            )
            for r in range(self.size[1]):
                for c in range(self.size[0]):
                    self._matrix[r][c] = [
                        board_items.BoardItemVoid(
                            pos=[r, c, 0], model=self.ui_board_void_cell, parent=self
                        )
                    ]

    def generate_void_cell(self):
        """This method return a void cell.

        If ui_board_void_cell_sprixel is defined it uses it, otherwise use
        ui_board_void_cell to generate the void item.

        :return: A void board item
        :rtype: :class:`~pygamelib.board_items.BoardItemVoid`

        Example::

            board.generate_void_cell()
        """
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell_sprixel, core.Sprixel
        ):
            return board_items.BoardItemVoid(
                sprixel=copy.deepcopy(self.ui_board_void_cell_sprixel),
                model=self.ui_board_void_cell_sprixel.model,
                parent=self,
            )
        else:
            return board_items.BoardItemVoid(model=self.ui_board_void_cell, parent=self)

    def init_cell(self, row, column, layer=0) -> None:
        """
        Initialize a specific cell of the board with BoardItemVoid that
        uses ui_board_void_cell as model.

        :param row: the row coordinate.
        :type row: int
        :param column: the column coordinate.
        :type column: int

        Example::

            myboard.init_cell(2,3,0)
        """
        # TODO: If the layer does not already exists this generate an index error. What
        # do we need to do? Should this method be responsible to init the missing
        # layers? -> My position for the moment is to leave that method at simple as
        # possible. It should be the responsibility of place_item to init the missing
        # layers.
        self._matrix[row][column][layer] = self.generate_void_cell()
        self._matrix[row][column][layer].store_position(row, column, layer)

    def check_sanity(self) -> None:
        """Check the board sanity.

        This is essentially an internal method called by the constructor.
        """
        sanity_check = 0
        if type(self.size) is list:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                "The 'size' parameter must be a list.",
            )
        if len(self.size) == 2:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                f"The 'size' parameter must be a list of 2 elements. size: {self.size}",
            )
        if type(self.size[0]) is int:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                ("The first element of the 'size' list must be an integer."),
            )
        if type(self.size[1]) is int:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                ("The second element of the 'size' list must be an integer."),
            )
        if type(self.name) is str:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO", "The 'name' parameter must be a string."
            )
        if type(self.ui_border_bottom) is str or isinstance(
            self.ui_border_bottom, core.Sprixel
        ):
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                ("The 'ui_border_bottom' parameter must be a string."),
            )
        if type(self.ui_border_top) is str or isinstance(
            self.ui_border_top, core.Sprixel
        ):
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO", ("The 'ui_border_top' parameter must be a string.")
            )
        if type(self.ui_border_left) is str or isinstance(
            self.ui_border_left, core.Sprixel
        ):
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO", ("The 'ui_border_left' parameter must be a string.")
            )
        if type(self.ui_border_right) is str or isinstance(
            self.ui_border_right, core.Sprixel
        ):
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO", ("The 'ui_border_right' parameter must be a string.")
            )
        if type(self.ui_board_void_cell) is str:
            sanity_check += 1
        else:
            raise base.PglException(
                "SANITY_CHECK_KO",
                ("The 'ui_board_void_cell' parameter must be a string."),
            )
        # TODO: The void_cell check should be done once and for all (str and sprixel at
        #  the same time)
        if self.ui_board_void_cell_sprixel is not None and isinstance(
            self.ui_board_void_cell_sprixel, core.Sprixel
        ):
            sanity_check += 1
        elif self.ui_board_void_cell_sprixel is not None and not isinstance(
            self.ui_board_void_cell_sprixel, core.Sprixel
        ):
            raise base.PglException(
                "SANITY_CHECK_KO",
                ("The 'ui_board_void_cell_sprixel' parameter must be a Sprixel."),
            )
        else:
            sanity_check += 1
        if self.size[0] > 80:
            if self.DISPLAY_SIZE_WARNINGS:
                base.Text.warn(
                    (
                        f"The first dimension of your board is {self.size[0]}. "
                        "It is a good practice to keep it at a maximum of 80 for "
                        "compatibility with older terminals."
                    )
                )

        if self.size[1] > 80:
            if self.DISPLAY_SIZE_WARNINGS:
                base.Text.warn(
                    (
                        f"The second dimension of your board is {self.size[1]}. "
                        "It is a good practice to keep it at a maximum of 80 for "
                        "compatibility with older terminals."
                    )
                )

        # If all sanity check clears return True else raise a general error.
        # I have no idea how the general error could ever occur but...
        # better safe than sorry! However we have to skip test coverage for the else.
        if sanity_check == 11 or sanity_check == 12:
            return True
        else:  # pragma: no cover
            raise base.PglException(
                "SANITY_CHECK_KO",
                f"The board data are not valid. (Score: {sanity_check}/12)",
            )

    @property
    def width(self):
        """A convenience read only property to get the width of the Board.

        It is absolutely equivalent to access to board.size[0].

        :return: The width of the board.
        :rtype: int

        Example::

            if board.size[0] != board.width:
                print('Houston, we have a problem...')
        """
        return self.size[0]

    @property
    def height(self):
        """A convenience read only property to get the height of the Board.

        It is absolutely equivalent to access to board.size[1].

        :return: The height of the board.
        :rtype: int

        Example::

            if board.size[1] != board.height:
                print('Houston, we have a problem...')
        """
        return self.size[1]

    def layers(self, row, column) -> int:
        """A method to get the number of layers at the Board's given coordinates.

        :return: The number of layers of the board.
        :rtype: int

        Example::

            if board.layers(game.player.row, game.player.column) > 1:
                print('The player is stomping on something!')
        """
        return len(self._matrix[row][column])

    def display_around(self, item, row_radius, column_radius) -> None:
        """Display only a part of the board.

        This method behaves like display() but only display a part of the board around
        an item (usually the player).
        Example::

            # This will display only a total of 30 cells vertically and
            # 60 cells horizontally.
            board.display_around(player, 15, 30)

        :param item: an item to center the view on (it has to be a subclass
            of BoardItem)
        :type item: :class:`~pygamelib.board_items.BoardItem`
        :param row_radius: The radius of display in number of rows showed. Remember that
            it is a radius not a diameter...
        :type row_radius: int
        :param column_radius: The radius of display in number of columns showed.
            Remember that... Well, same thing.
        :type column_radius: int

        It uses the same display algorithm than the regular display() method.
        """
        # First let's take care of the type checking
        if not isinstance(item, board_items.BoardItem):
            raise base.PglInvalidTypeException(
                "Board.display_around: object needs to be a BoardItem."
            )
        if type(row_radius) is not int or type(column_radius) is not int:
            raise base.PglInvalidTypeException(
                "Board.display_around: both row_radius and"
                " column_radius needs to be int."
            )
        clear_eol = "\x1b[K"
        # This statement doesn't registered as tested but it is. In tests/test_board.py
        # in test_partial_display.
        if isinstance(self.parent, Game) and isinstance(
            self.parent.terminal, Terminal
        ):  # pragma: no cover
            clear_eol = self.parent.terminal.clear_eol
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
        pos_row = item.pos[0]
        pos_col = item.pos[1]
        if isinstance(item, board_items.BoardComplexItem):
            pos_row = item.pos[0] + int(item.height / 2)
            pos_col = item.pos[1] + int(item.width / 2)
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
            column_max_bound = self.size[0] - 1
            if (self.size[0] - 2 * column_radius) >= 0:
                column_min_bound = self.size[0] - 2 * column_radius
        if row_min_bound <= 0:
            row_min_bound = 0
            row_max_bound = 2 * row_radius
        if row_max_bound >= self.size[1]:
            row_max_bound = self.size[1] - 1
            if (self.size[1] - 2 * row_radius) >= 0:
                row_min_bound = self.size[1] - 2 * row_radius
        if row_min_bound == 0:
            bt_size = column_radius * 2 + 1
            if bt_size >= self.size[0]:
                bt_size = self.size[0]
                # if pos_col - column_radius > 0:
                #     bt_size = self.size[0] - (pos_col - column_radius)
            print(f"{str(self.ui_border_top) * bt_size}{clear_eol}", end="")
            if column_min_bound <= 0 and column_max_bound >= self.size[0] - 1:
                print(f"{str(self.ui_border_top) * 2}{clear_eol}", end="")
            elif column_min_bound <= 0 or column_max_bound >= self.size[0]:
                print(f"{self.ui_border_top}{clear_eol}", end="")
            print("\r")
        render_cell = self.render_cell
        for br in range(row_min_bound, row_max_bound + 1):
            if column_min_bound == 0:
                print(self.ui_border_left, end="")
            bc = column_min_bound
            while bc <= column_max_bound:
                encoded_cell = render_cell(br, bc).__repr__()
                print(encoded_cell, end="")
                bc += 1
            if column_max_bound >= self.size[0] - 1:
                print(f"{self.ui_border_right}{clear_eol}", end="")
            print("\r")

        if row_max_bound >= self.size[1] - 1:
            bb_size = column_radius * 2 + 1
            if bb_size >= self.size[0]:
                bb_size = self.size[0]
                # if pos_col - column_radius > 0:
                #     bb_size = self.size[0] - (pos_col - column_radius)
            print(f"{str(self.ui_border_bottom) * bb_size}{clear_eol}", end="")
            if column_min_bound <= 0 and column_max_bound >= self.size[0] - 1:
                print(f"{str(self.ui_border_bottom) * 2}{clear_eol}", end="")
            elif column_min_bound <= 0 or column_max_bound >= self.size[0]:
                print(f"{self.ui_border_bottom}{clear_eol}", end="")
            print("\r")

    def display(self) -> None:
        """Display the entire board.

        This method display the Board (as in print()), taking care of
        displaying the borders, and everything inside.

        It uses the __str__ method of the item, which by default uses (in order)
        BoardItem.sprixel and (if no sprixel is defined) BoardItem.model. If you want to
        override this behavior you have to subclass BoardItem.
        """
        clear_eol = "\x1b[K"
        # This statement doesn't registered as tested but it is. In tests/test_board.py
        # in test_partial_display.
        if isinstance(self.parent, Game) and isinstance(
            self.parent.terminal, Terminal
        ):  # pragma: no cover
            clear_eol = self.parent.terminal.clear_eol
        print(
            "".join(
                [
                    str(self.ui_border_top) * len(self._matrix[0]),
                    str(self.ui_border_top) * 2,
                    clear_eol,
                    "\r",
                ]
            )
        )
        render_cell = self.render_cell
        for row in range(0, self.size[1]):
            print(self.ui_border_left, end="")
            for column in range(0, self.size[0]):
                print(render_cell(row, column), end="")
            print(str(self.ui_border_right) + clear_eol + "\r")
        print(
            "".join(
                [
                    str(self.ui_border_bottom) * len(self._matrix[0]),
                    str(self.ui_border_bottom) * 2,
                    clear_eol,
                    "\r",
                ]
            )
        )

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        """Render the board into from the display buffer to the frame buffer.

        This method is automatically called by :func:`pygamelib.engine.Screen.render`.

        :param buffer: A frame buffer to render the item into.
        :type buffer: numpy.array
        :param row: The row to render in.
        :type row: int
        :param column: The column to render in.
        :type column: int
        :param height: The total height of the display buffer.
        :type height: int
        :param width: The total width of the display buffer.
        :type width: int

        """
        row_start = 0
        row_end = self.size[1]
        column_start = 0
        column_end = self.size[0]
        pos_row = 0
        pos_col = 0
        vp_height = 0
        vp_width = 0
        if self.enable_partial_display:
            # We still need to clamp the viewport if we want to avoid
            # crashes in case the programmer poorly calculated the viewport.
            vp_height = self.partial_display_viewport[0]
            vp_width = self.partial_display_viewport[1]

            if self.size[0] < (2 * vp_width):
                vp_width = int(self.size[0] / 2)
            if self.size[1] < (2 * vp_height):
                vp_height = int(self.size[1] / 2)

            pos_row = self.partial_display_focus.row
            pos_col = self.partial_display_focus.column
            if isinstance(self.partial_display_focus, board_items.BoardComplexItem):
                pos_row = self.partial_display_focus.row + int(
                    self.partial_display_focus.height / 2
                )
                pos_col = self.partial_display_focus.column + int(
                    self.partial_display_focus.width / 2
                )
            # We don't want too many tests here for performances sake.
            # So if partial display is enabled we assume the rest of the
            # parameters are correct. If not, well it'll crash.
            row_start = pos_row - vp_height
            row_end = pos_row + vp_height
            if row_start < 0:
                row_start = 0
            if row_end > self.size[1]:
                row_end = self.size[1]
                row_start = self.size[1] - (2 * vp_height)
            elif row_end < (2 * vp_height):
                row_end = 2 * vp_height

            # compute start and stop coordinates before actually display the
            # board.
            column_start = pos_col - vp_width
            column_end = pos_col + vp_width
            if column_start < 0:
                column_start = 0
            elif column_start > self.size[0] - (vp_width * 2):
                column_start = self.size[0] - (vp_width * 2)
            if column_end > self.size[0]:
                column_end = self.size[0]
                column_start = self.size[0] - vp_width * 2
            elif column_end < (vp_width * 2):
                column_end = vp_width * 2

        # Trying to remove as many dot notation as possible for performances
        render_cell = self.render_cell
        # TODO: bind the rendering area to buffer_height and buffer_width.
        for br in range(row_start, row_end):
            cidx = 0
            bc = column_start
            while bc < column_end:
                cell = render_cell(br, bc)
                # encoded_cell = cell.__repr__()
                incr = cell.length
                try:
                    # buffer[row + br - row_start][column + cidx] = encoded_cell
                    buffer[row + br - row_start][column + cidx] = cell
                except IndexError:
                    break

                for tmpidx in range(1, incr):
                    try:
                        buffer[row + br][column + cidx + tmpidx] = ""
                    except IndexError:
                        break
                bc += 1
                cidx += incr
        # I dread the performance impact...
        # We render all the emitters attached to an item after the board has been drawn
        # So technically it should be the same as Screen.place(r,c,2)
        for _ in range(len(self._particle_emitters) - 1, -1, -1):
            emt = self._particle_emitters.pop()
            if emt.finished():
                continue
            # emt.row += self.screen_row
            # emt.column += self.screen_column
            emt.row += row - row_start
            emt.column += column - column_start
            emt.emit()
            emt.update()
            emt.render_to_buffer(
                buffer,
                emt.row,
                emt.column,
                buffer_height,
                buffer_width,
            )
            self._particle_emitters.add(emt)

    def render_cell(self, row, column):
        """
        .. versionadded:: 1.3.0

        Render the cell at given position.

        This method always return a :class:`~pygamelib.gfx.core.Sprixel` (it could be an
        empty one though). It automatically render the highest item (if items are
        overlapping for example). If the rendered :class:`~pygamelib.gfx.core.Sprixel`
        is configured to have transparent background, this method is going to go through
        the layers to make sure that it is rendering the sprixels correctly (i.e: with
        the right background color).

        For basic usage of the library it is unlikely that you will use it. It is part
        of the screen rendering stack introduced in version 1.3.0.
        Actually unless you need to write a different rendering system you won't use
        that method.

        :param row: The row to render.
        :type row: int
        :param column: The column to render.
        :type column: int

        :rtype: :class:`~pygamelib.gfx.core.Sprixel`

        :raise PglOutOfBoardBoundException: if row or column are
            out of bound.

        Example::

            # This renders the board from the top left corner of the screen.
            for row in range(0, myboard.height):
                for column in range(0, myboard.height):
                    myscreen.place(
                        myboard.render_cell(row, column)
                    ),
                    row,
                    column,
        """
        # TODO: For the particle engine add the ability to Sprixel to have a blend mode.
        #       This method should then do the blending from top to bottom until it
        #       finds a Sprixel that is not blendable.
        if row < self.size[1] and column < self.size[0]:
            # Here we are doing something similar to casting a ray and
            # render the first cell that collides. Or more accurately the first data
            # that allow the creation of a Sprixel.
            if (
                len(self._matrix[row][column]) > 0
                and self._matrix[row][column][-1].sprixel is not None
            ):
                item = self._matrix[row][column][-1]
                sprix = self._matrix[row][column][-1].sprixel
                # TEST for fixing wandering emitters...
                if (
                    hasattr(item, "particle_emitter")
                    and item.particle_emitter is not None
                ):
                    item.particle_emitter.row = row
                    item.particle_emitter.column = column
                # END TEST
                layers_len = len(self._matrix[row][column])
                if layers_len > 1:
                    idx = layers_len - 1
                    # For many reasons the item could be a void item, since we are over
                    # level 0 we don't care about them (they are unimportant for
                    # rendering). Therefor we try to discard them as quickly as possible
                    while isinstance(item, board_items.BoardItemVoid):
                        idx -= 1
                        item = self._matrix[row][column][idx]
                    sprix = self._matrix[row][column][idx].sprixel
                    # TEST for fixing wandering emitters...
                    if (
                        hasattr(item, "particle_emitter")
                        and item.particle_emitter is not None
                    ):
                        item.particle_emitter.row = row
                        item.particle_emitter.column = column
                    # END TEST
                    # We only make the copy here because most of the time we don't need
                    # to: if nothing is stacked under then we don't have any reason to
                    # build a new sprixel because we are not modifying it.
                    if sprix.bg_color is None or sprix.is_bg_transparent:
                        # sprix = copy.deepcopy(self._matrix[row][column][-1].sprixel)
                        sprix = self._matrix[row][column][-1].sprixel.copy()
                        # And now we are going down to make sure that we have pseudo
                        # transparency.
                        idx -= 1
                        while idx >= 0:
                            if (
                                not isinstance(
                                    self._matrix[row][column][idx],
                                    board_items.BoardItemVoid,
                                )
                                and not self._matrix[row][column][
                                    idx
                                ].sprixel.is_bg_transparent
                            ):
                                # As soon as we complete the sprixel we break out of
                                # here to limit the impact on performances
                                sprix.bg_color = self._matrix[row][column][
                                    idx
                                ].sprixel.bg_color
                                break
                            idx -= 1
                return sprix
            return core.Sprixel()
        else:
            raise base.PglOutOfBoardBoundException(
                (
                    f"Impossible to render cell at coordinates [{row},{column}]"
                    " because it's out of the board boundaries "
                    f"({self.size[0]}x{self.size[1]})."
                )
            )

    def item(self, row, column, layer=-1):  # layer = -1 or 0?
        """
        Return the item at the row, column, layer position if within
        board's boundaries.

        :param row: The row to probe.
        :type row: int
        :param column: The column to probe.
        :type column: int
        :param layer: The layer to probe (default: -1 i.e the top item).
        :type layer: int

        :rtype: pygamelib.board_items.BoardItem

        :raise PglOutOfBoardBoundException: if row, column or layer are
            out of bound.
        """
        if row < self.size[1] and column < self.size[0]:
            if layer >= len(self._matrix[row][column]):
                layer = -1
            if self._matrix[row][column][layer].parent is not None and isinstance(
                self._matrix[row][column][layer].parent, board_items.BoardComplexItem
            ):
                return self._matrix[row][column][layer].parent
            else:
                return self._matrix[row][column][layer]
        else:
            raise base.PglOutOfBoardBoundException(
                (
                    f"There is no item at coordinates [{row},{column},{layer}] "
                    f"because it's out of the board boundaries ({self.height},"
                    f"{self.width})."
                )
            )

    def place_item(
        self,
        item,
        row: int,
        column: int,
        layer: int = 0,
        auto_layer: bool = True,
    ):
        """
        Place an item at coordinates row, column and layer.

        If row, column or layer are out of the board boundaries,
        a PglOutOfBoardBoundException is raised.

        If the item is not a subclass of BoardItem, a PglInvalidTypeException

        The observers are notified of a successful placement with the
        :boldblue:`pygamelib.engine.Board.place_item:item_placed` event. The item
        that was deleted is passed as the :blue:`value` of the event.

        .. warning:: Nothing prevents you from placing an object on top of
            another. Be sure to check that. This method will check for items that
            are both overlappable **and** restorable to save them, but that's
            the extend of it.
        """
        if row < self.size[1] and column < self.size[0]:
            # First let's make sure that the BoardItem._auto_layer is up to date
            # Auto layer tells us to automatically pick the layer (in case the user
            # wants to have higher layer to draw overlays). But it's not implemented yet
            if isinstance(item, board_items.BoardItem):
                item._auto_layer = auto_layer
                if item.particle_emitter is not None and isinstance(
                    item.particle_emitter, particles.ParticleEmitter
                ):
                    self._particle_emitters.add(item.particle_emitter)
            if isinstance(item, board_items.BoardComplexItem):
                # First, we get the highest required layer
                max_layer = layer
                for ir in range(0, item.size[1]):
                    for ic in range(0, item.size[0]):
                        inner_pos_layer = layer
                        if layer >= len(self._matrix[row + ir][column + ic]):
                            break
                        else:
                            existing_item = self._matrix[row + ir][column + ic][
                                inner_pos_layer
                            ]
                            while (
                                existing_item.restorable()
                                and existing_item.overlappable()
                            ):
                                inner_pos_layer += 1
                                try:
                                    existing_item = self._matrix[row + ir][column + ic][
                                        inner_pos_layer
                                    ]
                                except IndexError:
                                    self._create_missing_layers(
                                        row + ir, column + ic, inner_pos_layer
                                    )
                                    existing_item = self._matrix[row + ir][column + ic][
                                        inner_pos_layer
                                    ]
                            if inner_pos_layer > max_layer:
                                max_layer = inner_pos_layer
                # Game.instance().session_log(f"place_item: max_layer={max_layer}")
                # TODO: code écris tard, vérifier que ça marche et supprimer la partie
                # vérification des layers dans _move_complex. Puis finisaliser cette
                # fonction.
                for ir in range(0, item.size[1]):
                    for ic in range(0, item.size[0]):
                        itm = item.item(ir, ic)
                        if not isinstance(itm, board_items.BoardItemVoid):
                            self.place_item(
                                itm,
                                row + ir,
                                column + ic,
                                max_layer,
                                False,
                            )
                            itm._auto_layer = auto_layer
                item.store_position(row, column, max_layer)
                self.notify(self, "pygamelib.engine.Board.place_item:item_placed", item)
                if isinstance(item, board_items.Movable):
                    self._movables.add(item)
                elif isinstance(item, board_items.Immovable):
                    self._immovables.add(item)
            elif isinstance(item, board_items.BoardItem):
                # First we look at the layers to see if the specified layer exists.
                existing_item = None
                try:
                    existing_item = self._matrix[row][column][layer]
                except IndexError:
                    # The layer might not exist yet
                    self._create_missing_layers(row, column, layer)
                    existing_item = self._matrix[row][column][layer]
                # If not and if the item is overlappable and restorable we increase the
                # layer number (to create a new layer).
                # existing_item should *never* be None here. If so, there's a big
                # problem. Therefor, it's better to not test and let the game crash.
                # if existing_item.restorable() and existing_item.overlappable():
                #     layer += 1
                #     self._adjust_items_layers(row, column, layer, +1)
                while existing_item.restorable() and existing_item.overlappable():
                    layer += 1
                    try:
                        existing_item = self._matrix[row][column][layer]
                    except IndexError:
                        self._create_missing_layers(row, column, layer)
                        existing_item = self._matrix[row][column][layer]
                # If we are replacing a void item and the item's background is
                # transparent, let's grab it's background color.
                # An alternative would be to have the BoardItemVoid to be restorable,
                # and to never overwrite it. But I'm afraid of the impact on the
                # performances (it means create a lot more new layers and that impacts
                # the performances dramatically).
                if (
                    isinstance(existing_item, board_items.BoardItemVoid)
                    and existing_item.sprixel is not None
                    and item.sprixel.is_bg_transparent
                ):
                    item.sprixel.bg_color = existing_item.sprixel.bg_color
                # Place the item on the board
                try:
                    self._matrix[row][column][layer] = item
                except IndexError:  # pragma: no cover
                    # This should literally never happen: we created relevant layers
                    # before. But, better safe than sorry.
                    self._matrix[row][column].append(item)
                # Take ownership of the item (if item doesn't have parent)
                if item.parent is None:
                    item.parent = self
                item.store_position(row, column, layer)
                self.notify(self, "pygamelib.engine.Board.place_item:item_placed", item)
                if isinstance(item, board_items.Movable):
                    if isinstance(item.parent, board_items.BoardComplexItem):
                        # This is actually tested in test_board.py in the test_item
                        # method.
                        self._movables.add(item.parent)  # pragma: no cover
                    else:
                        self._movables.add(item)
                elif isinstance(item, board_items.Immovable):
                    if isinstance(item.parent, board_items.BoardComplexItem):
                        self._immovables.add(item.parent)
                    else:
                        self._immovables.add(item)
            else:
                raise base.PglInvalidTypeException(
                    "The item passed in argument is not a subclass of BoardItem"
                )
        else:
            raise base.PglOutOfBoardBoundException(
                f"Cannot place item at coordinates [{row},{column},{layer}] because "
                f"it's out of the board boundaries ({self.size[0]}x{self.size[1]})."
            )

    def remove_item(self, item):
        """Remove an item from the board.

        If the item is a single BoardItem, this method is absolutely equivalent to
        calling :meth:`clear_cell`.
        If item is a derivative of BoardComplexItem, it is not as clear_cell() only
        clears a specific cell (that can be part of a complex item). This method
        actually remove the entire item and clears all its cells.

        The observers are notified of a successful removal with the
        :boldblue:`pygamelib.engine.Board.remove_item:item_removed` event. The item
        that was deleted is passed as the :blue:`value` of the event.

        :param item: The item to remove.
        :type item: :class:`~pygamelib.board_items.BoardItem`

        Example::

            game.current_board().remove_item(game.player)
        """
        if not isinstance(item, board_items.BoardItem):
            raise base.PglInvalidTypeException(
                "Board.remove_item(item): item must be a BoardItem."
            )
        cc = None
        if isinstance(item, board_items.BoardComplexItem):
            for r in range(item.row, item.row + item.height):
                for c in range(item.column, item.column + item.width):
                    cc = self.item(r, c, item.layer)
                    if cc == item:
                        break
                    else:
                        # I honestly think it's impossible to get there.
                        cc = None  # pragma: no cover
                if cc is not None:
                    break
        else:
            cc = self.item(item.row, item.column, item.layer)
        if cc is not None and item == cc:
            if isinstance(item, board_items.BoardComplexItem):
                for r in range(item.row, item.row + item.height):
                    for c in range(item.column, item.column + item.width):
                        self.clear_cell(r, c, item.layer)
            else:
                self.clear_cell(item.row, item.column, item.layer)
            self.notify(self, "pygamelib.engine.Board.remove_item:item_removed", item)
            return True
        else:
            raise base.PglException(
                "invalid_item",
                "Board.remove_item(item): The item is different from what is on the "
                "board at these coordinates.",
            )

    def _move_complex(self, item, direction, step=1):
        # Game.instance().session_log(
        #     base.Text("Starting to move complex", core.Color(0, 255, 0))
        # )
        # Since the user is not supposed to call directly that method we assume that it
        # is called by move(), therefor the item is a subclass of Movable.
        # If direction is not a vector, transform into one
        # move() now exclusively pass Vector2D objects to _move_* so we don't need that
        # anymore
        # if not isinstance(direction, base.Vector2D):
        #     direction = base.Vector2D.from_direction(direction, step)
        # Game.instance().log(f"_move_complex: direction={direction}")
        projected_position = item.position_as_vector() + direction
        if (
            projected_position is not None
            and projected_position.row >= 0
            and projected_position.column >= 0
            and (projected_position.row + item.height - 1) < self.size[1]
            and (projected_position.column + item.width - 1) < self.size[0]
        ):
            can_draw = True

            item_row = item.row
            item_column = item.column
            self.remove_item(item)
            for orow in range(0, item.size[1]):
                for ocol in range(0, item.size[0]):
                    new_row = projected_position.row + orow
                    new_column = projected_position.column + ocol
                    dest_item = self.item(new_row, new_column)
                    if isinstance(dest_item, board_items.Actionable):
                        if (
                            (
                                isinstance(item, board_items.Player)
                                and (
                                    (dest_item.perm == constants.PLAYER_AUTHORIZED)
                                    or (
                                        dest_item.perm
                                        == constants.ALL_CHARACTERS_AUTHORIZED
                                    )
                                )
                            )
                            or (
                                isinstance(item, board_items.NPC)
                                and (
                                    (dest_item.perm == constants.NPC_AUTHORIZED)
                                    or (
                                        dest_item.perm
                                        == constants.ALL_CHARACTERS_AUTHORIZED
                                    )
                                )
                            )
                            or (dest_item.perm == constants.ALL_MOVABLE_AUTHORIZED)
                        ):
                            dest_item.activate()
                    # Now taking care of pickable objects
                    pickable_item = self.item(new_row, new_column)
                    if (
                        pickable_item.pickable()
                        and isinstance(item, board_items.Movable)
                        and item.has_inventory()
                    ):
                        # Put the item in the inventory
                        item.inventory.add_item(pickable_item)
                        # And then clear the cell (this is usefull for the next one)
                        self.remove_item(pickable_item)
                    # Finally we check if the destination is overlappable
                    if dest_item != item and not dest_item.overlappable():
                        can_draw = False
                        break
            if can_draw:
                self.place_item(item, projected_position.row, projected_position.column)
            else:
                self.place_item(item, item_row, item_column)

    def move(self, item, direction, step=1):
        """
        Board.move() is a routing function. It does 2 things:

         1 - If the direction is a :class:`~pygamelib.base.Vector2D`, round the
            values to the nearest integer (as move works with entire board cells, i.e
            integers).
         2 - route toward the right moving function depending if the item is complex or
            not.

        Move an item in the specified direction for a number of steps.

        :param item: an item to move (it has to be a subclass of Movable)
        :type item: pygamelib.board_items.Movable
        :param direction: a direction from :ref:`constants-module`
        :type direction: pygamelib.constants or :class:`~pygamelib.base.Vector2D`
        :param step: the number of steps to move the item.
        :type step: int

        If the number of steps is greater than the Board, the item will
        be move to the maximum possible position.

        If the item is not a subclass of Movable, an PglObjectIsNotMovableException
        exception (see :class:`pygamelib.base.PglObjectIsNotMovableException`).

        Example::

            board.move(player,constants.UP,1)

        .. Important:: if the move is successful, an empty BoardItemVoid
            (see :class:`pygamelib.boards_item.BoardItemVoid`) will be put at the
            departure position (unless the movable item is over an overlappable
            item). If the movable item is over an overlappable item, the
            overlapped item is restored.

        .. Important:: Also important: If the direction is a
           :class:`~pygamelib.base.Vector2D`, the values will be rounded to the
           nearest integer (as move works with entire board cells). It allows for
           movement accumulation before actually moving. The step parameter is not used
           in that case.
        """
        if (
            self.parent is not None
            and isinstance(self.parent, Game)
            and self.parent.mode == constants.MODE_RT
            and isinstance(item, board_items.Movable)
            and item.can_move()
            and item.dtmove < item.movement_speed
        ):
            return
        elif not isinstance(item, board_items.Movable):  # pragma: no cover
            # This is actually test in tests/test_board.py in function test_move()
            # I have no idea why it is not registering as a tested statement
            raise base.PglObjectIsNotMovableException(
                (
                    f"Item '{item.name}' at position [{item.pos[0]}, "
                    f"{item.pos[1]}] is not a subclass of Movable, "
                    f"therefor it cannot be moved."
                )
            )
        item.dtmove = 0.0
        rounded_direction = base.Vector2D()
        # if isinstance(direction, base.Vector2D):
        #     # If direction is a vector, round the numbers to the next integer.
        #     rounded_direction = base.Vector2D(
        #         round(direction.row), round(direction.column)
        #     )
        # elif type(direction) is int:
        #     direction = base.Vector2D.from_direction(direction, step)
        #     # Else, just use the direction
        #     rounded_direction = direction
        #     if type(step) is not int:
        #         raise base.PglInvalidTypeException(
        #             "Board.move(item, direction, step): step must be an int."
        #         )
        # else:
        #     raise base.PglInvalidTypeException(
        #         "Board.move(item, direction, step): direction must be a Vector2D or"
        #         " a constant direction."
        #     )
        if type(direction) is int:
            if type(step) is not int:
                raise base.PglInvalidTypeException(
                    "Board.move(item, direction, step): step must be an int."
                )
            direction = base.Vector2D.from_direction(direction, step)
        if not isinstance(direction, base.Vector2D):
            raise base.PglInvalidTypeException(
                "Board.move(item, direction, step): direction must be a Vector2D or"
                " a constant direction."
            )
        item._accumulator += direction
        rounded_direction.row = round(item._accumulator.row - item._accumulator.row % 1)
        item._accumulator.row -= rounded_direction.row
        rounded_direction.column = round(
            item._accumulator.column - item._accumulator.column % 1
        )
        item._accumulator.column -= rounded_direction.column
        if isinstance(item, board_items.BoardComplexItem):
            return self._move_complex(item, rounded_direction, step)
        else:
            return self._move_simple(item, rounded_direction, step)

    def _move_simple(self, item, direction, step=1):
        # Since the user is not supposed to call directly that method we assume that it
        # is called by move(), therefor the item is a subclass of Movable.
        new_row = None
        new_column = None
        # move() now exclusively pass Vector2D objects to _move_* so we don't need that
        # anymore
        # if not isinstance(direction, base.Vector2D):
        #     direction = base.Vector2D.from_direction(direction, step)
        new_row = item.pos[0] + direction.row
        new_column = item.pos[1] + direction.column
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
            # (1.3.0+) item without a third parameter returns the item from the top
            # layer
            dest_item = self.item(new_row, new_column, item.pos[2])
            if isinstance(dest_item, board_items.Actionable):
                if (
                    (
                        isinstance(item, board_items.Player)
                        and (
                            (dest_item.perm == constants.PLAYER_AUTHORIZED)
                            or (dest_item.perm == constants.ALL_CHARACTERS_AUTHORIZED)
                        )
                    )
                    or (
                        isinstance(item, board_items.NPC)
                        and (
                            (dest_item.perm == constants.NPC_AUTHORIZED)
                            or (dest_item.perm == constants.ALL_CHARACTERS_AUTHORIZED)
                        )
                    )
                    or (dest_item.perm == constants.ALL_MOVABLE_AUTHORIZED)
                ):
                    dest_item.activate()
            # Now we check if the destination contains a pickable item.
            # NOTE: I'm not sure why I decided that pickables were not overlappable.
            #       So I removed that limitation.
            # pickable_item = self.item(new_row, new_column)
            if (
                dest_item.pickable()
                and isinstance(item, board_items.Movable)
                and item.has_inventory()
            ):
                # Put the item in the inventory
                item.inventory.add_item(dest_item)
                # And then clear the cell (this is usefull for the next one)
                self.remove_item(dest_item)
                dest_item = self.item(dest_item.row, dest_item.column, item.pos[2])
            # Finally we check if the destination is overlappable
            if dest_item.overlappable():
                # And if it is, we check if the destination is restorable
                # Before 1.3.0 only Immovable objects were restorable. After, all
                # BoardItems can be restorable. So the check for Immovable have been
                # removed.
                self.clear_cell(item.pos[0], item.pos[1], item.pos[2])
                self.place_item(item, new_row, new_column, dest_item.pos[2])

    def _create_missing_layers(self, row, column, target_layer):
        # Create the layers that are missing between the current layer stack and
        # target_layer
        for i in range(len(self._matrix[row][column]), target_layer + 1):
            self._matrix[row][column].append(None)
            self.init_cell(row, column, i)

    def _adjust_items_layers(self, row, column, layer, value):
        # Adjust the layers of all items over the specified layer by value.
        # WARNING: call that method AFTER creating or removing layers !!
        for lidx in range(layer, len(self._matrix[row][column])):
            self._matrix[row][column][lidx].pos[2] += value

    def clear_cell(self, row, column, layer=0):
        """Clear cell (row, column, layer)

        This method clears a cell, meaning it position a
        void_cell BoardItemVoid at these coordinates.

        It also removes the items from the the list of movables and immovables.

        :param row: The row of the item to remove
        :type row: int
        :param column: The column of the item to remove
        :type column: int
        :param layer: The layer of the item to remove. The default value is 0 to remain
           coherent with previous version of the library.
        :type layer: int

        Example::

            myboard.clear_cell(3,4,0)

        .. WARNING:: This method does not check the content before,
            it *will* overwrite the content.

        .. Important:: In the case of a BoardComplexItem derivative (Tile, ComplexPlayer
           , ComplexNPC, etc.) clearing one cell of the entire item is enough to remove
           the entire item from the list of movables or immovables.

        .. note:: Starting in 1.3.0 and the addition of board's layers, there is no
           more overlapping matrix. With no more moving items around this method should
           be a little faster. It also means that the layer parameter is really
           important (a wrong layer means that you'll clear the wrong cell). Be ready to
           catch an IndexError exception

        """
        if layer >= len(self._matrix[row][column]):
            # If the layer is greater than the number of layers, there's nothing to do
            # so we just return.
            # NOTE: That design choice is discutable. I think it could be better to
            # raise an exception.
            return

        item = self.item(row, column, layer)
        # Again: if item is None, there's a serious problem here. In that case we just
        # let the code crash to let the programmer know that something is wrong.
        # The pygamelib never lets a cell to be None.
        if item in self._movables:
            self._movables.discard(item)
        elif item in self._immovables:
            self._immovables.discard(item)

        if (
            item.particle_emitter is not None
            and item.particle_emitter in self._particle_emitters
        ):
            self._particle_emitters.discard(item.particle_emitter)
        # self._matrix[row][column][layer] = None
        # self.init_cell(row, column, layer)

        if layer == 0:
            # If the layer to clear is 0 there is nothing under it, so we
            # just put a void item.
            self.init_cell(row, column, 0)
        elif layer == len(self._matrix[row][column]) - 1:
            # If the layer is the last one we just remove it
            self._matrix[row][column].pop(layer)
            # Then we make sure that no void layers remains under it.
            self._clean_layers(row, column)
        elif layer < len(self._matrix[row][column]) - 1 and layer > 0:
            # If the layer is neither the first or last
            if self._matrix[row][column][-1]._auto_layer:
                self._matrix[row][column].pop(layer)
                self._adjust_items_layers(row, column, layer, -1)
            else:
                self.init_cell(row, column, layer)

        # Now making sure that we are not leaving a cell with no layer
        if len(self._matrix[row][column]) <= 0:
            # Since it is not supposed to happen it is a tough one to test. Excluding
            # for now.
            self._matrix[row][column].append(
                self.generate_void_cell()
            )  # pragma: no cover

    def _clean_layers(self, row, column):
        layer = len(self._matrix[row][column]) - 1
        while 1:
            if (
                isinstance(self._matrix[row][column][layer], board_items.BoardItemVoid)
                and layer > 0
            ):
                self._matrix[row][column].pop(layer)
                layer -= 1
            else:
                # This statement is tested in test_engine_screen.py in the
                # test_screen_buffer method (and it works or else it would lead to an
                # infinite loop).
                break  # pragma: no cover

    def get_movables(self, **kwargs):
        """Return a list of all the Movable objects in the Board.

        See :class:`pygamelib.board_items.Movable` for more on a Movable object.

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

        See :class:`pygamelib.board_items.Immovable` for more on
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

    def serialize(self):
        """Return a serialized version of the board.

        :return: A dictionary containing the board's attributes.

        Example::

            serialized_board_data = myboard.serialize()

        """
        data = {}
        data["name"] = self.name
        # Mostly to differentiate from serialization by Game.save_board() from pygamelib
        # version prior to 1.3.0.
        data["data_version"] = 2
        data["size"] = self.size
        data["player_starting_position"] = self.player_starting_position
        data["ui_border_left"] = self.ui_border_left
        data["ui_border_right"] = self.ui_border_right
        data["ui_border_top"] = self.ui_border_top
        data["ui_border_bottom"] = self.ui_border_bottom
        data["ui_board_void_cell"] = self.ui_board_void_cell
        if self.ui_board_void_cell_sprixel is not None:
            data[
                "ui_board_void_cell_sprixel"
            ] = self.ui_board_void_cell_sprixel.serialize()
        else:
            data["ui_board_void_cell_sprixel"] = core.Sprixel(
                self.ui_board_void_cell
            ).serialize()
        data["DISPLAY_SIZE_WARNINGS"] = self.DISPLAY_SIZE_WARNINGS
        data["partial_display_viewport"] = self.partial_display_viewport
        data["partial_display_focus"] = self.partial_display_focus
        data["enable_partial_display"] = self.enable_partial_display
        data["map_data"] = {}

        # Now we need to run through all the cells to store
        # anything that is not a BoardItemVoid
        for x in self._matrix:
            for y in x:
                for z in y:
                    if not isinstance(z, board_items.BoardItemVoid) and not isinstance(
                        z, board_items.Player
                    ):
                        data["map_data"][
                            str((z.row, z.column, z.layer))
                        ] = z.serialize()

        return data

    @classmethod
    def load(cls, data: dict = None):
        """
        Create a new Board object based on serialized data.

        If data is None, None is returned.

        If a color component is missing from data, it is set to 0 (see examples).

        Raises an exception if the color components are not integer.

        :param data: Data loaded from JSON data (serialized).
        :type data: dict
        :returns: Either a Board object or None if data where empty.
        :rtype: :class:`Board` | NoneType
        :raise: :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            # Loading from parsed JSON data
            new_board = Board.load(json.load("board_lvl_01.json"))
        """
        if data is None or data == "":
            return
        # Now we check that the data is in the correct format
        if "data_version" in data.keys() and data["data_version"] >= 2:
            tmp = cls(
                name=data["name"],
                size=data["size"],
                player_starting_position=data["player_starting_position"],
                ui_border_left=data["ui_border_left"],
                ui_border_right=data["ui_border_right"],
                ui_border_top=data["ui_border_top"],
                ui_border_bottom=data["ui_border_bottom"],
                ui_board_void_cell=data["ui_board_void_cell"],
                ui_board_void_cell_sprixel=core.Sprixel.load(
                    data["ui_board_void_cell_sprixel"]
                ),
                DISPLAY_SIZE_WARNINGS=data["DISPLAY_SIZE_WARNINGS"],
                partial_display_viewport=data["partial_display_viewport"],
                partial_display_focus=data["partial_display_focus"],
                enable_partial_display=data["enable_partial_display"],
            )
            for k in data["map_data"].keys():
                (r, c, l) = ast.literal_eval(k)
                item = Board.instantiate_item(data["map_data"][k])
                if item is not None:
                    tmp.place_item(item, r, c, l)
        return tmp

    @staticmethod
    def instantiate_item(data: dict):
        """Instantiate a BoardItem from its serialized data.

        :param data: The data to use to build the item.
        :type data: dict
        :returns: an instance of a :class:`~pygamelib.board_items.BoardItem`.

        .. important:: The actual object depends on the serialized data. It can be any
           derivative of BoardItem (even custom objects as long as they inherit from
           BoardItem) as long as they are importable by this class.

        Example::

            # First get some board item serialization data. For example:
            data = super_duper_npc.serialize()
            # Then instantiate a new one:
            another_super_duper_npc = Board.instantiate_item(data)
        """
        obj_full_str = data["object"].split("'")[-2]
        obj_str = obj_full_str.split(".")[-1]
        item = None
        # If it's a board item, we get it from the already imported module.
        if obj_str in dir(board_items):
            bi = eval(f"board_items.{obj_str}")
            item = bi.load(data)
        # otherwise, we import the module and instantiate the required object.
        # This means that the module is in the path of course.
        else:
            try:
                exec(f"import {obj_full_str.split('.')[0]}")
                bi = eval(f"{obj_full_str}")
                item = bi.load(data)
            except Exception as e:
                raise e
        return item

    def neighbors(self, obj, radius: int = 1):
        """Returns a list of neighbors (non void item) around an object.

        This method returns a list of objects that are all around an object between the
        position of an object and all the cells at **radius**.

        :param radius: The radius in which non void item should be included
        :type radius: int
        :param obj: The central object. The neighbors are calculated for that object.
        :type obj: :class:`~pygamelib.board_items.BoardItem`
        :return: A list of BoardItem. No BoardItemVoid is included.
        :raises PglInvalidTypeException: If radius is not an int.

        Example::

            for item in game.neighbors(npc, 2):
                print(f'{item.name} is around {npc.name} at coordinates '
                    '({item.pos[0]},{item.pos[1]})')
        """
        if type(radius) is not int:
            raise base.PglInvalidTypeException(
                "In Board.neighbors(obj, radius), radius must be an integer."
                f" Got {radius} of type {type(radius)} instead."
            )
        if not isinstance(obj, board_items.BoardItem):
            raise base.PglInvalidTypeException(
                "In Board.neighbors(object, radius), object must be a BoardItem."
                f" Got {obj} of type {type(obj)} instead."
            )
        return_array = []
        for x in range(-radius, radius + 1, 1):
            for y in range(-radius, radius + 1, 1):
                if x == 0 and y == 0:
                    continue
                true_x = obj.pos[0] + x
                true_y = obj.pos[1] + y
                if (true_x < self.size[1] and true_y < self.size[0]) and not isinstance(
                    self.item(true_x, true_y), board_items.BoardItemVoid
                ):
                    return_array.append(self.item(true_x, true_y))
        return return_array


class Game(base.PglBaseObject):
    """A class that serve as a game engine.

    This object is the central system that allow the management of a game. It holds
    boards (see :class:`pygamelib.engine.Board`), associate it to level, takes care of
    level changing, etc.



    .. note:: The game object has an object_library member that is always an empty array
        except just after loading a board. In this case, if the board have a "library"
        field, it is going to be used to populate object_library. This library is
        accessible through the Game object mainly so people have access to it across
        different Boards during level design in the editor. That architecture decision
        is debatable.

    .. note:: The constructor of Game takes care of initializing the terminal to
        properly render the colors on Windows.

    .. important:: The Game object automatically assumes ownership over the Player.

    .. role:: boldblue
    .. role:: blue

    """

    # TODO: Documentation for a future release.
    # FIXME: Lines messed up because linting.
    # :param enable_physic: Enable or disable physic. Please read after.
    # :type enable_physic: bool
    # When physic is enable, it automatically set the mode to MODE_RT. The movement is
    #  not
    # using step, step_horizontal and step_vertical but it using the velocity attribute
    #  of
    # :class:`pygamelib.board_items.Movable` objects. The velocity is integrated over
    #  time
    # and gravity is automatically added to the forces.
    # The engine sets Game.gravity to Vector2D(9.81, 0) (you can change it later).
    # Gravity
    # is automatically integrated over time and added to the velocity of movable
    #  objects.
    # If you want physics without gravity you just have to set it to a null vector.
    # If you want to manage gravity by yourself, also set Game.gravity to a null vector.
    # :class:`pygamelib.board_items.Movable` objects can explicitely request to not be
    # subjected to physic by setting the ignore_physic attribute to True. It is the
    # default for :class:`pygamelib.board_items.Projectile` objects.

    __instance = None  # Class variable stores the singleton instance of Game object

    def __init__(
        self,
        name="Game",
        player=None,
        boards={},
        menu={},
        current_level=None,
        enable_partial_display=False,
        partial_display_viewport=None,
        partial_display_focus=None,
        mode=constants.MODE_TBT,
        user_update=None,
        input_lag=0.01,
        user_update_paused=None,
        # enable_physic=False,
    ):
        """
        :param name: The Game name.
        :type name: str
        :param boards: A dictionary of boards with the level number as key and a board
            reference as value.
        :type boards: dict
        :param menu: A dictionary of menus with a category (str) as key and another
            dictionary (key: a shortcut, value: a description) as value.
        :type menu: dict
        :param current_level: The current level.
        :type current_level: int
        :param enable_partial_display: A boolean to tell the Game object to enable or
            not partial display of boards. Default: False.
        :type enable_partial_display: bool
        :param partial_display_viewport: A 2 int elements array that gives the
            **radius** of the partial display in number of row and column. Please see
            :func:`~pygamelib.engine.Board.display_around()`.
        :type partial_display_viewport: list
        :param partial_display_focus: The object that is going to be the center of the
           view when the board is displayed.
        :type partial_display_focus: :class:`~pygamelib.board_items.BoardItem`
        :param mode: The mode parameter configures the way the run() method is going to
           behave. The default value is constants.MODE_TBT. TBT is short for "Turn By
           Turn". In that mode, the Game object wait for an user input before looping.
           Exactly like when you wait for user input with get_key(). The other possible
           value is constants.MODE_RT. RT stands for "Real Time". In that mode, the Game
           object waits for a minimal amount of time (0.01 i.e 100 FPS, configurable
           through the input_lag parameter) in order to get the input from the user and
           call the update function right away. This parameter is *only* useful if you
           use Game.run().
        :type mode: int
        :param user_update: A reference to the main program update function. The update
           function is called for each new frame. It is called with 3 parameters: the
           game object, the user input (can be None) and the elapsed time since last
           frame.
        :type user_update: function
        :param user_update_paused: A reference to the update function called when the
           game is paused. It is called with the same 3 parameters than the regular
           update function: the game object, the user input (can be None) and the
           elapsed time since last frame. If not specified, the regular update function
           is called but nothing is done regarding NPCs, projectiles, animations, etc.
        :type user_update_paused: function
        :param input_lag: The amount of time the run() function is going to wait for a
           user input before returning None and calling the update function. Default is
           0.01.
        :type input_lag: float|int
        """
        super().__init__()
        self.name = name
        self._boards = boards
        self._menu = menu
        self.current_level = current_level
        self.player = player
        self.__state = constants.RUNNING
        self.enable_partial_display = enable_partial_display
        self.partial_display_viewport = partial_display_viewport
        self.partial_display_focus = partial_display_focus
        self._config = None
        self._configuration = None
        self._configuration_internals = None
        self.object_library = []
        self.terminal = base.Console.instance()
        self.screen = Screen()
        self.mode = mode
        self.user_update = user_update
        self.user_update_paused = None
        self.input_lag = input_lag
        self._logs = []
        self.ENABLE_SESSION_LOGS = False
        # TODO : In future release I'll add physic
        # self.enable_physic = enable_physic
        # # If physic is enabled we turn the mode to realtime (we need time integration)
        # if self.enable_physic:
        #     self.mode = constants.MODE_RT
        #     self.gravity = base.Vector2D(9.81, 0)
        # else:
        #     self.gravity = None

        base.init()
        # In the case where user_update is defined, we cannot start the game on our own.
        # We need the user to start it first.
        if self.user_update is not None:
            self.__state = constants.PAUSED
        if user_update_paused is not None:
            self.user_update_paused = user_update_paused
        self.previous_time = time.time()
        self.__execute_run = None

    @property
    def state(self):
        """Get/set the state of the game.

        :param value: The new state of the game (from the constants module).
        :type value: int
        :return: The state of the game.
        :rtype: int

        The observers are notified of a change of state with the
        :boldblue:`pygamelib.engine.Game.state` event. The new state is passed as the
        :blue:`value` of the event.
        """
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
        if value == constants.PAUSED:
            if self.user_update_paused is None:
                self.user_update_paused = self._fake_update_paused
        elif value == constants.RUNNING:
            self._set_run_function()
        self.notify(self, "pygamelib.engine.Game.state", value)

    @classmethod
    def instance(cls, *args, **kwargs):
        """Returns the instance of the Game object

        Creates a Game object on first call an then returns the same instance
        on further calls

        :return: Instance of Game object

        """
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    def run(self):
        """
        .. versionadded:: 1.2.0

        The run() method act as the main game loop and does a number of things for you:

         1. It grabs the user input. If the Game object is configured with MODE_TBT (the
            default), nothing happen until the user hit a key. If the mode is set to
            MODE_RT, it will wait for input_lag secondes for a user input before going
            to step 3.
         2. It calculate the elapsed time between 2 frames.
         3. Accumulates the elapsed time in the player dtmove variable (if there is a
            player object configured)
         4. It sets the cursor position to 0,0 (meaning that your user_update function
            will draw on top of the previously drawn window). The Board.display() and
            Board.display_around() method clean the end of their line.
         5. It calls the user_update function with 3 parameters: the game object, the
            key hit by the user (it can be None) and the elapsed time between to calls.
         6. Clears the end of the screen.
         7. Actuates NPCs (If there is at least one Board manage by Game).
         8. Actuates projectiles (If there is at least one Board manage by Game).
         9. Animates items (If there is at least one Board manage by Game).

        On the subject of particle emitters, the :class:`Board` object automatically
        update the ones that are attached to BoardItems. For all other particle emitters
        you need to call the update method of the emitters yourself (for now).

        In version 1.2.X, there was a bug when the game was paused. In that case nothing
        was happening anymore. The user update function was not called and events were
        not processed. On top of that it was impossible to use run() without associating
        a board object with a level.
        Starting with version 1.3.0, it is now possible to use run() without associating
        a board object with a level. There is also a new parameter to the
        constructor (user_update_paused) that allows you to specify a function that will
        be called when the game is paused. This function will be called with the same
        3 parameters than the regular update function: the game object, the user input
        (can be None) and the elapsed time since last frame.

        .. Important:: If you try to set the game state to PAUSED and the
           user_update_paused function is not defined, a notification will be issued
           and the game will continue to run. The notification message is
           :boldblue:`pygamelib.engine.Game.run:PauseNotAvailable`

        :raises: PglInvalidTypeException, PglInvalidTypeException

        Example::

            mygame.run()
        """
        # run() automatically position the cursor to 0,0 after calling user_update
        # if the lines are "end of line" safe (i.e using Game.display_line()) you don't
        # need to clear the screen.
        # The game will also automatically enter fullscreen mode and restore the
        # terminal state after.
        if self.user_update is None:
            raise base.PglInvalidTypeException(
                "Game.run(): user_update cannot be undefined."
            )
        if not callable(self.user_update):
            raise base.PglInvalidTypeException(
                "Game.run(): user_update must be callable."
            )
        # Auto start if game hasn't be started before
        if self.state == constants.PAUSED:
            self.start()
        # Update the inkey timeout based on mode
        # This cannot be automatically tested as it means the main loop requires an user
        # input.
        if self.mode == constants.MODE_TBT:  # pragma: no cover
            self.input_lag = None
        self.previous_time = time.perf_counter()
        if self.player is None:
            self.player = constants.NO_PLAYER
        # Now we check that we do have a current board. If not, it means that the user
        # wants to use the game object without any board.
        self._set_run_function()

        with self.terminal.cbreak(), self.terminal.hidden_cursor(), (
            self.terminal.fullscreen()
        ):
            self.__execute_run()

    # The goal of these _run_* functions is to avoid using if statements in the while
    # loop. Each crumble of performance is worth a little bit of extra code.
    def _run_with_board(self):
        # This runs until the game stops
        while self.state != constants.STOPPED:
            # But we only update if the game is not paused
            in_key = self.terminal.inkey(timeout=self.input_lag)
            elapsed = time.perf_counter() - self.previous_time
            self.previous_time = time.perf_counter()
            if self.state == constants.RUNNING:
                if self.player != constants.NO_PLAYER:
                    self.player.dtmove += elapsed
                # print(self.terminal.home, end="")
                self.user_update(self, in_key, elapsed)
                # print(self.terminal.clear_eos, end="")
                self.actuate_npcs(self.current_level, elapsed)
                self.actuate_projectiles(self.current_level, elapsed)
                self.animate_items(self.current_level, elapsed)
            elif self.state == constants.PAUSED:
                print(self.terminal.home, end="")
                self.user_update_paused(self, in_key, elapsed)
                print(self.terminal.clear_eos, end="")

    def _set_run_function(self):
        if self.current_level is None or self.current_board() is None:
            self.__execute_run = self._run_without_board
        else:
            self.__execute_run = self._run_with_board

    def _run_without_board(self):
        # This runs until the game stops
        while self.state != constants.STOPPED:
            in_key = self.terminal.inkey(timeout=self.input_lag)
            elapsed = time.perf_counter() - self.previous_time
            self.previous_time = time.perf_counter()
            # But we only update if the game is not paused
            if self.state == constants.RUNNING:
                print(self.terminal.home, end="")
                self.user_update(self, in_key, elapsed)
                print(self.terminal.clear_eos, end="")
            elif self.state == constants.PAUSED:
                print(self.terminal.home, end="")
                self.user_update_paused(self, in_key, elapsed)
                print(self.terminal.clear_eos, end="")

    def _fake_update_paused(self, game, in_key, elapsed):
        self.notify(
            self,
            "pygamelib.engine.Game.run:PauseNotAvailable",
            "pygamelib.engine.Game.run(): user_update_paused is not defined.",
        )
        self.start()

    def session_log(self, line: str) -> None:
        """Add a line to the session logs.

        Session logs needs to be activated first.

        :param line: The line to add to the logs.
        :type line: str

        Example::

            game = Game.instance()
            game.ENABLE_SESSION_LOGS = True
            game.session_log('Game engine initialized')

        .. note:: The session log system is nothing more than a list to do your "debug
           prints". If you want a real logging system, please use Python logging module.
        """
        if self.ENABLE_SESSION_LOGS:
            self._logs.append(line)

    def session_logs(self) -> list:
        """Return the complete session logs since instantiation.

        Example::

            game = Game.instance()
            game.ENABLE_SESSION_LOGS = True
            for line in game.logs():
                print(line)

        .. note:: The session log system is nothing more than a list to do your "debug
           prints". If you want a real logging system, please use Python logging module.
        """
        return self._logs

    def clear_session_logs(self) -> None:
        """Delete all the log lines from the logs.

        Example::

            game = Game.instance()
            game.clear_logs()

        .. note:: The session log system is nothing more than a list to do your "debug
           prints". If you want a real logging system, please use Python logging module.
        """
        self._logs = list()

    def add_menu_entry(self, category, shortcut, message, data=None):
        """Add a new entry to the menu.

        .. deprecated:: 1.3.0
           This function will be removed in version 1.4.0

        Add another shortcut and message to the specified category.

        Categories help organize the different sections of a menu or dialogues.

        :param category: The category to which the entry should be added.
        :type category: str
        :param shortcut: A shortcut (usually one key) to display.
        :type shortcut: str
        :param message: a message that explains what the shortcut does.
        :type message: str
        :param data: a data that you can get from the menu object.
        :type message: various

        The shortcut and data is optional.

        Example::

            game.add_menu_entry('main_menu','d','Go right',constants.RIGHT)
            game.add_menu_entry('main_menu',None,'-----------------')
            game.add_menu_entry('main_menu','v','Change game speed')

        """
        if category in self._menu.keys():
            self._menu[category].append(
                {"shortcut": shortcut, "message": message, "data": data}
            )
        else:
            self._menu[category] = [
                {"shortcut": shortcut, "message": message, "data": data}
            ]

    def delete_menu_category(self, category=None):
        """Delete an entire category from the menu.

        .. deprecated:: 1.3.0
           This function will be removed in version 1.4.0

        That function removes the entire list of messages that are attached to the
        category.

        :param category: The category to delete.
        :type category: str
        :raise PglInvalidTypeException: If the category is not a string

        .. important:: If the entry have no shortcut it's advised not to try to update
            unless you have only one NoneType as a shortcut.

        Example::

            game.add_menu_entry('main_menu','d','Go right')
            game.update_menu_entry('main_menu','d','Go LEFT',constants.LEFT)

        """
        if type(category) is str and category in self._menu:
            del self._menu[category]
        else:
            raise base.PglInvalidTypeException(
                "in Game.delete_menu_entry(): category cannot be anything else but a"
                "string."
            )

    def update_menu_entry(self, category, shortcut, message, data=None):
        """Update an entry of the menu.

        .. deprecated:: 1.3.0
           This function will be removed in version 1.4.0

        Update the message associated to a category and a shortcut.

        :param category: The category in which the entry is located.
        :type category: str
        :param shortcut: The shortcut of the entry you want to update.
        :type shortcut: str
        :param message: a message that explains what the shortcut does.
        :type message: str
        :param data: a data that you can get from the menu object.
        :type message: various

        .. important:: If the entry have no shortcut it's advised not to try to update
            unless you have only one NoneType as a shortcut.

        Example::

            game.add_menu_entry('main_menu','d','Go right')
            game.update_menu_entry('main_menu','d','Go LEFT',constants.LEFT)

        """
        for e in self._menu[category]:
            if e["shortcut"] == shortcut:
                e["message"] = message
                if data is not None:
                    e["data"] = data

    def get_menu_entry(self, category, shortcut):
        """Get an entry of the menu.

        .. deprecated:: 1.3.0
           This function will be removed in version 1.4.0

        This method return a dictionnary with 3 entries :

            * shortcut
            * message
            * data

        :param category: The category in which the entry is located.
        :type category: str
        :param shortcut: The shortcut of the entry you want to get.
        :type shortcut: str
        :return: The menu entry or None if none was found
        :rtype: dict

        Example::

            ent = game.get_menu_entry('main_menu','d')
            game.move_player(int(ent['data']),1)

        """
        if category in self._menu:
            for e in self._menu[category]:
                if e["shortcut"] == shortcut:
                    return e
        return None

    def display_menu(
        self, category, orientation=constants.ORIENTATION_VERTICAL, paginate=10
    ):
        """Display the menu.

        .. deprecated:: 1.3.0
           This function will be removed in version 1.4.0

        This method display the whole menu for a given category.

        :param category: The category to display. **Mandatory** parameter.
        :type category: str
        :param orientation: The shortcut of the entry you want to get.
        :type orientation: :class:`pygamelib.constants`
        :param paginate: pagination parameter (how many items to display before
                        changing line or page).
        :type paginate: int

        Example::

            game.display_menu('main_menu')
            game.display_menu('main_menu', constants.ORIENTATION_HORIZONTAL, 5)

        """
        line_end = "\n"
        if orientation == constants.ORIENTATION_HORIZONTAL:
            line_end = " | "
        if category not in self._menu:
            raise base.PglException(
                "invalid_menu_category",
                f"The '{category}' category is not registered in the menu. Did you add"
                f"a menu entry in that category with Game.add_menu_entry('{category}',"
                f"'some shortcut','some message') ? If yes, then you should check "
                f"for typos.",
            )
        pagination_counter = 1
        for k in self._menu[category]:
            if k["shortcut"] is None:
                print(k["message"], end=line_end)
            else:
                print(f"{k['shortcut']} - {k['message']}", end=line_end)
                pagination_counter += 1
                if pagination_counter > paginate:
                    print("")
                    pagination_counter = 1

    def clear_screen(self):
        """
        Clear the whole screen (i.e: remove everything written in terminal)

        .. deprecated:: 1.2.0
           Starting 1.2.0 we are using the pygamelib.engine.Screen object to manage
           the screen. That function is a simple forward and is kept for backward
           compatibility only. You should use Game.screen.clear()
        """
        self.screen.clear()

    @staticmethod
    def get_key():
        """Reads the next key-stroke returning it as a string.

        Example::

            key = Utils.get_key()
            if key == Utils.key.UP:
                print("Up")
            elif key == "q"
                exit()

        .. note:: See `readkey` documentation in `readchar` package.
        """
        # Not testable automatically
        return readkey()  # pragma: no cover

    def load_config(self, filename: str, section: str = "main") -> dict:
        """
        Load a configuration file from the disk.
        The configuration file must respect the INI syntax.
        The goal of these methods is to simplify configuration files management.

        :param filename: The filename to load. does not check for existence.
        :type filename: str
        :param section: The section to put the read config file into. This allow for
            multiple files for multiple purpose. Section is a human readable unique
            identifier.
        :type section: str
        :raise FileNotFoundError: If filename is not found on the disk.
        :raise json.decoder.JSONDecodeError: If filename could not be decoded as JSON.
        :returns: The parsed data.
        :rtype: dict

        .. warning:: **breaking changes:** before v1.1.0 that method use to load file
            using the configparser module. This have been dumped in favor of json files.
            Since that methods was apparently not used, there is no backward
            compatibility.

        Example::

            mygame.load_config('game_controls.json','game_control')

        """
        if self._configuration is None:
            self._configuration = {}
        if self._configuration_internals is None:
            self._configuration_internals = {}

        if section not in self._configuration_internals:
            self._configuration_internals[section] = {}

        with open(filename) as config_file:
            config_content = json.load(config_file)
            if section not in self._configuration.keys():
                self._configuration[section] = config_content
                self._configuration_internals[section]["loaded_from"] = filename
                return config_content

    def config(self, section: str = "main") -> dict:
        """Get the content of a previously loaded configuration section.

        :param section: The name of the section.
        :type section: str

        Example::

            if mygame.config('main')['pgl-version-required'] < 10200:
                print('The pygamelib version 1.2.0 or greater is required.')
                exit()
        """
        if section in self._configuration:
            return self._configuration[section]

    def create_config(self, section: str) -> None:
        """Initialize a new config section.

        The new section is a dictionary.

        :param section: The name of the new section.
        :type section: str

        Example::

            if mygame.config('high_scores') is None:
                mygame.create_config('high_scores')
            mygame.config('high_scores')['first_place'] = mygame.player.name
        """
        if self._configuration is None:
            self._configuration = {}
        if self._configuration_internals is None:
            self._configuration_internals = {}
        self._configuration[section] = {}
        self._configuration_internals[section] = {}

    def save_config(
        self, section: str = None, filename: str = None, append: bool = False
    ) -> None:
        """
        Save a configuration section.

        :param section: The name of the section to save on disk.
        :type section: str
        :param filename: The file to write in. If not provided it will write in the file
            that was used to load the given section. If section was not loaded from a
            file, save will raise an exception.
        :type filename: str
        :param append: Do we need to append to the file or replace the content
            (True = append, False = replace)
        :type append: bool

        Example::

            mygame.save_config('game_controls', 'data/game_controls.json')
        """
        if section is None:
            raise base.PglInvalidTypeException(
                "Game.save_config: section cannot be None."
            )
        elif section not in self._configuration:
            raise base.PglException(
                "unknown section", f"section {section} does not exists."
            )
        if (
            filename is None
            and "loaded_from" not in self._configuration_internals[section]
        ):
            raise base.PglInvalidTypeException(
                "filename cannot be None if section is new or was loaded manually."
            )
        elif filename is None:
            filename = self._configuration_internals[section]["loaded_from"]
        mode = "w"
        if append:
            mode = "a"
        with open(filename, mode) as file:
            json.dump(self._configuration[section], file)

    def add_board(self, level_number: int, board: Board) -> None:
        """Add a board for the level number.

        This method associate a Board (:class:`pygamelib.engine.Board`) to a level
        number.

        If the partial display is enabled at Game level (i.e: partial_display_viewport
        is not None and enable_partial_display is True), this method propagate the
        settings to the board automatically. Same for partial_display_focus.

        Example::

            game.add_board(1,myboard)

        :param level_number: the level number to associate the board to.
        :type level_number: int
        :param board: a Board object corresponding to the level number.
        :type board: pygamelib.engine.Board

        :raises PglInvalidTypeException: If either of these parameters are not of the
            correct type.
        """
        if type(level_number) is int:
            if isinstance(board, Board):
                # Propagate partial display settings.
                if (
                    self.enable_partial_display
                    and self.partial_display_viewport is not None
                ):
                    board.partial_display_viewport = self.partial_display_viewport
                    board.enable_partial_display = self.enable_partial_display
                    if self.partial_display_focus is not None:
                        board.partial_display_focus = self.partial_display_focus
                # Add the board to our list
                self._boards[level_number] = {
                    "board": board,
                    "npcs": [],
                    "projectiles": [],
                }
                # Taking ownership
                board.parent = self
            else:
                raise base.PglInvalidTypeException(
                    "The board paramater must be a pygamelib.engine.Board() object."
                )
        else:
            raise base.PglInvalidTypeException("The level number must be an int.")

    def __rename_level(self, init_lvl_num, dest_lvl_num):
        # Recursive method to find the first available position to re-index down all
        # boards.
        init_level = self._boards[init_lvl_num]
        if dest_lvl_num in self._boards.keys():
            self.__rename_level(dest_lvl_num, dest_lvl_num + 1)
            self._boards[dest_lvl_num] = init_level
        else:
            self._boards[dest_lvl_num] = init_level

    def insert_board(self, level_number: int, board: Board) -> None:
        """Insert a board for the level number.

        This method does basically the same thing than :meth:`add_board` except that if
        the level number is already associated it re-affect the numbers down.

        Example::

            game.insert_board(1,myboard_1)
            # level number 1 is associated with myboard_1
            game.insert_board(2,myboard_2)
            # level number 1 is associated with myboard_1
            # level number 2 is associated with myboard_2
            game.insert_board(2,myboard_3)
            # level number 1 is associated with myboard_1
            # level number 2 is now associated with myboard_3
            # level number 3 is associated with myboard_2

        :param level_number: the level number to associate the board to.
        :type level_number: int
        :param board: a Board object corresponding to the level number.
        :type board: pygamelib.engine.Board

        :raises PglInvalidTypeException: If either of these parameters are not of the
            correct type.
        """
        if type(level_number) is int:
            if isinstance(board, Board):
                if level_number in self._boards.keys():
                    self.__rename_level(level_number, level_number + 1)
                    self.add_board(level_number, board)
                else:
                    self.add_board(level_number, board)
            else:
                raise base.PglInvalidTypeException(
                    "The board paramater must be a pygamelib.engine.Board() object."
                )
        else:
            raise base.PglInvalidTypeException("The level number must be an int.")

    def get_board(self, level_number: int) -> Board:
        """
        This method returns the board associated with a level number.
        :param level_number: The number of the level.
        :type level_number: int

        :raises PglInvalidTypeException: if the level_number is not an int.

        Example::

            level1_board = mygame.get_board(1)
        """
        if type(level_number) is int:
            return self._boards[level_number]["board"]
        else:
            raise base.PglInvalidTypeException("The level number must be an int.")

    def current_board(self) -> Board:
        """
        This method return the board object corresponding to the current_level.

        Example::

            game.current_board().display()

        If current_level is set to a value with no corresponding board a PglException
        exception is raised with an invalid_level error.
        """
        if len(self._boards) <= 0:
            return None
        elif self.current_level in self._boards.keys():
            return self._boards[self.current_level]["board"]
        else:
            raise base.PglInvalidLevelException(
                "The current level does not correspond to any board."
            )

    def change_level(self, level_number: int) -> None:
        """
        Change the current level, load the board and place the player to the right
        place.

        Example::

            game.change_level(1)

        :param level_number: the level number to change to.
        :type level_number: int

        :raises base.PglInvalidTypeException: If parameter is not an int.
        """
        if type(level_number) is int:
            if self.player is None:
                raise base.PglException(
                    "undefined_player",
                    "Game.player is undefined. We cannot change level without a player."
                    " Please set player in your Game object: mygame.player = Player()"
                    " or set mygame.player = constants.NO_PLAYER",
                )
            if level_number in self._boards.keys():
                # If player is not None and not NO_PLAYER let's work
                if self.player != constants.NO_PLAYER:
                    # If it's not already the case, taking ownership of player
                    if self.player.parent != self:
                        self.player.parent = self
                    if self.player.pos[0] is not None or self.player.pos[1] is not None:
                        self._boards[self.current_level]["board"].clear_cell(
                            self.player.pos[0], self.player.pos[1]
                        )
                    self._boards[level_number]["board"].place_item(
                        self.player,
                        self._boards[level_number]["board"].player_starting_position[0],
                        self._boards[level_number]["board"].player_starting_position[1],
                    )

                self.current_level = level_number
                if isinstance(self.screen, Screen):
                    self.screen.trigger_rendering()
            else:
                raise base.PglInvalidLevelException(
                    f"Impossible to change level to an unassociated level (level number"
                    f" {level_number} is not associated with any board).\nHave you "
                    f"called:\ngame.add_board({level_number},Board()) ?"
                )
        else:
            raise base.PglInvalidTypeException(
                "level_number needs to be an int in change_level(level_number)."
            )

    def delete_level(self, lvl_number: int = None):
        """Delete a level and its associated Board from the game object.

        Both the level and the board can't be used after that (unless they are reloaded
        or replaced of course).

        :param lvl_number: The number of the level to remove.
        :type lvl_number: int

        :raises base.PglInvalidTypeException: If parameter is not an int.
        :raises base.PglInvalidLevelException: If parameter is not a valid level.

        Example::

            my_game.delete_level(1)
        """
        if lvl_number is not None:
            if lvl_number in self._boards.keys():
                del self._boards[lvl_number]
            else:
                raise base.PglInvalidLevelException(
                    f"Game.delete_level(lvl_number) : {lvl_number} is not a previously"
                    " associated level."
                )
        else:
            raise base.PglInvalidTypeException(
                "Game.delete_level(lvl_number) : lvl_number needs to be an int. "
                f"{type(lvl_number)} is not an int."
            )

    def delete_all_levels(self):
        """Delete all boards and their associated levels from the game object.

        You might want to think twice before using that function...

        Example::

            game.delete_all_levels()
        """
        self._boards = {}

    def add_npc(
        self, level_number, npc, row=None, column=None, layer=None, auto_layer=True
    ):
        """
        Add a NPC to the game. It will be placed on the board corresponding to the
        level_number. If row and column are not None, the NPC is placed at these
        coordinates. Else, it's randomly placed in an empty cell.

        Example::

            game.add_npc(1,my_evil_npc,5,2)

        :param level_number: the level number of the board.
        :type level_number: int
        :param npc: the NPC to place.
        :type npc: pygamelib.board_items.NPC
        :param row: the row coordinate to place the NPC at.
        :type row: int
        :param column: the column coordinate to place the NPC at.
        :type column: int

        If either of these parameters are not of the correct type, a
        PglInvalidTypeException exception is raised.

        .. Important:: If the NPC does not have an actuator, this method is going to
            affect a pygamelib.actuators.RandomActuator() to
            npc.actuator. And if npc.step == None, this method sets it to 1
        """
        if type(level_number) is int:
            if isinstance(npc, board_items.NPC):
                if row is None or column is None:
                    retry = 0
                    if row is not None and type(row) is not int:
                        raise base.PglInvalidTypeException("row must be an int.")
                    if column is not None and type(column) is not int:
                        raise base.PglInvalidTypeException("column must be an int.")
                    while True:
                        # TODO: Use NPC.width and NPC.height instead of -1!!!!
                        if row is None:
                            row = random.randint(
                                0, self._boards[level_number]["board"].size[1] - 1
                            )
                        if column is None:
                            column = random.randint(
                                0, self._boards[level_number]["board"].size[0] - 1
                            )
                        if isinstance(
                            self._boards[level_number]["board"].item(row, column),
                            board_items.BoardItemVoid,
                        ):
                            break
                        # Too much randomness to test
                        else:  # pragma: no cover
                            row = None
                            column = None
                            retry += 1
                if type(row) is int:
                    if type(column) is int:
                        if npc.actuator is None:
                            npc.actuator = actuators.RandomActuator(
                                moveset=[
                                    constants.UP,
                                    constants.DOWN,
                                    constants.LEFT,
                                    constants.RIGHT,
                                ],
                                parent=npc,
                            )
                        if npc.step is None:
                            npc.step = 1
                            npc.step_horizontal = 1
                            npc.step_vertical = 1
                        if layer is None:
                            self._boards[level_number]["board"].place_item(
                                npc, row, column
                            )
                        else:
                            self._boards[level_number]["board"].place_item(
                                npc, row, column, layer, auto_layer
                            )
                        self._boards[level_number]["npcs"].append(npc)
                    else:
                        raise base.PglInvalidTypeException("column must be an int.")
                else:
                    raise base.PglInvalidTypeException("row must be an int.")
            else:
                raise base.PglInvalidTypeException(
                    "The npc paramater must be a pygamelib.board_items.NPC() object."
                )
        else:
            raise base.PglInvalidTypeException("The level number must be an int.")

    def actuate_npcs(self, level_number, elapsed_time=0.0):
        """Actuate all NPCs on a given level

        This method actuate all NPCs on a board associated with a level. At the moment
        it means moving the NPCs but as the Actuators become more capable this method
        will evolve to allow more choice (like attack use objects, etc.)

        When all NPCs have been successfully actuated, the observers are notified of the
        change with the :boldblue:`pygamelib.engine.Game.actuate_npcs:npcs_actuated`
        event. Their is :blue:`value` passed for that event.

        :param level_number: The number of the level to actuate NPCs in.
        :type level_number: int
        :param elapsed_time: The amount of time that passed since last call. This
            parameter is not mandatory.
        :type elapsed_time: float

        Example::

            mygame.actuate_npcs(1)

        .. note:: This method only move NPCs when their actuator state is RUNNING. If it
            is PAUSED or STOPPED, the NPC is not moved.

        .. note:: Since version 1.2.0 it's possible for a Movable item to have
           different vertical and horizontal movement steps, so actuate_npc respect that
           by integrating the steps with a unit direction vector. It should be
           completely transparent and you should not expect any change. Just more
           movement freedom. If you do experience issues, please report a bug.

        .. note:: Since version 1.2.0 and the appearance of the realtime mode, we have
           to account for movement speed. This method does it.
        """
        if self.state == constants.RUNNING:
            if type(level_number) is int:
                if level_number in self._boards.keys():
                    self.screen.trigger_rendering()
                    for npc in self._boards[level_number]["npcs"]:
                        if npc.actuator.state == constants.RUNNING:
                            # Account for movement speed
                            npc.dtmove += elapsed_time
                            if (
                                self.mode == constants.MODE_RT
                                and npc.dtmove < npc.movement_speed
                            ):
                                continue
                            # Since version 1.2.0 horizontal and vertical movement
                            # amplitude can be different so we proceed in 2 steps:
                            #  1 - build a unit direction vector
                            #  2 - use its component to build a movement vector
                            nm = npc.actuator.next_move()
                            d = nm
                            if not isinstance(nm, base.Vector2D):
                                d = base.Vector2D.from_direction(nm, 1)
                            self._boards[level_number]["board"].move(
                                npc,
                                base.Vector2D(
                                    d.row * npc.step_vertical,
                                    d.column * npc.step_horizontal,
                                ),
                            )
                            # npc.dtmove = 0.0
                    self.notify(
                        self, "pygamelib.engine.Game.actuate_npcs:npcs_actuated"
                    )
                else:
                    raise base.PglInvalidLevelException(
                        f"Impossible to actuate NPCs for this level (level number "
                        f"{level_number} is not associated with any board)."
                    )
            else:
                raise base.PglInvalidTypeException(
                    "In actuate_npcs(level_number) the level_number must be an int."
                )

    def add_projectile(self, level_number, projectile, row=None, column=None):
        """
        Add a Projectile to the game. It will be placed on the board corresponding to
        level_number. Neither row nor column can be None.

        Example::

            game.add_projectile(1, fireball, 5, 2)

        :param level_number: the level number of the board.
        :type level_number: int
        :param projectile: the Projectile to place.
        :type projectile: :class:`~pygamelib.board_items.Projectile`
        :param row: the row coordinate to place the Projectile at.
        :type row: int
        :param column: the column coordinate to place the Projectile at.
        :type column: int

        If either of these parameters are not of the correct type, a
        PglInvalidTypeException exception is raised.

        .. Important:: If the Projectile does not have an actuator, this method is going
            to affect pygamelib.actuators.RandomActuator(moveset=[RIGHT])
            to projectile.actuator. And if projectile.step == None, this method sets it
            to 1.

        """
        if type(level_number) is int:
            if isinstance(projectile, board_items.Projectile):
                if row is None or column is None:
                    raise base.PglInvalidTypeException(
                        "In Game.add_projectile neither row nor column can be None."
                    )
                if type(row) is int:
                    if type(column) is int:
                        # If we're trying to send a projectile out of the board's bounds
                        # We do nothing and return.
                        if (
                            row >= self._boards[level_number]["board"].size[1]
                            or column >= self._boards[level_number]["board"].size[0]
                            or row < 0
                            or column < 0
                        ):
                            return
                        # If there is something were we should put the projectile,
                        # then we consider it an immediate hit.
                        check_object = self._boards[level_number]["board"].item(
                            row, column
                        )
                        if (
                            not isinstance(check_object, board_items.BoardItemVoid)
                            and not check_object.overlappable()
                        ):
                            if projectile.is_aoe:
                                # AoE is easy, just return everything in range
                                projectile.hit(
                                    self.neighbors(projectile.aoe_radius, check_object)
                                )
                                return
                            else:
                                projectile.hit([check_object])
                                return
                        if projectile.actuator is None:
                            projectile.actuator = actuators.RandomActuator(
                                moveset=[constants.RIGHT]
                            )
                        if projectile.step is None:
                            projectile.step = 1
                            projectile.step_vertical = 1
                            projectile.step_horizontal = 1
                        self._boards[level_number]["board"].place_item(
                            projectile, row, column
                        )
                        self._boards[level_number]["projectiles"].append(projectile)
                    else:
                        raise base.PglInvalidTypeException("column must be an int.")
                else:
                    raise base.PglInvalidTypeException("row must be an int.")
            else:
                raise base.PglInvalidTypeException(
                    "The projectile paramater must be a "
                    "pygamelib.board_items.Projectile() object."
                )
        else:
            raise base.PglInvalidTypeException("The level number must be an int.")

    def remove_npc(self, level_number, npc):
        """This methods remove the NPC from the level in parameter.

        :param level: The number of the level from where the NPC is to be removed.
        :type level: int
        :param npc: The NPC object to remove.
        :type npc: :class:`~pygamelib.board_items.NPC`

        Example::

            mygame.remove_npc(1, dead_npc)
        """
        self._boards[level_number]["npcs"].remove(npc)
        self.get_board(level_number).clear_cell(npc.pos[0], npc.pos[1])

    def actuate_projectiles(self, level_number, elapsed_time=0.0):
        """Actuate all Projectiles on a given level

        This method actuate all Projectiles on a board associated with a level.
        This method differs from actuate_npcs() as some logic is involved with
        projectiles that NPC do not have.
        This method decrease the available range by projectile.step each time it's
        called.
        It also detects potential collisions.
        If the available range falls to 0 or a collision is detected the projectile
        hit_callback is called.

        This method respects the Projectile.collision_exclusions parameter and does not
        register collisions with objects of a type present in that list.

        .. Important:: In this method, projectiles do not collide with overlappable
           items. If you want to detect collisions with overlappable objects, please
           implement your own projectile actuation method.

        :param level_number: The number of the level to actuate Projectiles in.
        :type level_number: int
        :param elapsed_time: The amount of time that passed since last call. This
            parameter is not mandatory.
        :type elapsed_time: float

        When all Projectiles have been successfully actuated, the observers are notified
        of the change with the
        :boldblue:`pygamelib.engine.Game.actuate_projectiles:projectiles_actuated`
        event. Their is :blue:`value` passed for that event.

        Example::

            mygame.actuate_projectiles(1)

        .. note:: This method only move Projectiles when their actuator state is
            RUNNING. If it is PAUSED or STOPPED, the Projectile is not moved.

        .. Important:: Please have a look at the
            :meth:`pygamelib.board_items.Projectile.hit` method for more information on
            the projectile hit mechanic.
        """
        if self.state == constants.RUNNING:
            if type(level_number) is int:
                if level_number in self._boards.keys():
                    self.screen.trigger_rendering()
                    board = self._boards[level_number]["board"]
                    # For each projectile we need to cover 3 cases:
                    #  1 - projectile range > 0 but the projectile collide with
                    #      something (a moving object that moves into the projectile)
                    #      => it's a hit
                    #  2 - Range still > 0, the projectile itself cannot move forward
                    #      because its path is blocked.  => it is also a hit
                    #  3 - Range falls to 0 without colliding with anything.
                    #      => it is a miss but we still need to callback with an empty
                    #      list or the AOE neighbors.

                    # First, create 3 vectors that are going to be used to project,
                    # check collisions and move the item.
                    dm = base.Vector2D()
                    pp = base.Vector2D()

                    for proj in self._boards[level_number]["projectiles"]:
                        if proj.actuator.state == constants.RUNNING:
                            # Account for movement speed
                            proj.dtmove += elapsed_time
                            if (
                                self.mode == constants.MODE_RT
                                and proj.dtmove < proj.movement_speed
                            ):
                                continue

                            if proj.range > 0:
                                umv = proj.actuator.next_move()
                                if not isinstance(umv, base.Vector2D):
                                    # Build a unit movement vector
                                    umv = base.Vector2D.from_direction(
                                        umv,
                                        1
                                        # proj.actuator.next_move(), 1
                                    )
                                # Build a movement vector

                                dm.row = umv.row * proj.step_vertical
                                dm.column = umv.column * proj.step_horizontal
                                # Then get a projected position (the projected position)
                                # is the position where the projectile should move if
                                # nothing blocks its path. And that's where it will be
                                # unless we detect a collision.
                                pp.row = proj.row + dm.row
                                pp.column = proj.column + dm.column
                                rppr = round(pp.row)
                                rppc = round(pp.column)
                                # v = proj.position_as_vector()
                                if (
                                    pp.row >= 0
                                    and rppr < board.height
                                    and pp.column >= 0
                                    and rppc < board.width
                                ):
                                    item = board.item(rppr, rppc)
                                    if (
                                        item != proj
                                        and not isinstance(
                                            item, board_items.BoardItemVoid
                                        )
                                        and not type(item) in proj.collision_exclusions
                                        and not item.overlappable()
                                        and (proj.collides_with(item, dm))
                                    ):
                                        if proj.is_aoe:
                                            # AoE is easy, just return
                                            # everything in range
                                            proj.hit(
                                                self.neighbors(proj.aoe_radius, proj)
                                            )
                                            return
                                        else:
                                            # Else just the item
                                            proj.hit([item])
                                            return
                                    else:
                                        board.move(proj, dm)
                                        proj.dtmove = 0.0
                                        proj.range -= proj.step
                                else:
                                    proj.range = 0
                            elif proj.range == 0:
                                if proj.is_aoe:
                                    proj.hit(self.neighbors(proj.aoe_radius, proj))
                                else:
                                    proj.hit([board.generate_void_cell()])
                            else:
                                self._boards[level_number]["projectiles"].remove(proj)
                                board.clear_cell(proj.pos[0], proj.pos[1], proj.pos[2])
                                # Since it's all in the same turn we don't need that
                                # code here
                                # if proj in self._boards[level_number][
                                #     "board"
                                # ]._movables and proj != self._boards[level_number][
                                #     "board"
                                # ].item(
                                #     proj.pos[0], proj.pos[1], proj.pos[2]
                                # ):
                                #     self._boards[level_number][
                                #         "board"
                                #     ]._movables.discard(proj)
                        elif proj.actuator.state == constants.STOPPED:
                            self._boards[level_number]["projectiles"].remove(proj)
                            board.clear_cell(proj.pos[0], proj.pos[1], proj.pos[2])
                            # There is a possibility when a lot of projectiles are on
                            # the board that some projectiles are missed in the cleaning
                            # process when their actuator is set to stop. The reason is
                            # that it needs one more turn to be cleared and during that
                            # turn the cell might have been cleaned. In that case we
                            # need to make sure no projectile remains in the movable
                            # stack.
                            if proj in self._boards[level_number][
                                "board"
                            ]._movables and proj != self._boards[level_number][
                                "board"
                            ].item(
                                proj.pos[0], proj.pos[1], proj.pos[2]
                            ):
                                self._boards[level_number]["board"]._movables.discard(
                                    proj
                                )
                    self.notify(
                        self,
                        "pygamelib.engine.Game.actuate_projectiles:"
                        "projectiles_actuated",
                    )
                else:
                    raise base.PglInvalidLevelException(
                        f"Impossible to actuate Projectiles for this level (level "
                        f"number {level_number} is not associated with any board)."
                    )
            else:
                raise base.PglInvalidTypeException(
                    "In actuate_npcs(level_number) the level_number must be an int."
                )

    def animate_items(self, level_number, elapsed_time=0.0):
        """That method goes through all the BoardItems of a given map and call
        Animation.next_frame().

        When all items have been successfully animated, the observers are notified of
        the change with the
        :boldblue:`pygamelib.engine.Game.animate_items:items_animated`
        event. Their is :blue:`value` passed for that event.

        :param level_number: The number of the level to animate items in.
        :type level_number: int
        :param elapsed_time: The amount of time that passed since last call. This
            parameter is not mandatory.
        :type elapsed_time: float

        :raise: :class:`~pygamelib.base.PglInvalidLevelException`
            :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            mygame.animate_items(1)

        """
        if self.state == constants.RUNNING:
            if type(level_number) is int:
                if level_number in self._boards.keys():
                    for item in (
                        self._boards[level_number]["board"].get_immovables()
                        + self._boards[level_number]["board"].get_movables()
                    ):
                        if item.animation is not None:
                            item.animation.dtanimate += elapsed_time
                            if (
                                self.mode == constants.MODE_RT
                                and item.animation.dtanimate
                                < item.animation.display_time
                            ):
                                continue
                            item.animation.dtanimate = 0.0
                            item.animation.next_frame()
                    self.notify(
                        self, "pygamelib.engine.Game.animate_items:items_animated"
                    )
                else:
                    raise base.PglInvalidLevelException(
                        "Impossible to animate items for this level (level number "
                        f"{level_number} is not associated with any board)."
                    )
            else:
                raise base.PglInvalidTypeException(
                    "In animate_items(level_number) the level_number must be an int."
                )

    def display_player_stats(
        self, life_model=graphics.RED_RECT, void_model=graphics.BLACK_RECT
    ):  # pragma: no cover
        """Display the player name and health.

        .. deprecated:: This method is completely deprecated and not even compatible
           with the Screen Buffer system. **It will be removed in 1.4.0**.

        This method print the Player name, a health bar (20 blocks of life_model). When
        life is missing the complement (20-life missing) is printed using void_model.
        It also display the inventory value as "Score".

        :param life_model: The character(s) that should be used to represent the
            *remaining* life.
        :type life_model: str
        :param void_model: The character(s) that should be used to represent the
            *lost* life.
        :type void_model: str

        .. note:: This method might change in the future. Particularly it could take a
            template of what to display.

        """
        if self.player is None or self.player == constants.NO_PLAYER:
            return ""
        info = ""
        info += f" {self.player.name}"
        nb_blocks = int((self.player.hp / self.player.max_hp) * 20)
        info += " [" + life_model * nb_blocks + void_model * (20 - nb_blocks) + "]"
        info += "     Score: " + str(self.player.inventory.value())
        print(info)

    def move_player(self, direction, step=1):
        """
        Easy wrapper for Board.move().

        Example::

            mygame.move_player(constants.RIGHT,1)
        """
        if (
            self.state == constants.RUNNING
            and self.player is not None
            and self.player != constants.NO_PLAYER
        ):
            self._boards[self.current_level]["board"].move(self.player, direction, step)
            if isinstance(self.screen, Screen):
                self.screen.trigger_rendering()

    def display_board(self):
        """Display the current board.

        The behavior of that function is dependant on how you configured this object.
        If you set enable_partial_display to True AND partial_display_viewport is set
        to a correct value, it will call Game.current_board().display_around() with the
        correct parameters.
        The partial display will be centered on the player (Game.player).
        Otherwise it will just call Game.current_board().display().

        If the player is not set or is set to constants.NO_PLAYER partial display won't
        activate automatically.

        Example::

            mygame.enable_partial_display = True
            # Number of rows, number of column (on each side, total viewport
            # will be 20x20 in that case).
            mygame.partial_display_viewport = [10, 10]
            # This will call Game.current_board().display_around()
            mygame.display()
            mygame.enable_partial_display = False
            # This will call Game.current_board().display()
            mygame.display()
        """
        if (
            self.enable_partial_display
            and self.partial_display_viewport is not None
            and type(self.partial_display_viewport) is list
            and self.player is not None
            and self.player != constants.NO_PLAYER
        ):
            # display_around(self, object, p_row, p_col)
            self.current_board().display_around(
                self.player,
                self.partial_display_viewport[0],
                self.partial_display_viewport[1],
            )
        else:
            self.current_board().display()

    def neighbors(self, radius=1, obj=None):
        """Get a list of neighbors (non void item) around an object.

        This method returns a list of objects that are all around an object between the
        position of an object and all the cells at **radius**.

        :param radius: The radius in which non void item should be included
        :type radius: int
        :param object: The central object. The neighbors are calculated for that object.
            If None, the player is the object.
        :type object: pygamelib.board_items.BoardItem
        :return: A list of BoardItem. No BoardItemVoid is included.
        :raises PglInvalidTypeException: If radius is not an int.

        Example::

            for item in game.neighbors(2):
                print(f'{item.name} is around player at coordinates '
                    '({item.pos[0]},{item.pos[1]})')
        """
        if obj is None:
            obj = self.player
        return self.current_board().neighbors(obj, radius)

    def load_board(self, filename, lvl_number=0):
        """Load a saved board

        Load a Board saved on the disk as a JSON file. This method creates a new Board
        object, populate it with all the elements (except a Player) and then return it.

        If the filename argument is not an existing file, the open function is going to
        raise an exception.

        This method, load the board from the JSON file, populate it with all BoardItem
        included, check for sanity, init the board with BoardItemVoid and then associate
        the freshly created board to a lvl_number.
        It then create the NPCs and add them to the board.

        :param filename: The file to load
        :type filename: str
        :param lvl_number: The level number to associate the board to. Default is 0.
        :type lvl_number: int
        :returns: a newly created board (see :class:`pygamelib.engine.Board`)

        Example::

            mynewboard = game.load_board( 'awesome_level.json', 1 )
            game.change_level( 1 )
        """
        data = dict()
        with open(filename, "r") as f:
            data = json.load(f)
        local_board = None
        if "data_version" in data.keys() and data["data_version"] >= 2:
            local_board = Board.load(data)
            self.add_board(lvl_number, local_board)
            for mov in local_board.get_movables():
                if isinstance(mov, board_items.NPC):
                    local_board.remove_item(mov)
                    self.add_npc(lvl_number, mov, mov.row, mov.column, mov.layer)
                    if isinstance(mov.actuator, actuators.PathFinder):
                        mov.actuator.game = self
                        mov.actuator.add_waypoint(mov.row, mov.column)
            # Now load the object library if there's any.
            if "library" in data.keys():
                self.object_library = []
                for e in data["library"]:
                    item = Board.instantiate_item(e)
                    if item is not None:
                        self.object_library.append(item)
        else:
            local_board = Board()
            data_keys = data.keys()
            if "name" in data_keys:
                local_board.name = data["name"]
            if "size" in data_keys:
                local_board.size = data["size"]
                # if len(local_board.size) < 3:
                #     local_board.size.append(2)
            if "player_starting_position" in data_keys:
                local_board.player_starting_position = data["player_starting_position"]
            if "ui_border_top" in data_keys:
                local_board.ui_border_top = data["ui_border_top"]
            if "ui_border_bottom" in data_keys:
                local_board.ui_border_bottom = data["ui_border_bottom"]
            if "ui_border_left" in data_keys:
                local_board.ui_border_left = data["ui_border_left"]
            if "ui_border_right" in data_keys:
                local_board.ui_border_right = data["ui_border_right"]
            if "ui_board_void_cell" in data_keys:
                local_board.ui_board_void_cell = data["ui_board_void_cell"]
            if "ui_board_void_cell_sprixel" in data_keys:
                local_board.ui_board_void_cell_sprixel = data[
                    "ui_board_void_cell_sprixel"
                ]
            # Now let's make it better: if we have a board_void_cell but not a
            # board_void_cell_sprixel we convert it.
            if local_board.ui_board_void_cell is not None and (
                local_board.ui_board_void_cell_sprixel is None
                or not isinstance(local_board.ui_board_void_cell_sprixel, core.Sprixel)
            ):
                local_board.ui_board_void_cell_sprixel = core.Sprixel(
                    local_board.ui_board_void_cell
                )
            # Now we need to recheck for board sanity
            local_board.check_sanity()
            # and re-initialize the board (mainly to attribute a new model to the void
            # cells as it's not dynamic).
            local_board.init_board()
            # Then add board to the game
            self.add_board(lvl_number, local_board)

            # Now load the library if any
            if "library" in data_keys:
                self.object_library = []
                for e in data["library"]:
                    item = Board.instantiate_item(e)
                    if item is not None:
                        self.object_library.append(item)

            # Now let's place the good stuff on the board
            if "map_data" in data_keys:
                for pos_x in data["map_data"].keys():
                    x = int(pos_x)
                    for pos_y in data["map_data"][pos_x].keys():
                        y = int(pos_y)
                        ref = data["map_data"][pos_x][pos_y]
                        obj_keys = ref.keys()
                        if "object" in obj_keys:
                            o = Game._ref2obj(ref)
                            if not isinstance(o, board_items.NPC) and not isinstance(
                                o, board_items.BoardItemVoid
                            ):
                                local_board.place_item(o, x, y)
                            elif isinstance(o, board_items.NPC):
                                self.add_npc(lvl_number, o, x, y)
                                if isinstance(o.actuator, actuators.PathFinder):
                                    o.actuator.game = self
                                    o.actuator.add_waypoint(x, y)

                        else:
                            base.Text.warn(
                                f"while loading the board in {filename}, at coordinates"
                                f' [{pos_x},{pos_y}] there is an entry without "object"'
                                " attribute. NOT LOADED."
                            )
        return local_board

    def save_board(self, lvl_number, filename):
        """Save a board to a JSON file

        This method saves a Board and everything in it but the BoardItemVoid.

        Not check are done on the filename, if anything happen you get the exceptions
        from open().

        :param lvl_number: The level number to get the board from.
        :type lvl_number: int
        :param filename: The path to the file to save the data to.
        :type filename: str

        :raises PglInvalidTypeException: If any parameter is not of the right type
        :raises PglInvalidLevelException: If the level is not associated with a Board.

        Example::

            game.save_board( 1, 'hac-maps/level1.json')

        If Game.object_library is not an empty array, it will be saved also.

        .. warning:: In version 1.3.0 the :class:`~pygamelib.engine.Board` class changed
           a lot and a layer system has been added. Therefor, boards saved from version
           1.3.0+ are *not* compatible with previous version. Previous boards can be
           loaded (:meth:`Game.load_board()` is backward compatible), but when saved
           they will be converted to the new format.
        """
        if type(lvl_number) is not int:
            raise base.PglInvalidTypeException(
                "lvl_number must be an int in Game.save_board()"
            )
        if type(filename) is not str:
            raise base.PglInvalidTypeException(
                "filename must be a str in Game.save_board()"
            )
        if lvl_number not in self._boards:
            raise base.PglInvalidLevelException(
                f"lvl_number {lvl_number}"
                " does not correspond to any level associated with a board in "
                "Game.save_board()"
            )
        # With version 1.3.0+ this method is a lot cleaner...
        data = self._boards[lvl_number]["board"].serialize()
        if len(self.object_library) > 0:
            data["library"] = []
            for o in self.object_library:
                data["library"].append(o.serialize())

        with open(filename, "w") as f:
            json.dump(data, f)

    def start(self):
        """Set the game engine state to RUNNING.

        The game has to be RUNNING for actuate_npcs() and move_player() to do anything.

        Example::

            mygame.start()
        """
        self.state = constants.RUNNING
        self.previous_time = time.perf_counter()

    def pause(self):
        """Set the game engine state to PAUSE.

        Example::

            mygame.pause()
        """
        self.state = constants.PAUSED

    def stop(self):

        """Set the game engine state to STOPPED.

        Example::

            mygame.stop()
        """
        self.state = constants.STOPPED

    @staticmethod
    def _string_to_constant(s):
        if type(s) is int:
            return s
        elif s == "UP":
            return constants.UP
        elif s == "DOWN":
            return constants.DOWN
        elif s == "RIGHT":
            return constants.RIGHT
        elif s == "LEFT":
            return constants.LEFT
        elif s == "DRUP":
            return constants.DRUP
        elif s == "DRDOWN":
            return constants.DRDOWN
        elif s == "DLDOWN":
            return constants.DLDOWN
        elif s == "DLUP":
            return constants.DLUP

    @staticmethod
    def _ref2obj(ref):
        obj_keys = ref.keys()
        local_object = board_items.BoardItemVoid()
        if "Wall" in ref["object"]:
            local_object = board_items.Wall()
        elif "Treasure" in ref["object"]:
            local_object = board_items.Treasure()
            if "value" in obj_keys:
                local_object.value = ref["value"]
            # size is deprecated in favor of inventory_space.
            # This is kept for backward compatibility and silent migration.
            if "size" in obj_keys:
                local_object._inventory_space = ref["size"]  # pragma: no cover
            if "inventory_space" in obj_keys:
                local_object._inventory_space = ref["inventory_space"]
        elif "GenericStructure" in ref["object"]:
            local_object = board_items.GenericStructure()
            if "value" in obj_keys:
                local_object.value = ref["value"]
            # size is deprecated in favor of inventory_space.
            # This is kept for backward compatibility and silent migration.
            if "size" in obj_keys:
                local_object._inventory_space = ref["size"]  # pragma: no cover
            if "inventory_space" in obj_keys:
                local_object._inventory_space = ref["inventory_space"]
            if "pickable" in obj_keys:
                local_object.set_pickable(ref["pickable"])
            if "overlappable" in obj_keys:
                local_object.set_overlappable(ref["overlappable"])
        elif "Door" in ref["object"]:
            local_object = board_items.Door()
            if "value" in obj_keys:
                local_object.value = ref["value"]
            # size is deprecated in favor of inventory_space.
            # This is kept for backward compatibility and silent migration.
            if "size" in obj_keys:
                local_object._inventory_space = ref["size"]  # pragma: no cover
            if "inventory_space" in obj_keys:
                local_object._inventory_space = ref["inventory_space"]
            if "pickable" in obj_keys:
                local_object.set_pickable(ref["pickable"])
            if "overlappable" in obj_keys:
                local_object.set_overlappable(ref["overlappable"])
            if "restorable" in obj_keys:
                local_object.set_restorable(ref["restorable"])
        elif "GenericActionableStructure" in ref["object"]:
            local_object = board_items.GenericActionableStructure()
            if "value" in obj_keys:
                local_object.value = ref["value"]
            # size is deprecated in favor of inventory_space.
            # This is kept for backward compatibility and silent migration.
            if "size" in obj_keys:
                local_object._inventory_space = ref["size"]  # pragma: no cover
            if "inventory_space" in obj_keys:
                local_object._inventory_space = ref["inventory_space"]
            if "pickable" in obj_keys:
                local_object.set_pickable(ref["pickable"])
            if "overlappable" in obj_keys:
                local_object.set_overlappable(ref["overlappable"])
        elif "NPC" in ref["object"]:
            local_object = board_items.NPC()
            if "value" in obj_keys:
                local_object.value = ref["value"]
            # size is deprecated in favor of inventory_space.
            # This is kept for backward compatibility and silent migration.
            if "size" in obj_keys:
                local_object._inventory_space = ref["size"]  # pragma: no cover
            if "inventory_space" in obj_keys:
                local_object._inventory_space = ref["inventory_space"]
            if "hp" in obj_keys:
                local_object.hp = ref["hp"]
            if "max_hp" in obj_keys:
                local_object.max_hp = ref["max_hp"]
            if "step" in obj_keys:
                local_object.step = ref["step"]
            if "remaining_lives" in obj_keys:
                local_object.remaining_lives = ref["remaining_lives"]
            if "attack_power" in obj_keys:
                local_object.attack_power = ref["attack_power"]
            if "actuator" in obj_keys:
                if "RandomActuator" in ref["actuator"]["type"]:
                    local_object.actuator = actuators.RandomActuator(moveset=[])
                    if "moveset" in ref["actuator"].keys():
                        for m in ref["actuator"]["moveset"]:
                            local_object.actuator.moveset.append(
                                Game._string_to_constant(m)
                            )
                elif "PathActuator" in ref["actuator"]["type"]:
                    local_object.actuator = actuators.PathActuator(path=[])
                    if "path" in ref["actuator"].keys():
                        for m in ref["actuator"]["path"]:
                            local_object.actuator.path.append(
                                Game._string_to_constant(m)
                            )
                elif "PatrolActuator" in ref["actuator"]["type"]:
                    local_object.actuator = actuators.PatrolActuator(path=[])
                    if "path" in ref["actuator"].keys():
                        for m in ref["actuator"]["path"]:
                            local_object.actuator.path.append(
                                Game._string_to_constant(m)
                            )
                elif "PathFinder" in ref["actuator"]["type"]:
                    local_object.actuator = actuators.PathFinder(
                        game=Game(), parent=local_object
                    )
                    if "circle_waypoints" in ref["actuator"].keys():
                        local_object.actuator.circle_waypoints = ref["actuator"][
                            "circle_waypoints"
                        ]
                    if "waypoints" in ref["actuator"].keys():
                        for m in ref["actuator"]["waypoints"]:
                            local_object.actuator.add_waypoint(m[0], m[1])
        # Now what remains is what is common to all BoardItem
        if not isinstance(local_object, board_items.BoardItemVoid):
            if "name" in obj_keys:
                local_object.name = ref["name"]
            if "model" in obj_keys:
                local_object.model = ref["model"]
            if "sprixel" in obj_keys:
                local_object.sprixel = core.Sprixel.load(ref["sprixel"])
            if "type" in obj_keys:
                local_object.type = ref["type"]
        return local_object


class Inventory(base.PglBaseObject):
    """A class that represent the Player (or NPC) inventory.

    This class is pretty straightforward: it is an object container, you can add, get
    and remove items and you can get a value from the objects in the inventory.

    On top of that, starting with version 1.3.0, a constraints system has been added.
    It allows to specify a certain amount of constraints that will be applied to the
    items when they are added to the inventory.

    For the moment, constraints are limited to the number of items with a given type/
    name/value (any combination of these three).

    When a constraint is violated, the item is not added to the inventory and a
    notification is broadcasted to the observers of the inventory. A
    PglInventoryException is also raised with name "constraint_violation" and the
    constraint details in description.

    .. note:: You can print() the inventory. This is mostly useful for debug as you want
        to have a better display in your game.

    .. warning:: The :class:`~pygamelib.engine.Game` engine and
        :class:`~pygamelib.board_items.Player` takes care to initiate an inventory for
        the player, you don't need to do it.

    """

    def __init__(self, max_size=10, parent=None):
        """
        The constructor takes two parameters: the maximum size of the inventory. And the
        Inventory owner/parent.

        .. role:: boldblue
        .. role:: blue

        Each :class:`~pygamelib.board_items.BoardItem` that is going to be put in the
        inventory has a size (default is 1), the total addition of all these size cannot
        exceed max_size.

        :param max_size: The maximum size of the inventory. Default value: 10.
        :type max_size: int
        :param parent: The parent object (usually a BoardItem).
        """
        super().__init__()
        self.max_size = max_size
        self.__items = []
        self.parent = parent
        self.__constraints = {}

    def __str__(self):
        s = "=============\n"
        s += "= inventory =\n"
        s += "============="
        types = {}
        for i in self.__items:
            if i.name in types.keys():
                types[i.name]["size"] += i.inventory_space
            else:
                types[i.name] = {
                    "size": i.inventory_space,
                    "model": i.model,
                }
        for k in types.keys():
            s += f"\n{types[k]['model']} : {types[k]['size']}"
        return s

    @property
    def items(self):
        """Return the list of all items in the inventory.

        :return: a list of :class:`~pygamelib.board_items.BoardItem`
        :rtype: list

        Example::

            for item in game.player.inventory.items:
                print(f"This is a mighty item: {item.name}")
        """
        return self.__items

    @property
    def constraints(self):
        """
        .. image:: https://img.shields.io/badge/-Alpha-orange

        Return the list of all constraints in the inventory.

        :return: a list of constraints (dict)
        :rtype: list

        Example::

            for cstr in game.player.inventory.constraints:
                print(f" - {cstr[name]}")
        """
        return self.__constraints.values()

    def add_item(self, item):
        """Add an item to the inventory.

        This method will add an item to the inventory unless:

         * it is not an instance of :class:`~pygamelib.board_items.BoardItem`,
         * you try to add an item that is not pickable,
         * there is no more space left in the inventory (i.e: the cumulated size of the
           inventory + your item.inventory_space is greater than the inventory max_size)
         * An existing constraint is violated.

        :param item: the item you want to add
        :type item: :class:`~pygamelib.board_items.BoardItem`
        :return: The index of the newly added item in the inventory or None if the item
           could not be added.
        :rtype: int|None
        :raise: :class:`~pygamelib.base.PglInventoryException`,
           :class:`~pygamelib.base.PglInvalidTypeException`

        When an item is successfully added, the observers are notified of the change
        with the :boldblue:`pygamelib.engine.Inventory.add_item` event. The item that
        was added is passed as the :blue:`value` of the event.

        When something goes wrong exceptions are raised. The following exceptions can be
        raised (:class:`~pygamelib.base.PglInventoryException`):

        * not_pickable: The item you try to add is not pickable.
        * not_enough_space: There is not enough space left in the inventory.
        * constraint_violation: A constraint is violated.

        A :class:`~pygamelib.base.PglInvalidTypeException` is raised when the item you
        try to add is not a :class:`~pygamelib.board_items.BoardItem`.

        .. role:: boldblue


        Example::

            item = Treasure(model=graphics.Models.MONEY_BAG,size=2,name='Money bag')
            try:
                mygame.player.inventory.add_item(item)
            expect PglInventoryException as e:
                if e.error == 'not_enough_space':
                    print(f"Impossible to add {item.name} to the inventory, there is no"
                    "space left in it!")
                    print(e.message)
                elif e.error == 'not_pickable':
                    print(e.message)

        .. Note:: In versions prior to 1.3.0, the inventory object was changing the
           name of the item if another item with the same name was already in the
           inventory. This is (fortunately) not the case anymore. The Inventory class
           does NOT modify the items that are stored into it anymore.

        """
        if isinstance(item, board_items.BoardItem):
            if item.pickable():
                # if (
                #     item.name is None
                #     or item.name == ""
                #     or item.name in self.__items.keys()
                # ):
                #     item.name = f"{item.name}_{uuid.uuid4().hex}"
                if (
                    hasattr(item, "inventory_space")
                    and self.max_size >= self.size() + item.inventory_space
                ):
                    itm_cstr = ["item_name", "item_type", "item_value"]
                    for cstr in self.__constraints.values():
                        for ics in itm_cstr:
                            if (
                                cstr[ics] is not None
                                and getattr(item, ics.split("_")[1]) == cstr[ics]
                                and len(self.search(cstr[ics])) >= cstr["max_number"]
                            ):
                                raise base.PglInventoryException(
                                    "constraint_violation",
                                    f"{item.name} cannot be added to the inventory, "
                                    f"the constraint {cstr['constraint_name']} is "
                                    "violated!",
                                )
                    self.__items.append(item)
                    self.notify(self, "pygamelib.engine.Inventory.add_item", item)
                    return len(self.__items) - 1
                else:
                    raise base.PglInventoryException(
                        "not_enough_space",
                        "There is not enough space left in the inventory. Max. size: "
                        + str(self.max_size)
                        + ", current inventory size: "
                        + str(self.size())
                        + " and item size: "
                        + str(item.inventory_space),
                    )
            else:
                raise base.PglInventoryException(
                    "not_pickable",
                    f"The item (name='{item.name}') is not pickable. Make sure to only "
                    "add pickable objects to the inventory.",
                )
        else:
            raise base.PglInvalidTypeException(
                "The item is not an instance of BoardItem. The item is of type: "
                + str(type(item))
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
        for i in self.__items:
            if hasattr(i, "inventory_space"):
                val += i.inventory_space
        return val

    def available_space(self) -> int:
        """Return the available space in the inventory.

        That is to say, Inventory.max_size - Inventory.size().

        The returned number is comprised between 0 and Inventory.max_size.

        :return: The size as an int.
        :rtype: int

        Example::

            method()
        """
        return max(0, self.max_size - self.size())

    def empty(self):
        """Empty the inventory.

        .. role:: boldblue

        The observers are notified that the Inventory has been emptied with the
        :boldblue:`pygamelib.engine.Inventory.empty` event. Nothing is passed as the
        value.

        Example::

            if inventory.size() > 0:
                inventory.empty()
        """
        self.__items = []
        self.notify(self, "pygamelib.engine.Inventory.empty", None)

    def value(self):
        """
        Return the cumulated value of the inventory.
        It can be used for scoring for example.

        :return: value of inventory
        :rtype: int

        Example::

            if inventory.value() >= 10:
                print('Victory!')
                break
        """
        val = 0
        for i in self.__items:
            if hasattr(i, "value"):
                val += i.value
        return val

    def items_name(self):
        """Return the list of all items names in the inventory.

        :return: a list of string representing the items names.
        :rtype: list

        """
        return [i.name for i in self.__items]

    def search(self, query):
        """Search for objects in the inventory.

        All objects that matches the query are going to be returned. Search is performed
        on the name and type of the object.

        :param query: the query that items in the inventory have to match to be returned
        :type name: str
        :returns: a list of BoardItems.
        :rtype: list

        Example::

            for item in game.player.inventory.search('mighty'):
                print(f"This is a mighty item: {item.name}")
        """
        if query is None:
            return []
        return [
            item
            for item in self.__items
            if query in item.name
            or query in item.type
            or (type(query) is int and query == item.value)
        ]

    def get_item(self, name):
        """Return the FIRST item corresponding to the name given in argument.

        :param name: the name of the item you want to get.
        :type name: str
        :return: An item.
        :rtype: :class:`~pygamelib.board_items.BoardItem` | None

        Example::

            life_container = mygame.player.inventory.get_item('heart_1')
            if isinstance(life_container,GenericActionableStructure):
                life_container.action(life_container.action_parameters)

        .. note:: Please note that the item object reference is returned but nothing is
            changed in the inventory. The item hasn't been removed.

        .. important:: Starting with version 1.3.0 this method does not raise exceptions
           anymore. Instead it returns None if no item is found. It's behavior also
           changed from returning a precise item to the first one that matches the name.

        """
        for i in self.__items:
            if i.name == name:
                return i

    def get_items(self, name):
        """Return ALL items matching the name given in argument.

        :param name: the name of the item you want to get.
        :type name: str
        :return: An array of items.
        :rtype: list

        Example::

            for life_container in mygame.player.inventory.get_items('heart_1'):
                if isinstance(life_container,GenericActionableStructure):
                    life_container.action(life_container.action_parameters)

        .. note:: Please note that the item object reference is returned but nothing is
            changed in the inventory. The item hasn't been removed.

        .. versionadded:: 1.3.0

        """
        rv = []
        for i in self.__items:
            if i.name == name:
                rv.append(i)
        return rv

    def delete_item(self, name):
        """Delete THE FIRST item matching the name given in argument.

        :param name: the name of the items you want to delete.
        :type name: str

        When an item is successfully removed, the observers are notified of the change
        with the :boldblue:`pygamelib.engine.Inventory.delete_item` event. The item that
        was deleted is passed as the :blue:`value` of the event.

        Example::

            mygame.player.inventory.delete_item('heart_1')

        .. important:: Starting with version 1.3.0 this method does not raise exceptions
           anymore. It's behavior also changed from deleting a precise item to deleting
           the first one that matches the name.

        """
        for i in range(len(self.__items)):
            if self.__items[i].name == name:
                self.notify(
                    self, "pygamelib.engine.Inventory.delete_item", self.__items[i]
                )
                del self.__items[i]
                break

    def delete_items(self, name):
        """Delete ALL items matching the name given in argument.

        :param name: the name of the items you want to delete.
        :type name: str

        The observers are notified of each deletion
        with the :boldblue:`pygamelib.engine.Inventory.delete_item` event. The item
        that was deleted is passed as the :blue:`value` of the event.

        Example::

            mygame.player.inventory.delete_items('heart_1')

        .. versionadded:: 1.3.0

        """
        for i in range(len(self.__items) - 1, -1, -1):
            if self.__items[i].name == name:
                self.notify(
                    self, "pygamelib.engine.Inventory.delete_item", self.__items[i]
                )
                del self.__items[i]

    def add_constraint(
        self,
        constraint_name: str,
        item_type: str = None,
        item_name: str = None,
        item_value: int = None,
        max_number: int = 1,
    ):
        """
        .. image:: https://img.shields.io/badge/-Alpha-orange

        Add a constraint to the inventory.

        :param constraint_name: the name of the constraint.
        :type constraint_name: str
        :param item_type: the type of the item.
        :type item_type: str
        :param item_name: the name of the item.
        :type item_name: str
        :param item_value: the value of the item.
        :type item_name: int
        :param max_number: the maximum number of items that match the item_* parameters
           that can be in the inventory.
        :type max_number: int

        The observers are notified of the addition of the constraint with the
        :boldblue:`pygamelib.engine.Inventory.add_constraint` event. The constraint that
        was added is passed as the :blue:`value` of the event as a dictionnary.

        .. versionadded:: 1.3.0

        """
        if item_name is None and item_type is None and item_value is None:
            raise base.PglInventoryException(
                "invalid_constraint",
                "You must specify at least one of item_name, item_type or item_value",
            )
        if constraint_name is None or constraint_name == "" or max_number is None:
            raise base.PglInventoryException(
                "invalid_constraint",
                "You must specify constraint_name and max_number",
            )
        self.__constraints[constraint_name] = {
            "constraint_name": constraint_name,
            "max_number": max_number,
            "item_type": item_type,
            "item_name": item_name,
            "item_value": item_value,
        }
        self.notify(
            self,
            "pygamelib.engine.Inventory.add_constraint",
            self.__constraints[constraint_name],
        )

    def remove_constraint(self, constraint_name: str):
        """
        .. image:: https://img.shields.io/badge/-Alpha-orange

        Remove a constraint from the inventory.

        :param constraint_name: the name of the constraint.
        :type constraint_name: str

        The observers are notified of the removal of the constraint with the
        :boldblue:`pygamelib.engine.Inventory.remove_constraint` event. The constraint
        that was removed is passed as the :blue:`value` of the event as a dictionnary.

        .. versionadded:: 1.3.0

        """
        if constraint_name in self.__constraints:
            self.notify(
                self,
                "pygamelib.engine.Inventory.remove_constraint",
                self.__constraints[constraint_name],
            )
            del self.__constraints[constraint_name]

    def clear_constraints(self):
        """Remove all constraints from the inventory.


        The observers are notified with the
        :boldblue:`pygamelib.engine.Inventory.clear_constraints` event. The
        :blue:`value` is set to None for this event.

        .. versionadded:: 1.3.0

        """
        self.notify(
            self,
            "pygamelib.engine.Inventory.clear_constraints",
            None,
        )
        self.__constraints = {}

    def serialize(self):
        """Serialize the inventory in a dictionary.

        :returns: The serialized data.
        :rtype: dict

        .. versionadded:: 1.3.0

        Example::

            json.dump(my_inventory.serialize(), out_file)
        """
        ret_data = dict()
        ret_data["max_size"] = self.max_size
        ret_data["items"] = [i.serialize() for i in self.__items]
        return ret_data

    @classmethod
    def load(cls, data: dict):
        """Load serialized data into a new Inventory object.

        :param data: The serialized data
        :type data: dict
        :return: A new Inventory object.
        :rtype: :class:`Inventory`

        .. versionadded:: 1.3.0

        Example::

            my_player.inventory = Inventory.load(data)
        """
        inv = cls(max_size=data["max_size"])
        for di in data["items"]:
            item = Board.instantiate_item(di)
            if di is not None:
                inv.add_item(item)
        return inv


class Screen(base.PglBaseObject):
    """
    The screen object is pretty straightforward: it is an object that allow manipulation
    of the screen.

    .. role:: boldgreen

    .. WARNING:: Starting with version 1.3.0 the terminal parameter has been removed.
       The Screen object now takes advantage of base.Console.instance() to get a
       reference to a blessed.Terminal object.

    Version 1.3.0 introduced a new way of managing the screen. It rely on an internally
    managed display buffer that allows for easier positioning and more regular
    rendering. This comes at a cost though as the performances takes a hit. The screen
    should still be able to be refreshed between 50 and 60+ times per seconds (and still
    around 30 times per second within a virtual machine). These numbers obviously
    depends on the terminal used, the screen size and the content to display.

    This change introduce two ways of displaying things on the screen:

       * The **Improved Screen Management** stack (referred to as :boldgreen:`ISM` later
         in the doc).
       * The **Legacy Direct Display** stack.

    It is safer to consider them mutually incompatible. In reality the **Improved Screen
    Management** will always use the whole display but you can use the methods from the
    **Direct Display** stack to write over the buffer. It is really **NOT** advised.

    We introduced the **Improved Screen Management** stack because the direct display is
    messy and does not allow us to do what we want in term of positioning, UI, etc.

    A typical usage consist of:

       * Placing elements on the screen with :func:`place()`
       * Update the screen with :func:`update()`

    That's it! The screen maintain its own state and knows when to re-render the display
    buffer. You don't need to manually call :func:`render()`. This helps with
    performances as the frame buffer is only rendered when needed.

    Example::

        screen = Screen()
        # The next 3 lines do the same thing: display a message centered on the screen.
        # Screen Buffer style
        screen.place('This is centered', screen.vcenter, screen.hcenter)
        screen.update()
        # Direct Display style
        screen.display_at('This is centered', screen.vcenter, screen.hcenter)
        # The rest of this example uses the Screen Buffer (because placing a Board
        # anywhere on the Screen is not supported by the Direct Display stack).
        # delete the previous message and place a Board at the center of the screen
        screen.delete(screen.vcenter, screen.hcenter)
        screen.place(
            my_awesome_board,
            screen.vcenter - int(my_awesome_board.height/2),
            screen.hcenter - int(my_awesome_board.width/2)
        )
        screen.update()

    **Precisions about the Improved Screen Management stack:**

    You don't need to know how the frame buffer works to use it. However, if you are
    interested in more details, here they are.

    The Improved Screen Management stacks uses a double numpy buffer to represent the
    screen. One buffer is used to place elements as objects (that's the buffer managed
    by :func:`place()` or :func:`delete()`). It is never directly printed to the screen.
    It is here to simplify screen maintenance. This buffer is called the **display
    buffer**. It is practical to use to place, move and delete elements on the screen
    space. But as said before it cannot be directly printed to the screen. It needs to
    be rendered first.

    For example, if you want to use a sprite on a title screen and want to move it
    around (or animate the screen). Normally (i.e with Direct Display) you would display
    the sprite at a specific position and then would either call :func:`clear()` or
    overwrite all the sprite with spaces to erase and replace and/or move it. And that's
    very slow.

    With the **Improved Screen Management** you :func:`place()` the sprite and then just
    :func:`delete()` it. And since it is only one object reference it is a very fast
    operation (we only place or delete one cell of the buffer).

    When :func:`update()` is called, it first look at the state of the buffers and call
    :func:`render()` if needed (i.e: if something has change in the display buffer). The
    buffers are only rendered when needed.

    When :func:`render()` is called it goes through the display buffer and render
    each elements transforming it into a printable sequence that is stored in the
    frame buffer. The rendering is done from the bottom right corner of the screen to
    the top left corner. This allows for cleaning junk characters at no additional cost.

    **TL;DR:** The **display buffer** hold the objects placed on the screen while the
    **frame buffer** hold the rendered representation of the display buffer.

    The Screen object also inherits from the :class:`~pygamelib.base.PglBaseObject` and
    if the object that is :func:`place()`-ed is an instance of
    :class:`~pygamelib.base.PglBaseObject`, the screen will automatically attach itself
    to the object. When notified of a change it will trigger a render cycle before the
    next update.

    In terms of performances, depending on your terminal emulator and CPU you will most
    certainly achieve over 30 FPS. Here are a couple of benchmark results:

     * On an Intel Core i7 @ 4.20 GHz: 50 to 70 FPS.
     * On an AMD Ryzen 9 5950X @ 4.80 GHz: 60 to 100 FPS.

    The new **Improved Screen Management** is faster than the legacy stack in most of
    the cases. The only case when the legacy Direct Display stack might be faster is
    in the case of a game or application with only simple ASCII characters and not a lot
    of things to display.

    Here are some compiled benchmark results of both of systems over 150 runs:

    +------------------------+----------------------------+-----------------------+
    |      Benchmark         | Improved Screen Management | Legacy Direct Display |
    +========================+============================+=======================+
    | Sprite (place, render  |    10.0 msec. or 71 FPS    | 380.0 msec. or 3 FPS  |
    | and update screen),    |                            |                       |
    | Sprite size: 155x29    |                            |                       |
    +------------------------+----------------------------+-----------------------+
    | Sprite 200 updates     |   620.0 msec. or 76 FPS    | 9830.0 msec. or 20 FPS|
    +------------------------+----------------------------+-----------------------+
    | Phase 1 - 500 frames.  |   11.02 msec. per frame    | 12.65 msec. per frame |
    | Single board avg load  |   or 91 FPS                | or 79 FPS             |
    +------------------------+----------------------------+-----------------------+
    | Phase 2 - 500 frames.  |   18.18 msec. per frame    | 28.34 msec. per frame |
    | Dual board high load   |   or 55 FPS                | or 35 FPS             |
    +------------------------+----------------------------+-----------------------+
    | Overall - 1000 frames. |   14.60 msec. per frame    | 20.49 msec. per frame |
    |                        |   or 68 FPS                | or 49 FPS             |
    +------------------------+----------------------------+-----------------------+

    You can use the 2 benchmark scripts to compare on your system:

     * benchmark-screen-buffer.py
     * benchmark-screen-direct-display.py

    The frame buffer system has been tested on the following terminals:

    * xterm-256color
    * Konsole
    * Kitty
    * Alacritty
    * GNOME Terminal

    Performances are consistants across the different terminals. The only exception is
    the GNOME Terminal, which is slower than the others (about 20~30 % slower).


    """

    def __init__(self, width: int = None, height: int = None):
        """The constructor takes the following (optional) parameters.

        :param width: The width of the screen.
        :type width: int
        :param height: The height of the screen.
        :type height: int

        Setting any of these parameters fixes the screen size regardless of the actual
        console/terminal resolution. Leaving any of these parameters unset will let the
        constructor use the actual console/terminal resolution instead.

        Please have a look at the examples for more on this topic.

        Example::

            # Let's assume a terminal resolution of 170(width)x75(height).
            screen = Screen()
            # Next line display: "Screen width=170 height=75"
            print(f"Screen width={screen.width} height={screen.height}")
            screen = Screen(50)
            # Next line display: "Screen width=50 height=75"
            print(f"Screen width={screen.width} height={screen.height}")
            screen = Screen(height=50)
            # Next line display: "Screen width=170 height=50"
            print(f"Screen width={screen.width} height={screen.height}")
            screen = Screen(50, 50)
            # Next line display: "Screen width=50 height=50"
            print(f"Screen width={screen.width} height={screen.height}")
        """
        super().__init__()
        # get a terminal instance
        self.terminal = base.Console.instance()
        # Create the 2 buffers.
        self.__width = width
        self.__height = height
        if self.__width is None:
            self.__width = self.terminal.width
        if self.__height is None:
            self.__height = self.terminal.height
        self._display_buffer = np.array(
            [
                [core.Sprixel(" ") for i in range(0, self.__width, 1)]
                for j in range(0, self.__height, 1)
            ]
        )
        self._frame_buffer = np.array(
            [
                [core.Sprixel(" ") for i in range(0, self.__width, 1)]
                for j in range(0, self.__height, 1)
            ]
        )
        self._is_dirty = False
        self._run_threaded_loop = False
        self._rendering_thread = None
        self.__scene_graph = []

    def clear(self):
        """
        This methods clear the screen.
        """
        sys.stdout.write(self.terminal.clear)
        sys.stdout.flush()

    def clear_buffers(self):
        """This methods clear the Screen's buffers (both display and frame buffer).

        Make sure that you really want to clear the buffers before doing so, because
        this is a slow operation.

        Once the buffer is cleared nothing is left in it, you have to reposition (place)
        everything.

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        self._display_buffer = np.array(
            [
                [core.Sprixel(" ") for i in range(0, self.__width, 1)]
                for j in range(0, self.__height, 1)
            ]
        )
        self._frame_buffer = np.array(
            [
                [core.Sprixel(" ") for i in range(0, self.__width, 1)]
                for j in range(0, self.__height, 1)
            ]
        )
        self._is_dirty = False

    def clear_frame_buffer(self):
        """
        This methods clear the frame buffer (but not the display buffer). This means
        that the next time :func:`update()` is called, rendering will be triggered.

        Make sure that you really want to clear the buffers before doing so, because
        this is a slow operation. It might however be faster than manually update screen
        cells.

        Once the buffer is cleared nothing is left in it, it sets the Screen for a
        rendering update.

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.
        """
        self._frame_buffer = np.array(
            [
                [core.Sprixel(" ") for i in range(0, self.__width, 1)]
                for j in range(0, self.__height, 1)
            ]
        )
        self._is_dirty = True

    @property
    def width(self):
        """
        This property returns the width of the terminal window in number of characters.
        """
        return self.__width

    @property
    def height(self):
        """
        This property returns the height of the terminal window in number of characters.
        """
        return self.__height

    @property
    def need_rendering(self):
        """
        This property return True if the display buffer has been updated since the last
        rendering cycle and the screen needs to re-render the frame buffer.

        It returns False otherwise.

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        return self._is_dirty

    @property
    def buffer(self):
        """
        The buffer property return a numpy.array as a writable frame buffer.

        The buffer is a 2D plane (like a screen) and anything can render in it. However,
        it is recommended to place objects through Screen.place() and update the screen
        with Screen.update() (update calls render() if needed and do the actual
        display).

        .. WARNING:: Everything that is stored in the buffer *must* be printable. Each
           cell of the frame buffer represent a single character on screen, so you need
           to take care of that when you write into that buffer or you will corrupt the
           display. If :attr:`need_rendering` returns True, you need to manually call
           :func:`render()` before writing anything into the frame buffer. Or else it
           will be squashed in the next rendering cycle.

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        return self._frame_buffer

    @property
    def vcenter(self):
        """Return the vertical center of the screen as an int.

        Example::

            screen.place('vertically centered', screen.vcenter, 0)
        """
        return int(self.height / 2)

    @property
    def hcenter(self):
        """Return the horizontal center of the screen as an int.

        Example::

            screen.place('horizontally centered', 0, screen.hcenter)
        """
        return int(self.width / 2)

    def update(self):
        """
        Update the screen. Update means write the frame buffer on screen.

        Example::

            mygame = Game()
            sc = core.SpriteCollection.load_json_file('title_screens.spr')
            mygame.screen.place(sc['welcome_screen'], 0, 0)
            mygame.screen.update()

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        if self._is_dirty:
            self.render()
        print(self.terminal.home, end="", flush=False)
        screen_buffer = self._frame_buffer
        for row in range(0, screen_buffer.shape[0] - 1):
            print("".join(map(str, screen_buffer[row])), flush=False)
        print(
            "".join(map(str, screen_buffer[screen_buffer.shape[0] - 1])),
            end="",
            flush=False,
        )
        print(self.terminal.clear_eos, end="", flush=True)

    def render(self):
        """Render the display buffer into the frame buffer.

        Example::

            screen.render()
            screen.update()

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        if self._is_dirty is False:
            return
        # All these variables are here for performances.
        # https://wiki.python.org/moin/PythonSpeed/PerformanceTips (old but I do get
        # better performances with that trick)
        row = self._display_buffer.shape[0] - 1
        screen_buffer = self._frame_buffer
        display_buffer = self._display_buffer
        s_width = display_buffer.shape[1]
        s_height = display_buffer.shape[0]
        later_passes = []
        while row >= 0:
            col = display_buffer.shape[1] - 1
            while col >= 0:
                i = display_buffer[row][col]
                # Test if the cell should be rendered on a later pass.
                if (
                    hasattr(i, "__rendering_pass")
                    and getattr(i, "__rendering_pass") > 1
                    and hasattr(i, "render_to_buffer")
                ):
                    if getattr(i, "__rendering_pass") < len(later_passes):
                        later_passes[getattr(i, "__rendering_pass")].append(
                            {"item": i, "row": row, "column": col}
                        )
                    else:
                        later_passes.extend(
                            []
                            for _ in range(
                                getattr(i, "__rendering_pass") - len(later_passes)
                            )
                        )
                        later_passes[getattr(i, "__rendering_pass") - 1].append(
                            {"item": i, "row": row, "column": col}
                        )
                    col -= 1
                    continue
                i.render_to_buffer(
                    screen_buffer,
                    row,
                    col,
                    s_height,
                    s_width,
                )
                # # If not, we render the cell now.
                # if hasattr(i, "render_to_buffer"):
                #     # If the item is capable of rendering itself in the buffer, we let
                #     # it do so.
                #     i.render_to_buffer(
                #         screen_buffer,
                #         row,
                #         col,
                #         s_height,
                #         s_width,
                #     )
                # elif hasattr(i, "__repr__"):
                #     # Else we use the __repr__ method to render the cell.
                #     # It is for the sprixels.
                #     screen_buffer[row][col] = i.__repr__()
                col -= 1
            row -= 1
        # Now we render the later passes.
        for items in later_passes:
            for i in items:
                # Since we already cheched if the item is capable of rendering itself,
                # we can safely assume it has a render_to_buffer method.
                i["item"].render_to_buffer(
                    screen_buffer, i["row"], i["column"], s_height, s_width
                )

        self._is_dirty = False

    def force_render(self):
        """

        Force the immediate rendering of the display buffer.

        If you just want to mark the frame buffer for rendering before the next update
        use :func:`trigger_rendering` instead.

        Example::

            screen.force_render()

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        self._is_dirty = True
        self.render()

    def force_update(self):
        """

        Same as :func:`force_render()` but also force the immediate screen update.

        Example::

            screen.force_update()

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        self._is_dirty = True
        self.update()

    def trigger_rendering(self):
        """
        Trigger the frame buffer for rendering at the next update.

        Example::

            screen.trigger_rendering()

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Direct Display** stack.

        """
        self._is_dirty = True

    def place(self, element=None, row=None, column=None, rendering_pass=1):
        """Place an element on the screen.

        This method places an element in the screen display buffer. The element is then
        going to be rendered in the frame buffer before being printed on screen.

        The following elements can be placed on screen:

         * All BoardItem derivatives.
         * All BoardComplexItem derivatives.
         * :class:`Board` object.
         * :class:`~pygamelib.base.Text` objects.
         * :class:`~pygamelib.gfx.core.Sprite` objects.
         * :class:`~pygamelib.gfx.core.Sprixel` objects.
         * Regular Python str.
         * Any object that expose a render_to_buffer() method.

        Here is the required signature for render_to_buffer:

        **render_to_buffer(self, buffer, row, column, buffer_height, buffer_width)**

        The buffer parameter will always be a numpy array, row and column are the
        position to render to. Finally buffer_height and buffer_width are the dimension
        of the buffer.

        The buffer is rendered in 2 passes. By default all elements are rendered in pass
        1. But if for some reason something needs to be drawn over other elements (like
        if a dialog/popup is needed for example), the element can be set to be rendered
        only during the second pass.

        :param element: The element to place.
        :type element: various
        :param row: The row to render to.
        :type row: int
        :param column: The column to render to.
        :type column: int
        :param rendering_pass: When to render the element. You can have any number of
           rendering passes but you have to be careful of performances. Higher passses
           render on top of lower passes. You can see the render passes as plane to
           write on. The default pass is 1.
        :type rendering_pass: int

        .. Warning:: to be rendered on the second+ pass an element *needs* to implement
           render_to_buffer(...). This excludes all standard types (but not
           :class:`~pygamelib.base.Text`). Regular Python strings and object that can be
           print() can still be used in the first pass.

        Example::

            screen.place(my_sprite, 0, 0)

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        if element is None or row is None or column is None:
            raise base.PglInvalidTypeException(
                "Screen.place(item, row, column) none of the parameters can be None."
            )
        if pgl_isinstance(element, "pygamelib.gfx.ui.Dialog") and rendering_pass < 2:
            rendering_pass = 2
        if row >= self.height:
            raise base.PglException(
                "out_of_screen_boundaries",
                f"Screen.place(item, row, column) : row={row} is out of screen height "
                f"(i.e {self.height})",
            )
        if column >= self.width:
            raise base.PglException(
                "out_of_screen_boundaries",
                f"Screen.place(item, row, column) : column={column} is out of screen "
                f"width (i.e {self.width})",
            )
        if type(element) is str:
            # If it's a string we convert it to a Text object.
            element = base.Text(element)

        if isinstance(element, base.PglBaseObject):
            element.attach(self)
            element.store_screen_position(row, column)

        if isinstance(element, core.Sprixel) or hasattr(element, "render_to_buffer"):
            try:
                setattr(element, "__rendering_pass", rendering_pass)
            except AttributeError:
                pass
            self._display_buffer[row][column] = element
            # if isinstance(element, base.PglBaseObject):
            #     # Game.instance().session_log(f"Attaching to {element}")
            #     element.attach(self)
            #     element.store_screen_position(row, column)
            self._is_dirty = True
            return
        else:
            raise base.PglInvalidTypeException(
                f"Screen.place(item, row, column) : item type {type(element)} is not"
                " supported."
            )

    def delete(self, row=None, column=None):
        """Delete a element on screen.

        It is important to note that if you placed an element that occupies more than 1
        cell, you only have to erase that specific position not the entire area.

        :param row: The row coordinate of the element to delete.
        :type row: int
        :param column: The column coordinate of the element to delete.
        :type column: int

        Example::

            board = Board(size=[20,20])
            screen.place(board, 2, 2)
            # With this we have placed a board at screen coordinates 2,2 and the board
            # will display on screen coordinates from 2,2 to 22,22.
            # However, to delete the board we don't need to clean all these cells.
            # Just the one where we placed the board:
            screen.delete(2, 2)

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        if row is not None and column is not None:
            if isinstance(self._display_buffer[row][column], base.PglBaseObject):
                self._display_buffer[row][column].detach(self)
            self._display_buffer[row][column] = core.Sprixel(" ")
            self._is_dirty = True

    def get(self, row: int, column: int):
        """
        Get an element from the display buffer at the specified screen coordinates.

        The element is returned from the display buffer (pre-rendering).

        :param row: The row of the element to get.
        :type row: int
        :param column: The column of the element to get.
        :type column: int

        Example::

            board = Board(size=[20,20])
            screen.place(board, 2, 2)
            my_board = screen.get(2,2)

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-ISM-green

        .. NOTE:: This method is part of the **Improved Screen Management** rendering
           stack and is incompatible with the methods identified as being part of the
           **Legacy Direct Display** stack.

        """
        if type(row) is int and type(column) is int:
            return self._display_buffer[row][column]

    def display_line(self, *text, end="\n", file=sys.stdout, flush=False):
        """

        A wrapper to Python's print() builtin function except it will always add an
        ANSI sequence to clear the end of the line. Making it more suitable to use in
        a user_update callback.

        The reason is that with line with variating length, if you use run() but not
        clear(), some characters will remain on screen because run(), for performances
        concerns does not clear the entire screen. It just bring the cursor back to the
        top left corner of the screen.
        So if you want to benefit from the increase performances you should use
        display_line().

        :param \*text: objects that can serialize to str. The ANSI sequence to clear the
           end of the line is *always* appended to the the text.
        :type \*text: str|objects
        :param end: end sub string added to the printed text. Usually a carriage return.
        :type end: str
        :param file:
        :type file: stream
        :param flush:
        :type flush: bool

        Example::

            screen.display_line(f'This line will display correctly: {elapsed_time}')
            # That line will have trailing characters that are not cleared after redraw
            # if you don't use clear().
            print(f'That one won't: {elapsed_time}')

        .. versionadded:: 1.2.0

        .. image:: https://img.shields.io/badge/rendering%20stack-Direct%20Display-blue

        .. NOTE:: This method is part of the **Legacy Direct Display** rendering stack
           and is incompatible with the methods identified as being part of the
           **Improved Screen Management** stack.

        """
        # Funny how the documentation is waaayyy bigger than the code ;)
        print(
            *text,
            self.terminal.clear_eol,
            end=end,
            file=file,
            flush=flush,
        )

    def display_at(
        self,
        text,
        row=0,
        column=0,
        clear_eol=False,
        end="\n",
        file=sys.stdout,
        flush=False,
    ):
        """
        Displays text at a given position. If clear_eol is True, also clear the end of
        line.
        Additionally you can specify all the parameters of a regular print() if you
        need to.

        :param text: The text to display. Please note that in that case text is a single
            string.
        :type text: str
        :param row: The row position in the terminal window.
        :type row: int
        :param column: The column position in the terminal window.
        :type column: int
        :param clear_eol: If True this clears the end of the line (everything after the
            last character displayed by that method).
        :type clear_eol: bool
        :param end: end sub string added to the printed text. Usually a carriage return.
        :type end: str
        :param file:
        :type file: stream
        :param flush:
        :type flush: bool

        .. IMPORTANT:: The cursor is only moved for printing the text. It is returned to
            its previous position after.

        .. Note:: The position respect the row/column convention accross the library. It
            is reversed compared to the blessed module.

        Example::

            screen.display_at('This is centered',
                              int(screen.height/2),
                              int(screen.width/2),
                              clear_eol=True,
                              end=''
                            )

        .. image:: https://img.shields.io/badge/rendering%20stack-Direct%20Display-blue

        .. NOTE:: This method is part of the **Legacy Direct Display** rendering stack
           and is incompatible with the methods identified as being part of the
           **Improved Screen Management** stack.

        """
        eol = ""
        if clear_eol:
            eol = self.terminal.clear_eol
        with self.terminal.location(column, row):
            print(text, eol, end=end, file=file, flush=flush)

    def display_sprite_at(
        self,
        sprite,
        row=0,
        column=0,
        filler=core.Sprixel(" "),
        file=sys.stdout,
        flush=False,
    ):
        """
        Displays a sprite at a given position.
        If a :class:`~pygamelib.gfx.core.Sprixel` is empty, then it's going to be
        replaced by filler.

        :param sprite: The sprite object to display.
        :type sprite: :class:`~pygamelib.gfx.core.Sprite`
        :param row: The row position in the terminal window.
        :type row: int
        :param column: The column position in the terminal window.
        :type column: int
        :param filler: A sprixel object to replace all empty sprixels in sprite.
        :type filler: :class:`~pygamelib.gfx.core.Sprixel`
        :param file:
        :type file: stream
        :param flush: print() parameter to flush the stream after printing
        :type flush: bool

        Example::

            screen.display_sprite_at(panda_sprite,
                                     int(screen.height/2),
                                     int(screen.width/2)
                                     )

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-Direct%20Display-blue

        .. NOTE:: This method is part of the **Legacy Direct Display** rendering stack
           and is incompatible with the methods identified as being part of the
           **Improved Screen Management** stack.

        """
        null_sprixel = core.Sprixel()
        for r in range(0, sprite.size[1]):
            for c in range(0, sprite.size[0]):
                if sprite._sprixels[r][c] == null_sprixel:
                    self.display_at(filler, row + r, column + c, file=file, flush=flush)
                else:
                    self.display_at(
                        sprite._sprixels[r][c],
                        row + r,
                        column + c,
                        file=file,
                        flush=flush,
                    )

    def display_sprite(
        self, sprite, filler=core.Sprixel(" "), file=sys.stdout, flush=False
    ):
        """
        Displays a sprite at the current cursor position.
        If a :class:`~pygamelib.gfx.core.Sprixel` is empty, then it's going to be
        replaced by filler.

        :param sprite: The sprite object to display.
        :type sprite: :class:`~pygamelib.gfx.core.Sprite`
        :param filler: A sprixel object to replace all empty sprixels in sprite.
        :type filler: :class:`~pygamelib.gfx.core.Sprixel`
        :param file:
        :type file: stream
        :param flush: print() parameter to flush the stream after printing
        :type flush:

        Examples::

            screen.display_sprite(panda_sprite)

        .. versionadded:: 1.3.0

        .. image:: https://img.shields.io/badge/rendering%20stack-Direct%20Display-blue

        .. NOTE:: This method is part of the **Legacy Direct Display** rendering stack
           and is incompatible with the methods identified as being part of the
           **Improved Screen Management** stack.

        """
        null_sprixel = core.Sprixel()
        for r in range(0, sprite.size[1]):
            for c in range(0, sprite.size[0]):
                if sprite._sprixels[r][c] == null_sprixel:
                    print(filler, end="")
                else:
                    print(
                        sprite._sprixels[r][c],
                        end="",
                        file=file,
                        flush=flush,
                    )
            print()

    def handle_notification(self, subject, attribute=None, value=None):
        # We don't really care about the reason for the notification. We just want to
        # know that something changed.
        """
        When a Screen object is notified, it set the display buffer to be rendered
        before the next update.
        """
        self._is_dirty = True
