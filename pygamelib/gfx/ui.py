__docformat__ = "restructuredtext"
"""
.. autosummary::
   :toctree: .

   pygamelib.gfx.ui.UiConfig
   pygamelib.gfx.ui.Dialog
   pygamelib.gfx.ui.Box
   pygamelib.gfx.ui.ProgressBar
   pygamelib.gfx.ui.ProgressDialog
   pygamelib.gfx.ui.VerticalProgressBar
   pygamelib.gfx.ui.MessageDialog
   pygamelib.gfx.ui.LineInputDialog
   pygamelib.gfx.ui.MultiLineInputDialog
   pygamelib.gfx.ui.FileDialog
   pygamelib.gfx.ui.GridSelector
   pygamelib.gfx.ui.GridSelectorDialog
   pygamelib.gfx.ui.ColorPicker
   pygamelib.gfx.ui.ColorPickerDialog

"""
from pygamelib.assets import graphics
from pygamelib.gfx import core
from pygamelib import base, constants
from pygamelib import functions
from pathlib import Path

# TODO: make sure that Sprixels works as parameters for UiConfig (and are correctly
# processed)


class UiConfig(object):
    """A configuration object for the UI module. TEST

    This object's function is to configure the look and feel of the UI widgets.

    :param game: The game object.
    :type game: :class:`~pygamelib.engine.Game`
    :param box_vertical_border: The vertical border of a box.
    :type box_vertical_border: str
    :param box_horizontal_border: The horizontal border of a box.
    :type box_horizontal_border: str
    :param box_top_left_corner: The top left corner of a box.
    :type box_top_left_corner: str
    :param box_top_right_corner: The top right corner of a box.
    :type box_top_right_corner: str
    :param box_bottom_left_corner: The bottom left corner of a box.
    :type box_bottom_left_corner: str
    :param box_bottom_right_corner: The bottom right corner of a box.
    :type box_bottom_right_corner: str
    :param box_vertical_and_right: The left junction between two boxes.
    :type box_vertical_and_right: str
    :param box_vertical_and_left: The right junction between two boxes.
    :type box_vertical_and_left: str
    :param fg_color: The foreground color (for text and content).
    :type fg_color: :class:`~pygamelib.gfx.core.Color`
    :param bg_color: The background color (for text and content).
    :type bg_color: :class:`~pygamelib.gfx.core.Color`
    :param border_fg_color: The foreground color (for borders).
    :type border_fg_color: :class:`~pygamelib.gfx.core.Color`
    :param border_bg_color: The background color (for borders).
    :type border_bg_color: :class:`~pygamelib.gfx.core.Color`
    :param borderless_dialog: Is the dialog borderless or not.
    :type borderless_dialog: bool

    Example::

        method()
    """

    __instance = None

    def __init__(
        self,
        game=None,
        box_vertical_border=graphics.BoxDrawings.LIGHT_VERTICAL,
        box_horizontal_border=graphics.BoxDrawings.LIGHT_HORIZONTAL,
        box_top_left_corner=graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT,
        box_top_right_corner=graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT,
        box_bottom_left_corner=graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT,
        box_bottom_right_corner=graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT,
        box_vertical_and_right=graphics.BoxDrawings.LIGHT_VERTICAL_AND_RIGHT,
        box_vertical_and_left=graphics.BoxDrawings.LIGHT_VERTICAL_AND_LEFT,
        fg_color=core.Color(255, 255, 255),
        bg_color=core.Color(0, 128, 128),
        border_fg_color=core.Color(255, 255, 255),
        border_bg_color=None,
        borderless_dialog=True,
    ):
        super().__init__()
        if game is None:
            raise base.PglInvalidTypeException(
                "UiConfig: the 'game' parameter cannot be None."
            )
        self.game = game
        self.box_vertical_border = box_vertical_border
        self.box_horizontal_border = box_horizontal_border
        self.box_top_left_corner = box_top_left_corner
        self.box_top_right_corner = box_top_right_corner
        self.box_bottom_left_corner = box_bottom_left_corner
        self.box_bottom_right_corner = box_bottom_right_corner
        self.box_vertical_and_right = box_vertical_and_right
        self.box_vertical_and_left = box_vertical_and_left
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_fg_color = border_fg_color
        self.border_bg_color = border_bg_color
        self.borderless_dialog = borderless_dialog

    @classmethod
    def instance(cls, *args, **kwargs):
        """Returns the instance of the UiConfig object

        Creates an UiConfig object on first call an then returns the same instance
        on further calls

        :return: Instance of Game object

        """
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance


class Dialog(object):
    def __init__(self, config=None) -> None:
        super().__init__()
        if config is None or not isinstance(config, UiConfig):
            raise base.PglInvalidTypeException(
                "The config parameter cannot be None and needs to be a UiConfig object."
            )
        setattr(self, "_config", config)
        setattr(self, "_user_input", "")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self._config = value
        else:
            raise base.PglInvalidTypeException(
                "Dialog.config = value: value needs to be an UiConfig object."
            )

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, value):
        if type(value) is str:
            self._user_input = value
        else:
            raise base.PglInvalidTypeException(
                "Dialog.user_input = value: value needs to be a str."
            )

    def show():
        raise NotImplementedError


class Box(object):
    def __init__(
        self,
        width: int,
        height: int,
        title: str = "",
        config: UiConfig = None,
        fill: bool = False,
        filling_sprixel: core.Sprixel = None,
    ):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__title = title
        self.__fill = fill
        self.__filling_sprixel = filling_sprixel
        self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        # Caching system to avoid tons of objects creations at rendering.
        self._cache["dialog_vertical_border"] = core.Sprixel(
            self.__config.box_vertical_border,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["dialog_horizontal_border"] = core.Sprixel(
            self.__config.box_horizontal_border,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["top_right_corner"] = core.Sprixel(
            self.__config.box_top_left_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["top_left_corner"] = core.Sprixel(
            self.__config.box_top_right_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["bottom_right_corner"] = core.Sprixel(
            self.__config.box_bottom_left_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["bottom_left_corner"] = core.Sprixel(
            self.__config.box_bottom_right_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        if isinstance(self.__title, base.Text):
            self._cache["title"] = self.__title
        else:
            self._cache["title"] = base.Text(
                self.__title,
                self.__config.border_fg_color,
                self.__config.border_bg_color,
            )
        self._cache["title_sprite"] = core.Sprite.from_text(self._cache["title"])

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self.__config = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.config = value: value needs to be an UiConfig object."
            )

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if isinstance(value, base.Text) or type(value) is str:
            self.__title = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.title = value: value needs to be a Text object or str."
            )

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if type(value) is int:
            self.__width = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if type(value) is int:
            self.__height = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        vert_sprix = self._cache["dialog_vertical_border"]
        horiz_sprix = self._cache["dialog_horizontal_border"]
        buffer[row][column] = self._cache["top_right_corner"]
        if self._cache["title"] == "":
            for c in range(column + 1, column + self.__width - 1):
                buffer[row][c] = horiz_sprix
        else:
            for c in range(
                column + 1,
                column
                + 1
                + round(self.__width / 2 - len(self._cache["title"].text) / 2),
            ):
                buffer[row][c] = horiz_sprix
            self._cache["title_sprite"].render_to_buffer(
                buffer,
                row,
                column
                + 1
                + int(self.__width / 2 - 1 - len(self._cache["title"].text) / 2),
                buffer_height,
                buffer_width,
            )
            cs = (
                column
                + 1
                + int(self.__width / 2 - 1 - len(self._cache["title"].text) / 2)
                + len(self._cache["title"].text)
            )
            for c in range(
                cs, cs + int(self.__width / 2 - len(self._cache["title"].text) / 2)
            ):
                buffer[row][c] = horiz_sprix
        buffer[row][column + self.__width - 1] = self._cache["top_left_corner"]
        for r in range(1, self.__height - 1):
            buffer[row + r][column] = vert_sprix
            buffer[row + r][column + self.__width - 1] = vert_sprix
        buffer[row + self.__height - 1][column] = self._cache["bottom_right_corner"]
        for c in range(column + 1, column + self.__width - 1):
            buffer[row + self.__height - 1][c] = horiz_sprix
        buffer[row + self.__height - 1][column + self.__width - 1] = self._cache[
            "bottom_left_corner"
        ]
        if self.__fill:
            for r in range(row + 1, row + self.__height - 1):
                for c in range(column + 1, column + self.__width - 1):
                    buffer[r][c] = self.__filling_sprixel


class ProgressBar(object):
    """
    A simple horizontal progress bar widget.

    :param value: The initial value parameter. It represents the progression.
    :type value: int
    :param maximum: The maximum value held by the progress bar. Any value over the
       maximum is ignored.
    :type maximum: int
    :param width: The width of the progress bar widget (in number of screen cells).
    :type width: int

    Example::

        # Create a default progress bar with the default configuration
        progress_bar = ProgressBar(config=UiConfig.instance())
        # Place the progress bar in the middle of the screen
        screen.place(
            progress_bar, screen.vcenter, screen.hcenter - int(progress_bar.width)
        )
        for progress in range(progress_bar.maximum + 1):
            # Do something useful
            progress_bar.value = progress
            screen.update()
    """

    def __init__(
        self,
        value=0,
        maximum=100,
        width=20,
        progress_marker=graphics.GeometricShapes.BLACK_RECTANGLE,
        empty_marker=" ",
        config=None,
    ):
        super().__init__()
        self.__value = value
        self.__maximum = maximum
        self.__width = width
        self.__progress_marker = progress_marker
        self.__empty_marker = empty_marker
        self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        if isinstance(self.__empty_marker, core.Sprixel):
            self._cache["pb_empty"] = self.__empty_marker
        else:
            self._cache["pb_empty"] = core.Sprixel(
                self.__empty_marker, self.__config.bg_color, self.__config.fg_color
            )
        if isinstance(self.__progress_marker, core.Sprixel):
            self._cache["pb_progress"] = self.__progress_marker
        else:
            self._cache["pb_progress"] = core.Sprixel(
                self.__progress_marker, self.__config.bg_color, self.__config.fg_color
            )

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self.__config = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.config(value): value needs to be an UiConfig object."
            )

    @property
    def progress_marker(self):
        return self.__progress_marker

    @progress_marker.setter
    def progress_marker(self, value):
        if isinstance(value, base.Text):
            self.__progress_marker = value.text
            self._cache["pb_progress"] = value
            self._build_cache()
        elif type(value) is str:
            self.__progress_marker = value
            self._cache["pb_progress"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.progress_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def empty_marker(self):
        return self.__progress_marker

    @empty_marker.setter
    def empty_marker(self, value):
        if isinstance(value, base.Text):
            self.__empty_marker = value.text
            self._cache["pb_empty"] = value
            self._build_cache()
        elif type(value) is str:
            self.__empty_marker = value
            self._cache["pb_empty"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.empty_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if type(value) is int:
            self.__value = value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.value: value needs to be an int."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def maximum(self):
        return self.__maximum

    @maximum.setter
    def maximum(self, value):
        if type(value) is int:
            self.__maximum = value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.maximum: value needs to be an int."
            )
        self.__config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        for c in range(0, prog):
            buffer[row][column + c] = self._cache["pb_progress"]
        for c in range(prog, self.__width):
            buffer[row][column + c] = self._cache["pb_empty"]


class ProgressDialog(Dialog):
    def __init__(
        self,
        label=base.Text("Progress dialog"),
        value=0,
        maximum=100,
        width=20,
        progress_marker=graphics.GeometricShapes.BLACK_RECTANGLE,
        empty_marker=" ",
        adaptive_width=True,
        destroy_on_complete=True,
        config=None,
    ):
        super().__init__(config=config)
        self.__label = label
        self.__value = value
        self.__maximum = maximum
        self.__width = width
        self.__progress_marker = progress_marker
        self.__empty_marker = empty_marker
        self.__adaptive_width = adaptive_width
        self.destroy_on_complete = destroy_on_complete
        self.__destroy = False
        # self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        if isinstance(self.__label, base.Text):
            self._cache["label"] = self.__label
        else:
            self._cache["label"] = base.Text(
                self.__label, self.config.fg_color, self.config.bg_color
            )
        # Adapt the width of the dialog based on the size of the text
        if self.__adaptive_width and self.__width != self._cache["label"].length:
            self.__width = len(self._cache["label"].text)
        self._cache["pb"] = ProgressBar(
            self.__value,
            self.__maximum,
            self.__width,
            self.__progress_marker,
            self.__empty_marker,
            config=self.config,
        )
        if not self.config.borderless_dialog:
            self._cache["borders"] = Box(
                self.__width, 2, self._cache["label"], config=self.config
            )

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        if isinstance(value, base.Text):
            self.__label = value.text
            self._cache["label"] = value
            self._build_cache()
        elif type(value) is str:
            self.__label = value
            self._cache["label"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.label: value needs to be a str or pygamelib.base.Text."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if type(val) is int:
            self.__value = val
            self._cache["pb"].value = self.__value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.value: value needs to be an int."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def maximum(self):
        return self.__maximum

    @maximum.setter
    def maximum(self, value):
        if type(value) is int:
            self.__maximum = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.maximum: value needs to be an int."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        if self.__destroy:
            self.config.game.screen.delete(row, column)
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(self.__width + 2, 4, config=self.config)
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lbl = core.Sprite.from_text(self._cache["label"])

        lbl.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )
        self._cache["pb"].render_to_buffer(
            buffer, row + 1 + offset, column + offset, buffer_height, buffer_width
        )
        # prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        # for c in range(0, prog):
        #     buffer[row + 1 + offset][column + c + offset] = self._cache["pb_progress"]
        # for c in range(prog, self.__width):
        #     buffer[row + 1 + offset][column + c + offset] = self._cache["pb_empty"]
        if self.destroy_on_complete and self.__value == self.__maximum:
            self.__destroy = True


class VerticalProgressBar(object):
    def __init__(
        self,
        value=0,
        maximum=100,
        height=10,
        progress_marker="#",
        empty_marker=" ",
        config=None,
    ):
        super().__init__()


class MessageDialog(Dialog):
    def __init__(
        self,
        data: list = None,
        width: int = 20,
        height: int = None,
        adaptive_height: bool = True,
        alignement: int = None,
        config: UiConfig = None,
    ) -> None:
        super().__init__(config=config)
        if alignement is None:
            alignement = constants.ALIGN_LEFT
        if adaptive_height is False and height is None:
            adaptive_height = True
        self.__cache = {"data": []}
        # TODO: add height and width?
        self.__width = width
        self.__height = height
        self.__adaptive_height = adaptive_height
        self.__data = list()
        if data is not None:
            for d in data:
                self.add_line(d, alignement)

    def _build_cache(self) -> None:
        self.__cache = {"data": []}
        height = self.__height
        if height is None:
            height = len(self.__data)
        for e in self.__data:
            if isinstance(e[0], core.Sprixel) or type(e[0]) is str:
                self.__cache["data"].append(e[0])
            elif isinstance(e[0], base.Text):
                self.__cache["data"].append(core.Sprite.from_text(e[0]))
            elif hasattr(e[0], "render_to_buffer"):
                self.__cache["data"].append(e[0])
        if not self.config.borderless_dialog:
            self.__cache["border"] = Box(
                self.__width,
                height + 2,
                config=self.config,
                fill=True,
                filling_sprixel=core.Sprixel(" ", bg_color=self.config.bg_color),
            )

    @property
    def height(self):
        if self.__adaptive_height:
            h = 0
            if not self.config.borderless_dialog:
                h += 2
            return len(self.__data) + h
        else:
            return self.__height

    @height.setter
    def height(self, value):
        if type(value) is int:
            self.__height = value
        else:
            raise base.PglInvalidTypeException(
                "MessageDialog.height = value: value needs to be an int. It is a "
                f"{type(value)}"
            )

    def add_line(self, data, alignement=constants.ALIGN_LEFT) -> None:
        if (
            isinstance(data, core.Sprixel)
            or type(data) is str
            or isinstance(data, base.Text)
            or hasattr(data, "render_to_buffer")
        ):
            self.__data.append([data, alignement])
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                f"MessageDialog.add_line(data, alignement): 'data' type {type(data)} is"
                " not supported"
            )

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        render_string = functions.render_string_to_buffer
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            self.__cache["border"].render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )
        for idx in range(len(self.__cache["data"])):
            padding = 0
            alignement = self.__data[idx][1]
            data = self.__data[idx][0]
            if alignement == constants.ALIGN_RIGHT:
                if type(data) is str:
                    padding = self.__width - len(data) - 2
                elif hasattr(data, "length"):
                    padding = self.__width - data.length - 2
            elif alignement == constants.ALIGN_CENTER:
                if type(data) is str:
                    padding = int((self.__width - len(data) - 2) / 2)
                elif hasattr(data, "length"):
                    padding = int((self.__width - data.length - 2) / 2)
            if isinstance(self.__cache["data"][idx], core.Sprixel):
                buffer[row + offset + idx][column + offset + padding] = self.__cache[
                    "data"
                ][idx]
            elif hasattr(self.__cache["data"][idx], "render_to_buffer"):
                self.__cache["data"][idx].render_to_buffer(
                    buffer,
                    row + offset + idx,
                    column + offset + padding,
                    buffer_height,
                    buffer_width,
                )
            elif type(self.__cache["data"][idx]) is str:
                render_string(
                    self.__cache["data"][idx],
                    buffer,
                    row + offset + idx,
                    column + offset + padding,
                    buffer_height,
                    buffer_width,
                )

    def show(self) -> None:
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.update()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER" or inkey.name == "KEY_ESCAPE":
                    break
            inkey = term.inkey(timeout=0.1)
        return None


class LineInputDialog(Dialog):
    def __init__(
        self,
        label="Input a value:",
        default="",
        filter=constants.PRINTABLE_FILTER,
        config=None,
    ) -> None:
        super().__init__(config=config)
        self.__label = label
        self.__default = str(default)
        self.__filter = filter
        if self.__label is None or not (
            isinstance(self.__label, base.Text) or type(self.__label) is str
        ):
            raise base.PglInvalidTypeException(
                "LineInputDialog: label must be a str or pygamelib.base.Text."
            )
        if self.__default is None or not (
            isinstance(self.__default, base.Text) or type(self.__default) is str
        ):
            raise base.PglInvalidTypeException(
                "LineInputDialog: default must be a str."
            )
        if type(self.__label) is str:
            self.__label = base.Text(self.__label)
        self.user_input = self.__default

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        if isinstance(value, base.Text):
            self.__label = value.text
            self._cache["label"] = value
        elif type(value) is str:
            self.__label = value
            self._cache["label"].text = value
        else:
            raise base.PglInvalidTypeException(
                "LineInputDialog.label: value needs to be a str or pygamelib.base.Text."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(self.__label.length + 2, 4, config=self.config)
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lbl = core.Sprite.from_text(self.__label)
        lbl.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )
        inp = core.Sprite.from_text(base.Text(f"> {self.user_input}"))
        inp.render_to_buffer(
            buffer, row + 1 + offset, column + offset, buffer_height, buffer_width
        )

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.update()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    break
                elif inkey.name == "KEY_ESCAPE":
                    self.user_input = ""
                    break
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.user_input = self.user_input[:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif (
                    self.__filter == constants.PRINTABLE_FILTER and inkey.isprintable()
                ) or (self.__filter == constants.INTEGER_FILTER and inkey.isdigit()):
                    self.user_input += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        return self.user_input


class MultiLineInputDialog(Dialog):
    def __init__(
        self,
        fields=[
            {
                "label": "Input a value:",
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
            }
        ],
        config=None,
    ) -> None:
        super().__init__(config=config)
        self.__fields = fields
        if self.__fields is None or not (type(self.__fields) is list):
            raise base.PglInvalidTypeException(
                "MultiInputDialog: fields must be a list of dictionaries."
            )
        self.user_input = ""
        self.__cache = list()
        self._build_cache()
        self.__current_field = 0

    def _build_cache(self):
        self.__cache = list()
        for field in self.__fields:
            if isinstance(field["label"], base.Text):
                self.__cache.append(field["label"])
            elif type(field["label"]) is str:
                self.__cache.append(base.Text(field["label"]))
            field["user_input"] = field["default"]

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, value):
        if type(value) is list:
            self.__fields = value
        else:
            raise base.PglInvalidTypeException(
                "MultiInputDialog.label: value needs to be a list of dictionaries."
            )
        self._build_cache()
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        offset = 0
        max_text_width = 0
        if not self.config.borderless_dialog:
            # find the max width of the box
            for field in self.__fields:
                if (
                    isinstance(field["label"], base.Text)
                    and field["label"].length > max_text_width
                ):
                    max_text_width = field["label"].length
                elif (
                    type(field["label"]) is str and len(field["label"]) > max_text_width
                ):
                    max_text_width = len(field["label"])
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                max_text_width + 2, len(self.__fields) * 2 + 2, config=self.config
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lc = 0
        fidx = 0
        for field in self.__fields:
            if self.__cache[fidx].length < max_text_width:
                self.__cache[fidx].text = self.__cache[fidx].text + " " * (
                    max_text_width - self.__cache[fidx].length
                )
            lbl = core.Sprite.from_text(self.__cache[fidx])
            lbl.render_to_buffer(
                buffer, row + offset + lc, column + offset, buffer_height, buffer_width
            )
            t = base.Text(
                f"> {field['user_input']}"
                f"{' '*(max_text_width-len(field['user_input'])-2)}"
            )
            if fidx == self.__current_field:
                t.fg_color = core.Color(0, 255, 0)
            inp = core.Sprite.from_text(t)
            inp.render_to_buffer(
                buffer,
                row + 1 + offset + lc,
                column + offset,
                buffer_height,
                buffer_width,
            )
            lc += 2
            fidx += 1

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.trigger_rendering()
        screen.update()
        self.__current_field = 0
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    break
                elif inkey.name == "KEY_TAB":
                    self.__current_field += 1
                    self.__current_field = self.__current_field % len(self.__fields)
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_ESCAPE":
                    for field in self.__fields:
                        field["user_input"] = ""
                    break
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.__fields[self.__current_field]["user_input"] = self.__fields[
                        self.__current_field
                    ]["user_input"][:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif (
                    self.__fields[self.__current_field]["filter"]
                    == constants.PRINTABLE_FILTER
                    and inkey.isprintable()
                ) or (
                    self.__fields[self.__current_field]["filter"]
                    == constants.INTEGER_FILTER
                    and inkey.isdigit()
                ):
                    self.__fields[self.__current_field]["user_input"] += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        return self.__fields


class FileDialog(Dialog):
    def __init__(
        self,
        path: Path = None,
        width: int = 20,
        height: int = 10,
        title: str = "File dialog",
        show_hidden_files: bool = False,
        filter: str = "*",
        config: UiConfig = None,
    ) -> None:
        super().__init__(config=config)
        self.__path = None
        if path is not None and isinstance(path, Path):
            self.__path = path
        self.__original_path = self.__path
        self.__show_hidden_files = False
        if show_hidden_files is not None and type(show_hidden_files) is bool:
            self.__show_hidden_files = show_hidden_files
        self.__filter = ""
        if filter is not None and type(filter) is str:
            self.__filter = filter
        self.__width = 20
        if width is not None and type(width) is int:
            self.__width = width
        self.__height = 10
        if height is not None and type(height) is int:
            self.__height = height
        self.__title = "File dialog"
        if title is not None and type(title) is str:
            self.__title = title
        self.__browsing_position = 0
        self.__current_selection = ""
        self.__current_pannel = 0
        self.user_input = ""
        self.__file_icon = core.Sprite(
            size=[1, 1], sprixels=[[core.Sprixel(graphics.Models.PAGE_FACING_UP)]]
        )
        self.__dir_icon = core.Sprite(
            size=[1, 1], sprixels=[[core.Sprixel(graphics.Models.FILE_FOLDER)]]
        )
        # Files/directory cache
        self.__files = []
        self._build_file_cache()
        # Sprite/Sprixel cache
        self.__cache = {}
        self._build_cache()

    def _build_file_cache(self):
        # We are only accessing the filesystem when we change directory.
        self.__files = []
        self.__files = sorted(
            [
                x
                for x in self.__path.iterdir()
                if (
                    x.is_dir()
                    and (
                        (self.__show_hidden_files and x.name.startswith("."))
                        or (not self.__show_hidden_files and not x.name.startswith("."))
                    )
                )
            ]
        )
        self.__files.extend(
            sorted(
                [
                    x
                    for x in self.__path.glob(self.__filter)
                    if (
                        x.is_file()
                        and (
                            (self.__show_hidden_files and x.name.startswith("."))
                            or (
                                not self.__show_hidden_files
                                and not x.name.startswith(".")
                            )
                        )
                    )
                ]
            )
        )

    def _build_cache(self):
        self.__cache = {}
        self.__cache["vertical_and_right"] = core.Sprixel(
            self.config.box_vertical_and_right,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )
        self.__cache["vertical_and_left"] = core.Sprixel(
            self.config.box_vertical_and_left,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )
        self.__cache["vertical_border"] = core.Sprixel(
            self.config.box_vertical_border,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )
        self.__cache["horizontal_border"] = core.Sprixel(
            self.config.box_horizontal_border,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )
        self.__cache["bottom_right_corner"] = core.Sprixel(
            self.config.box_bottom_left_corner,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )
        self.__cache["bottom_left_corner"] = core.Sprixel(
            self.config.box_bottom_right_corner,
            self.config.border_bg_color,
            self.config.border_fg_color,
        )

    @property
    def path(self):
        """
        Return the current path.

        :returns: The dialog's current path.
        :rtype: :class:`pathlib.Path`
        """
        return self.__path

    @path.setter
    def path(self, new_path: Path) -> None:
        if isinstance(new_path, Path):
            self.__path = new_path
        else:
            raise base.PglInvalidTypeException(
                "FileDialog.path = new_path -> new_path must be a Path object."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def filter(self):
        """
        Return the current file filter.

        :returns: The dialog's current filter.
        :rtype: str
        """
        return self.__filter

    @filter.setter
    def filter(self, new_filter: str) -> None:
        if type(new_filter) is str:
            self.__filter = new_filter
        else:
            raise base.PglInvalidTypeException(
                "FileDialog.filter = new_filter -> new_filter must be a string."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def show_hidden_files(self):
        """
        Return a boolean, if True the file dialog is going to show hidden files, and, if
        False, it won't.

        :returns: The dialog's current show_hidden_files value.
        :rtype: bool
        """
        return self.__show_hidden_files

    @show_hidden_files.setter
    def show_hidden_files(self, value: bool) -> None:
        if type(value) is bool:
            self.__show_hidden_files = value
        else:
            raise base.PglInvalidTypeException(
                "FileDialog.show_hidden_files = value -> value must be a boolean."
            )
        self.config.game.screen.trigger_rendering()

    # properties for width and height

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        # TODO: The actual dialog size is bigger than the the one passed in parameter
        #       because I had to the size (for the file name) instead of drawing INTO
        #       the alloted height.
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                self.__width,
                self.__height,
                self.__title,
                self.config,
                True,
                core.Sprixel(" ", bg_color=None),
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
            buffer[row + self.__height - 1][column] = self.__cache["vertical_and_right"]
            buffer[row + self.__height - 1][column + self.__width - 1] = self.__cache[
                "vertical_and_left"
            ]
            buffer[row + self.__height][column] = self.__cache["vertical_border"]
            buffer[row + self.__height][column + self.__width - 1] = self.__cache[
                "vertical_border"
            ]
            buffer[row + self.__height + 1][column] = self.__cache[
                "bottom_right_corner"
            ]
            buffer[row + self.__height + 1][column + self.__width - 1] = self.__cache[
                "bottom_left_corner"
            ]
            for tc in range(column + 1, column + self.__width - 1):
                buffer[row + self.__height + 1][tc] = self.__cache["horizontal_border"]
        # For files: graphics.Model.PAGE_FACING_UP
        # For folders: graphics.Model.FILE_FOLDER ou graphics.Models.OPEN_FILE_FOLDER
        r = row + offset
        c = column + offset
        idx = 0
        # files = sorted([x for x in self.__path.iterdir() if x.is_dir()])
        # self.config.game.log(f"FileDialog.render_to_buffer: dirs={files}")
        # files.extend(
        #     sorted([x for x in self.__path.glob(self.__filter) if x.is_file()])
        # )
        # for i in self.__files:
        # for idx in range(self.__browsing_position, len(self.__files)):
        start = int(self.__browsing_position / (self.__height - 2)) * (
            self.__height - 2
        )
        for idx in range(start, len(self.__files)):
            i = self.__files[idx]
            icon = core.Sprite()
            if i.is_dir():
                icon = self.__dir_icon
            elif i.is_file():
                icon = self.__file_icon
                # if idx == self.__browsing_position:
                #     self.__user_input = i.name
            icon.render_to_buffer(buffer, r, c, buffer_height, buffer_width)
            txt = base.Text(i.name)
            if idx == self.__browsing_position:
                txt.fg_color = core.Color(0, 255, 0)
                txt.style = constants.BOLD
                self.__current_selection = i
            lbl = core.Sprite.from_text(txt)
            lbl.render_to_buffer(
                buffer,
                r,
                c + self.__dir_icon.sprixel(0, 0).length,
                buffer_height,
                buffer_width,
            )
            r += 1
            if r >= self.__height + row - 1:
                break

        # Write the user input in the buffer
        tidx = 1
        for c in self.user_input:
            buffer[row + self.__height][column + tidx] = c
            tidx += 1
            if tidx >= self.__width - 1:
                break
        for c in range(tidx, self.__width - 1):
            buffer[row + self.__height][column + c] = " "

    def show(self) -> Path:
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.trigger_rendering()
        screen.update()
        self.__current_field = 0
        while 1:
            if inkey != "":
                tmpp = self.__path / self.__current_selection
                if inkey.name == "KEY_ENTER":
                    if tmpp.is_dir():
                        self.__path = tmpp.resolve()
                        self.user_input = ""
                        self._build_file_cache()
                        self.__browsing_position = 0
                        screen.trigger_rendering()
                        screen.update()
                    elif self.user_input is not None and self.user_input != "":
                        if self.__path.is_file():
                            self.__path = self.__path.parent / self.user_input
                        elif self.__path.is_dir():
                            self.__path = self.__path / self.user_input
                        break
                elif tmpp.is_file() and inkey == " ":
                    self.__path = tmpp
                    self.user_input = tmpp.name
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_TAB":
                    self.__current_pannel += 1
                    self.__current_pannel = self.__current_pannel % 2
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_ESCAPE":
                    self.__path = self.__original_path
                    break
                elif inkey.name == "KEY_UP":
                    self.__browsing_position -= 1
                    self.__browsing_position = functions.clamp(
                        self.__browsing_position, 0, len(self.__files) - 1
                    )
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_DOWN":
                    self.__browsing_position += 1
                    self.__browsing_position = functions.clamp(
                        self.__browsing_position, 0, len(self.__files) - 1
                    )
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_LEFT":
                    if self.__path.is_dir():
                        self.__path = self.__path.parent
                    else:
                        self.__path = self.__path.parent.parent
                    self._build_file_cache()
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.user_input = self.user_input[:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.isprintable():
                    self.config.game.log(f"Got inkey={inkey}")
                    self.user_input += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        return self.__path


class GridSelector(object):
    def __init__(
        self,
        choices: list = None,
        max_height: int = None,
        max_width: int = None,
        config: UiConfig = None,
    ) -> None:
        super().__init__()
        self.__choices = []
        if choices is not None and type(choices) is list:
            self.__choices = choices
        self.__max_height = 5
        if max_height is not None and type(max_height) is int:
            self.__max_height = max_height
        self.__max_width = 10
        if max_width is not None and type(max_width) is int:
            self.__max_width = max_width
        self._config = config
        self.__current_choice = 0
        self.__current_page = 0
        self.__cache = []
        self._build_cache()
        self.__items_per_page = int(self.__max_height / 2 * self.__max_width / 2)
        config.game.log(f"items per page={self.__items_per_page}")

    def _build_cache(self):
        self.__cache = []
        for choice in self.__choices:
            s = choice
            if type(s) is str:
                s = core.Sprixel(choice)
            # TODO: For v1 we only support sprixels of size=1
            # Reason is that some emojis are returning a length of 1 when it's actually
            # 2. And for the moment I have no idea why.
            if s.length > 1:
                continue
            if not isinstance(s, core.Sprixel):
                raise base.PglInvalidTypeException(
                    "GridSelector: the choices must be strings or Sprixels."
                )
            self.__cache.append(s)
        self.__items_per_page = int(self.__max_height / 2 * self.__max_width / 2)

    @property
    def choices(self):
        return self.__choices

    @choices.setter
    def choices(self, value):
        if type(value) is list:
            self.__choices = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.choices = value: 'value' must be a list. "
                f"'{value}' is not a list"
            )

    @property
    def max_height(self):
        return self.__max_height

    @max_height.setter
    def max_height(self, value):
        if type(value) is int:
            self.__max_height = value
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.max_height = value: 'value' must be an int. "
                f"'{value}' is not an int"
            )

    @property
    def max_width(self):
        return self.__max_width

    @max_width.setter
    def max_width(self, value):
        if type(value) is int:
            self.__max_width = value
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.max_width = value: 'value' must be an int. "
                f"'{value}' is not an int"
            )

    @property
    def current_choice(self) -> int:
        return self.__current_choice

    @current_choice.setter
    def current_choice(self, index: int = None):
        if type(index) is int:
            self.__current_choice = index
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.set_selected(index): 'index' must be an int. "
                f"'{index}' is not an int"
            )

    @property
    def current_page(self):
        return self.__current_page

    @current_page.setter
    def current_page(self, value: int):
        if type(value) is int:
            self.__current_page = value
            start = self.__current_page * self.__items_per_page
            if self.__current_choice < start:
                self.__current_choice = start
            elif self.__current_choice + self.__items_per_page > start:
                self.__current_choice = start
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.current_page = value: 'value' must be an int. "
                f"'{value}' is not an int"
            )

    def current_sprixel(self):
        return self.__cache[self.__current_choice]

    def items_per_page(self):
        return self.__items_per_page

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        self.__max_width = functions.clamp(self.__max_width, 0, buffer_width - 2)
        self.__max_height = functions.clamp(self.__max_height, 0, buffer_height - 2)
        crow = 1
        ccol = 1
        col_offset = 1
        row_offset = 1
        start = self.__current_page * self.__items_per_page
        for i in range(start, len(self.__cache)):
            buffer[row + row_offset][column + col_offset] = self.__cache[i]
            if i == self.__current_choice % len(self.__choices):
                border_fg_color = self._config.border_fg_color
                self._config.border_fg_color = core.Color(0, 255, 0)
                sel = Box(self.__cache[i].length + 2, 3, config=self._config)
                sel.render_to_buffer(
                    buffer,
                    row + row_offset - 1,
                    column + col_offset - 1,
                    buffer_height,
                    buffer_width,
                )
                self._config.border_fg_color = border_fg_color
            for xtr in range(1, self.__cache[i].length):
                buffer[row + row_offset][column + col_offset + xtr] = ""
                col_offset += 1
            col_offset += self.__cache[i].length + 1
            ccol += 1
            if col_offset > self.__max_width:
                crow += 1
                row_offset += 2
                ccol = 1
                col_offset = 1
            if (
                row + row_offset >= buffer_height
                or column + col_offset >= buffer_width
                or row_offset > self.__max_height
                or i >= start + self.__items_per_page
            ):
                break


class GridSelectorDialog(Dialog):
    def __init__(
        self,
        choices: list = None,
        max_height: int = None,
        max_width: int = None,
        title: str = None,
        config: UiConfig = None,
    ) -> None:
        super().__init__(config=config)
        self.__grid_selector = None
        if not config.borderless_dialog:
            self.__grid_selector = GridSelector(
                choices, max_height - 3, max_width - 3, config
            )
        else:
            self.__grid_selector = GridSelector(choices, max_height, max_width, config)
        self.__title = ""
        if title is not None and type(title) is str:
            self.__title = title

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value is not None and type(value) is str:
            self.__title = value
        else:
            raise base.PglInvalidTypeException(
                "GridSelectorDialog.title = value: 'value' must be a str. "
                f"'{value}' is not a str"
            )

    @property
    def grid_selector(self):
        return self.__grid_selector

    @grid_selector.setter
    def grid_selector(self, value):
        if isinstance(value, GridSelector):
            self.__grid_selector = value
        else:
            raise base.PglInvalidTypeException(
                "GridSelectorDialog.grid_selector = value: 'value' must be a "
                "GridSelector object. "
            )

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.trigger_rendering()
        screen.update()
        self.__current_field = 0
        ret_sprixel = core.Sprixel()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    ret_sprixel = self.__grid_selector.current_sprixel()
                    break
                elif inkey.name == "KEY_ESCAPE":
                    ret_sprixel = core.Sprixel()
                    break
                elif inkey.name == "KEY_UP":
                    self.__grid_selector.current_choice -= int(
                        self.__grid_selector.max_width / 2
                    )
                    screen.force_update()
                elif inkey.name == "KEY_DOWN":
                    self.__grid_selector.current_choice += int(
                        self.__grid_selector.max_width / 2
                    )
                    screen.force_update()
                elif inkey.name == "KEY_LEFT":
                    self.__grid_selector.current_choice -= 1
                    screen.force_update()
                elif inkey.name == "KEY_RIGHT":
                    self.__grid_selector.current_choice += 1
                    screen.force_update()
                elif inkey.name == "KEY_PGDOWN":
                    self.__grid_selector.current_page += 1
                    if (
                        self.__grid_selector.current_page
                        * self.__grid_selector.items_per_page()
                        >= len(self.__grid_selector.choices)
                    ):
                        self.__grid_selector.current_page -= 1
                    screen.force_update()
                elif inkey.name == "KEY_PGUP":
                    self.__grid_selector.current_page -= 1
                    if self.__grid_selector.current_page < 0:
                        self.__grid_selector.current_page = 0
                    screen.force_update()
            inkey = term.inkey(timeout=0.1)
        return ret_sprixel

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                self.__grid_selector.max_width + 3,
                self.__grid_selector.max_height + 3,
                self.__title,
                self.config,
                True,
                core.Sprixel(" ", bg_color=None),
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
            pagination = f"{self.__grid_selector.current_page+1}/{round(len(self.__grid_selector.choices)/self.__grid_selector.items_per_page())}"
            lp = len(pagination)
            for c in range(0, lp):
                buffer[row + self.__grid_selector.max_height + 2][
                    column + self.__grid_selector.max_width + 2 - lp + c
                ] = pagination[c]
        self.__grid_selector.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )


class ColorPicker(object):
    def __init__(self, orientation: int = None, config: UiConfig = None) -> None:
        super().__init__()
        self.__orientation = constants.ORIENTATION_HORIZONTAL
        if orientation is not None and type(orientation) is int:
            self.__orientation = orientation
        self._config = None
        if isinstance(config, UiConfig):
            self._config = config
        self.__color = core.Color()
        self.__sprixel = core.Sprixel(" ")
        self.__red = 128
        self.__green = 128
        self.__blue = 128
        self.__selection = 0

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if isinstance(value, core.Color):
            self.__color = value
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.color = value: "value" needs to be a Color object.'
                f"{type(value)} is not a color object."
            )

    @property
    def red(self):
        return self.__red

    @red.setter
    def red(self, value):
        if type(value) is int:
            self.__red = value
            self.__red = functions.clamp(self.__red, 0, 255)
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.red = value: "value" needs to be an integer.'
                f"{type(value)} is not an integer."
            )

    @property
    def green(self):
        return self.__green

    @green.setter
    def green(self, value):
        if type(value) is int:
            self.__green = value
            self.__green = functions.clamp(self.__green, 0, 255)
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.green = value: "value" needs to be an integer.'
                f"{type(value)} is not an integer."
            )

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, value):
        if type(value) is int:
            self.__blue = value
            self.__blue = functions.clamp(self.__blue, 0, 255)
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.blue = value: "value" needs to be an integer.'
                f"{type(value)} is not an integer."
            )

    @property
    def selection(self):
        return self.__selection

    @selection.setter
    def selection(self, value):
        if type(value) is int:
            self.__selection = value
            self.__selection = functions.clamp(self.__selection, 0, 2)
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.selection = value: "value" needs to be an integer.'
                f"{type(value)} is not an integer."
            )

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        # Red: 128 Green: 24 Blue: 128
        colors_data = [
            [core.Sprixel(" ", core.Color(255, 0, 0)), str(self.__red)],
            [core.Sprixel(" ", core.Color(0, 255, 0)), str(self.__green)],
            [core.Sprixel(" ", core.Color(0, 0, 255)), str(self.__blue)],
        ]
        offset = 0
        row += 1
        for idx in range(0, len(colors_data)):
            data = colors_data[idx]
            col_str = str(data[1])
            buffer[row][column + offset] = data[0]
            offset += 1
            buffer[row][column + offset] = ":"
            offset += 2
            if idx == self.__selection:
                sel = Box(len(col_str) + 2, 3, config=self._config)
                sel.render_to_buffer(
                    buffer, row - 1, column + offset - 1, buffer_height, buffer_width
                )
            for c in range(offset, offset + len(col_str)):
                buffer[row][column + c] = data[1][c - offset]
            offset += len(col_str) + 1
        color = core.Color(self.__red, self.__green, self.__blue)
        self.__sprixel.bg_color = color
        buffer[row][column + offset + 1] = "="
        buffer[row][column + offset + 3] = self.__sprixel


class ColorPickerDialog(Dialog):
    def __init__(self, config) -> None:
        super().__init__(config=config)
        self.__color_picker = ColorPicker(
            orientation=constants.ORIENTATION_HORIZONTAL, config=config
        )

    def set_color(self, color: core.Color) -> None:
        if isinstance(color, core.Color):
            self.__color_picker.red = color.r
            self.__color_picker.blue = color.b
            self.__color_picker.green = color.g

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """
        :param name: some param
        :type name: str

        Example::

            method()
        """
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                27,
                5,
                "Pick a color",
                self.config,
                True,
                core.Sprixel(" ", bg_color=None),
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        self.__color_picker.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.force_update()
        self.__current_field = 0
        ret_color = core.Color()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    ret_color = core.Color(
                        self.__color_picker.red,
                        self.__color_picker.green,
                        self.__color_picker.blue,
                    )
                    break
                elif inkey.name == "KEY_ESCAPE":
                    ret_color = None
                    break
                elif inkey.name == "KEY_UP":
                    if self.__color_picker.selection == 0:
                        self.__color_picker.red += 1
                    elif self.__color_picker.selection == 1:
                        self.__color_picker.green += 1
                    elif self.__color_picker.selection == 2:
                        self.__color_picker.blue += 1
                    screen.force_update()
                elif inkey.name == "KEY_DOWN":
                    if self.__color_picker.selection == 0:
                        self.__color_picker.red -= 1
                    elif self.__color_picker.selection == 1:
                        self.__color_picker.green -= 1
                    elif self.__color_picker.selection == 2:
                        self.__color_picker.blue -= 1
                    screen.force_update()
                elif inkey.name == "KEY_LEFT":
                    self.__color_picker.selection -= 1
                    screen.force_update()
                elif inkey.name == "KEY_RIGHT":
                    self.__color_picker.selection += 1
                    screen.force_update()
            inkey = term.inkey(timeout=0.1)
        return ret_color
