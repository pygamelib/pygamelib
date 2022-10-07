__docformat__ = "restructuredtext"
"""
The base module is a collection of base objects that are used by the entire library,
from Math module to specific exceptions.

This module regroup all the specific exceptions of the library.
The idea behind most exceptions is to provide more context and info that the standard
exceptions.

.. autosummary::
   :toctree: .

   pygamelib.base.PglBaseObject
   pygamelib.base.Console
   pygamelib.base.Math
   pygamelib.base.PglException
   pygamelib.base.PglInvalidLevelException
   pygamelib.base.PglInvalidTypeException
   pygamelib.base.PglInventoryException
   pygamelib.base.PglObjectIsNotMovableException
   pygamelib.base.PglOutOfBoardBoundException
   pygamelib.base.Vector2D
   pygamelib.base.Text
"""
from pygamelib import constants
from pygamelib.functions import pgl_isinstance
import math
from colorama import Fore, Back, Style, init
from blessed import Terminal

# import time
from typing import Any

# Initialize terminal colors for colorama.
init()


class PglBaseObject(object):
    """The base object of most of the pygamelib's classes.

    .. versionadded:: 1.3.0

    The PglBaseObject has 2 goals:

     * Store the object's screen position.
     * Implements a modified observer design pattern.

    It is "modified" as it acts both as the observer and the client. The idea behind it
    is that any object can observe and be observed by any other objects.

    The base logic of the pattern is already implemented and probably does not require
    re-implementation on the child object.
    However, the :func:`~pygamelib.base.PglBaseObject.handle_notification()` method
    needs to be implemented in each client. The actual processing of the notification is
    indeed specific to each object.

    Storing the screen position is particularly useful for
    :class:`~pygamelib.board_items.BoardItem` subclasses as they only know their
    position relative to the :class:`~pygamelib.engine.Board` but might need to know
    their absolute screen coordinates.

    This is a lightweight solution to that issue. It is not foolproof however! The
    screen_row and screen_column attributes are not wrapped properties and can be
    modified to mess up things. It shouldn't be done lightly. You have been warned!
    """

    def __init__(self) -> None:
        """
        Like the object class, this class constructor takes no parameter.
        """
        super().__init__()
        self._observers = []
        self._screen_row = -1
        """The absolute row (or y) coordinate on the screen."""
        self._screen_column = -1
        """The absolute column (or x) coordinate on the screen."""
        # self._last_updated = time.time()

    @property
    def screen_row(self) -> int:
        """
        A property to get/set the screen row.

        :param value: the screen row
        :type value: int
        :rtype: int
        """
        return self._screen_row

    @screen_row.setter
    def screen_row(self, value: int) -> None:
        if type(value) is int:
            self._screen_row = value

    @property
    def screen_column(self) -> int:
        """
        A property to get/set the screen column.

        :param value: the screen column
        :type value: int
        :rtype: int
        """
        return self._screen_column

    @screen_column.setter
    def screen_column(self, value: int) -> None:
        if type(value) is int:
            self._screen_column = value

    def store_screen_position(self, row: int, column: int) -> bool:
        """Store the screen position of the object.

        This method is automatically called by Screen.place().

        :param row: The row (or y) coordinate.
        :type row: int
        :param column: The column (or x) coordinate.
        :type column: int

        Example::

            an_object.store_screen_coordinate(3,8)
        """
        if type(row) is int and type(column) is int:
            self.screen_column = column
            self.screen_row = row
            return True
        return False

    def notify(self, modifier=None, attribute: str = None, value: Any = None) -> None:

        """
        Notify all the observers that a change occurred.

        :param modifier: An optional parameter that identify the modifier object to
           exclude it from the notified objects.
        :type modifier: :class:`~pygamelib.base.PglBaseObject`
        :param attribute: An optional parameter that identify the attribute that has
           changed.
        :type attribute: str
        :param value: An optional parameter that identify the new value of the
           attribute.
        :type value: Any

        Example::

           # This example is silly, you would usually notify other objects from inside
           # an object that changes a value that's important for the observers.
           color = Color(255,200,125)
           color.attach(some_text_object)
           color.notify()
        """
        # Let's get an eventual modifier out of the list so we don't have to add an if
        # to the for loop.
        cache = None
        if modifier in self._observers:
            cache = self._observers.pop(self._observers.index(modifier))
        for observer in self._observers:
            observer.handle_notification(self, attribute, value)
        # Restore the cached object
        if cache is not None:
            self._observers.append(cache)

    def attach(self, observer):

        """
        Attach an observer to this instance. It means that until it is detached, it will
        be notified every time that a notification is issued (usually on changes).

        An object cannot add itself to the list of observers (to avoid infinite
        recursions).

        :param observer: An observer to attach to this object.
        :type observer: :class:`~pygamelib.base.PglBaseObject`

        :returns: True or False depending on the success of the operation.
        :rtype: bool

        Example::

            myboard = Board()
            screen = Game.instance().screen
            # screen will be notified of all changes in myboard
            myboard.attach(screen)

        """
        if observer == self:
            return False
        if observer not in self._observers:
            self._observers.append(observer)
            return True

    def detach(self, observer):

        """
        Detach an observer from this instance.
        If observer is not in the list this returns False.

        :param observer: An observer to detach from this object.
        :type observer: :class:`~pygamelib.base.PglBaseObject`

        :returns: True or False depending on the success of the operation.
        :rtype: bool

        Example::

            # screen will no longer be notified of the changes in myboard.
            myboard.detach(screen)
        """

        try:
            self._observers.remove(observer)
            return True
        except ValueError:
            return False

    def handle_notification(self, subject, attribute=None, value=None):
        """
        A virtual method that needs to be implemented by the observer.
        By default it does nothing but each observer needs to implement it if something
        needs to be done when notified.

        This method always receive the notifying object as first parameter. The 2 other
        parameters are optional and can be None.

        You can use the attribute and value as you see fit. You are free to consider
        attribute as an event and value as the event's value.

        :param subject: The object that has changed.
        :type subject: :class:`~pygamelib.base.PglBaseObject`
        :param attribute: The attribute that has changed, it is usually a "FQDN style"
           string. This can be None.
        :type attribute: str
        :param value: The new value of the attribute. This can be None.
        :type value: Any
        """
        pass


class Console:
    __instance = None

    @classmethod
    def instance(cls):
        """Returns the instance of the blessed.Terminal object.

        .. versionadded:: 1.3.0

        The pygamelib extensively use the Terminal object from the blessed module.
        However we find ourselves in need of a Terminal instance a lot, so to help with
        memory and execution time we just encapsulate the Terminal object in a singleton
        so any object can use it without instantiating it many times (and messing up
        with the contexts).

        :return: Instance of blessed.Terminal object

        Example::

           term = Console.instance()

        """
        if cls.__instance is None:
            cls.__instance = Terminal()
        return cls.__instance


class Text(PglBaseObject):
    """
    An object to manipulate and display text in multiple contexts.

    .. versionadded:: 1.2.0

    The Text class is a collection of text formatting and display static methods.

    You can either instantiate an object or use the static methods.

    The Text object allow for easy text manipulation through its collection of
    independent attributes. They help to set the text, its style and the foreground and
    background colors.

    The Text object can be converted to a :class:`~pygamelib.gfx.core.Sprite` through
    the Sprite.from_text() method. This is particularly useful to the place text on the
    game :class:`~pygamelib.engine.Board`.
    """

    def __init__(self, text="", fg_color=None, bg_color=None, style="", font=None):
        """
        :param text: The text to manipulate
        :type text: str
        :param fg_color: The foreground color for the text.
        :type fg_color: :class:`~pygamelib.gfx.core.Color`
        :param bg_color: The background color for the text.
        :type bg_color: :class:`~pygamelib.gfx.core.Color`
        :param style: The style for the text.
        :type style: str
        :param font: The font in which the text is going to be displayed (only works
           when using Screen.place() and Screen.update())
        :type font: :class:`~pygamelib.gfx.core.Font`
        """
        super().__init__()
        self.__text = ""
        self.__bg_color = None
        self.__fg_color = None
        self.__fgcc = ""
        self.__bgcc = ""
        self.__length = 0
        self.__font = None
        if type(text) is str:
            self.__text = text
            self.__length = self.__length = Console.instance().length(self.__text)
        if fg_color is None or pgl_isinstance(fg_color, "pygamelib.gfx.core.Color"):
            self.__fg_color = fg_color
            if fg_color is not None:
                fg_color.attach(self)
        else:
            raise PglInvalidTypeException(
                "Text(text, bg_color, fg_color, style): fg_color needs to be a "
                "pygamelib.gfx.core.Color object."
            )
        if bg_color is None or pgl_isinstance(bg_color, "pygamelib.gfx.core.Color"):
            self.__bg_color = bg_color
            if bg_color is not None:
                bg_color.attach(self)
        else:
            raise PglInvalidTypeException(
                "Text(text, bg_color, fg_color, style): bg_color needs to be a "
                "pygamelib.gfx.core.Color object."
            )
        self.__build_color_cache()
        self.style = style
        """The style attribute sets the style of the text. It needs to be a str."""
        self.parent = None
        """This object's parent. It needs to be a
        :class:`~pygamelib.board_items.BoardItem`."""
        self._sprite_data = None
        self._item = None
        if font is not None:
            if pgl_isinstance(font, "pygamelib.gfx.core.Font"):
                self.__font = font
            else:
                raise PglInvalidTypeException(
                    "Text(): the font parameter needs to be a Font object."
                )

    def serialize(self):
        """Return a dictionary with all the attributes of this object.

        .. versionadded:: 1.3.0

        :return: A dictionary with all the attributes of this object.
        :rtype: dict
        """
        ret_data = dict()
        ret_data["object"] = str(self.__class__)
        if self.__bg_color is not None:
            ret_data["bg_color"] = self.__bg_color.serialize()
        else:
            ret_data["bg_color"] = None
        if self.__fg_color is not None:
            ret_data["fg_color"] = self.__fg_color.serialize()
        else:
            ret_data["fg_color"] = None
        if self.__font is not None:
            ret_data["font_name"] = self.__font.name
        else:
            ret_data["font_name"] = None
        if self.style is not None:
            ret_data["style"] = self.style
        else:
            ret_data["style"] = ""
        ret_data["text"] = self.__text
        return ret_data

    @classmethod
    def load(cls, data: dict = None):
        """Load data and create a new Text object out of it.

        .. versionadded:: 1.3.0

        :param data: Data to create a new actuator (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new Text object.
        :rtype: Text

        Example::

            title = base.Text.load( previous_title.serialize() )
        """
        font = None
        # For circle dependencies issue I have to eval the import only here.
        # Now: why exec() and eval()? Good question!
        exec("from pygamelib.gfx import core")
        color_class = eval("core.Color")
        if "font_name" in data.keys() and data["font_name"] is not None:
            font_class = eval("core.Font")
            font = font_class(data["font_name"])
        obj = cls(
            data["text"],
            color_class.load(data["fg_color"]),
            color_class.load(data["bg_color"]),
            data["style"],
            font,
        )
        return obj

    def handle_notification(self, target, attribute=None, value=None):
        if (
            attribute == "pygamelib.gfx.core.Color.r:changed"
            or attribute == "pygamelib.gfx.core.Color.g:changed"
            or attribute == "pygamelib.gfx.core.Color.b:changed"
        ):
            self.__build_color_cache()

    @property
    def text(self):
        """The text attribute. It needs to be a str.

        .. versionadded:: 1.3.0

        .. role:: boldblue

        When the text is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.base.Text.text:changed` event. The new text
        is passed as the `value` parameter.
        """
        return self.__text

    @text.setter
    def text(self, value):
        if type(value) is str:
            self.__text = value
        elif isinstance(value, Text):
            self.__text = value.text
        self.__length = self.__length = Console.instance().length(self.__text)
        self.notify(self, "pygamelib.base.Text.text:changed", self.__text)

    @property
    def bg_color(self):
        """The bg_color attribute sets the background color. It needs to be a
        :class:`~pygamelib.gfx.core.Color`.

        .. versionadded:: 1.3.0

        .. role:: boldblue

        When the background color is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.base.Text.bg_color:changed` event. The new color
        is passed as the `value` parameter.
        """
        return self.__bg_color

    @bg_color.setter
    def bg_color(self, value):
        if pgl_isinstance(value, "pygamelib.gfx.core.Color"):
            if self.__bg_color is not None:
                self.__bg_color.detach(self)
            self.__bg_color = value
            self.__bg_color.attach(self)
            self.notify(self, "pygamelib.base.Text.bg_color:changed", value)
        elif value is None:
            if self.__bg_color is not None:
                self.__bg_color.detach(self)
            self.__bg_color = value
            self.notify(self, "pygamelib.base.Text.bg_color:changed", value)
            self.__bgcc = Back.RESET
        else:
            raise PglInvalidTypeException(
                "Text.bg_color can only be a pygamelib.gfx.core.Color object."
            )
        self.__build_color_cache()

    @property
    def fg_color(self):
        """
        The fg_color attribute sets the foreground color. It needs to be a
        :class:`~pygamelib.gfx.core.Color`.

        .. versionadded:: 1.3.0

        .. role:: boldblue

        When the foreground color is changed, the observers are notified of the change
        with the :boldblue:`pygamelib.base.Text.fg_color:changed` event. The new color
        is passed as the `value` parameter.
        """
        return self.__fg_color

    @fg_color.setter
    def fg_color(self, value):
        if pgl_isinstance(value, "pygamelib.gfx.core.Color"):
            if self.__fg_color is not None:
                self.__fg_color.detach(self)
            self.__fg_color = value
            self.__fg_color.attach(self)
            self.notify(self, "pygamelib.base.Text.fg_color:changed", value)
        elif value is None:
            if self.__fg_color is not None:
                self.__fg_color.detach(self)
            self.__fg_color = value
            self.notify(self, "pygamelib.base.Text.fg_color:changed", value)
            self.__fgcc = Fore.RESET
        else:
            raise PglInvalidTypeException(
                "Text.fg_color can only be a pygamelib.gfx.core.Color object."
            )
        self.__build_color_cache()

    def __build_color_cache(self):
        t = Console.instance()
        if self.bg_color is not None and pgl_isinstance(
            self.bg_color, "pygamelib.gfx.core.Color"
        ):
            self.__bgcc = t.on_color_rgb(
                self.bg_color.r, self.bg_color.g, self.bg_color.b
            )
        if self.fg_color is not None and pgl_isinstance(
            self.fg_color, "pygamelib.gfx.core.Color"
        ):
            self.__fgcc = t.color_rgb(self.fg_color.r, self.fg_color.g, self.fg_color.b)

    def __repr__(self):
        return "".join([self.__bgcc, self.__fgcc, self.style, self.text, "\x1b[0m"])

    def __str__(self):
        return self.__repr__()

    # def __setattr__(self, key, value):
    #     print(f"{key} changed with value={value}")
    #     super(Text, self).__setattr__(key, value)

    def print_formatted(self):
        """Print the text with the current font activated.

        .. versionadded:: 1.3.0

        If the font is not set, it is strictly equivalent to use Python's
        print(text_object).
        """
        if self.__font is None:
            print(self)
        else:
            glyph = self.__font.glyph
            colors = {}
            if self.fg_color is not None:
                colors["fg_color"] = self.fg_color
            if self.bg_color is not None:
                colors["bg_color"] = self.bg_color
            # First, we get the glyphs.
            # We the need to print them line by line.
            for line in self.text.splitlines():
                glyphs = []
                for char in line:
                    glyphs.append(glyph(char, **colors))
                for ri in range(0, self.__font.height):
                    for g in glyphs:
                        for ci in range(0, g.width):
                            print(g.sprixel(ri, ci), end="")
                        for _ in range(self.__font.horizontal_spacing):
                            print(" ", end="")
                    print()
                # print()
                for _ in range(self.__font.vertical_spacing):
                    print()

    @property
    def length(self):
        """Return the true length of the text.

        .. versionadded:: 1.3.0

        With UTF8 and emojis the length of a string as returned by python's
        :func:`len()` function is often very wrong.
        For example, the len("\\x1b[48;2;139;22;19m\\x1b[38;2;160;26;23m▄\\x1b[0m")
        returns 39 when it should return 1.

        This method returns the actual printing/display size of the text.

        .. Note:: This is a read only value. It is automatically updated when the text
           property is changed.

        Example::

            game.screen.place(my_text, 0, game.screen.width - my_text.length)
        """
        if self.__font is None:
            return self.__length
        else:
            max_length = 0
            # Squash the dot notation
            glyph = self.__font.glyph
            for line in self.text.splitlines():
                length = 0
                for char in line:
                    font_glyph = glyph(char)
                    length += font_glyph.size[0] + self.__font.horizontal_spacing
                if length > max_length:
                    max_length = length
            return max_length

    # Text is a special case in the buffer rendering system and I know special cases are
    # bad but it works well... Text is automatically converted into a Sprite during
    # rendering.
    # The apparent reason is that the BG color is not reset by simply the background to
    # None
    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        """Render the Text object from the display buffer to the frame buffer.

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
        row_idx = 0
        # Here we have some duplicate code. The reason is optimization.
        # If we were to test if the font is set or not in the loop, we would execute
        # as many comparisons as there are characters in the text for that purpose.
        # That test can be done once and for all at the expense of writing twice the
        # rendering code.
        # It is a small counterpart considering the increase in performances.
        # As an example, if you have about a 100 characters on screen (for the different
        # labels), this solution will do 1 test at the beginning + 2 tests (boundaries)
        # per loop + the character rendering or: 201 "if" + the rendering operations of
        # the glyph.
        # Putting everything in the same loop, would add one more test to the loop so:
        # 3 tests per loop + the character rendering or 300 "if" + the glyph rendering.
        # This would add 100 tests *every frame*.
        if self.__font is None:
            for line in self.text.splitlines():
                idx = 0
                for char in line:
                    if column + idx >= buffer_width:
                        break
                    if row + row_idx >= buffer_height:
                        break
                    buffer[row + row_idx][column + idx] = "".join(
                        [self.__bgcc, self.__fgcc, self.style, char, "\x1b[0m"]
                    )
                    idx += 1
                row_idx += 1
        else:
            row_incr = self.__font.height + self.__font.vertical_spacing
            font_horizontal_spacing = self.__font.horizontal_spacing
            # Squash the dot notation
            glyph = self.__font.glyph
            colors = {
                "fg_color": None,
                "bg_color": None,
            }
            if self.__font.colorable:
                if self.fg_color is not None:
                    colors["fg_color"] = self.fg_color
                if self.bg_color is not None:
                    colors["bg_color"] = self.bg_color
            # t = Console.instance()
            # bgcc = t.on_color_rgb(self.bg_color.r, self.bg_color.g, self.bg_color.b)
            # filler = f"{bgcc} \x1b[0m"
            for line in self.text.splitlines():
                idx = 0
                for char in line:
                    # NOTE: We don't need to check for the boundaries since we are
                    # actually rendering a sprite and Sprite.render_to_buffer already
                    # bind its rendering area to the available space.
                    # if column + idx >= buffer_width:
                    #     break
                    # if row + row_idx >= buffer_height:
                    #     break
                    font_glyph = glyph(char, colors["fg_color"], colors["bg_color"])
                    font_glyph.render_to_buffer(
                        buffer, row + row_idx, column + idx, buffer_height, buffer_width
                    )
                    # This code is lacking the rows
                    # for i in range(
                    #     font_glyph.size[0], font_glyph.size[0] +
                    #       font_horizontal_spacing
                    # ):
                    #     buffer[row + row_idx][column + idx + i] = filler
                    idx += font_glyph.size[0] + font_horizontal_spacing
                row_idx += row_incr

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

    .. deprecated:: 1.3.0
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

    .. deprecated:: 1.3.0
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

    .. deprecated:: 1.3.0
    """


class PglObjectIsNotMovableException(Exception):
    """
    Exception raised if the object that is being moved is not a subclass of Movable.
    """

    def __init__(self, message):
        self.message = message


class HacObjectIsNotMovableException(PglObjectIsNotMovableException):
    """Simple forward to PglObjectIsNotMovableException

    .. deprecated:: 1.3.0
    """


class PglInvalidLevelException(Exception):
    """
    Exception raised if a level is not associated to a board in Game().
    """

    def __init__(self, message):
        self.message = message


class HacInvalidLevelException(PglInvalidLevelException):
    """Forward to PglInvalidLevelException

    .. deprecated:: 1.3.0
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

    .. deprecated:: 1.3.0
    """


class Vector2D(object):
    """A 2D vector class.

    .. versionadded:: 1.2.0

    Contrary to the rest of the library Vector2D uses floating point numbers for its
    coordinates/direction/orientation. However since the rest of the library uses
    integers, the numbers are rounded to 2 decimals.
    You can alter that behavior by increasing or decreasing the rounding_precision
    parameter (if you want integer for example).

    Vector2D use the row/column internal naming convention as it is easier to visualize
    for developers that are still learning python or the pygamelib. If it is a concept
    that you already understand and are more familiar with the x/y coordinate system you
    can also use x and y.

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
        super().__init__()
        # column is x and row is y
        self.__row = row
        self.__column = column
        self.rounding_precision = 2
        """The rounding_precision attributes is used when vectors values are calculated
        and the result rounded for convenience. It can be changed anytime to increase or
        decrease the precision anytime."""

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.__row}, {self.__column})"

    def __str__(self):
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
        if isinstance(other, Vector2D):
            if other.row == self.__row and other.column == self.__column:
                return True
            return False
        return NotImplemented

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
            math.sqrt(self.row**2 + self.column**2), self.rounding_precision
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

    def serialize(self):
        """Returns a dictionary with the attributes of the vector.

        .. versionadded:: 1.3.0

        :returns: A dictionary with the attributes of the vector.
        :rtype: dict

        Example::

            gravity = Vector2D(9.81, 0)
            gravity_dict = gravity.serialize()
            print(gravity_dict)
        """
        return {"row": self.row, "column": self.column}

    @classmethod
    def load(cls, data):
        """Loads a vector from a dictionary.

        .. versionadded:: 1.3.0

        :param data: A dictionary with the attributes of the vector.
        :type data: dict
        :returns: A vector.
        :rtype: :class:`~pygamelib.base.Vector2D`

        Example::

            gravity_dict = {"row": 9.81, "column": 0}
            gravity = Vector2D.load(gravity_dict)
        """
        return cls(data["row"], data["column"])


class Math(object):
    """The math class regroup math functions required for game development.

    .. versionadded:: 1.2.0

    For the moment there is only static methods in that class but it will evolve in the
    future.

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def intersect(
        row1: int,
        column1: int,
        width1: int,
        height1: int,
        row2: int,
        column2: int,
        width2: int,
        height2: int,
    ) -> bool:
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
    def distance(row1: int, column1: int, row2: int, column2: int) -> float:
        """Return the euclidean distance between to points.

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
                            )
        """
        return math.sqrt((column2 - column1) ** 2 + (row2 - row1) ** 2)

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """Return the linear interpolation between 2 values relative to a third value.

        .. versionadded:: 1.3.0

        :param a: Start value of the interpolation. Returned if t is 0.
        :type a: float
        :param b: End value of the interpolation. Returned if t is 1.
        :type b: float
        :param t: A value between 0 and 1 used to interpolate between a and b.
        :type t: float

        Example::

            value = lerp(0, 100, 0.5) # 50
        """
        return (1 - t) * a + t * b
