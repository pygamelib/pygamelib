__docformat__ = "restructuredtext"

"""This module contains the core classes for the "graphic" system.

.. autosummary::
   :toctree: .

   pygamelib.gfx.core.Color
   pygamelib.gfx.core.Sprixel
   pygamelib.gfx.core.Sprite
   pygamelib.gfx.core.SpriteCollection
   pygamelib.gfx.core.Animation
   pygamelib.gfx.core.Font
"""
from pygamelib import base
from pygamelib.constants import State
from pygamelib.assets import graphics
from pygamelib.functions import pgl_isinstance
import random
import time
from collections import UserDict
from uuid import uuid4
import json
import re
from pygamelib import assets
import importlib_resources
from pathlib import Path


class Color(base.PglBaseObject):
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
        if type(r) is int and type(g) is int and type(b) is int:
            self.__r = r
            self.__g = g
            self.__b = b
        else:
            raise base.PglInvalidTypeException(
                "Color(r, g, b): all parameters must be integers."
            )

    @property
    def r(self):
        """
        The r property controls the intensity of the red color. You can set it to an
        integer between 0 and 255 (both included).

        When this property is set, the observers are notified with the
        :boldblue:`pygamelib.gfx.core.Color.r:changed` event. The :blue:`value` of the
        event is the new value of the property.

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
            self.notify(self, "pygamelib.gfx.core.Color.r:changed", val)
        else:
            raise base.PglInvalidTypeException(
                "The value for red needs to be an integer between 0 and 255."
            )

    @property
    def g(self):
        """
        The g property controls the intensity of the green color. You can set it to an
        integer between 0 and 255 (both included).

        When this property is set, the observers are notified with the
        :boldblue:`pygamelib.gfx.core.Color.g:changed` event. The :blue:`value` of the
        event is the new value of the property.

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
            self.notify(self, "pygamelib.gfx.core.Color.g:changed", val)
        else:
            raise base.PglInvalidTypeException(
                "The value for green needs to be an integer between 0 and 255."
            )

    @property
    def b(self):
        """
        The b property controls the intensity of the blue color. You can set it to an
        integer between 0 and 255 (both included).

        When this property is set, the observers are notified with the
        :boldblue:`pygamelib.gfx.core.Color.b:changed` event. The :blue:`value` of the
        event is the new value of the property.

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
            self.notify(self, "pygamelib.gfx.core.Color.b:changed", val)
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
        if re.search("\[4[01234567]{1}m", string):
            # Here we deal with legacy colors,
            if "[40m" in string:
                return cls(0, 0, 0)
            elif "[41m" in string:
                return cls(255, 0, 0)
            elif "[42m" in string:
                return cls(0, 255, 0)
            elif "[43m" in string:
                return cls(255, 255, 0)
            elif "[44m" in string:
                return cls(0, 0, 255)
            elif "[45m" in string:
                return cls(255, 0, 255)
            elif "[46m" in string:
                return cls(0, 255, 255)
            elif "[47m" in string:
                return cls(255, 255, 255)
        else:
            match = re.findall(".*\[[34]8;2;(\d+);(\d+);(\d+)m.*", string)
            if len(match) > 0:
                return Color(int(match[0][0]), int(match[0][1]), int(match[0][2]))
        return None

    def __eq__(self, other):
        if isinstance(other, Color):
            if self.r == other.r and self.g == other.g and self.b == other.b:
                return True
            return False
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    @classmethod
    def random(cls):
        """Create and return a new random color.

        :rtype: :class:`Color`

        Example::

            my_color = Color.random()
        """
        return cls(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def copy(self):
        """Returns a (deep) copy of this color.

        Example::

            red = Color(255, 0, 0)
            red2 = red.copy()
        """
        return Color(self.r, self.g, self.b)

    def blend(self, other_color, fraction=0.5):
        """
        Blend the color with another one. Fraction controls the amount of other_color
        that is included (0 means no inclusion at all).

        :param other_color: The color to blend with.
        :type other_color: :class:`~pygamelib.gfx.core.Color`
        :param fraction: The blending modulation factor between 0 and 1.
        :type fraction: float
        :return: A new Color object that contains the blended color.
        :rtype: :class:`~pygamelib.gfx.core.Color`

        Example::

            a = Color(200, 200, 200)
            b = Color(25, 25, 25)
            # c is going to be Color(112, 112, 112)
            c = a.blend(b, 0.5)
        """
        if type(fraction) is not float or fraction < 0.0 or fraction > 1.0:
            raise base.PglInvalidTypeException(
                "Color.blend(other_color, fraction): fraction needs to be a float "
                f"between 0.0 and 1.0 (faction={fraction})."
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

        If data is None, None is returned.

        If a color component is missing from data, it is set to 0 (see examples).

        Raises an exception if the color components are not integer.

        :param data: Data loaded from JSON data (deserialized).
        :type data: dict
        :returns: Either a Color object or None if data where empty.
        :rtype: :class:`Color` | NoneType
        :raise: :class:`~pygamelib.base.PglInvalidTypeException`

        Example::

            # Loading from parsed JSON data
            new_color = Color.load(json_parsed_data['default_sprixel']['fg_color'])

            # Loading from incomplete data
            color = Color.load({'red':25,'green':35})
            # Result in the following Color object:
            # Color(25, 35, 0)
        """
        if data is None or data == "":
            return
        elif type(data) is str and (
            ("[38;" in data or "[48;" in data) or re.search("\[4[01234567]{1}m", data)
        ):
            # This is for backward compatibility with 1.2.X
            return cls.from_ansi(data)
        # print(f"Color.load(): data received: '{data}'")
        for c in ["red", "green", "blue"]:
            if c not in data:
                data[c] = 0
            elif type(data[c]) is not int:
                raise base.PglInvalidTypeException(
                    f"In Color.load(data) the {c} component is not an integer."
                )
        return cls(data["red"], data["green"], data["blue"])

    def randomize(self):
        """Set a random value for each of the components of an existing color.

        When this method is called, the observers are notified with the
        :boldblue:`pygamelib.gfx.core.Color.randomized` event. The :blue:`value` of the
        event is the new color.

        :returns: None
        :rtype: NoneType

        Example::

            color = Color()
            color.randomize()
        """
        self.r = random.randrange(256)
        self.g = random.randrange(256)
        self.b = random.randrange(256)
        self.notify(self, "pygamelib.gfx.core.Color.randomized", self)


class Sprixel(base.PglBaseObject):

    """
    A sprixel is the representation of 1 cell of the sprite or one cell on the Board.
    It is not really a pixel but it is the closest notion we'll have.
    A Sprixel has a background color, a foreground color and a model.
    All regular BoardItems can now use a sprixel instead of a model (but simple model is
    still supported of course).

    In the terminal, a sprixel is represented by a single character.

    If the background color and the is_bg_transparent are None, the sprixel will be
    automatically configured with transparent background.
    In that case, as we cannot really achieve transparency in the console, the sprixel
    will take the background color of whatever it is overlapping.

    .. Important:: **BREAKING CHANGE**: in version 1.3.0 background and foreground
       colors use the new :class:`Color` object. Therefor, Sprixel does not accept ANSI
       sequences anymore for the bg_color and fg_color parameters.


    Example::

        player = Player(sprixel=Sprixel(
                                        '#',
                                        Color(128,56,32),
                                        Color(255,255,0),
                                        ))
    """

    def __init__(self, model="", bg_color=None, fg_color=None, is_bg_transparent=None):
        """
        :param model: The model, it can be any string. Preferrably a single character.
        :type model: str
        :param bg_color: A Color object to configure the background color.
        :type bg_color: :class:`Color`
        :param fg_color: A Color object to configure the foreground color.
        :type fg_color: :class:`Color`
        :param is_bg_transparent: Set the background of the Sprixel to be transparent.
           It tells the engine to replace the background of the Sprixel by the
           background color of the overlapped sprixel.
        :type is_bg_transparent: bool

        """
        super().__init__()
        self.__color_cache = ""
        self.__bg_color = None
        self.__fg_color = None
        self.__length = 0
        self.model = model
        self.__length = base.Console.instance().length(model)
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
        return f"{self.__color_cache}{self.model}\x1b[0m"

    def __str__(self):  # pragma: no cover
        return self.__repr__()

    def __build_color_cache(self):
        t = base.Console.instance()
        bgc = fgc = ""
        if self.bg_color is not None and isinstance(self.bg_color, Color):
            bgc = t.on_color_rgb(self.bg_color.r, self.bg_color.g, self.bg_color.b)
        if self.fg_color is not None and isinstance(self.fg_color, Color):
            fgc = t.color_rgb(self.fg_color.r, self.fg_color.g, self.fg_color.b)
        self.__color_cache = f"{bgc}{fgc}"

    def __eq__(self, other):
        if isinstance(other, Sprixel):
            if (
                self.model == other.model
                and self.bg_color == other.bg_color
                and self.fg_color == other.fg_color
            ):
                return True
            else:
                return False
        return NotImplemented

    def __ne__(self, other):
        if (
            self.model != other.model
            or self.bg_color != other.bg_color
            or self.fg_color != other.fg_color
        ):
            return True
        else:
            return False

    def __mul__(self, other):
        if isinstance(other, int):
            # return [copy.deepcopy(self)] * other
            return [self.copy()] * other
        raise NotImplementedError

    def copy(self):
        """
        Returns a (deep) copy of the sprixel.

        .. versionadded:: 1.3.0

        """
        return Sprixel(
            self.model,
            None if self.bg_color is None else self.bg_color.copy(),
            None if self.fg_color is None else self.fg_color.copy(),
            self.is_bg_transparent,
        )

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        """Render the sprixel from the display buffer to the frame buffer.

        .. versionadded:: 1.3.0

        This method is automatically called by :func:`pygamelib.engine.Screen.render`.

        :param buffer: A screen buffer to render the item into.
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
        buffer[row][column] = self.__repr__()

    @staticmethod
    def from_ansi(string, model="▄"):
        """Takes an ANSI string, parse it and return a Sprixel.

        :param string: The ANSI string to parse.
        :type string: str
        :param model: The character used to represent the sprixel in the ANSI sequence.
            Default is "▄"
        :type model: str

        Example::

            new_sprixel = Sprixel.from_ansi(
                "\\x1b[48;2;139;22;19m\\x1b[38;2;160;26;23m▄\\x1b[0m"
            )

        .. warning:: This has mainly be tested with ANSI string generated by climage.
           If you find any issue, please
           `report it <https://github.com/pygamelib/pygamelib/issues>`_
        """
        new_sprixel = Sprixel()
        if "[48;" in string and "[38;" in string and model in string:
            (colors, end) = string.split(model)
            new_sprixel.model = model
            for e in colors.split("m"):
                if "[48;" in e:
                    # new_sprixel.bg_color = f"{e}m"
                    new_sprixel.bg_color = Color.from_ansi(f"{e}m")
                elif "[38;" in e:
                    # new_sprixel.fg_color = f"{e}m"
                    new_sprixel.fg_color = Color.from_ansi(f"{e}m")
        elif "[38;" in string and model in string:
            (colors, end) = string.split(model)
            new_sprixel.model = model
            for e in colors.split("m"):
                if "[38;" in e:
                    # new_sprixel.fg_color = f"{e}m"
                    new_sprixel.fg_color = Color.from_ansi(f"{e}m")
        elif "[48;" in string and model in string:
            (colors, end) = string.split(model)
            new_sprixel.model = model
            for e in colors.split("m"):
                if "[48;" in e:
                    # new_sprixel.bg_color = f"{e}m"
                    new_sprixel.bg_color = Color.from_ansi(f"{e}m")
        if new_sprixel.bg_color is not None:
            new_sprixel.is_bg_transparent = False
        return new_sprixel

    @property
    def length(self):
        """Return the true length of the model.

        .. versionadded:: 1.3.0

        With UTF8 and emojis the length of a string as returned by python's
        :func:`len()` function is often very wrong.
        For example, the len("\\x1b[48;2;139;22;19m\\x1b[38;2;160;26;23m▄\\x1b[0m")
        returns 39 when it should return 1.

        This method returns the actual printing/display size of the sprixel's model.

        .. Note:: This is a read only value. It is automatically updated when the model
           is changed.

        Example::

            if sprix.length > 2:
                print(
                    f"Warning: that sprixel {sprix} will break the rest of the "
                    "board's alignement"
                    )
        """
        return self.__length

    @property
    def model(self):
        """A property to get/set the model of the Sprixel.

        :param value: The new model
        :type value: str

        When the model is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.gfx.core.Sprixel.model:changed` event. The new
        model is passed as the `value` parameter.

        Example::

            # Get the sprixel's model
            sprix.model
            # Set the sprixel's model to "@"
            sprix.model = "@"
        """
        return self.__model

    @model.setter
    def model(self, value):
        if type(value) is str:
            self.__model = value
            self.__length = base.Console.instance().length(self.__model)
            self.notify(self, "pygamelib.gfx.core.Sprixel.model:changed", self.__model)
        else:
            raise base.PglInvalidTypeException(
                f"A Sprixel.model must be a string. {value} is not a string."
            )

    @property
    def bg_color(self):
        """A property to get/set the background color of the Sprixel.

        :param value: The new color
        :type value: :class:`Color`

        When the bg_color is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.gfx.core.Sprixel.bg_color:changed` event. The new
        bg_color is passed as the `value` parameter.

        Example::

            # Access the sprixel's color
            sprix.bg_color
            # Set the sprixel's background color to some blue
            sprix.bg_color = Color(0,128,255)
        """
        return self.__bg_color

    @bg_color.setter
    def bg_color(self, value):
        if isinstance(value, Color) or value is None:
            self.__bg_color = value
            self.__build_color_cache()
            self.notify(self, "pygamelib.gfx.core.Sprixel.bg_color:changed", value)
        else:
            raise base.PglInvalidTypeException(
                "A Sprixel.bg_color must be a Color object."
            )

    @property
    def fg_color(self):
        """A property to get/set the foreground color of the Sprixel.

        :param value: The new color
        :type value: :class:`Color`

        When the fg_color is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.gfx.core.Sprixel.fg_color:changed` event. The new
        fg_color is passed as the `value` parameter.

        Example::

            # Access the sprixel's color
            sprix.fg_color
            # Set the sprixel's foreground color to some green
            sprix.fg_color = Color(0,255,128)
        """
        return self.__fg_color

    @fg_color.setter
    def fg_color(self, value):
        if isinstance(value, Color) or value is None:
            self.__fg_color = value
            self.__build_color_cache()
            self.notify(self, "pygamelib.gfx.core.Sprixel.fg_color:changed", value)
        else:
            raise base.PglInvalidTypeException(
                "A Sprixel.fg_color must be a Color object."
            )

    def serialize(self):
        """Serialize a Sprixel into a dictionary.

        .. versionadded:: 1.3.0

        :returns: The class as a  dictionary
        :rtype: dict

        Example::

            json.dump( sprixel.serialize() )
        """
        return {
            "model": self.model,
            "bg_color": self.bg_color and self.bg_color.serialize() or None,
            "fg_color": self.fg_color and self.fg_color.serialize() or None,
            "is_bg_transparent": self.is_bg_transparent,
        }

    @classmethod
    def load(cls, data):
        """
        Create a new Sprixel object based on serialized data.

        .. versionadded:: 1.3.0

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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
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
        This class method returns a sprixel that is the equivalent of
        pygamelib.assets.graphics.YELLOW_SQUARE.
        The difference is that YELLOW_SQUARE is a string and this one is a Sprixel that
        can be manipulated more easily.

        .. Note:: Yellow is often rendered as brown.

        Example::

            sprixel = Sprixel.yellow_square()
        """
        return cls("  ", Color(255, 255, 0))


class Sprite(base.PglBaseObject):
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
        default_sprixel=None,
        parent=None,
        size=[2, 2],
        name=None,
    ):
        super().__init__()
        self.size = size
        self.parent = parent
        self.name = name
        if default_sprixel is None:
            self.default_sprixel = Sprixel()
        else:
            self.default_sprixel = default_sprixel
        self.row_offset = 0
        self.column_offset = 0
        # Double linking here, GC will hate it...
        self._initial_text_object = None
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

    def copy(self):
        """
        Returns a (deep) copy of the sprite.

        .. versionadded:: 1.3.0

        """
        tmp_sprixels = []
        for row in range(0, self.size[1]):
            tmp = []
            for column in range(0, self.size[0]):
                tmp.append(self.sprixel(row, column).copy())
            tmp_sprixels.append(tmp)
        return Sprite(
            tmp_sprixels, self.default_sprixel.copy(), self.parent, name=self.name
        )

    def sprixel(self, row=0, column=None):
        """Return a sprixel at a specific position within the sprite.

        If the column is set to None, the whole row is returned.

        :param row: The row to access within the sprite.
        :type row: int
        :param column: The column to access within the sprite.
        :type column: int
        :return: :class:`Sprixel`

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

    def set_sprixel(self, row, column, value):
        """
        Set a specific sprixel in the sprite to the given value.

        :param row: The row of the sprite (WARNING: internal sprite coordinates)
        :type row: int
        :param column: The column of the sprite (same warning)
        :type column: int
        :param value: The sprixel to set at [row, column]
        :type value: :class:`Sprixel`

        When a sprixel is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.gfx.core.Sprite.sprixel:changed` event. A
        structure is passed as the `value` parameter. This structure has 3 members: row,
        column and sprixel.

        Example::

            my_sprite.set_sprixel(1, 2, Sprixel("#",fg_color=green))
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
        if not isinstance(value, Sprixel):
            raise base.PglInvalidTypeException(
                "Sprite.set_sprixel(row, column, val) val needs to be a Sprixel"
            )
        self._sprixels[row][column] = value
        self.notify(
            self,
            "pygamelib.gfx.core.Sprite.sprixel:changed",
            {"row": row, "column": column, "sprixel": value},
        )

    @classmethod
    def from_text(cls, text_object):
        """
        Create a Sprite from a :class:`~pygamelib.base.Text` object.

        :param text_object: A text object to transform into Sprite.
        :type text_object: :class:`~pygamelib.base.Text`

        Example::

            # The Text object allow for easy manipulation of text
            village_name = base.Text('Khukdale',fg_red, bg_green)
            # It can be converted into a Sprite to be displayed on the Board
            village_sign = board_items.Tile(sprite=Sprite.from_text(village_name))
            # And can be used as formatted text
            notifications.push( f'You enter the dreaded village of {village_name}' )
        """
        sprixels = []
        # TODO: why is it not style = text_object.style ?
        # style = ""
        # NOTE: I leave this TODO because I'm not sure exactly why it was put here and
        #       not changed immediately. There may be side effects.
        style = text_object.style
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
        obj = cls(sprixels=sprixels)
        text_object._sprite_data = text_object.text
        obj._initial_text_object = text_object
        return obj

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
            zero = sprite_file.tell()
            line = sprite_file.readline()
            parser_mode = 0
            parser_sep = ""
            if "▄" in line:
                parser_mode = 1
                parser_sep = "▄"
            elif "  " in line:
                parser_mode = 2
                parser_sep = "  "
            if parser_mode < 1 or parser_mode > 2:
                raise base.PglException(
                    "sprite_file_format_not_supported",
                    f"The file {filename} is not a valid sprite file.",
                )
            sprite_file.seek(zero)
            sprixels_list = []
            height = 0
            max_width = 0
            while True:
                line = sprite_file.readline()
                if not line:
                    break
                width = 0
                sprixels_list.append([])
                for s in line.rstrip().split(parser_sep):
                    if s != "\x1b[0m":
                        sprixels_list[height].append(
                            Sprixel.from_ansi(f"{s}{parser_sep}\x1b[0m", parser_sep)
                        )
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

        .. versionadded:: 1.3.0

        :param state: a boolean to enable or disable background transparency
        :type name: bool

        When the transparency is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.gfx.core.Sprite.transparency:changed` event. The
        new transparency state is passed as the `value` parameter.

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
        self.notify(self, "pygamelib.gfx.core.Sprite.transparency:changed", state)

    def serialize(self):
        """Serialize a Sprite into a dictionary.

        .. versionadded:: 1.3.0

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

    @property
    def width(self):
        """
        Property that returns the width of the Sprite.

        .. versionadded:: 1.3.0

        Contrary to Sprite.size[0], this property *always* calls Sprite.calculate_size()
        before returning the width.
        """
        self.calculate_size()
        return self.size[0]

    @property
    def height(self):
        """
        Property that returns the height of the Sprite.

        .. versionadded:: 1.3.0

        Contrary to Sprite.size[1], this property *always* calls Sprite.calculate_size()
        before returning the height.
        """
        self.calculate_size()
        return self.size[1]

    @classmethod
    def load(cls, data):
        """
        Create a new Sprite object based on serialized data.

        .. versionadded:: 1.3.0

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

    def scale(self, ratio=1.0):
        """Scale a sprite up and down using the nearest neighbor algorithm.

        .. versionadded:: 1.3.0

        :param ratio: The scaling ration.
        :type ratio: float
        :return: An upscaled/downscaled sprite.
        :rtype: :class:`Sprite`

        .. Note:: The sprites generated with pgl-converter.py don't scale well yet if
           the --unicode flag is active

        Example::

            bigger_sprite = original_sprite.scale(2)
        """
        if ratio == 1.0:
            return self
        elif ratio == 0.0:
            return
        # First let's set some var. o_ prefix original Sprite value n_ the new ones
        o_height = self.height
        o_width = self.width
        n_height = int(ratio * self.height)
        n_width = int(ratio * self.width)
        new_sprite = Sprite(
            size=[n_width, n_height],
            default_sprixel=self.default_sprixel,
            parent=self.parent,
        )
        # Now let's apply a nearest neighbor algorithm
        column_ratio = int((o_width << 16) / n_width) + 1
        row_ratio = int((o_height << 16) / n_height) + 1
        for i in range(0, n_height):
            for j in range(0, n_width):
                c2 = (j * column_ratio) >> 16
                r2 = (i * row_ratio) >> 16
                new_sprite.set_sprixel(i, j, self.sprixel(r2, c2))
        return new_sprite

    def tint(self, color: Color, ratio: float = 0.5):
        """Tint a copy of the sprite with the color.

        .. versionadded:: 1.3.0

        This method creates a copy of the sprite and tint all its sprixels with the
        color at the specified ratio.
        It then returns the new sprite. **The original sprite is NOT modified**.

        :param color: The tint color.
        :type color: :class:`Color`
        :param ratio: The tint ration between 0.0 and 1.0 (default: 0.5)
        :type ratio: float
        :returns: :class:`Sprite`

        Example::

            player_sprites = core.SpriteCollection.load_json_file("gfx/player.spr")
            player_sprites["sick"] = player_sprites["normal"].tint(
                                        core.Color(0, 255, 0), 0.3
                                    )
        """
        if ratio < 0.0 or ratio > 1.0:
            raise base.PglInvalidTypeException(
                "Sprite.tint(color, ratio): ratio must be a float between 0 and 1 "
                f"(rate={ratio})"
            )
        new_sprite = Sprite(
            size=self.size,
            sprixels=None,
            default_sprixel=self.default_sprixel,
            parent=self.parent,
        )
        for row in range(0, self.size[1]):
            for col in range(0, self.size[0]):
                # new_sprix: Sprixel = copy.deepcopy(self._sprixels[row][col])
                new_sprix: Sprixel = self._sprixels[row][col].copy()
                if new_sprix.bg_color is not None:
                    new_sprix.bg_color = new_sprix.bg_color.blend(color, ratio)
                if new_sprix.fg_color is not None:
                    new_sprix.fg_color = new_sprix.fg_color.blend(color, ratio)
                new_sprite.set_sprixel(row, col, new_sprix)
        return new_sprite

    def modulate(self, color: Color, ratio: float = 0.5):
        """Modulate the sprite colors with the color in parameters.

        .. versionadded:: 1.3.0

        This method tint all the sprixels of the sprite with the color at the specified
        ratio.
        **The original sprite IS modified**.

        If you want to keep the original sprite intact consider using :py:meth:`tint()`.

        :param color: The modulation color.
        :type color: :class:`Color`
        :param ratio: The modulation ratio between 0.0 and 1.0 (default: 0.5)
        :type ratio: float
        :returns: None

        When this method is called, the observers are notified of the change
        with the :boldblue:`pygamelib.core.Sprite.color:modulated` event. No arguments
        are passed along this event.

        Example::

            player_sprites = core.SpriteCollection.load_json_file("gfx/player.spr")
            # After that, the sprite is quite not "normal" anymore...
            player_sprites["normal"].modulate(core.Color(0, 255, 0), 0.3)
        """
        if ratio < 0.0 or ratio > 1.0:
            raise base.PglInvalidTypeException(
                "Sprite.tint(color, ratio): ratio must be a float between 0 and 1 "
                f"(rate={ratio})"
            )
        for row in range(0, self.size[1]):
            for col in range(0, self.size[0]):
                sprix: Sprixel = self._sprixels[row][col]
                if sprix.bg_color is not None:
                    sprix.bg_color = sprix.bg_color.blend(color, ratio)
                if sprix.fg_color is not None:
                    sprix.fg_color = sprix.fg_color.blend(color, ratio)
        self.notify(self, "pygamelib.core.Sprite.color:modulated")

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        """Render the sprite from the display buffer to the frame buffer.

        .. versionadded:: 1.3.0

        This method is automatically called by :func:`pygamelib.engine.Screen.render`.

        :param buffer: A screen buffer to render the item into.
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
        # NOTE: This entire non-sense is not required anymore
        # Check if the text has changed to update the sprite...
        # I'm not so sure about all this update thing...
        # if (
        #     self._initial_text_object is not None
        #     and
        # self._initial_text_object._sprite_data != self._initial_text_object.text
        # ):
        #     i = Sprite.from_text(self._initial_text_object)
        #     self._sprixels = i._sprixels
        #     self._initial_text_object._sprite_data =
        # i._initial_text_object._sprite_data
        #     self.size = i.size
        #     # display_buffer[row][col] = i

        ro = self.row_offset
        co = self.column_offset
        # Attempt at optimization.
        null_sprixel = Sprixel()
        get_sprixel = self.sprixel
        for sr in range(row, min(self.size[1] + row, buffer_height)):
            for sc in range(column, min(self.size[0] + column, buffer_width)):
                sprix = get_sprixel(sr - row + ro, sc - column + co)
                # Need to check the empty/null sprixel in the sprite
                # because for the sprite we just skip and leave the
                # sprixel that is behind but when it comes to screen we
                # cannot leave a blank cell.
                if sprix == null_sprixel:
                    continue
                # TODO: If the Sprite has sprixels with length > 1 this
                # is going to be a mess.
                # buffer[sr][sc] = sprix.__repr__()
                buffer[sr][sc] = sprix
                for c in range(sc + 1, sc + sprix.length):
                    buffer[sr][c] = null_sprixel


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

    def __init__(self, data=None):
        if data is None:
            data = dict()
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

    def rename(self, old_key, new_key):
        """Rename a key in the collection.

        This methods also takes care of renaming the Sprite associated with the old key
        name.

        :param old_key: The key to rename
        :type old_key: str
        :param new_key: The new key name
        :type new_key: str

        Example::

            my_collection.rename('panda', 'panda walk 01')
        """
        self.data[new_key] = self.data.pop(old_key)
        self.data[new_key].name = new_key


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
    :param frames: an array of "frames" (string, sprixel, sprite) or a sprite collection
    :type frames: array[str| :class:`Sprixel` | :class:`Sprite` ] |
        :class:`SpriteCollection`
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

    .. Important:: When a :class:`SpriteCollection` is used as the *frames* parameter
       the sprites' names are ordered so the frames are displayed in correct order. This
       means that 'walk_1' is going to be displayed before 'walk_2'. Otherwise
       SpriteCollection is un-ordered.

    Example ::

        def redraw_screen(game_object):
            game_object.clear_screen()
            game_object.display_board()

        item = BoardItem(model=Sprite.ALIEN, name='Friendly Alien')
        # By default BoardItem does not have any animation, we have to
        # explicitly create one
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
        self.state = State.RUNNING
        self.display_time = display_time
        self.auto_replay = auto_replay
        self.parent = None
        if frames is None:
            frames = []
        elif isinstance(frames, SpriteCollection):
            nf = []
            for sn in sorted(frames.keys()):
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

    def serialize(self):
        """
        Serialize the Animation object.

        The `refresh_screen` callback function is not serialized. Neither is the parent.

        :return: A dictionary containing the Animation object's data.
        :rtype: dict
        """
        ret_data = {}
        ret_data["display_time"] = self.display_time
        ret_data["auto_replay"] = self.auto_replay
        if isinstance(self.frames[0], Sprite):
            ret_data["frame_type"] = "sprite"
        elif isinstance(self.frames[0], Sprixel):
            ret_data["frame_type"] = "sprixel"
        else:
            ret_data["frame_type"] = "str"
        ret_data["frames"] = []
        for frame in self.frames:
            if isinstance(frame, Sprite) or isinstance(frame, Sprixel):
                ret_data["frames"].append(frame.serialize())
            else:
                ret_data["frames"].append(frame)
        ret_data["_frame_index"] = self._frame_index
        ret_data["_initial_index"] = self._initial_index
        return ret_data

    @classmethod
    def load(cls, data):
        """
        Load a serialized Animation object.

        :param data: The serialized Animation object.
        :type data: dict
        :return: The loaded Animation object.
        :rtype: :class:`Animation`
        """
        # Start by constructing a default Animation object (because we have some
        # specific cases to handle)
        obj = cls()
        # Unrelated note: all this function's code after this line has been written by
        # Github's Copilot... This is really a time saver.
        obj.display_time = data["display_time"]
        obj.auto_replay = data["auto_replay"]
        if data["frame_type"] == "sprite":
            obj.frames = []
            for frame in data["frames"]:
                obj.frames.append(Sprite.load(frame))
        elif data["frame_type"] == "sprixel":
            obj.frames = []
            for frame in data["frames"]:
                obj.frames.append(Sprixel.load(frame))
        else:
            obj.frames = data["frames"]
        obj._frame_index = data["_frame_index"]
        obj._initial_index = data["_initial_index"]
        return obj

    @property
    def dtanimate(self):
        """
        The time elapsed since the last frame was displayed.
        """
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
        """Set the animation state to State.RUNNING.

        If the animation state is not State.RUNNING, animation's next_frame()
        function return the last frame returned.

        Example::

            item.animation.start()
        """
        self.state = State.RUNNING

    def pause(self):
        """Set the animation state to PAUSED.

        Example::

            item.animation.pause()
        """
        self.state = State.PAUSED

    def stop(self):
        """Set the animation state to STOPPED.

        Example::

            item.animation.stop()
        """
        self.state = State.STOPPED

    def add_frame(self, frame):
        """Add a frame to the animation.

        The frame has to be a string (that includes sprites from the Sprite
        module and squares from the Utils module).

        Raise an exception if frame is not a string.

        :param frame: The frame to add to the animation.
        :type frame: str|:class:`Sprite`|:class:`Sprixel`
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

        That method takes care of automatically resetting the animation if the
        last frame is reached if the state is State.RUNNING.

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
        if not pgl_isinstance(self.parent, "pygamelib.board_items.BoardItem"):
            raise base.PglInvalidTypeException(
                "The parent needs to be a sub class of BoardItem."
            )
        if self.state == State.STOPPED:
            return
        elif self.state == State.RUNNING:
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
        if self.state == State.PAUSED or self.state == State.STOPPED:
            return False
        if self.refresh_screen is None or not callable(self.refresh_screen):
            raise base.PglInvalidTypeException(
                "The refresh_screen parameter needs to be a callback "
                "function reference."
            )
        if not pgl_isinstance(self.parent, "pygamelib.board_items.BoardItem"):
            raise base.PglInvalidTypeException(
                "The parent needs to be a sub class of BoardItem."
            )
        self.reset()
        previous_time = time.time()
        ctrl = 0
        while ctrl < len(self.frames):
            if self.dtanimate >= self.display_time:
                # Dirty but that's a current limitation: to really update a complex item
                # on the board, we need to either move or replace an item after
                # updating the sprite. This is mostly for sprites that have null items
                # but we don't want to let any one slip. An item on a Screen is not
                # concerned by that.
                # Also: this is convoluted...
                if (
                    pgl_isinstance(
                        self.parent, "pygamelib.board_items.BoardComplexItem"
                    )
                    and self.parent.parent is not None
                    and (
                        pgl_isinstance(self.parent.parent, "pygamelib.engine.Board")
                        or pgl_isinstance(self.parent.parent, "pygamelib.engine.Game")
                    )
                ):
                    b = None
                    if pgl_isinstance(self.parent.parent, "pygamelib.engine.Board"):
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


# Font is a class
# Font load a font data and allow an unified access to it
# Font data consist of a sprite file and a json file that describes the font
# FONT_NAME/glyphs.spr contains the sprites and FONT_NAME/config.json contains the
# information.
# Ideally a font can be used by base.Text to render text.
# Fonts API:
#    * load('FONT_NAME') -> Load the font and return None
#    * glyph('GLYPH_NAME',FG COLOR,BG COLOR) -> Access and return the glyph as a Sprite.
#
# config.json looks like that:
# {
#     "scalable": false,
#     "monospace": true,
#     "tintable": true,
#     "fg_color": {
#         "red": 255,
#         "green": 255,
#         "blue": 255
#     },
#     "bg_color": null,
#     "glyphs_map": {
#         "a": "A",
#         "b": "B",
#         "c": "C",
#         "d": "D",
#         "e": "E",
#         "f": "F",
#         "g": "G",
#         "h": "H",
#         "i": "I",
#         "j": "J",
#         "k": "K",
#         "l": "L",
#         "m": "M",
#         "n": "N",
#         "o": "O",
#         "p": "P",
#         "q": "Q",
#         "r": "R",
#         "s": "S",
#         "t": "T",
#         "u": "U",
#         "v": "V",
#         "w": "W",
#         "x": "X",
#         "y": "Y",
#         "z": "Z"
#     }
# }
#
# scalable is a boolean. If true it means that the fond is made of scalable elements and
# look the same if the Sprite.scale() method is used.
#
# monospace is telling the user if the font is size consistent (all glyph have the same
# dimension)
#
# tintable hints the ability to tint the sprite with a color or not.
#
# fg_color contains the font foreground color.
#
# bg_color contains the font background color.
#
# This is highly recommended to use white as foreground and None as background.
# Since fonts can be drawn with multiple technics and looks can be achieved by using
# Sprixels background and foreground colors, Font cannot determine what is foreground
# and what is background. Therefor if tintable is true, it will compare colors and
# replace the corresponding color. Colored glyphs are cached.
#
# glyph_map is optional but is used to map any glyph to another glyph. The format is:
# "<glyph that IS NOT in glyph.spr>" : "<glyph the IS in glyph.spr>"
#              key                                value
# The value MUST BE present in glyph.spr


class Font:
    """
    .. versionadded:: 1.3.0

    The Font class allow to load and manipulate a pygamelib "font".
    A font consist of a sprite collection and a configuration file.

    If you want to create your own font, please have a look at the font creation
    tutorial.

    In general the Font class is not used directly but passed to a
    :class:`~pygamelib.base.Text` object. The text is then rendered using the font.

    For performance consideration, it is advised to load the font once and to reuse the
    object in multiple text objects.

    Glyphs are cached (particularly if you change the colors) so it is always beneficial
    to reuse a font object.

    Example::

        myfont = Font("8bits")
        # If you print() mytext, it will use the terminal font and print in cyan.
        # But if you Sreen.place() it, it will render using the 8bits sprite font.
        mytext = Text("Here's a cool text", fg_color = Color(0,255,255), font=myfont)

    """

    def __init__(self, font_name: str = None, search_directories: list = None) -> None:
        """

        :param font_name: The name of the font to load upon object construction.
        :type font_name: str
        :param search_directories: A list of directories to search for the font. The
           items of the list are strings representing a relative or absolute path.
        :type search_directories: list

        .. important:: The search directories **must** contain a "fonts" directory, that
           itself contains the font at the correct format.

        .. Note::  Version 1.3.0 comes with a pygamelib specific font called 8bits. It
           also comes with a handfull of fonts imported from the figlet fonts.
           Please go to `http://www.figlet.org/ <http://www.figlet.org/>`_ for more
           information.

           The conversion script will be made available in the Pygamelib Github
           organization (`https://github.com/pygamelib <https://github.com/pygamelib>`_
           ).

        Example::

            myfont = Font("8bits")
        """
        # TODO: Add a parameter to specify a list of directories to look into.
        super().__init__()
        self.__glyphs_cache = {}
        self.__config = None
        self.__sprite_collection = None
        self.__name = None
        self.__search_directories = set()
        self.__search_directories.add(importlib_resources.files(assets))
        if search_directories is not None:
            for ds in search_directories:
                if isinstance(ds, Path):
                    self.__search_directories.add(ds)
                else:
                    self.__search_directories.add(Path(ds))
        if font_name is not None:
            self.load(font_name)

    def load(self, font_name: str = None) -> None:
        """
        Load a font by name. Once the font is loaded glyphs can be accessed through the
        :func:`~pygamelib.gfx.core.Font.glyph` method.

        This method is automatically called is the Font constructor is called with a
        font name.

        :param font_name: The name of the font to load upon object construction.
        :type font_name: str

        Example::

            # The 2 following examples do exactly the same thing.
            # Example 1: instantiate and load
            myfont = Font()
            myfont.load("8bits")
            # Example 2: load from instantiation
            myfont2 = Font("8bits")
            # At that point myfont and myfont2 are exactly the same (and there is no
            # good justification to instantiate or load the font twice).
        """
        # # TODO: rework load to use the array of directories. DONE
        # glyphs_path = importlib_resources.files(assets).joinpath(
        #     "fonts", font_name, "glyphs.spr"
        # )
        # config_path = importlib_resources.files(assets).joinpath(
        #     "fonts", font_name, "config.json"
        # )
        glyphs_path = config_path = None
        for dir in self.__search_directories:
            glyphs_path = dir.joinpath("fonts", font_name, "glyphs.spr")
            config_path = dir.joinpath("fonts", font_name, "config.json")
            if glyphs_path.exists() and config_path.exists():
                break
        # This will throw a FileNotFoundError if the font is not present.
        self.__sprite_collection = SpriteCollection.load_json_file(glyphs_path)
        with open(config_path) as config_file:
            self.__config = json.load(config_file)
        self.__config["fg_color"] = Color.load(self.__config["fg_color"])
        self.__config["bg_color"] = Color.load(self.__config["bg_color"])
        self.__name = font_name
        if "glyphs_map" in self.__config.keys():
            for glyph in self.__config["glyphs_map"].keys():
                self.__sprite_collection[glyph] = self.__sprite_collection[
                    self.__config["glyphs_map"][glyph]
                ]

    @property
    def height(self) -> int:
        """
        Returns the height of the font as specified in the font config file.

        :rtype: int

        Example::

            screen.place(text, last_row + myfont.height, first_text_column)
        """
        return self.__config["height"]

    @property
    def scalable(self) -> bool:
        """
        Returns the scalability of the font as specified in the font config file.

        :rtype: bool
        """
        return self.__config["scalable"]

    @property
    def monospace(self) -> bool:
        """
        Returns if the font is monospace as specified in the font config file.

        :rtype: bool
        """
        return self.__config["monospace"]

    @property
    def colorable(self) -> bool:
        """
        Returns the "colorability" of the font as specified in the font config file.

        :rtype: bool
        """
        return self.__config["colorable"]

    @property
    def glyphs_map(self) -> dict:
        """
        Returns the glyph map of the font as specified in the font config file.

        :rtype: dict
        """
        return self.__config["glyphs_map"]

    @property
    def horizontal_spacing(self) -> int:
        """
        Returns the horizontal spacing recommended by the font (as specified in the font
        config file).

        As a user of the font class using the Font class to change the look of some
        text, you will rarely use that value directly (it is directly used by
        Text.render_to_buffer()).

        If your goal is to use the Font class to do glyph rendering as you see fit, use
        the horizontal spacing value to place each glyph relatively to the one on its
        left or right.

        :rtype: int

        """
        return self.__config["horizontal_spacing"]

    @property
    def vertical_spacing(self) -> int:
        """
        Returns the vertical spacing recommended by the font (as specified in the font
        config file).

        :rtype: int

        Example::

            screen.place(
                text,
                last_row + myfont.height() + myfont.vertical_spacing(),
                first_text_column
            )
        """
        return self.__config["vertical_spacing"]

    @property
    def name(self) -> str:
        """
        Return the name of the font. The name is the string that was used to load the
        font.

        Example::

            myfont = Font("8bits")
            if myfont.name() != "8bits":
                print("Something very wrong just occurred!")
        """
        return self.__name

    @staticmethod
    def __glyph_colors_to_string(
        glyph_name: str = None, fg_color: Color = None, bg_color: Color = None
    ) -> str:
        # Serialize a glyph and its colors as a string.
        serstr = glyph_name
        for c in (fg_color, bg_color):
            if c is None:
                serstr = f"{serstr}:{-1}:{-1}:{-1}"
            else:
                serstr = f"{serstr}:{c.r}:{c.g}:{c.b}"
        return serstr

    def glyph(
        self,
        glyph_name: str = None,
        fg_color: Color = None,
        bg_color: Color = None,
    ) -> Sprite:
        """
        This method take a glyph name in parameter and returns its representation as a
        :class:`~pygamelib.gfx.core.Sprite`.

        The glyph name is usually the name of a character (like "a") but it is not
        mandatory and can be anything. The default glyph (returned when no glyph matches
        the requested glyph) is called "default" for example.

        :param glyph_name: The glyph name
        :type glyph_name: str
        :returns: A glyphe as a :class:`Sprite`
        :rtype: :class:`Sprite`

        Example::

            myfont = Font("8bits")
            row = 5
            column = 10
            for letter in "this is a text":
                glyph = myfont.glyph(letter)
                screen.place(glyph, row, column)
                column += glyph.width + myfont.horizontal_spacing()

            # Please note that in real life you would just do this
            mytext = Text("this is a text", font=myfont)
            screen.place(mytext, row, column)
        """
        if self.__sprite_collection is None:
            return
        if glyph_name not in self.__sprite_collection.keys():
            glyph_name = "default"
        if fg_color is None and bg_color is None:
            return self.__sprite_collection[glyph_name]
        else:
            gcolstr = Font.__glyph_colors_to_string(glyph_name, fg_color, bg_color)
            if gcolstr in self.__glyphs_cache.keys():
                return self.__glyphs_cache[gcolstr]
            else:
                # new_sprite = copy.deepcopy(self.__sprite_collection[glyph_name])
                new_sprite = self.__sprite_collection[glyph_name].copy()
                sprite_sprixel = new_sprite.sprixel
                cfg = self.__config
                for r in range(new_sprite.height):
                    for c in range(new_sprite.width):
                        if sprite_sprixel(r, c).fg_color == cfg["fg_color"]:
                            sprite_sprixel(r, c).fg_color = fg_color
                        elif sprite_sprixel(r, c).fg_color == cfg["bg_color"]:
                            sprite_sprixel(r, c).fg_color = bg_color
                        if sprite_sprixel(r, c).bg_color == cfg["fg_color"]:
                            sprite_sprixel(r, c).bg_color = fg_color
                        elif sprite_sprixel(r, c).bg_color == cfg["bg_color"]:
                            sprite_sprixel(r, c).bg_color = bg_color
                self.__glyphs_cache[gcolstr] = new_sprite
                return new_sprite
