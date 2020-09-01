"""
The Game.py module has only one class: Game. It is what could be called the game engine.
It holds a lot of methods that helps taking care of some complex mechanics behind the
curtain.

This module contains the Inventory class.

This module regroup all the specific exceptions of the library.
The idea behind most exceptions is to provide more context and info that the standard
exceptions.

This module contains the Board class.
It is the base class for all levels.

.. autosummary::
   :toctree: .

   Math
   PglException
   PglInvalidLevelException
   PglInvalidTypeException
   PglObjectIsNotMovableException
   PglOutOfBoardBoundException
   Vector2D
   Text
"""
from pygamelib import constants
import math
from colorama import Fore, Back, Style, init

# Initialize terminal colors for colorama.
init()


class Text:
    """
    An object to manipulate and display text in multiple contexts.

    .. versionadded:: 1.2.0

    The Text class is a collection of text formating and display static methods.

    You can either instantiate an object or use the static methods.

    The Text object allow for easy text manipulation through its collection of
    independent attributes. They help to set the text, its style and the foreground and
    background colors.

    The Text object can generate a :class:`~pygamelib.gfx.core.Sprite` to represent
    itself. This is particularly useful to the place text on the game
    :class:`~pygamelib.engine.Board`.

    :param text: The text to manipulate
    :type text: str
    :param fg_color: The foreground color for the text.
    :type fg_color: str
    :param bg_color: The background color for the text.
    :type bg_color: str
    :param style: The style for the text.
    :type style: str
    """

    def __init__(self, text="", fg_color="", bg_color="", style=""):
        self.text = text
        """The text attribute. It needs to be a str."""
        self.fg_color = fg_color
        """The fg_color attribute sets the foreground color. It needs to be a str."""
        self.bg_color = bg_color
        """The bg_color attribute sets the background color. It needs to be a str."""
        self.style = style
        """The style attribute sets the style of the text. It needs to be a str."""
        self.parent = None
        """This object's parent. It needs to be a
        :class:`~pygamelib.board_items.BoardItem`."""
        self._sprite = None
        self._item = None

    def __repr__(self):
        return "".join([self.bg_color, self.fg_color, self.style, self.text, "\x1b[0m"])

    def __str__(self):  # pragma: no cover
        return self.__repr__()

    @staticmethod
    def warn(message):
        """Print a warning message.

        The warning is a regular message prefixed by WARNING in black on a yellow
        background.

        :param message: The message to print.
        :type message: str

        Example::

            base.Text.warn("This is a warning.")
        """
        print(Fore.BLACK + Back.YELLOW + "WARNING" + Style.RESET_ALL + ": " + message)

    @staticmethod
    def fatal(message):
        """Print a fatal message.

        The fatal message is a regular message prefixed by FATAL in white on a red
        background.

        :param message: The message to print.
        :type message: str

        Example::

            base.Text.fatal("|x_x|")
        """
        print(
            Fore.WHITE
            + Back.RED
            + Style.BRIGHT
            + "FATAL"
            + Style.RESET_ALL
            + ": "
            + message
        )

    @staticmethod
    def info(message):
        """Print an informative message.

        The info is a regular message prefixed by INFO in white on a blue background.

        :param message: The message to print.
        :type message: str

        Example::

            base.Text.info("This is a very informative message.")
        """
        print(Fore.WHITE + Back.BLUE + "INFO" + Style.RESET_ALL + ": " + message)

    @staticmethod
    def debug(message):
        """Print a debug message.

        The debug message is a regular message prefixed by INFO in blue on a green
        background.

        :param message: The message to print.
        :type message: str

        Example::

            base.Text.debug("This is probably going to success, eventually...")
        """
        print(
            Fore.BLUE
            + Back.GREEN
            + Style.BRIGHT
            + "DEBUG"
            + Style.RESET_ALL
            + ": "
            + message
        )

    @staticmethod
    def print_white_on_red(message):
        """Print a white message over a red background.

        :param message: The message to print.
        :type message: str

        Example::

            base.Text.print_white_on_red("This is bright!")
        """
        print(Fore.WHITE + Back.RED + message + Style.RESET_ALL)

    # Colored bright functions
    @staticmethod
    def green_bright(message):
        """
        Return a string formatted to be bright green

        :param message: The message to format.
        :type message: str
        :return: The formatted string
        :rtype: str

        Example::

            print( Text.green_bright("This is a formatted message") )

        """
        return Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def blue_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLUE + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def red_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.RED + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def yellow_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.YELLOW + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def magenta_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.MAGENTA + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def cyan_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.CYAN + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def white_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.WHITE + Style.BRIGHT + message + Style.RESET_ALL

    @staticmethod
    def black_bright(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLACK + Style.BRIGHT + message + Style.RESET_ALL

    # Colored normal functions
    @staticmethod
    def green(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.GREEN + message + Style.RESET_ALL

    @staticmethod
    def blue(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLUE + message + Style.RESET_ALL

    @staticmethod
    def red(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.RED + message + Style.RESET_ALL

    @staticmethod
    def yellow(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.YELLOW + message + Style.RESET_ALL

    @staticmethod
    def magenta(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.MAGENTA + message + Style.RESET_ALL

    @staticmethod
    def cyan(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.CYAN + message + Style.RESET_ALL

    @staticmethod
    def white(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.WHITE + message + Style.RESET_ALL

    @staticmethod
    def black(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLACK + message + Style.RESET_ALL

    # Colored dim function
    @staticmethod
    def green_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.GREEN + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def blue_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLUE + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def red_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.RED + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def yellow_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.YELLOW + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def magenta_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.MAGENTA + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def cyan_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.CYAN + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def white_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.WHITE + Style.DIM + message + Style.RESET_ALL

    @staticmethod
    def black_dim(message):
        """
        This method works exactly the way green_bright() work with different color.
        """
        return Fore.BLACK + Style.DIM + message + Style.RESET_ALL


class PglInvalidTypeException(Exception):
    """
    Exception raised for invalid types.
    """

    def __init__(self, message):
        self.message = message


class HacInvalidTypeException(PglInvalidTypeException):
    """A simple forward to PglInvalidTypeException
    """


class PglException(Exception):
    """
    Exception raised for non specific errors in the pygamelib.
    """

    def __init__(self, error, message):
        self.error = error
        self.message = message


class HacException(PglException):
    """A simple forward to PglException
    """


class PglOutOfBoardBoundException(Exception):
    """
    Exception for out of the board's boundaries operations.
    """

    def __init__(self, message):
        self.message = message


class PglOutOfItemBoundException(Exception):
    """
    Exception for out of the item's boundaries operations.
    """

    def __init__(self, message):
        self.message = message


class HacOutOfBoardBoundException(PglOutOfBoardBoundException):
    """Simple forward to PglOutOfBoardBoundException
    """


class PglObjectIsNotMovableException(Exception):
    """
    Exception raised if the object that is being moved is not a subclass of Movable.
    """

    def __init__(self, message):
        self.message = message


class HacObjectIsNotMovableException(PglObjectIsNotMovableException):
    """Simple forward to PglObjectIsNotMovableException
    """


class PglInvalidLevelException(Exception):
    """
    Exception raised if a level is not associated to a board in Game().
    """

    def __init__(self, message):
        self.message = message


class HacInvalidLevelException(PglInvalidLevelException):
    """Forward to PglInvalidLevelException
    """


class PglInventoryException(Exception):
    """
    Exception raised for issue related to the inventory.
    The error is an explicit string, and the message explains the error.
    """

    def __init__(self, error, message):
        self.error = error
        self.message = message


class HacInventoryException(PglInventoryException):
    """Forward to PglInventoryException.
    """


class Vector2D:
    """A 2D vector class.

    .. versionadded:: 1.2.0

    Contrary to the rest of the library Vector2D uses floating point numbers for its
    coordinates/direction/orientation. However since the rest of the library uses
    integers, the numbers are rounded to 2 decimals.
    You can alter that behavior by increasing or decreasing (if you want integer for
    example).

    Vector2D use the row/column internal naming convention as it is easier to visualize
    For learning developers. If it is a concept that you already understand and are
    more familiar with the x/y coordinate system you can also use x and y.

     - x is equivalent to column
     - y is equivalent to row

    Everything else is the same.

    Vectors can be printed and supports basic operations:

     - addition
     - substraction
     - multiplication

    Let's elaborate a bit more on the multiplication. The product behaves in 2 different
    ways:

    If you multiply a vector with a scalar (int or float), the return value is a
    Vector2D with each vector component multiplied by said scalar.

    If you multiply a Vector2D with another Vector2D you ask for the the cross
    product of vectors. This is an undefined mathematical operation in 2D as the
    cross product is supposed to be perpendicular to the 2 other vectors (along the
    z axis in our case). Since we don't have depth (z) in 2D, this will return the
    magnitude of the signed cross product of the 2 vectors.

    Example of products::

        v1 = base.Vector2D(1,2)
        v2 = base.Vector2D(3,4)
        # This returns -2
        mag = v1 * v2
        # This returns a Vector2D with values (-1, -2)
        inv = v1 * -1
        # This return a Vector2D with values (2.85, 3.8) or 95% of v2
        dim = v2 * 0.95

    :param row: The row/y parameter.
    :type row: int
    :param column: The column/x parameter.
    :type column: int

    Example::

        gravity = Vector2D(9.81, 0)
        # Remember that minus on row is up.
        speed = Vector2D(-0.123, 0.456)
        # In that case you might want to increase the rounding precision
        speed.rounding_precision = 3
    """

    def __init__(self, row=0.0, column=0.0):
        # column is x and row is y
        self.__row = row
        self.__column = column
        self.rounding_precision = 2
        """The rounding_precision attributes is used when vectors values are calculated
        and the result rounded for convenience. It can be changed anytime to increase or
        decrease the precision anytime."""

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.__row}, {self.__column})"

    def __str__(self):  # pragma: no cover
        return self.__repr__()

    def __add__(self, other):
        row = round(self.__row + other.row, self.rounding_precision)
        column = round(self.__column + other.column, self.rounding_precision)
        return Vector2D(row, column)

    def __sub__(self, other):
        row = round(self.__row - other.row, self.rounding_precision)
        column = round(self.__column - other.column, self.rounding_precision)
        return Vector2D(row, column)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2D(
                round(self.__row * other, self.rounding_precision),
                round(self.__column * other, self.rounding_precision),
            )
        if isinstance(other, Vector2D):
            return round(
                self.row * other.column - self.column * other.row,
                self.rounding_precision,
            )

    def __eq__(self, other):
        if other.row == self.__row and other.column == self.__column:
            return True
        return False

    @property
    def row(self):
        """
        The row component of the vector.
        """
        return self.__row

    @row.setter
    def row(self, value):
        if isinstance(value, (int, float)):
            self.__row = round(value, self.rounding_precision)
        else:
            raise PglInvalidTypeException("Vector2D.row needs to be an int or a float.")

    @property
    def y(self):
        """
        y is an alias for row.
        """
        return self.row

    @y.setter
    def y(self, value):
        self.row = value

    @property
    def column(self):
        """
        The column component of the vector.
        """
        return self.__column

    @column.setter
    def column(self, value):
        if isinstance(value, (int, float)):
            self.__column = round(value, self.rounding_precision)
        else:
            raise PglInvalidTypeException(
                "Vector2D.column needs to be an int or a float."
            )

    @property
    def x(self):
        """
        x is an alias for column.
        """
        return self.column

    @x.setter
    def x(self, value):
        self.column = value

    def length(self):
        """
        Returns the length of a vector.

        :rtype: float

        Example::

            if speed.length() == 0.0:
                print('We are not moving... at all...')
        """
        return round(
            math.sqrt(self.row ** 2 + self.column ** 2), self.rounding_precision
        )

    def unit(self):
        """Returns a normalized unit vector.

        :returns: A unit vector
        :rtype: :class:`~pygamelib.base.Vector2D`

        Example::

            gravity = Vector2D(9.81, 0)
            next_position = item.position_as_vector() + gravity.unit()
        """
        if self.length() == 0.0:
            return Vector2D()
        return Vector2D(
            round(self.__row / self.length(), self.rounding_precision),
            round(self.__column / self.length(), self.rounding_precision),
        )

    @classmethod
    def from_direction(cls, direction, step):
        """Build and return a Vector2D from a direction.

        Directions are from the constants module.

        :param direction: A direction from the constants module.
        :type direction: int
        :param step: The number of cell to cross in one movement.
        :type step: int

        Example::

            v2d_up = Vector2D.from_direction(constants.UP, 1)
        """
        if direction == constants.NO_DIR:
            return cls(0, 0)
        elif direction == constants.UP:
            return cls(-step, 0)
        elif direction == constants.DOWN:
            return cls(+step, 0)
        elif direction == constants.LEFT:
            return cls(0, -step)
        elif direction == constants.RIGHT:
            return cls(0, +step)
        elif direction == constants.DRUP:
            return cls(-step, +step)
        elif direction == constants.DRDOWN:
            return cls(+step, +step)
        elif direction == constants.DLUP:
            return cls(-step, -step)
        elif direction == constants.DLDOWN:
            return cls(+step, -step)


class Math(object):
    """The math class regroup math functions required for game development.

    .. versionadded:: 1.2.0

    For the moment there is only static methods in that class but it will evolve in the
    future.

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def intersect(row1, column1, width1, height1, row2, column2, width2, height2):
        """This function check if 2 rectangles intersect.

        The 2 rectangles are defined by their positions (row, column) and dimension
        (width and height).

        :param row1: The row of the first rectangle
        :type row1: int
        :param column1: The column of the first rectangle
        :type column1: int
        :param width1: The width of the first rectangle
        :type width1: int
        :param height1: The height of the first rectangle
        :type height1: int
        :param row2: The row of the second rectangle
        :type row2: int
        :param column2: The column of the second rectangle
        :type row2: int
        :param width2: The width of the second rectangle
        :type width2: int
        :param height2: The height of the second rectangle
        :type height2: int
        :returns: A boolean, True if the rectangles intersect False, otherwise.

        Example::

            if intersect(projectile.row, projectile.column, projectile.width,
                         projectile.height, bady.row, bady.column, bady.width,
                         bady.height):
                projectile.hit([bady])
        """
        # Shortcut: if they are at the same position they obviously intersect
        if row1 == row2 and column1 == column2:
            return True
        return (
            max(row1, row1 + height1 - 1) >= min(row2, row2 + height2 - 1)
            and min(row1, row1 + height1 - 1) <= max(row2, row2 + height2 - 1)
            and max(column1, column1 + width1 - 1) >= min(column2, column2 + width2 - 1)
            and min(column1, column1 + width1 - 1) <= max(column2, column2 + width2 - 1)
        )

    @staticmethod
    def distance(row1, column1, row2, column2):
        """Return the euclidian distance between to points.

        Points are identified by their row and column.
        If you want the distance in number of cells, you need to round the result (see
        example).

        :param row1: the row number (coordinate) of the first point.
        :type row1: int
        :param column1: the column number (coordinate) of the first point.
        :type column1: int
        :param row2: the row number (coordinate) of the second point.
        :type row2: int
        :param column2: the column number (coordinate) of the second point.
        :type column2: int
        :return: The distance between the 2 points.
        :rtype: float

        Example::

            distance = round(base.Math.distance(player.row,
                                            player.column,
                                            npc.row,
                                            npc.column)
        """
        return math.sqrt((column2 - column1) ** 2 + (row2 - row1) ** 2)
