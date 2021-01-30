__docformat__ = "restructuredtext"
"""
The ui module contains the classes to easily build user interface for your games.

.. Important:: It works exclusively with the screen buffer system (place, delete,
   render, update, etc.).
   It doesn't work with Screen functions like display_at().

.. autosummary::
   :toctree: .

   UiConfig
   Box
   ProgressDialog
"""
from pygamelib.assets import graphics
from pygamelib.gfx import core
from pygamelib import base


class UiConfig(object):
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


class Box(object):
    def __init__(self, width, height, title="", config=None):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__title = title
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
                "Box.config(value): value needs to be an UiConfig object."
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
        # scr.place(
        #     core.Sprixel(graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT, fg_color=color),
        #     row,
        #     column + self.__width - 1,
        # )
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


class ProgressBar(object):
    """
    A simple progress bar widget.

    :param name: some param
    :type name: str

    Example::

        method()
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
        self._build_cache()

    def _build_cache(self):
        self._cache = {
            "pb_empty": core.Sprixel(
                self.__empty_marker, self.__config.bg_color, self.__config.fg_color
            ),
            "pb_progress": core.Sprixel(
                self.__progress_marker, self.__config.bg_color, self.__config.fg_color
            ),
            "label": base.Text(
                self.__label, self.__config.fg_color, self.__config.bg_color
            ),
        }

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
        self.__config.game.screen.trigger_rendering()

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
        if self.__destroy:
            self.__config.game.screen.delete(row, column)
        lbl = core.Sprite.from_text(self._cache["label"])
        lbl.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        for c in range(0, prog):
            buffer[row + 1][column + c] = self._cache["pb_progress"]
        for c in range(prog, self.__width):
            buffer[row + 1][column + c] = self._cache["pb_empty"]
        if self.destroy_on_complete and self.__value == self.__maximum:
            self.__destroy = True


class ProgressDialog(object):
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
        super().__init__()
        self.__label = label
        self.__value = value
        self.__maximum = maximum
        self.__width = width
        self.__progress_marker = progress_marker
        self.__empty_marker = empty_marker
        self.__adaptive_width = adaptive_width
        self.destroy_on_complete = destroy_on_complete
        self.__destroy = False
        self.__config = config
        self._build_cache()

    def _build_cache(self):
        self._cache = {
            "pb_empty": core.Sprixel(
                self.__empty_marker, self.__config.bg_color, self.__config.fg_color
            ),
            "pb_progress": core.Sprixel(
                self.__progress_marker, self.__config.bg_color, self.__config.fg_color
            ),
            "label": base.Text(
                self.__label, self.__config.fg_color, self.__config.bg_color
            ),
        }
        if not self.__config.borderless_dialog:
            self._cache["borders"] = Box(self.__width, 2, self._cache["label"])

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
        if self.__destroy:
            self.__config.game.screen.delete(row, column)
        lbl = core.Sprite.from_text(self._cache["label"])
        lbl.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        for c in range(0, prog):
            buffer[row + 1][column + c] = self._cache["pb_progress"]
        for c in range(prog, self.__width):
            buffer[row + 1][column + c] = self._cache["pb_empty"]
        if self.destroy_on_complete and self.__value == self.__maximum:
            self.__destroy = True
