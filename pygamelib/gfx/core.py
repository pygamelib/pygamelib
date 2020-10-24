__docformat__ = "restructuredtext"

"""This module contains the core classes for the "graphic" system.

.. autosummary::
   :toctree: .

   Color
   Sprixel
   Sprite
   SpriteCollection
   Animation
"""
from pygamelib import board_items
from pygamelib import base
from pygamelib import constants
from pygamelib.assets import graphics
import time
from collections import UserDict
from uuid import uuid4
import json
import re


class Color(object):
    """
    .. versionadded:: 1.3.0

    A color represented by red, green and blue (RGB) components.
    Values are integer between 0 and 255 (both included).

    :param r: The red component of the color.
    :type r: int
    :param g: The green component of the color.
    :type g: int
    :param b: The blue component of the color.
    :type b: int

    Example::

        # color is blue
        color = Color(0, 0, 255)
        # and now color is pink
        color.r = 255
    """

    def __init__(self, r=0, g=0, b=0):
        super().__init__()
        self.__r = r
        self.__g = g
        self.__b = b

    @property
    def r(self):
        """
        The r property controls the intensity of the red color. You can set it to an
        integer between 0 and 255 (both included).

        Example::

           color = Color(128, 128, 0)
           print(f"Value for r is {color.r}")
           color.r = 255
           print(f"New value for r is {color.r}")
        """
        return self.__r

    @r.setter
    def r(self, val):
        if type(val) is int and val >= 0 and val <= 255:
            self.__r = val
        else:
            raise base.PglInvalidTypeException(
                "The value for red needs to be an integer between 0 and 255."
            )

    @property
    def g(self):
        """
        The g property controls the intensity of the green color. You can set it to an
        integer between 0 and 255 (both included).

        Example::

           color = Color(128, 128, 0)
           print(f"Value for g is {color.g}")
           color.g = 255
           print(f"New value for g is {color.g}")
        """
        return self.__g

    @g.setter
    def g(self, val):
        if type(val) is int and val >= 0 and val <= 255:
            self.__g = val
        else:
            raise base.PglInvalidTypeException(
                "The value for green needs to be an integer between 0 and 255."
            )

    @property
    def b(self):
        """
        The b property controls the intensity of the blue color. You can set it to an
        integer between 0 and 255 (both included).

        Example::

           color = Color(128, 128, 0)
           print(f"Value for b is {color.b}")
           color.b = 255
           print(f"New value for b is {color.b}")
        """
        return self.__b

    @b.setter
    def b(self, val):
        if type(val) is int and val >= 0 and val <= 255:
            self.__b = val
        else:
            raise base.PglInvalidTypeException(
                "The value for blue needs to be an integer between 0 and 255."
            )

    @classmethod
    def from_ansi(cls, string):
        """Create and return a Color object based on an ANSI color string.

        .. IMPORTANT:: The string must be RGB, i.e '\x1b[38;2;RED;GREEN;BLUEm' or
           '\x1b[48;2;RED;GREEN;BLUEm' for foreground and background colors. This
           method will return None if the color string is not RGB.
           It is also important to understand that Color is independent from the
           foreground of background, it is just a color. Therefor '\x1b[38;2;89;32;93m'
           and '\x1b[48;2;89;32;93m' will both be parsed into Color(89, 32, 93).

        :param string: The ANSI color string to convert.
        :type string: str

        Example::

            color = Color.from_ansi()
        """
        match = re.findall(".*\[[34]8;2;(\d+);(\d+);(\d+)m.*", string)
        if len(match) > 0:
            return Color(match[0][0], match[0][1], match[0][2])
        return None

    def __eq__(self, other):
        if self.r == other.r and self.g == other.g and self.b == other.b:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    def blend(self, other_color, fraction=0.5):
        """
        Blend the color with another one. Fraction controls the amount of other_color
        that is included (0 means no inclusion at all).

        :param other_color: The color to blend with.
        :type other_color: :class:`~pygamelib.gfx.core.Color`
        :param fraction: The blending modulation factor between 0 and 1.
        :type fraction: float

        Example::

            a = Color(200, 200, 200)
            b = Color(25, 25, 25)
            # c is going to be Color(112, 112, 112)
            c = a.blend(b, 0.5)
        """
        if type(fraction) is not float or fraction < 0.0 or fraction > 1.0:
            raise base.PglInvalidTypeException(
                "fraction needs to be a float between 0.0 and 1.0."
            )
        if not isinstance(other_color, Color):
            raise base.PglInvalidTypeException(
                "other_color needs to be a Color object."
            )
        return Color(
            int((other_color.r - self.r) * fraction + self.r),
            int((other_color.g - self.g) * fraction + self.g),
            int((other_color.b - self.b) * fraction + self.b),
        )

    def serialize(self):
        """Serialize a Color into a dictionary.

        :returns: The class as a  dictionary
        :rtype: dict

        Example::

            json.dump( color.serialize() )
        """
        return {
            "red": self.r,
            "green": self.g,
            "blue": self.b,
        }

    @classmethod
    def load(cls, data):
        """
        Create a new Color object based on serialized data.

        :param data: Data loaded from JSON data (deserialized).
        :type data: dict
        :rtype: :class:`Color`

        Example::

            new_sprite = Color.load(json_parsed_data['default_sprixel']['fg_color'])
        """
        return cls(data["red"], data["green"], data["blue"])


class Sprixel(object):

    """
    A sprixel is the representation of 1 cell of the sprite or one cell on the Board.
    It is not really a pixel but it is the closest notion we'll have.
    A Sprixel has a background color, a foreground color and a model.
    All regular BoardItems can have use Sprixel instead of model.

    If the background color and the is_bg_transparent are None or empty strings,
    the sprixel will be automatically configured with transparent background.
    In that case, as we can really achieve transparency in the console, the sprixel will
    take the background color of whatever it is overlapping.

    :param model: The model, it can be any string. Preferrably a single character.
    :type model: str
    :param bg_color: An ANSI escape sequence to configure the background color.
    :type bg_color: str
    :param fg_color: An ANSI escape sequence to configure the foreground color.
    :type fg_color: str
    :param is_bg_transparent: Set the background of the Sprixel to be transparent. It
       tells the engine to replace the background of the Sprixel by the background color
       of the overlapped sprixel.
    :type is_bg_transparent: bool

    Example::

        player = Player(sprixel=Sprixel(
                                        '#',
                                        Color(128,56,32),
                                        Color(255,255,0),
                                        ))
    """

    def __init__(self, model="", bg_color=None, fg_color=None, is_bg_transparent=None):
        super().__init__()
        self.model = model
        if bg_color is None or isinstance(bg_color, Color):
            self.bg_color = bg_color
        else:
            raise base.PglInvalidTypeException(
                "Sprixel(model, bg_color, fg_color): bg_color needs to be a Color "
                "object."
            )
        if fg_color is None or isinstance(fg_color, Color):
            self.fg_color = fg_color
        else:
            raise base.PglInvalidTypeException(
                "Sprixel(model, bg_color, fg_color): fg_color needs to be a Color "
                "object."
            )
        self.is_bg_transparent = False
        if type(is_bg_transparent) is bool:
            self.is_bg_transparent = is_bg_transparent
        elif (bg_color is None) and (
            is_bg_transparent is None or is_bg_transparent == ""
        ):
            self.is_bg_transparent = True

    def __repr__(self):
        t = base.Console.instance()
        bgc = fgc = ""
        if self.bg_color is not None and isinstance(self.bg_color, Color):
            bgc = t.on_color_rgb(self.bg_color.r, self.bg_color.g, self.bg_color.b)
        if self.fg_color is not None and isinstance(self.fg_color, Color):
            fgc = t.color_rgb(self.fg_color.r, self.fg_color.g, self.fg_color.b)
        return f"{bgc}{fgc}{self.model}\x1b[0m"

    def __str__(self):  # pragma: no cover
        return self.__repr__()

    def __eq__(self, other):
        if (
            self.model == other.model
            and self.bg_color == other.bg_color
            and self.fg_color == other.fg_color
        ):
            return True
        else:
            return False

    def __ne__(self, other):
        if (
            self.model != other.model
            or self.bg_color != other.bg_color
            or self.fg_color != other.fg_color
        ):
            return True
        else:
            return False

    @staticmethod
    def from_ansi(string):
        """Takes an ANSI string, parse it and return a Sprixel.

        :param string: The ANSI string to parse.
        :type string: str

        Example::

            new_sprixel = Sprixel.from_ansi(
                "\\x1b[48;2;139;22;19m\\x1b[38;2;160;26;23m▄\\x1b[0m"
            )

        .. warning:: This has mainly be tested with ANSI string generated by climage.
        """
        new_sprixel = Sprixel()
        if "[48;" in string and "[38;" in string and "▄" in string:
            (colors, end) = string.split("▄")
            new_sprixel.model = "▄"
            for e in colors.split("m"):
                if "[48;" in e:
                    # new_sprixel.bg_color = f"{e}m"
                    new_sprixel.bg_color = Color.from_ansi(f"{e}m")
                elif "[38;" in e:
                    # new_sprixel.fg_color = f"{e}m"
                    new_sprixel.fg_color = Color.from_ansi(f"{e}m")
        elif "[38;" in string and "▄" in string:
            (colors, end) = string.split("▄")
            new_sprixel.model = "▄"
            for e in colors.split("m"):
                if "[38;" in e:
                    # new_sprixel.fg_color = f"{e}m"
                    new_sprixel.fg_color = Color.from_ansi(f"{e}m")
        elif "[48;" in string and "▄" in string:
            (colors, end) = string.split("▄")
            new_sprixel.model = "▄"
            for e in colors.split("m"):
                if "[48;" in e:
                    # new_sprixel.bg_color = f"{e}m"
                    new_sprixel.bg_color = Color.from_ansi(f"{e}m")
        if new_sprixel.bg_color is not None:
            new_sprixel.is_bg_transparent = False
        return new_sprixel

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if type(value) is str:
            self.__model = value
        else:
            raise base.PglInvalidTypeException(
                f"A Sprixel.model must be a string. {value} is not a string."
            )

    @property
    def bg_color(self):
        return self.__bg_color

    @bg_color.setter
    def bg_color(self, value):
        if isinstance(value, Color) or value is None:
            self.__bg_color = value
        else:
            raise base.PglInvalidTypeException(
                f"A Sprixel.bg_color must be a Color object."
            )

    @property
    def fg_color(self):
        return self.__fg_color

    @fg_color.setter
    def fg_color(self, value):
        if isinstance(value, Color) or value is None:
            self.__fg_color = value
        else:
            raise base.PglInvalidTypeException(
                f"A Sprixel.fg_color must be a Color object."
            )

    def serialize(self):
        """Serialize a Sprixel into a dictionary.

        :returns: The class as a  dictionary
        :rtype: dict

        Example::

            json.dump( sprixel.serialize() )
        """
        return {
            "model": self.model,
            "bg_color": self.bg_color and self.bg_color.serialize() or {},
            "fg_color": self.fg_color and self.fg_color.serialize() or {},
            "is_bg_transparent": self.is_bg_transparent,
        }

    @classmethod
    def load(cls, data):
        """
        Create a new Sprixel object based on serialized data.

        :param data: Data loaded from JSON data (deserialized).
        :type data: dict
        :rtype: :class:`Sprixel`

        Example::

            new_sprite = Sprixel.load(json_parsed_data['default_sprixel'])
        """
        sprix = cls(
            data["model"], Color.load(data["bg_color"]), Color.load(data["fg_color"])
        )
        sprix.is_bg_transparent = bool(data["is_bg_transparent"])
        return sprix

    @classmethod
    def black_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.BLACK_RECT.
        The difference is that BLACK_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.black_rect()
        """
        return cls(" ", Color(0, 0, 0))

    @classmethod
    def black_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.BLACK_SQUARE.
        The difference is that BLACK_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.black_square()
        """
        return cls("  ", Color(0, 0, 0))

    @classmethod
    def white_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.WHITE_RECT.
        The difference is that WHITE_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.white_rect()
        """
        return cls(" ", Color(255, 255, 255))

    @classmethod
    def white_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.WHITE_SQUARE.
        The difference is that WHITE_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.white_square()
        """
        return cls("  ", Color(255, 255, 255))

    @classmethod
    def red_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.RED_RECT.
        The difference is that RED_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.red_rect()
        """
        return cls(" ", Color(255, 0, 0))

    @classmethod
    def red_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.RED_SQUARE.
        The difference is that RED_SQUARE is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.red_square()
        """
        return cls("  ", Color(255, 0, 0))

    @classmethod
    def green_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.GREEN_RECT.
        The difference is that GREEN_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.green_rect()
        """
        return cls(" ", Color(0, 255, 0))

    @classmethod
    def green_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.GREEN_SQUARE.
        The difference is that GREEN_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.green_square()
        """
        return cls("  ", Color(0, 255, 0))

    @classmethod
    def blue_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.BLUE_RECT.
        The difference is that BLUE_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.blue_rect()
        """
        return cls(" ", Color(0, 0, 255))

    @classmethod
    def blue_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.BLUE_SQUARE.
        The difference is that BLUE_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.blue_square()
        """
        return cls("  ", Color(0, 0, 255))

    @classmethod
    def cyan_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.CYAN_RECT.
        The difference is that CYAN_RECT is a string and this one is a Sprixel that can
        be manipulated more easily.

        Example::

            sprixel = Sprixel.cyan_rect()
        """
        return cls(" ", Color(0, 255, 255))

    @classmethod
    def cyan_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.CYAN_SQUARE.
        The difference is that CYAN_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.cyan_square()
        """
        return cls("  ", Color(0, 255, 255))

    @classmethod
    def magenta_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.MAGENTA_RECT.
        The difference is that MAGENTA_RECT is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.magenta_rect()
        """
        return cls(" ", Color(255, 0, 255))

    @classmethod
    def magenta_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.MAGENTA_SQUARE.
        The difference is that MAGENTA_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        Example::

            sprixel = Sprixel.magenta_square()
        """
        return cls("  ", Color(255, 0, 255))

    @classmethod
    def yellow_rect(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.YELLOW_RECT.
        The difference is that YELLOW_RECT is a string and this one is a Sprixel that
        can be manipulated more easily.

        .. Note:: Yellow is often rendered as brown.

        Example::

            sprixel = Sprixel.yellow_rect()
        """
        return cls(" ", Color(255, 255, 0))

    @classmethod
    def yellow_square(cls):
        """
        This classmethod returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.YELLOW_SQUARE.
        The difference is that YELLOW_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        .. Note:: Yellow is often rendered as brown.

        Example::

            sprixel = Sprixel.yellow_square()
        """
        return cls("  ", Color(255, 255, 0))


class Sprite(object):
    """
    The Sprite object represent a 2D "image" that can be used to represent any complex
    item.
    Obviously, a sprite in the pygamelib is not really an image, it is a series of
    glyphs (or characters) with colors (foreground and background) information.

    A Sprite object is a 2D array of :class:`Sprixel`.

    If you use the climage python module, you can load the generated result into a
    Sprite through Sprite.load_from_ansi_file().

    :param sprixels: A 2D array of :class:`Sprixel`.
    :type sprixels: list
    :param default_sprixel: A default Sprixel to complete lines that are not long
       enough. By default, it's an empty Sprixel.
    :type default_sprixel: :class:`Sprixel`
    :param parent: The parent object of this Sprite. If it's left to None, the
       :class:`~pygamelib.board_items.BoardComplexItem` constructor takes ownership of
       the sprite.
    :type parent: :class:`~pygamelib.board_items.BoardComplexItem` (suggested)
    :param size: A 2 elements list that represent the width and height ([width, height])
       of the Sprite. It is only needed if you create an empty Sprite. If you load from
       a file or provide an array of sprixels it's obviously calculated automatically.
       Default value: [2, 2].
    :type size: list
    :param name: The name of sprite. If none is given, an UUID will be automatically
       generated.
    :type name: str

    Example::

        void = Sprixel()
        # This represent a panda
        panda_sprite = Sprite(
            sprixels=[
                [void, void, void, void, void, void, void, void],
                [
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    void,
                    void,
                    void,
                    void,
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                ],
                [
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                ],
                [
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                ],
                [
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.red_rect(),
                    Sprixel.red_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                ],
                [
                    void,
                    void,
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    void,
                    void,
                ],
                [
                    void,
                    void,
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.white_rect(),
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                ],
                [
                    void,
                    void,
                    Sprixel.black_rect(),
                    Sprixel.black_rect(),
                    void,
                    void,
                    void,
                    void,
                ],
            ],
        )
    """

    def __init__(
        self,
        sprixels=None,
        default_sprixel=Sprixel(),
        parent=None,
        size=[2, 2],
        name=None,
    ):
        super().__init__()
        self.size = size
        self.parent = parent
        self.name = name
        self.default_sprixel = default_sprixel
        if self.name is None or type(self.name) is not str:
            self.name = str(uuid4())
        if sprixels is not None and len(sprixels) > 0:
            self._sprixels = []
            height = 0
            max_width = 0
            for row in sprixels:
                self._sprixels.append([])
                if len(row) > max_width:
                    max_width = len(row)
                width = 0
                for column in row:
                    self._sprixels[height].append(sprixels[height][width])
                    width += 1
                height += 1
            self.size = [max_width, len(self._sprixels)]

        else:
            self.empty()

    def __repr__(self):
        string = []
        for scanline in self._sprixels:
            string.append("".join(map(lambda i: i.__repr__(), scanline)))
        return "\n".join(string)

    def __str__(self):  # pragma: no cover
        return self.__repr__()

    def empty(self):
        """Empty the sprite and fill it with default sprixels.

        Example::

            player_sprite.empty()
        """
        self._sprixels = [
            [self.default_sprixel for i in range(0, self.size[0])]
            for j in range(0, self.size[1])
        ]

    def sprixel(self, row=0, column=None):
        """Return a sprixel at a specific position within the sprite.

        If the column is set to None, the whole row is returned.

        :param row: The row to access within the sprite.
        :type row: int
        :param column: The column to access within the sprite.
        :type column: int

        Example::

            # Return the entire line at row index 2
            scanline = house_sprite.sprixel(2)
            # Return the specific sprixel at sprite internal coordinate 2,3
            house_sprixel = house_sprite.sprixel(2, 3)

        .. WARNING:: For performance consideration sprixel() does not check the size of
           its matrix. This method is called many times during rendering and 2 calls to
           len() in a row are adding up pretty quickly.
           It checks the boundary of the sprite using the cached size. Make sure it is
           up to date!
        """
        if type(row) is not int:
            raise base.PglInvalidTypeException("Sprite.sprixel(): Row is not an int.")
        if row < 0 or row >= self.size[1]:
            raise base.PglException(
                "out_of_sprite_boundaries",
                f"Sprite.sprixel(): Row ({row}) is out of the Sprite boundaries.",
            )
        if column is None:
            return self._sprixels[row]
        else:
            if type(column) is not int:
                raise base.PglInvalidTypeException(
                    "Sprite.sprixel(): Column is not an int."
                )
            if column < 0 or column >= self.size[0]:
                raise base.PglException(
                    "out_of_sprite_boundaries",
                    f"Sprite.sprixel(): Column ({column}) is out of the "
                    "Sprite boundaries.",
                )
            return self._sprixels[row][column]

    def set_sprixel(self, row, column, val):
        """
        Set a specific sprixel in the sprite to the given value.
        :param name: some param
        :type name: str

        Example::

            method()
        """
        if type(row) is not int or type(column) is not int:
            raise base.PglInvalidTypeException(
                "Sprite.set_sprixel(row, column, val) row and column needs to be "
                "integer."
            )
        if row < 0 or row >= self.size[1] or column < 0 or column >= self.size[0]:
            raise base.PglException(
                "out_of_sprite_boundaries",
                f"Sprite.set_sprixel(): ({row},{column}) is out of bound.",
            )
        if not isinstance(val, Sprixel):
            raise base.PglInvalidTypeException(
                "Sprite.set_sprixel(row, column, val) val needs to be a Sprixel"
            )
        self._sprixels[row][column] = val

    @classmethod
    def from_text(cls, text_object):
        """
        Create a Sprite from a :class:`~pygamelib.base.Text` object.

        :param text_object: A text object to transform into Sprite.
        :type text_object: :class:`~pygamelib.base.Text`

        Example::

            # The Text object allow for easy manipulation of text
            village_name = base.Text('khukdale',fg_red, bg_green)
            # It can be converted into a Sprite to be displayed on the Board
            village_sign = board_items.Tile(sprite=Sprite.from_text(village_name))
            # And can be used as formatted text
            notifications.push( f'You enter the dreaded village of {village_name}' )
        """
        sprixels = []
        style = ""
        max_width = 0
        for line in text_object.text.splitlines():
            sprixels.append([])
            if len(line) > max_width:
                max_width = len(line)
            for char in line:
                sprixels[-1].append(
                    Sprixel(
                        style + char + base.Style.RESET_ALL,
                        text_object.bg_color,
                        text_object.fg_color,
                    )
                )
        return cls(sprixels=sprixels)

    @classmethod
    def load_from_ansi_file(cls, filename, default_sprixel=None):
        """Load an ANSI encoded file into a Sprite object.

        This class method can load a file produced by the climage python module and
        load it into a Sprite class. Each character is properly decoded into a
        :class:`Sprixel` with model, background and foreground colors.

        A Sprite is rectangular (at least for the moment), so in case the file is
        not shaped as a rectangle, this method automatically fills the void with a
        default sprixel (to make sure all lines in the sprite have the same length).
        By default, it fills the table with None "values" but you can specify a default
        sprixel.

        The reasons the default sprixel is set to None is because None values in a
        sprite are not translated into a component in
        :class:`~pygamelib.board_items.BoardComplexItem` (i.e no sub item is generated).

        :param filename: The path to a file to load.
        :type filename: str
        :param default_sprixel: The default Sprixel to fill a non rectangular shaped
           sprite.
        :type default_sprixel: None | :class:`Sprixel`

        Example::

            player_sprite = gfx_core.Sprite.load_from_ansi_file('gfx/models/player.ans')
        """
        if default_sprixel is None:
            default_sprixel = Sprixel(" ", None, None)
        new_sprite = cls(default_sprixel=default_sprixel)
        with open(filename, "r") as sprite_file:
            sprixels_list = []
            height = 0
            max_width = 0
            while True:
                line = sprite_file.readline()
                if not line:
                    break
                width = 0
                sprixels_list.append([])
                for s in line.rstrip().split("▄"):
                    if s != "\x1b[0m":
                        sprixels_list[height].append(Sprixel.from_ansi(f"{s}▄\x1b[0m"))
                        width += 1
                if width > max_width:
                    max_width = width
                height += 1
            for row in range(0, len(sprixels_list)):
                if len(sprixels_list[row]) < max_width:
                    for column in range(len(sprixels_list[row]), max_width):
                        sprixels_list[row].append(default_sprixel)
            new_sprite._sprixels = sprixels_list
            new_sprite.size = [max_width, height]
        return new_sprite

    def flip_horizontally(self):
        """Flip the sprite horizontally.

        This method performs a symmetry versus the vertical axis.

        At the moment, glyph are not inverted. Only the position of the sprixels.

        The flipped sprite is returned (original sprite is not modified).

        :rtype: :class:`Sprite`

        Example::

            reflection_sprite = player_sprite.flip_horizontally()
        """
        new_sprite = Sprite(
            size=self.size,
            sprixels=None,
            default_sprixel=self.default_sprixel,
            parent=self.parent,
        )
        nc = 0
        # Flipping horizontally is just a symmetry vs a vertical axis
        for col in range(self.size[0] - 1, -1, -1):
            for row in range(0, self.size[1]):
                new_sprite.set_sprixel(row, nc, self._sprixels[row][col])
            nc += 1
        return new_sprite

    def flip_vertically(self):
        """Flip the sprite vertically (i.e upside/down).

        At the moment, glyph are not inverted. Only the position of the sprixels.
        There is one exception however, as climage uses the '▄' utf8 glyph as a marker,
        that specific glyph is inverted to '▀' and vice versa.

        The flipped sprite is returned (original sprite is not modified).

        :rtype: :class:`Sprite`

        Example::

            reflection_sprite = player_sprite.flip_vertically()
        """
        new_sprite = Sprite(
            size=self.size,
            sprixels=None,
            default_sprixel=self.default_sprixel,
            parent=self.parent,
        )
        nr = 0
        for row in range(self.size[1] - 1, -1, -1):
            for col in range(0, self.size[0]):
                new_sprix = self._sprixels[row][col]
                if new_sprix.model == graphics.Blocks.LOWER_HALF_BLOCK:
                    new_sprix.model = graphics.Blocks.UPPER_HALF_BLOCK
                elif new_sprix.model == graphics.Blocks.UPPER_HALF_BLOCK:
                    new_sprix.model = graphics.Blocks.LOWER_HALF_BLOCK
                new_sprite.set_sprixel(nr, col, new_sprix)
            nr += 1
        return new_sprite

    def calculate_size(self):
        """
        Calculate the size of the sprite and update the size variable.

        The size is immediately returned.

        It is done separately for concerns about performances of doing that everytime
        the size is requested.

        :rtype: list

        Example::

            spr_size = spr.calculate_size()
            if spr_size != spr.size:
                raise PglException(
                            'perturbation_in_the_Force',
                            'Something is very wrong with the sprite!'
                        )
        """
        # Warning: recalculate the size of the Sprite, it is much faster
        # although not safe to use self.size
        height = 0
        max_width = 0
        for row in self._sprixels:
            width = 0
            for col in row:
                width += 1
            if width > max_width:
                max_width = width
            height += 1
        self.size = [max_width, height]
        return self.size

    def set_transparency(self, state):
        """This method enable transparent background to all the sprite's sprixels.

        :param state: a boolean to enable or disable background transparency
        :type name: bool

        Example::

            player_sprite.set_transparency(True)

        .. WARNING:: This set background transparency on all sprixels, make sure you are
           not using background colors as part of your sprite before doing that.
           It can also be used as a game/rendering mechanic. Just make sure you know
           what you do.
           As a reminder, by default, sprixels with no background have transparent
           background enable.
        """
        for line in self._sprixels:
            for s in line:
                s.is_bg_transparent = state

    def serialize(self):
        """Serialize a Sprite into a dictionary.

        :returns: The class as a  dictionary
        :rtype: dict

        Example::

            json.dump( sprite.serialize() )
        """
        ret_dict = {
            "size": self.size,
            "name": self.name,
            "default_sprixel": self.default_sprixel.serialize(),
            "sprixels": [],
        }
        for row in range(0, self.size[1]):
            tmp = []
            for column in range(0, self.size[0]):
                tmp.append(self.sprixel(row, column).serialize())

            ret_dict["sprixels"].append(tmp)

        return ret_dict

    @classmethod
    def load(cls, data):
        """
        Create a new Sprite object based on serialized data.

        :param data: Data loaded from a JSON sprite file (deserialized).
        :type data: dict
        :rtype: :class:`Sprite`

        Example::

            new_sprite = Sprite.load(json_parsed_data)
        """
        sprixels = []
        try:
            for row in range(0, int(data["size"][1])):
                tmp = []
                for column in range(0, int(data["size"][0])):
                    tmp.append(Sprixel.load(data["sprixels"][row][column]))
                sprixels.append(tmp)
            new_sprite = cls(
                name=data["name"],
                default_sprixel=Sprixel.load(data["default_sprixel"]),
                sprixels=sprixels,
            )
            return new_sprite
        except IndexError:
            raise base.PglException(
                "invalid_sprite_size",
                "Sprite.load(data): sprixels array size is different from sprite "
                "computed size.",
            )


class SpriteCollection(UserDict):
    """
    SpriteCollection is a dictionnary class that derives collections.UserDict.

    Its main goal is to provide an easy to use object to load and save sprite files.
    On top of traditional dict method, it provides the following capabilities:

     - loading and writing from and to JSON files,
     - data serialization,
     - shortcut to add sprites to the dictionnary.

    A SpriteCollection is an unordered indexed list of Sprites (i.e a dictionnary).

    Sprites are indexed by their names in that collection.

    Example::

       # Load a sprite file
       sprites_village1 = SpriteCollection.load_json_file('gfx/village1.spr')
       # display the Sprites with their name
       for sprite_name in sprites_village1:
           print(f'{sprite_name}:\\n{sprites_village1[sprite_name]}')
       # Add an empty sprite with name 'house_placeholder'
       sprites_village1.add( Sprite(name='house_placeholder') )
       # This is absolutely equivalent to:
       sprites_village1['house_placeholder'] = Sprite(name='house_placeholder')
       # And now rewrite the sprite file with the new placeholder house
       sprites_village1.to_json_file('gfx/village1.spr')

    """

    def __init__(self, data=dict()):
        super().__init__(data)

    @classmethod
    def load(cls, data):
        """
        Load serialized data and return a new SpriteCollection object.

        :param data: Serialized data that need to be expanded into objects.
        :type data: str
        :returns: A new SpriteCollection object.
        :rtype: :class:`SpriteCollection`

        Example::

            sprites_village1 = SpriteCollection.load(
                sprites_village_template.serialize()
            )
        """
        if "sprites_count" in data.keys() and data["sprites_count"] is not None:
            if (
                "sprites" in data.keys()
                and data["sprites"] is not None
                and type(data["sprites"]) is dict
            ):
                sc = cls()
                if data["sprites_count"] == len(data["sprites"]):
                    for spr_name in data["sprites"]:
                        sc.data[spr_name] = Sprite.load(data["sprites"][spr_name])
                    return sc
                else:
                    raise base.PglException(
                        "corrupted_sprite_data",
                        "SpriteCollection.load(data): sprites count is different from "
                        "actual number of sprites.",
                    )
        else:
            raise base.PglException(
                "invalid_sprite_data",
                "SpriteCollection.load(data): Invalid sprite data, sprites_count is "
                "missing.",
            )

    @staticmethod
    def load_json_file(filename):
        """
        Load a JSON sprite file into a new SpriteCollection object.

        :param filename: The complete path (relative or absolute) to the sprite file.
        :type filename: str
        :returns: A new SpriteCollection object.
        :rtype: :class:`SpriteCollection`

        Example::

            sprites_village1 = SpriteCollection.load_json_file('gfx/village1.spr')
        """
        with open(filename) as sprites_file:
            sprites_data = json.load(sprites_file)
            return SpriteCollection.load(sprites_data)

    def serialize(self):
        """
        Return a serialized version of the SpriteCollection. The serialized data can be
        pass to the JSON module to export.

        :returns: The SpriteCollection object serialized as a dictionnary.
        :rtype: dict

        Example::

            data = sprites_village1.serialize()
        """
        ret_data = dict()
        ret_data["sprites_count"] = len(self.data)
        ret_data["sprites"] = dict()
        for spr_name in self.data:
            ret_data["sprites"][spr_name] = self.data[spr_name].serialize()
        return ret_data

    def to_json_file(self, filename):
        """
        Export the SpriteCollection object in JSON and writes it on the disk.

        :param filename: The complete path (relative or absolute) to the sprite file to
           write.
        :type filename: str

        Example::

            sprites_village1.to_json_file('gfx/village1.spr')
        """
        with open(filename, "w") as file:
            json.dump(self.serialize(), file)

    def add(self, sprite):
        """
        Add a Sprite to the collection. This method is simply a shortcut to the usual
        dictionnary affectation. The collection requires the name of the Sprite to be
        the key. That method does that automatically.

        :param sprite: A Sprite object to add to the collection.
        :type sprite: :class:`Sprite`

        .. WARNING:: As SpriteCollection index Sprites by their name if you change the
           Sprite's name *after* adding it to the collection you will need to manually
           update the keys.

        Example::

            sprites_village1 = SpriteCollection.load_json_file('gfx/village1.spr')
            new_village = SpriteCollection()
            new_village.add( copy.deepcopy( sprites_village1.get('bakery') ) )
            print( new_village['bakery'] )
        """
        if isinstance(sprite, Sprite):
            self.data[sprite.name] = sprite
        else:
            raise base.PglInvalidTypeException(
                "SpriteCollection.add(sprite): require a Sprite object."
            )


class Animation(object):
    """
    The Animation class is used to give the ability to have more than one model
    for a BoardItem. A BoardItem can have an animation and all of them that
    are available to the Game object can be animated through
    Game.animate_items(lvl_number).
    To benefit from that, BoardItem.animation must be set explicitely.
    An animation is controlled via the same state system than the Actuators.

    The frames are all stored in a list called frames, that you can access
    through Animation.frames.

    :param display_time: The time each frame is displayed
    :type display_time: float
    :param auto_replay: controls the auto replay of the animation, if false
        once the animation is played it stays on the last
        frame of the animation.
    :type auto_replay: bool
    :param frames: an array of "frames" (string, sprixel or sprite)
    :type frames: array[str|Sprixel|Sprite]
    :param animated_object: The object to animate. This parameter is deprecated.
        Please use parent instead. It is only kept for backward compatibility.
        The parent parameter always takes precedence over this one.
    :type animated_object: :class:`~pygamelib.board_items.BoardItem`
    :param parent: The parent object. It is also the object to animate.
        Important: We cannot animate anything else that BoardItems and subclasses.
    :type parent: :class:`~pygamelib.board_items.BoardItem`
    :param refresh_screen: The callback function that controls the redrawing of
        the screen. This function reference should come from the main game.
    :type refresh_screen: function

    Example ::

        def redraw_screen(game_object):
            game_object.clear_screen()
            game_object.display_board()

        item = BoardItem(model=Sprite.ALIEN, name='Friendly Alien')
        # By default BoardItem does not have any animation, we have to
        # explicitely create one
        item.animation = Animation(display_time=0.1, parent=item,
                                   refresh_screen=redraw_screen)
    """

    def __init__(
        self,
        display_time=0.05,
        auto_replay=True,
        frames=None,
        animated_object=None,
        refresh_screen=None,
        initial_index=None,
        parent=None,
    ):
        self.state = constants.RUNNING
        self.display_time = display_time
        self.auto_replay = auto_replay
        if frames is None:
            frames = []
        elif isinstance(frames, SpriteCollection):
            nf = []
            for sn in frames:
                nf.append(frames[sn])
            frames = nf

        self.frames = frames
        if initial_index is None:
            self._frame_index = 0
            self._initial_index = 0
        else:
            self._frame_index = initial_index
            self._initial_index = initial_index
        if animated_object is not None and parent is None:
            self.parent = animated_object
            self.animated_object = animated_object
        elif parent is not None:
            self.parent = parent
            self.animated_object = parent
        self.refresh_screen = refresh_screen
        self.__dtanimate = 0.0

    @property
    def dtanimate(self):
        return self.__dtanimate

    @dtanimate.setter
    def dtanimate(self, value):
        if type(value) is float or type(value) is int:
            self.__dtanimate = value
        else:
            raise base.PglInvalidTypeException(
                "Animation.dtanimate(value): value needs to be an int or float."
            )

    def start(self):
        """Set the animation state to constants.RUNNING.

        If the animation state is not constants.RUNNING, animation's next_frame()
        function return the last frame returned.

        Example::

            item.animation.start()
        """
        self.state = constants.RUNNING

    def pause(self):
        """Set the animation state to PAUSED.

        Example::

            item.animation.pause()
        """
        self.state = constants.PAUSED

    def stop(self):
        """Set the animation state to STOPPED.

        Example::

            item.animation.stop()
        """
        self.state = constants.STOPPED

    def add_frame(self, frame):
        """Add a frame to the animation.

        The frame has to be a string (that includes sprites from the Sprite
        module and squares from the Utils module).

        Raise an exception if frame is not a string.

        :param frame: The frame to add to the animation.
        :type frame: str
        :raise: :class:`pygamelib.base.PglInvalidTypeException`

        Example::

            item.animation.add_frame(Sprite.ALIEN)
            item.animation.add_frame(Sprite.ALIEN_MONSTER)
        """
        if (
            type(frame) is str
            or isinstance(frame, Sprixel)
            or isinstance(frame, Sprite)
        ):
            self.frames.append(frame)
        else:
            raise base.PglInvalidTypeException(
                'The "frame" parameter must be a string, Sprixel or Sprite.'
            )

    def search_frame(self, frame):
        """Search a frame in the animation.

        That method is returning the index of the first occurrence of "frame".

        Raise an exception if frame is not a string.

        :param frame: The frame to find.
        :type frame: str
        :rtype: int
        :raise: :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            item.animation.remove_frame(
                item.animation.search_frame(Sprite.ALIEN_MONSTER)
            )

        """
        if (
            type(frame) is str
            or isinstance(frame, Sprixel)
            or isinstance(frame, Sprite)
        ):
            return self.frames.index(frame)
        else:
            raise base.PglInvalidTypeException(
                'The "frame" parameter must be a string.'
            )

    def remove_frame(self, index):
        """Remove a frame from the animation.

        That method remove the frame at the specified index and return it
        if it exists.

        If the index is out of bound an exception is raised.
        If the index is not an int an exception is raised.

        :param index: The index of the frame to remove.
        :type index: int
        :rtype: str
        :raise: IndexError, PglInvalidTypeException

        Example::

            item.animation.remove_frame( item.animation.search_frame(
                Sprite.ALIEN_MONSTER)
            )

        """
        if type(index) is not int:
            raise base.PglInvalidTypeException('The "index" parameter must be an int.')
        if index <= self._frame_index and self._frame_index > 0:
            self._frame_index -= 1
        return self.frames.pop(index)

    def reset(self):
        """Reset the Animation to the first frame.

        Example::

            item.animation.reset()
        """
        self._frame_index = self._initial_index

    def current_frame(self):
        """Return the current frame.

        Example::

            item.model = item.animation.current_frame()
        """
        return self.frames[self._frame_index]

    def next_frame(self):
        """Update the parent's model, sprixel or sprite with the next frame of the
        animation.

        That method takes care of automatically replaying the animation if the
        last frame is reached if the state is constants.RUNNING.

        If the the state is PAUSED it still update the parent.model
        and returning the current frame. It does NOT actually go to next frame.

        If parent is not a sub class of
        :class:`~pygamelib.board_items.BoardItem` an exception is raised.

        :raise: :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            item.animation.next_frame()

        .. WARNING:: If you use Sprites as frames, you need to make sure your Animation
            is attached to a :class:`~pygamelib.board_items.BoardComplexItem`.

        """
        if not isinstance(self.parent, board_items.BoardItem):
            raise base.PglInvalidTypeException(
                "The parent needs to be a sub class of BoardItem."
            )
        if self.state == constants.STOPPED:
            return
        elif self.state == constants.RUNNING:
            self._frame_index += 1
            if self._frame_index >= len(self.frames):
                if self.auto_replay:
                    self.reset()
                else:
                    self._frame_index = len(self.frames) - 1
        if type(self.frames[self._frame_index]) is str:
            self.parent.model = self.frames[self._frame_index]
        elif isinstance(self.frames[self._frame_index], Sprixel):
            self.parent.sprixel = self.frames[self._frame_index]
        elif isinstance(self.frames[self._frame_index], Sprite):
            self.parent.sprite = self.frames[self._frame_index]
            self.parent.update_sprite()
        else:
            raise base.PglInvalidTypeException(
                "Animation.next_frame(): the frame is neither a string, a sprixel nor a"
                " sprite."
            )
        return self.frames[self._frame_index]

    def play_all(self):
        """Play the entire animation once.

        That method plays the entire animation only once, there is no auto
        replay as it blocks the game (for the moment).

        If the the state is PAUSED or STOPPED, the animation does not play and
        the method return False.

        If parent is not a sub class of
        :class:`~pygamelib.board_items.BoardItem` an exception is raised.

        If screen_refresh is not defined or is not a function an exception
        is raised.

        :raise: :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            item.animation.play_all()
        """
        if self.state == constants.PAUSED or self.state == constants.STOPPED:
            return False
        if self.refresh_screen is None or not callable(self.refresh_screen):
            raise base.PglInvalidTypeException(
                "The refresh_screen parameter needs to be a callback "
                "function reference."
            )
        if not isinstance(self.parent, board_items.BoardItem):
            raise base.PglInvalidTypeException(
                "The parent needs to be a sub class of BoardItem."
            )
        self.reset()
        previous_time = time.time()
        ctrl = 0
        while ctrl < len(self.frames):
            if self.dtanimate >= self.display_time:
                # Dirty but that's a current limitation: to restore stuff on the board's
                # overlapped matrix, we need to either move or replace an item after
                # updating the sprite. This is only for sprites that have null items but
                # we don't want to let any one slip.
                # Also: this is convoluted...
                if (
                    isinstance(self.parent, board_items.BoardComplexItem)
                    and self.parent.parent is not None
                    and (
                        isinstance(self.parent.parent, board_items.engine.Board)
                        or isinstance(self.parent.parent, board_items.engine.Game)
                    )
                ):
                    b = None
                    if isinstance(self.parent.parent, board_items.engine.Board):
                        b = self.parent.parent
                    else:
                        b = self.parent.parent.current_board()
                    pos = self.parent.pos
                    # We have to think that someone could try to animate the player
                    # while not on the current board.
                    try:
                        b.remove_item(self.parent)
                    except Exception:
                        return
                    self.next_frame()
                    b.place_item(self.parent, pos[0], pos[1])
                else:
                    self.next_frame()
                self.refresh_screen()
                ctrl += 1
                self.dtanimate = 0
            self.dtanimate += time.time() - previous_time
            previous_time = time.time()
        return True
