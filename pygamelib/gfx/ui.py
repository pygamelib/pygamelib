__docformat__ = "restructuredtext"
"""
.. autosummary::
   :toctree: .

   pygamelib.gfx.ui.UiConfig
   pygamelib.gfx.ui.Dialog
   pygamelib.gfx.ui.Box
   pygamelib.gfx.ui.ProgressBar
   pygamelib.gfx.ui.ProgressDialog
   pygamelib.gfx.ui.MessageDialog
   pygamelib.gfx.ui.LineInputDialog
   pygamelib.gfx.ui.MultiLineInputDialog
   pygamelib.gfx.ui.FileDialog
   pygamelib.gfx.ui.GridSelector
   pygamelib.gfx.ui.GridSelectorDialog
   pygamelib.gfx.ui.ColorPicker
   pygamelib.gfx.ui.ColorPickerDialog
   pygamelib.gfx.ui.MenuBar
   pygamelib.gfx.ui.Menu
   pygamelib.gfx.ui.MenuAction

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

    This object's purpose is to configure the look and feel of the UI widgets.
    It does nothing by itself.

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
    :param fg_color_inactive: The foreground color for inactive items like menu entries.
    :type fg_color_inactive: :class:`~pygamelib.gfx.core.Color`
    :param bg_color_selected: The background color (for selected text and content).
    :type bg_color_selected: :class:`~pygamelib.gfx.core.Color`
    :param bg_color_not_selected: The background color (for non selected text and
       content).
    :type bg_color_not_selected: :class:`~pygamelib.gfx.core.Color`
    :param fg_color_selected: The foreground color (for selected text and content).
    :type fg_color_selected: :class:`~pygamelib.gfx.core.Color`
    :param fg_color_not_selected: The foreground color (for non selected text and
       content).
    :type fg_color_not_selected: :class:`~pygamelib.gfx.core.Color`
    :param bg_color_menu_not_selected: The menu background color (for expanded menu
       items).
    :type bg_color_menu_not_selected: :class:`~pygamelib.gfx.core.Color`
    :param border_fg_color: The foreground color (for borders).
    :type border_fg_color: :class:`~pygamelib.gfx.core.Color`
    :param border_bg_color: The background color (for borders).
    :type border_bg_color: :class:`~pygamelib.gfx.core.Color`
    :param borderless_dialog: Is the dialog borderless or not.
    :type borderless_dialog: bool

    Example::

        config_ui_red = UiConfig(
            fg_color=Color(255,0,0),
            border_fg_color=Color(255,0,0)
        )
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
        fg_color_inactive=core.Color(128, 128, 128),
        bg_color_selected=core.Color(128, 128, 128),
        bg_color_not_selected=None,
        fg_color_selected=core.Color(0, 255, 0),
        fg_color_not_selected=core.Color(255, 255, 255),
        bg_color_menu_not_selected=core.Color(128, 128, 128),
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
        self.fg_color_inactive = fg_color_inactive
        self.bg_color_selected = bg_color_selected
        self.bg_color_not_selected = bg_color_not_selected
        self.fg_color_selected = fg_color_selected
        self.fg_color_not_selected = fg_color_not_selected
        self.bg_color_menu_not_selected = bg_color_menu_not_selected
        self.border_fg_color = border_fg_color
        self.border_bg_color = border_bg_color
        self.borderless_dialog = borderless_dialog

    @classmethod
    def instance(cls, *args, **kwargs):
        """Returns the instance of the UiConfig object

        Creates an UiConfig object on first call an then returns the same instance
        on further calls.
        Useful for a default configuration. It accepts all the parameters from the
        constructor.

        :return: Instance of Game object

        """
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance


class Dialog(object):
    """
    Dialog is a virtual class that can be subclassed to create actual dialogs.

    All classes that inherits from Dialog have the following constraints:

     * They need to implement a show() method.
     * They are automatically rendered on the second pass by the
       :class:`~pygamelib.engine.Screen` object.

    It stores the :class:`UiConfig` object and provide a helper attribute for user
    inputs.
    """

    def __init__(self, config=None) -> None:
        """
        This constructor takes only one parameter.

        :param config: The config object.
        :type config: :class:`UiConfig`.
        """
        super().__init__()
        if config is None or not isinstance(config, UiConfig):
            raise base.PglInvalidTypeException(
                "The config parameter cannot be None and needs to be a UiConfig object."
            )
        setattr(self, "_config", config)
        setattr(self, "_user_input", "")

    @property
    def config(self):
        """
        Get and set the config object (:class:`UiConfig`).
        """
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
        """
        Facility to store and retrieve the user input.
        """
        return self._user_input

    @user_input.setter
    def user_input(self, value):
        if type(value) is str:
            self._user_input = value
        else:
            raise base.PglInvalidTypeException(
                "Dialog.user_input = value: value needs to be a str."
            )

    def _store_position(self, row, column):
        self._position = [row, column]

    def show(self):  # pragma: no cover
        """
        This is a virtual method, calling it directly will only raise a
        NotImplementedError. Each class that inheritate Dialog needs to implement
        show().
        """
        raise NotImplementedError


class Box(object):
    """
    A simple object to draw a box on screen.

    The Box object's looks and feel is highly configurable through the :class:`UiConfig`
    object.
    """

    def __init__(
        self,
        width: int,
        height: int,
        title: str = "",
        config: UiConfig = None,
        fill: bool = False,
        filling_sprixel: core.Sprixel = None,
        title_alignment: int = constants.ALIGN_CENTER,
    ):
        """
        The box constructor takes the following parameters.

        :param width: The width of the box.
        :type width: int
        :param height: The height of the box.
        :type height: int
        :param title: The title of the box (encased in the top border).
        :type title: str | :class:`~base.Text`
        :param config: The configuration object.
        :type config: :class:`UiConfig`
        :param fill: A tag to tell the box object to fill its inside (or not).
        :type fill: bool
        :param filling_sprixel: If fill is True, the filling Sprixel is used to fill the
           inside of the box.
        :type filling_sprixel: :class:`~core.Sprixel`
        :param title_alignment: The alignment of the title in the top bar. It is a
           constant from the constant module and can be ALIGN_LEFT, ALIGN_RIGHT and
           ALIGN_CENTER. THIS FEATURE IS NOT YET IMPLEMENTED.
        :type title_alignment: int

        .. TODO:: Implement the title alignment.

        Example::

            config = UiConfig(bg_color=None)
            box = Box(30, 10, 'This is a box')
            screen.place(box, 20, 20)
            screen.update()
        """
        super().__init__()
        self.__width = width
        self.__height = height
        self.__title = title
        self.__fill = fill
        self.__filling_sprixel = filling_sprixel
        self.__config = config
        self._cache = {}
        self.__title_alignment = title_alignment
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
    def config(self) -> UiConfig:
        """
        Get and set the config object (:class:`UiConfig`).
        """
        return self.__config

    @config.setter
    def config(self, value: UiConfig) -> None:
        if isinstance(value, UiConfig):
            self.__config = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.config = value: value needs to be an UiConfig object."
            )

    @property
    def title(self):
        """
        Get and set the title, only accepts str or :class:`~base.Text`.
        """
        return self.__title

    @title.setter
    def title(self, value) -> None:
        if isinstance(value, base.Text) or type(value) is str:
            self.__title = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.title = value: value needs to be a Text object or str."
            )

    @property
    def width(self) -> int:
        """
        Get and set the width of the box, only accept int.
        """
        return self.__width

    @width.setter
    def width(self, value: int) -> None:
        if type(value) is int:
            self.__width = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    @property
    def height(self) -> int:
        """
        Get and set the height of the box, only accept int.
        """
        return self.__height

    @height.setter
    def height(self, value: int) -> None:
        if type(value) is int:
            self.__height = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        """Render the box from the display buffer to the frame buffer.

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
        vert_sprix = self._cache["dialog_vertical_border"]
        horiz_sprix = self._cache["dialog_horizontal_border"]
        buffer[row][column] = self._cache["top_right_corner"]
        self_width = self.__width
        self_height = self.__height
        if column + self.__width >= buffer_width:
            self.__width = buffer_width - column
        if row + self.__height >= buffer_height:
            self.__height = buffer_height - row
        if self._cache["title"].text == "":
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
        self.__width = self_width
        self.__height = self_height


class ProgressBar(object):
    """
    A simple horizontal progress bar widget.

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
        """
        :param value: The initial value parameter. It represents the progression.
        :type value: int
        :param maximum: The maximum value held by the progress bar. Any value over the
           maximum is ignored.
        :type maximum: int
        :param width: The width of the progress bar widget (in number of screen cells).
        :type width: int
        :param progress_marker: The progress marker is displayed on progression. It is
           the sprixel that fills the bar. Please see below.
        :type progress_marker: :class:`pygamelib.gfx.core.Sprixel`
        :param empty_marker: The empty marker is displayed instead of the progress
           marker when the bar should be empty (when the value is too low to fill the
           bar for example). Please see below.
        :type empty_marker: :class:`pygamelib.gfx.core.Sprixel`
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Here is a representation of were the progress and empty markers are used.
        ::

            Progress marker
               |
            [=====--------------]
                       |
                    Empty marker


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
        """
        Get and set the config object (:class:`UiConfig`).
        """
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
        """
        Get and set the progress marker, preferrably a :class:`~core.Sprixel` but could
        be a str.
        """
        return self.__progress_marker

    @progress_marker.setter
    def progress_marker(self, value):
        if isinstance(value, core.Sprixel):
            self.__progress_marker = value
            self._cache["pb_progress"] = value
        elif isinstance(value, base.Text):
            self.__progress_marker = value.text
            self._build_cache()
        elif type(value) is str:
            self.__progress_marker = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.progress_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def empty_marker(self):
        """
        Get and set the empty marker, preferrably a :class:`~core.Sprixel` but could
        be a str.
        """
        return self.__progress_marker

    @empty_marker.setter
    def empty_marker(self, value):
        if isinstance(value, core.Sprixel):
            self.__empty_marker = value
            self._cache["pb_empty"] = value
        elif isinstance(value, base.Text):
            self.__empty_marker = value.text
            self._build_cache()
        elif type(value) is str:
            self.__empty_marker = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.empty_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def value(self):
        """
        Get and set the current progress value, it has to be an int.
        """
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
        """
        Get and set the maximum possible progress, it has to be an int.
        """
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
        """Render the object from the display buffer to the frame buffer.

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
        prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        for c in range(0, prog):
            buffer[row][column + c] = self._cache["pb_progress"]
        for c in range(prog, self.__width):
            buffer[row][column + c] = self._cache["pb_empty"]


class ProgressDialog(Dialog):
    """
    ProgressDialog is a progress bar widget as a dialog (or popup). The main difference
    with a progress bar with borders is that it is automatically rendered on the second
    pass by the screen object (therefore, is visible on top of other graphical elements
    ).

    This dialog requires external interactions so it is the only dialog widget that does
    not provide a useful show() implementation. As a matter of fact, show do nothing at
    all.

    ProgressDialog is mainly a label, a box and a :class:`ProgressBar` bundled together.
    """

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
        """
        The constructor accepts the following parameters.

        :param label: A label to display on top of the progress bar.
        :type label: str | :class:`base.Text`
        :param value: The initial value parameter. It represents the progression.
        :type value: int
        :param maximum: The maximum value held by the progress bar. Any value over the
           maximum is ignored.
        :type maximum: int
        :param width: The width of the progress bar widget (in number of screen cells).
        :type width: int
        :param progress_marker: The progress marker is displayed on progression. It is
           the sprixel that fills the bar. Please see below.
        :type progress_marker: :class:`pygamelib.gfx.core.Sprixel`
        :param empty_marker: The empty marker is displayed instead of the progress
           marker when the bar should be empty (when the value is too low to fill the
           bar for example). Please see below.
        :type empty_marker: :class:`pygamelib.gfx.core.Sprixel`
        :param adaptive_width: If True, the dialog will automatically adapt to the size
           of the label.
        :type adaptive_width: bool
        :param destroy_on_complete: If True, the dialog will remove itself from the
           screen when complete (i.e: when value == maximum)
        :type destroy_on_complete:
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            # Create a default progress bar with the default configuration
            progress_dial = ProgressDialog(
                "Please wait while I'm doing something super duper important",
                config=UiConfig.instance(),
            )
            # Place the progress bar in the middle of the screen
            screen.place(
                progress_dial, screen.vcenter, screen.hcenter - int(progress_bar.width)
            )
            for progress in range(progress_dial.maximum + 1):
                # Do something useful
                progress_dial.value = progress
                screen.update()
        """
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
        """
        Get and set the label of the dialog, it has to be a str or :class:`base.Text`.
        """
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
        """
        Get and set the current progress value, it has to be an int.
        """
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
        """
        Get and set the maximum possible progress, it has to be an int.
        """
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
        """Render the object from the display buffer to the frame buffer.

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

    def show(self):  # pragma: no cover
        """
        The show method does nothing in the ProgressDialog. It is a notable exception
        and the only dialog widget in the UI module to do that.
        """
        pass


# TODO: Well... code this class
# class VerticalProgressBar(object):
#     def __init__(
#         self,
#         value=0,
#         maximum=100,
#         height=10,
#         progress_marker="#",
#         empty_marker=" ",
#         config=None,
#     ):
#         super().__init__()


class MessageDialog(Dialog):
    """
    The message dialog is a popup that can display multiple lines of text.

    It supports formatted text (:class:`base.Text`), python strings,
    :class:`pygamelib.gfx.core.Sprixel`, :class:`core.Sprite` and more generally
    anything that can be rendered on screen (i.e: posess a render_to_buffer(self, buffer
    , row, column, buffer_height, buffer_width) method).

    Each line can be aligned separately using :py:const:`constants.ALIGN_RIGHT`,
    :py:const:`constants.ALIGN_LEFT` or :py:const:`constants.ALIGN_CENTER`. Please see
    :meth:`add_line`.

    It also implements the `show()` virtual method of :class:`Dialog`.
    This method is blocking and has its own event loop. It does not return anything.

    ESC or ENTER close the dialog.

    For the moment, the full message dialog needs to be displayed on screen. There is no
    pagination, but it is going to be implemented in a future release.

    As all dialogs it also has a `user_input` property that reflects the user input. It
    is not used here however.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.

    .. TODO:: Implements pagination.

    """

    def __init__(
        self,
        data: list = None,
        width: int = 20,
        height: int = None,
        adaptive_height: bool = True,
        alignment: int = None,
        title: str = None,
        config: UiConfig = None,
    ) -> None:
        """
        :param data: A list of data to display inside the MessageDialog. Elements in
           the list can contain various data types like :class:`base.Text`, python
           strings, :class:`pygamelib.gfx.core.Sprixel`, :class:`core.Sprite`
        :type data: list
        :param width: The width of the message dialog widget (in number of screen
           cells).
        :type width: int
        :param height: The height of the message dialog widget (in number of screen
           cells).
        :type height: int
        :param adaptive_height: If True, the dialog height will be automatically adapted
           to match the content size.
        :type adaptive_height: bool
        :param alignment: The alignment to apply to the data parameter. Please use the
           constants.ALIGN_* constants. The default value is
           :py:const:`constants.ALIGN_LEFT`
        :type alignment: int
        :param title: The short title of the dialog. Only used when the dialog is not
           borderless.
        :type title: str
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            msg = MessageDialog(
                [
                    base.Text('HELP', core.Color(0,125,255), style=constants.BOLD),
                    base.Text('----', core.Color(0,125,255), style=constants.BOLD),
                    '',
                ],
                20,
                5,
                True,
                constants.ALIGN_CENTER,
            )
            msg.add_line('This is aligned on the right', constants.ALGIN_RIGHT)
            msg.add_line('This is aligned on the left')
            screen.place(msg, 10, 10)
            msg.show()

        """
        super().__init__(config=config)
        if alignment is None:
            alignment = constants.ALIGN_LEFT
        if adaptive_height is False and height is None:
            adaptive_height = True
        self.__cache = {"data": []}
        self.__width = width
        self.__height = height
        self.__adaptive_height = adaptive_height
        self.__data = list()
        if data is not None:
            for d in data:
                self.add_line(d, alignment)
        self.__title = title
        if self.__title is None:
            self.__title = ""
        elif isinstance(self.__title, base.Text):
            # cannot be a Text object as it is styled with the border style.
            self.__title = self.__title.text
        elif not (type(title) is str or isinstance(self.__title, base.Text)):
            raise base.PglInvalidTypeException("MessageDialog: title must be a str.")

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
    def height(self) -> int:
        """
        Get and set the height of the message dialog, it has to be an int.
        """
        if self.__adaptive_height:
            h = 0
            if not self.config.borderless_dialog:
                h += 2
            return len(self.__data) + h
        else:
            return self.__height

    @height.setter
    def height(self, value: int):
        if type(value) is int:
            self.__height = value
        else:
            raise base.PglInvalidTypeException(
                "MessageDialog.height = value: value needs to be an int. It is a "
                f"{type(value)}"
            )

    @property
    def title(self) -> str:
        """
        Get and set the title of the dialog, it has to be a str.
        """
        return self.__title

    @title.setter
    def title(self, value) -> None:
        if isinstance(value, base.Text):
            self.__title = value.text
        elif type(value) is str:
            self.__title = value
        else:
            raise base.PglInvalidTypeException(
                "MessageDialog.title: value needs to be a str."
            )
        self.config.game.screen.trigger_rendering()

    def add_line(self, data, alignment=constants.ALIGN_LEFT) -> None:
        """
        Add a line to the message dialog.

        The line can be any type of data that can be rendered on screen. This means that
        any object that expose a render_to_buffer(self, buffer, row, column,
        buffer_height, buffer_width) method can be added as a "line".
        Python strings are also obviously accepted.

        Here is a non-exhaustive list of supported types:

         * :class:`~pygamelib.base.Text`,
         * python strings (str),
         * :class:`~pygamelib.gfx.core.Sprixel`,
         * :class:`~pygamelib.gfx.core.Sprite`,
         * most board items,
         * etc.

        :param data: The data to add to the message dialog.
        :type data: various
        :param alignment: The alignment of the line to add.
        :type alignment: :py:const:`constants.ALIGN_RIGHT` |
           :py:const:`constants.ALIGN_LEFT` | :py:const:`constants.ALIGN_CENTER`

        Example::

            msg.add_line(
                base.Text(
                    'This is centered and very red',
                    core.Color(255,0,0),
                ),
                constants.ALGIN_CENTER,
            )
        """
        if (
            isinstance(data, core.Sprixel)
            or type(data) is str
            or isinstance(data, base.Text)
            or hasattr(data, "render_to_buffer")
        ):
            self.__data.append([data, alignment])
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                f"MessageDialog.add_line(data, alignment): 'data' type {type(data)} is"
                " not supported"
            )

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        render_string = functions.render_string_to_buffer
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            self.__cache["border"].render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )
        for idx in range(len(self.__cache["data"])):
            padding = 0
            alignment = self.__data[idx][1]
            data = self.__data[idx][0]
            if alignment == constants.ALIGN_RIGHT:
                if type(data) is str:
                    padding = self.__width - len(data) - 2
                elif hasattr(data, "length"):
                    padding = self.__width - data.length - 2
            elif alignment == constants.ALIGN_CENTER:
                if type(data) is str:
                    padding = int((self.__width - len(data) - 2) / 2)
                elif hasattr(data, "length"):
                    padding = int((self.__width - data.length - 2) / 2)
            if isinstance(self.__cache["data"][idx], core.Sprixel):
                # TODO: Manage the Sprixels that have a size > 1
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

    def show(self) -> None:  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns the key pressed .

        Example::

            key_pressed = msg.show()
            if key_pressed.name = 'KEY_ENTER':
                // do something
            else:
                print('Good bye')
        """
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
        screen.delete(self._position[0], self._position[1])
        return inkey


class LineInputDialog(Dialog):
    """
    The LineInputDialog allows the user to enter and edit a single line of text.

    This dialog can be configured to accept either anything printable or only digits.

    The show() method returns the user input.

    **Key mapping**:

     * ESC: set the user input to "" and exit from the :meth:`show()` method.
     * ENTER: Exit from the :meth:`show()` method. Returns the user input.
     * BACKSPACE / DELETE: delete a character (both keys have the same result)
     * All other keys input characters in the input field.

    In all cases, when the dialog is closed, the user input is returned.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.

    """

    def __init__(
        self,
        title=None,
        label="Input a value:",
        default="",
        filter=constants.PRINTABLE_FILTER,
        config=None,
    ) -> None:
        """
        :param title: The short title of the dialog. Only used when the dialog is not
           borderless.
        :type title: str
        :param label: The label of the dialog (usually a one line instruction).
        :type label: str | :class:`base.Text`
        :param default: The default value in the input field.
        :type default: str
        :param filter: Sets the type of accepted input. It comes from the
           :mod:`constants` module.
        :type filter: :py:const:`constants.PRINTABLE_FILTER` |
           :py:const:`constants.INTEGER_FILTER`
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            line_input = LineInputDialog(
                "Name the pet",
                "Enter the name of your pet:",
                "Stupido",
            )
            screen.place(line_input, 10, 10)
            pet_name = line_input.show()
        """
        super().__init__(config=config)
        self.__title = title
        self.__label = label
        self.__default = default
        self.__filter = filter
        if self.__title is None:
            self.__title = ""
        elif isinstance(self.__title, base.Text):
            # cannot be a Text object as it is styled with the border style.
            self.__title = self.__title.text
        elif not (type(title) is str or isinstance(self.__title, base.Text)):
            raise base.PglInvalidTypeException("LineInputDialog: title must be a str.")
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
    def label(self) -> base.Text:
        """
        Get and set the label of the dialog, it has to be a str or :class:`base.Text`.
        """
        return self.__label

    @label.setter
    def label(self, value) -> None:
        if isinstance(value, base.Text):
            self.__label = value
        elif type(value) is str:
            self.__label = base.Text(value)
        else:
            raise base.PglInvalidTypeException(
                "LineInputDialog.label: value needs to be a str or pygamelib.base.Text."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def title(self) -> str:
        """
        Get and set the title of the dialog, it has to be a str.
        """
        return self.__title

    @title.setter
    def title(self, value) -> None:
        if isinstance(value, base.Text):
            self.__title = value.text
        elif type(value) is str:
            self.__title = value
        else:
            raise base.PglInvalidTypeException(
                "LineInputDialog.title: value needs to be a str."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(self.__label.length + 2, 4, config=self.config, title=self.title)
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lbl = core.Sprite.from_text(self.__label)
        lbl.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )
        inp = core.Sprite.from_text(base.Text(f"> {self.user_input}"))
        inp.render_to_buffer(
            buffer, row + 1 + offset, column + offset, buffer_height, buffer_width
        )

    def show(self):  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns the either "" or what is displayed in the input field.

        Example::

            value = line_input.show()
        """
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
        screen.delete(self._position[0], self._position[1])
        return self.user_input


class MultiLineInputDialog(Dialog):
    """
    The MultiLineInputDialog behave essentially like the :class:`LineInputDialog` but is
    more configurable to allow the user to enter and edit a multiple lines of text.

    Each field of this dialog can be individually configured to accept either anything
    printable or only digits.

    The show() method returns the user input.

    **Key mapping**:

     * ESC: set the user input to "" and exit from the :meth:`show()` method.
     * ENTER: Exit from the :meth:`show()` method. Returns the user input.
     * BACKSPACE / DELETE: delete a character (both keys have the same result).
     * TAB: cycle through the fields.
     * All other keys input characters in the input field.

    In all cases, when the dialog is closed, the user input is returned.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.
    """

    def __init__(
        self,
        fields=[
            {
                "label": "Input a value:",
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
            }
        ],
        title: str = None,
        config=None,
    ) -> None:
        """
        :param fields: A list of dictionnary that represent the fields to present to the
           user. Please see bellow for a description of the dictionnary.
        :type fields: list
        :param title: The short title of the dialog. Only used when the dialog is not
           borderless.
        :type title: str
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        The fields needs to be a list that contains dictionaries. Each of the
        dictionaries needs to contain 3 fields:

         * "label": A one line instruction displayed over the field. This is a string.
         * "default": A string that is going to pre-fill the input field.
         * "filter": A filter to configure the acceptable inputs.

        The filters are coming from the constants module and can be either
        :py:const:`constants.INTEGER_FILTER` or :py:const:`constants.PRINTABLE_FILTER`.

        Example::

            fields = [
                {
                    "label": "Enter the height of the new sprite:",
                    "default": "",
                    "filter": constants.INTEGER_FILTER,
                },
                {
                    "label": "Enter the width of the new sprite:",
                    "default": "",
                    "filter": constants.INTEGER_FILTER,
                },
                {
                    "label": "Enter the name of the new sprite:",
                    "default": f"Sprite {len(sprite_list)}",
                    "filter": constants.PRINTABLE_FILTER,
                },
            ]
            multi_input = MultiLineInput(fields, conf)
            screen.place(multi_input, 10, 10)
            completed_fields = multi_input.show()
        """
        super().__init__(config=config)
        self.__title = title
        self.__fields = fields
        if self.__fields is None or not (type(self.__fields) is list):
            raise base.PglInvalidTypeException(
                "MultiInputDialog: fields must be a list of dictionaries."
            )
        if self.__title is None:
            self.__title = ""
        elif isinstance(self.__title, base.Text):
            # cannot be a Text object as it is styled with the border style.
            self.__title = self.__title.text
        elif not (type(title) is str or isinstance(self.__title, base.Text)):
            raise base.PglInvalidTypeException(
                "MultiLineInputDialog: title must be a str."
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
        """
        Get and set the fields of the dialog, see the constructor for the format or this
        list.
        """
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

    @property
    def title(self) -> str:
        """
        Get and set the title of the dialog, it has to be a str.
        """
        return self.__title

    @title.setter
    def title(self, value) -> None:
        if isinstance(value, base.Text):
            self.__title = value.text
        elif type(value) is str:
            self.__title = value
        else:
            raise base.PglInvalidTypeException(
                "MultiLineInputDialog.title: value needs to be a str."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(
        self, buffer, row, column, buffer_height, buffer_width
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
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
                max_text_width + 2,
                len(self.__fields) * 2 + 2,
                config=self.config,
                title=self.title,
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

    def show(self):  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns a list of dictionaries with the content of each
        fields. The list of dictionaries is the same than the fields constructor
        parameter but each key has an additional 'user_input' field that contains the
        user input.

        If the fields parameter was:

        ::

            [
                {
                    "label": "Input a value:",
                    "default": "",
                    "filter": constants.PRINTABLE_FILTER,
                }
            ]

        The returned value would be:

        ::

            [
                {
                    "label": "Input a value:",
                    "default": "",
                    "filter": constants.PRINTABLE_FILTER,
                    "user_input": "some input",
                }
            ]

        Example::

            fields = multi_input.show()
        """
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
        screen.delete(self._position[0], self._position[1])
        return self.__fields


class FileDialog(Dialog):
    """
    The FileDialog is a file selection dialog: it allow the user to select a file on
    disk in a relatively easy way. File can then be use for any purpose by the program,
    like for "save as" or "open" features.

    The show() method returns the path selected by the user.

    **Key mapping**:

     * ESC: set the path to None and exit from the :meth:`show()` method.
     * ENTER: Exit from the :meth:`show()` method. Returns the currently selected path.
     * BACKSPACE / DELETE: delete a character (both keys have the same result).
     * UP / DOWN: Navigate between the files.
     * LEFT / RIGHT: Navigate between the directories.
     * All other keys input characters in the input field.

    In all cases, when the dialog is closed, a path is returned. It can be a file name
    entered by the user or an existing file. The returned value can also be None if the
    user pressed ESC. There is no guarantee that the returned path is correct. Please,
    check it before doing anything with it.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.
    """

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
        """

        :param path: The path to start in. This path is made absolute by the
           constructor.
        :type path: :class:`pathlib.Path`
        :param width: The width of the file dialog widget (in number of screen cells).
        :type width: int
        :param height: The height of the file dialog widget (in number of screen cells).
        :type height: int
        :param title: The title of the dialog (written in the upper border).
        :type title: str
        :param show_hidden_files: Does the file dialog needs to show the hidden files or
            not.
        :type show_hidden_files: bool
        :param filter: A string that will be used to filter the files shown to the user.
            For example "\*.spr".
        :type filter: str
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            file_dialog = FileDialog( Path("."), 30, 10, "Open file", False, conf)
            screen.place(file_dialog, 10, 10)
            file = file_dialog.show()
        """
        super().__init__(config=config)
        self.__path = None
        if path is not None and isinstance(path, Path):
            self.__path = path.resolve()
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
        # self.__current_panel = 0
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
        try:
            self.__files = sorted(
                [
                    x
                    for x in self.__path.iterdir()
                    if (
                        x.is_dir()
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
        # Cannot be reliably tested in CI env. PR are welcomed!
        except PermissionError:  # pragma: no cover
            # TODO: Send a message to the user about that
            pass

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
        Get/set the current path.

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
        Get/set the current file filter.

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
        Get/set the property, if True the file dialog is going to show hidden files, and
        , if False, it won't.

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
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        # TODO: The actual dialog size is bigger than the the one passed in parameter
        #       because I add to the size (for the file name) instead of drawing INTO
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
                if i.is_file():
                    # Can't be tested since the widget do not offer the ability to
                    # manipulate __browsing_position from the outside.
                    self.user_input = i.name  # pragma: no cover
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

    def show(self) -> Path:  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns a :class:`pathlib.Path` object or None if the user
        pressed the ESC key. The path can point to an existing file or not.

        Example::

            fields = multi_input.show()
        """
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
                    if self.user_input is not None and self.user_input != "":
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
                # NOTE: I have no idea what was the idea behind that current panel
                # thing...
                # elif inkey.name == "KEY_TAB":
                #     self.__current_panel += 1
                #     self.__current_panel = self.__current_panel % 2
                #     screen.trigger_rendering()
                #     screen.update()
                elif inkey.name == "KEY_ESCAPE":
                    self.__path = None
                    break
                elif inkey.name == "KEY_UP":
                    if len(self.__files) > 0:
                        self.__browsing_position -= 1
                        self.__browsing_position = functions.clamp(
                            self.__browsing_position, 0, len(self.__files) - 1
                        )
                        next_file = self.__path / self.__files[self.__browsing_position]
                        if next_file.is_file():
                            self.user_input = next_file.name
                        screen.trigger_rendering()
                        screen.update()
                elif inkey.name == "KEY_DOWN":
                    if len(self.__files) > 0:
                        self.__browsing_position += 1
                        self.__browsing_position = functions.clamp(
                            self.__browsing_position, 0, len(self.__files) - 1
                        )
                        next_file = self.__path / self.__files[self.__browsing_position]
                        if next_file.is_file():
                            self.user_input = next_file.name
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
                elif inkey.name == "KEY_RIGHT":
                    if tmpp.is_dir():
                        self.__path = tmpp.resolve()
                        self.user_input = ""
                        self._build_file_cache()
                        self.__browsing_position = 0
                        screen.trigger_rendering()
                        screen.update()
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.user_input = self.user_input[:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.isprintable():
                    self.user_input += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        screen.delete(self._position[0], self._position[1])
        return self.__path


class GridSelector(object):
    """
    The GridSelector is a widget that present a list of elements as a grid to the user.

    It also provides the API to draw and manage the cursor and to retrieve the selected
    element.

    .. WARNING:: In the first version of that widget, only the characters that have a
        length of 1 are supported. This excludes some UTF8 characters and most of the
        emojis.

    """

    def __init__(
        self,
        choices: list = None,
        max_height: int = None,
        max_width: int = None,
        config: UiConfig = None,
    ) -> None:
        """
        :param choices: A list of choices to present to the user. The elements of the
           list needs to be str or :class:`~pygamelib.gfx.core.Sprixel`.
        :type choices: list
        :param max_height: The maximum height of the grid selector.
        :type max_height: int
        :param max_width: The maximum width of the grid selector.
        :type max_width: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            choices = ["@","#","$","%","&","*","[","]"]
            grid_selector = GridSelector(choices, 10, 30, conf)
            screen.place(grid_selector, 10, 10)
            screen.update()
        """
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
        # config.game.log(f"items per page={self.__items_per_page}")

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
    def choices(self) -> int:
        """
        Get and set the list of choices, it has to be a list of
        :class:`~pygamelib.gfx.core.Sprixel` or str.
        """
        return self.__choices

    @choices.setter
    def choices(self, value):
        """
        Get and set the list of choices, it has to be a list of
        :class:`~pygamelib.gfx.core.Sprixel` or str.
        """
        if type(value) is list:
            self.__choices = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.choices = value: 'value' must be a list. "
                f"'{value}' is not a list"
            )

    @property
    def max_height(self) -> int:
        """
        Get and set the maximum height of the grid selector, it needs to be an int.
        """
        return self.__max_height

    @max_height.setter
    def max_height(self, value):
        if type(value) is int:
            self.__max_height = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.max_height = value: 'value' must be an int. "
                f"'{value}' is not an int"
            )

    @property
    def max_width(self) -> int:
        """
        Get and set the maximum width of the grid selector, it needs to be an int.
        """
        return self.__max_width

    @max_width.setter
    def max_width(self, value):
        if type(value) is int:
            self.__max_width = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.max_width = value: 'value' must be an int. "
                f"'{value}' is not an int"
            )

    @property
    def current_choice(self) -> int:
        """
        Get and set the currently selected item's index (the current choice), it needs
        to be an int.
        Use :meth:`current_sprixel` to get the actual current item.
        """
        return self.__current_choice

    @current_choice.setter
    def current_choice(self, index: int = None):
        if type(index) is int:
            # self.__current_choice = functions.clamp(index, 0, len(self.__cache) - 1)
            clp = functions.clamp(
                index,
                self.current_page * self.items_per_page(),
                min(
                    (self.current_page + 1) * self.items_per_page() - 1,
                    len(self.__cache) - 1,
                ),
            )
            if clp == index:
                self.__current_choice = clp
        else:
            raise base.PglInvalidTypeException(
                "GridSelector.set_selected(index): 'index' must be an int. "
                f"'{index}' is not an int"
            )

    @property
    def current_page(self) -> int:
        """
        Get and set the current page of the grid selector, it needs to be an int.
        """
        return self.__current_page

    @current_page.setter
    def current_page(self, value: int):
        if type(value) is int:
            self.__current_page = functions.clamp(
                value, 0, round(len(self.__cache) / self.__items_per_page)
            )
            # There's on particular case: when we have less items than space per page
            if len(self.__cache) <= self.__items_per_page:
                self.__current_page = 0
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

    def cursor_up(self) -> None:
        """
        Move the selection cursor one row up.
        """
        self.current_choice -= round(self.max_width / 2)

    def cursor_down(self) -> None:
        """
        Move the selection cursor one row down.
        """
        self.current_choice += round(self.max_width / 2)

    def cursor_left(self) -> None:
        """
        Move the selection cursor one column to the left.
        """
        self.current_choice -= 1

    def cursor_right(self) -> None:
        """
        Move the selection cursor one column to the right.
        """
        self.current_choice += 1

    def page_up(self) -> None:
        """
        Change the current page to the one immediately up (current_page - 1).
        """
        self.current_page -= 1

    def page_down(self) -> None:
        """
        Change the current page to the one immediately down (current_page + 1).
        """
        self.current_page += 1

    def current_sprixel(self) -> core.Sprixel:
        """
        Returns the currently selected sprixel.
        """
        return self.__cache[self.__current_choice]

    def items_per_page(self) -> int:
        """
        Returns the number of items per page.

        """
        return self.__items_per_page

    def nb_pages(self) -> int:
        """
        Returns the number of pages.
        """
        count = len(self.__cache) / self.items_per_page()
        if count > int(count):
            count = int(count) + 1
        else:
            count = round(count)
        return count

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        # TODO: The following line is a hack, I do not yet know why the first cell
        #       is not cleared when re-rendered (the coordinates calculation is probably
        #       wrong somewhere).
        buffer[row][column] = " "
        self.__max_width = functions.clamp(self.__max_width, 0, buffer_width - 2)
        self.__max_height = functions.clamp(self.__max_height, 0, buffer_height - 2)
        crow = 1
        ccol = 1
        col_offset = 1
        row_offset = 1
        start = self.__current_page * self.__items_per_page
        for i in range(start, len(self.__cache)):
            buffer[row + row_offset][column + col_offset] = self.__cache[i]
            # if i == self.__current_choice % len(self.__choices):
            if i == self.__current_choice % len(self.__cache):
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
            # This cannot be covered yet because no character with a length > 1 is built
            # into the cache. This needs to be removed when support for characters with
            # length > 1.
            for xtr in range(1, self.__cache[i].length):  # pragma: no cover
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
    """
    The GridSelectorDialog is an easy wrapper around the :class:`GridSelector` object.
    It offers a simple interface for the programmer to present a :class:`GridSelector`
    to the user and retrieve its selection.

    The show() method returns the path selected by the user.

    **Key mapping**:

     * ESC: set the selected item to an empty Sprixel and exit from the show() method.
     * ENTER: Exit from the show() method. Returns the currently selected sprixel.
     * UP / DOWN / LEFT / RIGHT: Navigate between the files.
     * PAGE_UP / PAGE_DOWN: Go to previous / next page if there's any.

    In all cases, when the dialog is closed, a :class:`~pygamelib.gfx.core.Sprixel` is
    returned.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.
    """

    def __init__(
        self,
        choices: list = None,
        max_height: int = None,
        max_width: int = None,
        title: str = None,
        config: UiConfig = None,
    ) -> None:
        """
        :param choices: A list of choices to present to the user. The elements of the
           list needs to be str or :class:`~pygamelib.gfx.core.Sprixel`.
        :type choices: list
        :param max_height: The maximum height of the grid selector.
        :type max_height: int
        :param max_width: The maximum width of the grid selector.
        :type max_width: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            choices = ["@","#","$","%","&","*","[","]"]
            grid_dialog = GridSelector(choices, 10, 30, conf)
            screen.place(grid_dialog, 10, 10)
            grid_dialog.show()
        """
        super().__init__(config=config)
        self.__grid_selector = None
        if not config.borderless_dialog:
            self.__grid_selector = GridSelector(
                choices, max_height - 3, max_width - 4, config
            )
        else:
            self.__grid_selector = GridSelector(choices, max_height, max_width, config)
        self.__title = ""
        if title is not None and type(title) is str:
            self.__title = title

    @property
    def title(self):
        """
        Get / set the title of the dialog, it needs to be a str.
        """
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
        """
        Get / set the GridSelector object, it has to be a
        :class:`~pygamelib.gfx.ui.GridSelector` object.
        """
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

    def show(self):  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns the selected item as a
        :class:`~pygamelib.gfx.core.Sprixel` or None if the user pressed the ESC key.

        :return: The selected item.
        :rtype: :class:`~pygamelib.gfx.core.Sprixel`

        Example::

            item = grid_dialog.show()
        """
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
                    ret_sprixel = None
                    break
                elif inkey.name == "KEY_UP":
                    self.__grid_selector.cursor_up()
                    screen.force_update()
                elif inkey.name == "KEY_DOWN":
                    self.__grid_selector.cursor_down()
                    screen.force_update()
                elif inkey.name == "KEY_LEFT":
                    self.__grid_selector.cursor_left()
                    screen.force_update()
                elif inkey.name == "KEY_RIGHT":
                    self.__grid_selector.cursor_right()
                    screen.force_update()
                elif inkey.name == "KEY_PGDOWN":
                    self.__grid_selector.page_down()
                    screen.force_update()
                elif inkey.name == "KEY_PGUP":
                    self.__grid_selector.page_up()
                    screen.force_update()

            inkey = term.inkey(timeout=0.1)
        screen.delete(self._position[0], self._position[1])
        return ret_sprixel

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                self.__grid_selector.max_width + 4,
                self.__grid_selector.max_height + 3,
                self.__title,
                self.config,
                True,
                core.Sprixel(" ", bg_color=None),
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
            # TODO: It looks like there is a bug in the pagination.
            gs = self.__grid_selector
            # Pages are numbered from 0.
            pagination = f"{gs.current_page+1}/{gs.nb_pages()}"
            lp = len(pagination)
            for c in range(0, lp):
                buffer[row + self.__grid_selector.max_height + 2][
                    column + self.__grid_selector.max_width + 2 - lp + c
                ] = pagination[c]
        self.__grid_selector.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )


class ColorPicker(object):
    """
    The ColorPicker widget is a simple object to select the red, green and blue
    components of a color.

    It provides the API to set/get each color channel independently as well as the
    mechanism to select and draw a selection box around one specific channel to give the
    user a visual cue about what he is modifying.
    """

    def __init__(self, orientation: int = None, config: UiConfig = None) -> None:
        """
        The constructor is really simple and takes only 2 arguments.

        :param orientation: One of the 2 orientation constants
           :py:const:`pygamelib.constants.ORIENTATION_HORIZONTAL` or
           :py:const:`pygamelib.constants.ORIENTATION_VERTICAL`
        :type orientation: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        The default orientation is horizontal.

        .. WARNING:: The orientation parameter is ignored for the moment.

        Example::

            color_picker = ColorPicker(constants.ORIENTATION_HORIZONTAL, conf)
            screen.place(color_picker, 10, 10)
            screen.update()
        """
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
        """
        Get / set the edited color.

        The setter automatically forward the individual red, green and blue values to
        to the proper properties of that widget.

        :param value: The color object.
        :type value: :class:`~pygamelib.gfx.core.Color`

        Example::

            current_color = color_picker.color
            current_color.r += 10
            color_picker.color = current_color
        """
        return core.Color(self.__red, self.__green, self.__blue)

    @color.setter
    def color(self, value):
        if isinstance(value, core.Color):
            self.__red = value.r
            self.__green = value.g
            self.__blue = value.b
        else:
            raise base.PglInvalidTypeException(
                'ColorPicker.color = value: "value" needs to be a Color object.'
                f"{type(value)} is not a color object."
            )

    @property
    def red(self):
        """
        Get / set the red component of the color, the value needs to be an int between 0
        and 255.
        """
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
        """
        Get / set the green component of the color, the value needs to be an int between
        0 and 255.
        """
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
        """
        Get / set the blue component of the color, the value needs to be an int between
        0 and 255.
        """
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
        """
        Get / set the selection, it needs to be an int between 0 and 2 included.

        0 correspond to the red channel, 1 to the green channel and 2 to the blue
        channel.

        When this widget is rendered a :class:`~pygamelib.gfx.ui.Box` will be rendered
        around the specified channel.
        """
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
        """Render the object from the display buffer to the frame buffer.

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
        # TODO: implement the vertical orientation
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
    """
    The ColorPickerDialog is a dialog wrapper around the :class:`ColorPicker` widget.

    It serves the same purpose: present a way to easily select a custom color to the
    user.

    It does it as an immediately usable dialog.

    The show() method returns the :class:`~pygamelib.gfx.core.Color` selected by the
    user. If the user pressed the ESC key, it returns None.

    **Key mapping**:

     * ESC: Exit from the show() method and return None.
     * ENTER: Exit from the show() method. Returns the currently selected color.
     * UP / DOWN: Increase/decrease the currently selected channel by 1.
     * PAGE_UP / PAGE_DOWN: Increase/decrease the currently selected channel by 10.
     * LEFT / RIGHT: Navigate between color channels.

    Like all dialogs, it is automatically destroyed on exit of the :meth:`show()`
    method. It is also deleted from the screen buffer.
    """

    def __init__(self, title: str = None, config: UiConfig = None) -> None:
        """
        The constructor only take the configuration as parameter.

        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example::

            color_dialog = ColorPickerDialog(conf)
            color_dialog.set_color( core.Color(128, 128, 128) )
            screen.place(color_dialog, 10, 10)
            new_color = color_dialog.show()
        """
        super().__init__(config=config)
        self.__color_picker = ColorPicker(
            orientation=constants.ORIENTATION_HORIZONTAL, config=config
        )
        self.__title = title
        if self.__title is None:
            self.__title = "Pick a color"

    @property
    def title(self):
        """
        Get / set the dialog title, it needs to be a str.
        """
        return self.__title

    @title.setter
    def title(self, value):
        if value is not None and type(value) is str:
            self.__title = value
        else:
            raise base.PglInvalidTypeException(
                "ColorPickerDialog.title = value: 'value' must be a str. "
                f"'{value}' is not a str"
            )

    def set_color(self, color: core.Color) -> None:
        """
        Set the color shown in the dialog.

        :param color: The color to edit.
        :type color: :class:`~pygamelib.gfx.core.Color`

        Example::

            color_dialog.set_color( core.Color(128, 128, 128) )
        """
        if isinstance(color, core.Color):
            self.__color_picker.red = color.r
            self.__color_picker.blue = color.b
            self.__color_picker.green = color.g

    def set_selection(self, selection: int = 0):
        """
        Set the channel selection.

        :param selection: The number of the channel to select (0 = red, 1 = green and 2
           = blue).
        :type selection: int

        Example::

            color_dialog.set_selection(1)
        """
        self.__color_picker.selection = selection

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                27,
                5,
                self.title,
                self.config,
                True,
                core.Sprixel(" ", bg_color=None),
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        self.__color_picker.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )

    def show(self):  # pragma: no cover
        """
        Show the dialog and execute the event loop.
        Until this method returns, all keyboards event are processed by the local event
        loop. This is also true if called from the main event loop.

        This event loop returns the edited :class:`~pygamelib.gfx.core.Color` or None
        if the user pressed the ESC key.

        :return: The editor color.
        :rtype: :class:`~pygamelib.gfx.core.Color`

        Example::

            new_color = color_dialog.show()
        """
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
                elif inkey.name in ["KEY_UP", "KEY_DOWN", "KEY_PGDOWN", "KEY_PGUP"]:
                    value = 0
                    if "PG" in inkey.name:
                        value = 10
                    else:
                        value = 1
                    if "DOWN" in inkey.name:
                        value *= -1
                    if self.__color_picker.selection == 0:
                        self.__color_picker.red += value
                    elif self.__color_picker.selection == 1:
                        self.__color_picker.green += value
                    elif self.__color_picker.selection == 2:
                        self.__color_picker.blue += value
                    screen.force_update()
                elif inkey.name == "KEY_LEFT":
                    self.__color_picker.selection -= 1
                    screen.force_update()
                elif inkey.name == "KEY_RIGHT":
                    self.__color_picker.selection += 1
                    screen.force_update()
            inkey = term.inkey(timeout=0.1)
        screen.delete(self._position[0], self._position[1])
        return ret_color


class MenuAction(object):
    """
    A menu action is a menu entry that executes a callback when activated. Usually a
    Menuaction represents an action from the user interface like open file, save, quit,
    etc.

    Therefor a MenuAction is fairly simple, at its simplest it has a title and a
    callable reference to a function.

    An action cannot be used by itself but can be added to a :class:`MenuBar` or a
    :class:`Menu`.

    Like everything in the UI module, MenuAction are styled through a :class:`UiConfig`
    object. Unlike the other classes of that module however, the configuration object is
    not mandatory when instanciating this class. The reason is that the :class:`MenuBar`
    object impose the configuration to its managed :class:`MenuAction` and
    :class:`Menu`.
    """

    def __init__(
        self,
        title: base.Text = None,
        action=None,
        parameter=None,
        padding: int = 1,
        config: UiConfig = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param title: The title of the action (i.e: its label)
        :type title: str | :class:`~pygamelib.base.Text`
        :param action: A reference to a callable function that is going to be executed
           when the action is activated. If set to None, nothing will happen when the
           action is activated.
        :type action: callable
        :param parameter: A parameter that is passed to the callback action if not None.
        :type parameter: Any
        :param padding: The horizontal padding, i.e the number of space characters added
           to the left and right of the action.
        :type padding: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example ::

            menubar = MenuBar(config=UiConfig.instance())
            file_menu = Menu(
                "File",
                [
                    MenuAction("Open", open_file),
                    MenuAction("Save", save_file),
                    MenuAction("Save as", save_file_as),
                    MenuAction("Quit", exit_application),
                ]
            )
            menubar.add_entry( file_menu )
            menubar.add_entry( MenuAction("Help", display_help) )
            screen.place(menubar, 0, 0)
            screen.update()
        """
        super().__init__()
        self.__config = config
        self.__selected = False
        self.__title = None
        self.__padding = padding
        self._parent = None
        self.__parameter = parameter
        # TODO: Check types.
        self.__padding_cache = base.Text(" " * self.__padding)
        if isinstance(title, base.Text):
            self.__title = title
        elif type(title) is str:
            self.__title = base.Text(title)
        else:
            raise base.PglInvalidTypeException(
                "MenuAction(): title needs to be a pygamelib.base.Text object."
            )
        self.__action = None
        if callable(action) or action is None:
            self.__action = action
        else:
            raise base.PglInvalidTypeException(
                "MenuAction(): action needs to be a callable function reference."
            )

    @property
    def title(self) -> base.Text:
        """
        Get / set the title of the action, it needs to be a str or a
        :class:`~pygamelib.base.Text` object.

        The title is used in the :class:`Menu`. In the following image, the title of
        the first action in the expanded menu is "Open", followed by "Save".

        .. image:: menu.png
           :alt: menu
        """
        return self.__title

    @title.setter
    def title(self, value: base.Text):
        if isinstance(value, base.Text):
            self.__title = value
        elif type(value) is str:
            self.__title = base.Text(value)
        else:
            raise base.PglInvalidTypeException(
                "Menu.title = value: value needs to be a pygamelib.base.Text object."
            )

    @property
    def action(self):
        """
        Get / set the action's callback, it needs to be a callable.
        """
        return self.__action

    @action.setter
    def action(self, value):
        if callable(value):
            self.__action = value
        else:
            raise base.PglInvalidTypeException(
                "Menu.action = value: value needs to be a callable function reference."
            )

    @property
    def config(self):
        """
        Get / set the config of the MenuAction, it needs to be a :class:`UiConfig`.
        """
        return self.__config

    @config.setter
    def config(self, value: UiConfig):
        if isinstance(value, UiConfig):
            self.__config = value
        else:
            raise base.PglInvalidTypeException(
                "MenuAction.config = value: value needs to be a "
            )

    @property
    def selected(self) -> bool:
        """
        Get / set the selected of the MenuAction, it needs to be a boolean.

        This changes the representation (way it's drawn) of the menu entry.
        """
        return self.__selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if type(value) is bool:
            self.__selected = value
            if self.config is not None:
                if self.__selected:
                    self.title.bg_color = self.config.bg_color_selected
                    self.title.fg_color = self.config.fg_color_selected
                    self.__padding_cache.bg_color = self.config.bg_color_selected
                    self.__padding_cache.fg_color = self.config.fg_color_selected
                else:
                    if isinstance(self._parent, Menu):
                        self.title.bg_color = self.config.bg_color_menu_not_selected
                        self.__padding_cache.bg_color = (
                            self.config.bg_color_menu_not_selected
                        )
                    else:
                        self.title.bg_color = self.config.bg_color_not_selected
                        self.__padding_cache.bg_color = (
                            self.config.bg_color_not_selected
                        )
                    self.title.fg_color = self.config.fg_color_not_selected
                    self.__padding_cache.fg_color = self.config.fg_color_not_selected
        else:
            raise base.PglInvalidTypeException(
                "MenuAction.selected = value: value needs to be a bool"
            )

    def activate(self):  # pragma: no cover
        """
        Execute and return the result of the callback.

        Example::

            file_save_action.activate()
        """
        if callable(self.__action):
            if self.__parameter is not None:
                return self.__action(self.__parameter)
            else:
                return self.__action()

    @property
    def padding(self):
        """
        Get / set the padding before and after the menu action, it needs to be an int.
        """
        return self.__padding

    @padding.setter
    def padding(self, value):
        if type(value) is int:
            self.__padding = value
            self.__padding_cache = base.Text(" " * self.__padding)
        else:
            raise base.PglInvalidTypeException(
                "MenuAction.padding = value: value needs to be an int."
            )

    def title_width(self):
        """
        Return the actual width of the action's title. This takes into account the
        padding.

        Example::

            menu_action.title_width()
        """
        return self.__title.length + self.__padding_cache.length * 2

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        if self.padding > 0:
            self.__padding_cache.render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )
            self.__title.render_to_buffer(
                buffer, row, column + self.__padding, buffer_height, buffer_width
            )
            self.__padding_cache.render_to_buffer(
                buffer,
                row,
                column + self.title_width() - self.__padding_cache.length,
                buffer_height,
                buffer_width,
            )
        else:
            self.__title.render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )


class Menu(object):
    """
    The Menu object consists of a list of other Menu objects and/or :class:`MenuAction`
    objects.

    It has a title that is used in a :class:`MenuBar` and the list of its entries is
    displayed when the menu is expanded.

    A Menu object can contains an arbitrary number of entries with an arbitrary depth of
    submenus.
    """

    def __init__(
        self,
        title: base.Text = None,
        entries: list = None,
        padding: int = 1,
        config: UiConfig = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param title: The title of the action (i.e: its label)
        :type title: str | :class:`~pygamelib.base.Text`
        :param entries: A list of :class:`MenuAction` or other Menu objects.
        :type entries: list
        :param padding: The horizontal padding, i.e the number of space characters added
           to the left and right of the title.
        :type padding: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`

        Example ::

            menubar = MenuBar(config=UiConfig.instance(game=Game.instance()))
            file_menu = Menu(
                "File",
                [
                    MenuAction("Open", open_file),
                    MenuAction("Save", save_file),
                    MenuAction("Save as", save_file_as),
                    MenuAction("Quit", exit_application),
                ]
            )
            menubar.add_entry( file_menu )
            menubar.add_entry( MenuAction("Help", display_help) )
            screen.place(menubar, 0, 0)
            screen.update()
        """
        super().__init__()
        self.__title = title
        self.__config = config
        self.__padding = padding
        self.__selected = False
        self.__entries = []
        self._position = []
        self._parent = None
        self.__current_index = -1
        self.__expanded = False
        # TODO: Check types. Again...
        self.__padding_cache = base.Text(" " * self.__padding)
        self.__menu_width_padding_cache = base.Text(" ")
        if isinstance(title, base.Text):
            self.__title = title
        elif type(title) is str:
            self.__title = base.Text(title)
        else:
            raise base.PglInvalidTypeException(
                "Menu title needs to be a pygamelib.base.Text object."
            )
        if entries is not None:
            for entry in entries:
                if isinstance(entry, MenuAction) or isinstance(entry, Menu):
                    entry._parent = self
                    if config is not None:
                        entry.config = config
                    entry.selected = False
                    self.__entries.append(entry)
                else:
                    raise base.PglInvalidTypeException(
                        "Menu(entries=list_of_entries): each entry must be a MenuAction"
                        " or a Menu object."
                    )

    def _store_position(self, row, column):
        self._position = [row, column]

    def add_entry(self, entry):
        """
        Add an entry to the menu. An entry can be a :class:`MenuAction` or a
        :class:`Menu`.
        Entries are displayed in the order of there additions from left to right.

        .. IMPORTANT:: The config of the entry is overwritten by the config of the
           Menu. That is why it's not mandatory for :class:`Menu` and
           :class:`MenuAction`.

        :param entry: The entry to add.
        :type entry: :class:`MenuAction` | :class:`Menu`

        Example::

            menu.add_entry( Menu('File') )
            menu.add_entry( MenuAction('Exit', quit_application) )
        """
        if not isinstance(entry, Menu) and not isinstance(entry, MenuAction):
            raise base.PglInvalidTypeException(
                "Menu.add_entry(value): value needs to be a Menu or MenuAction "
                "object"
            )
        entry.config = self.config
        entry._parent = self
        entry.selected = False
        self.__entries.append(entry)

    @property
    def title(self) -> base.Text:
        """
        Get / set the title of the Menu, it needs to be a :class:`~pygamelib.base.Text`
        object or a python str.

        The title is used in the :class:`MenuBar`. In the following image, the title of
        the expanded menu is "File".

        .. image:: menu.png
           :alt: menu
        """
        return self.__title

    @title.setter
    def title(self, value: base.Text):
        if isinstance(value, base.Text):
            self.__title = value
        elif type(value) is str:
            self.__title = base.Text(value)
        else:
            raise base.PglInvalidTypeException(
                "Menu.title = value: value needs to be a pygamelib.base.Text object."
            )

    def title_width(self) -> int:
        """
        Return the actual width of the menu title. This takes into account the padding.

        Example::

            menu.title_width()
        """
        return self.__title.length + self.__padding * 2

    def menu_width(self) -> int:
        """
        Calculate and return the maximum width of the menu based on the widest element.
        This includes the padding.

        :return: the menu width.
        :rtype: int

        """
        mw = 0
        for e in self.__entries:
            if e.title_width() > mw:
                mw = e.title_width()
        return mw

    @property
    def padding(self):
        """
        Get / set the padding before and after the menu, it needs to be an int.

        The padding is only used when the menu is nested into another menu.
        """
        return self.__padding

    @padding.setter
    def padding(self, value):
        if type(value) is int:
            self.__padding = value
            self.__padding_cache = base.Text(" " * self.__padding)
        else:
            raise base.PglInvalidTypeException(
                "Menu.padding = value: value needs to be an int."
            )

    @property
    def config(self):
        """
        Get / set the config of the Menu, it needs to be a :class:`UiConfig`.
        """
        return self.__config

    @config.setter
    def config(self, value: UiConfig):
        if isinstance(value, UiConfig):
            self.__config = value
            for entry in self.__entries:
                entry.config = self.__config
                # little trick to update the visual of the menu items the first time
                # We should probably do something better.
                entry.selected = entry.selected
        else:
            raise base.PglInvalidTypeException(
                "Menu.config = value: value needs to be an UiConfig object."
            )

    @property
    def selected(self) -> bool:
        """
        Get / set the selected status of the Menu, it needs to be a boolean.

        This changes the representation (way it's drawn) of the menu entry.
        """
        return self.__selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if type(value) is bool:
            self.__selected = value
            if self.config is not None:
                if self.__selected:
                    self.title.bg_color = self.config.bg_color_selected
                    self.title.fg_color = self.config.fg_color_selected
                    self.__padding_cache.bg_color = self.config.bg_color_selected
                    self.__padding_cache.fg_color = self.config.fg_color_selected
                    self.__menu_width_padding_cache.bg_color = (
                        self.config.bg_color_selected
                    )
                else:
                    if isinstance(self._parent, Menu):
                        self.title.bg_color = self.config.bg_color_menu_not_selected
                        self.__padding_cache.bg_color = (
                            self.config.bg_color_menu_not_selected
                        )
                        self.__menu_width_padding_cache.bg_color = (
                            self.config.bg_color_menu_not_selected
                        )
                    else:
                        self.title.bg_color = self.config.bg_color_not_selected
                        self.__padding_cache.bg_color = (
                            self.config.bg_color_not_selected
                        )
                        self.__menu_width_padding_cache.bg_color = (
                            self.config.bg_color_not_selected
                        )
                    self.title.fg_color = self.config.fg_color_not_selected
                    self.__padding_cache.fg_color = self.config.fg_color_not_selected
        else:
            raise base.PglInvalidTypeException(
                "MenuAction.selected = value: value needs to be a bool"
            )

    @property
    def entries(self) -> list:
        """
        Get / set the entries of the Menu, it needs to be a list of :class:`MenuAction`
        objects.
        """
        return self.__entries

    @entries.setter
    def entries(self, value: list) -> None:
        if type(value) is list:
            for entry in value:
                if not isinstance(entry, Menu) and not isinstance(entry, MenuAction):
                    raise base.PglInvalidTypeException(
                        "Menu.entries = value: value needs to be a list of Menu or "
                        "MenuAction objects (an object within the list is not a Menu or"
                        " a MenuAction object)."
                    )

            self.__entries = value
        else:
            raise base.PglInvalidTypeException(
                "Menu.entries = value: value needs to be a list of Menu or "
                "MenuAction objects."
            )

    def current_entry(self):
        """
        Return the currently selected menu entry.

        It can be either a :class:`Menu` object or a :class:`MenuAction` object.
        """
        if self.__current_index >= 0:
            return self.__entries[self.__current_index % len(self.__entries)]

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        self._store_position(row, column)
        menu_width = self.menu_width()
        if self.padding > 0:
            self.__padding_cache.render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )
            self.__title.render_to_buffer(
                buffer, row, column + self.__padding, buffer_height, buffer_width
            )
            self.__padding_cache.render_to_buffer(
                buffer,
                row,
                column + self.title_width() - self.__padding,
                buffer_height,
                buffer_width,
            )
        else:
            self.__title.render_to_buffer(
                buffer, row, column, buffer_height, buffer_width
            )

        # Can't be automatically tested as it is set by activate().
        if self.__expanded:  # pragma: no cover
            row_offset = 1
            col_offset = 0
            if isinstance(self._parent, Menu):
                row_offset = 0
                col_offset = self._parent.menu_width()
            for e in self.__entries:
                e.render_to_buffer(
                    buffer,
                    row + row_offset,
                    column + col_offset,
                    buffer_height,
                    buffer_width,
                )
                for pc in range(
                    column + col_offset + e.title_width(),
                    column + col_offset + menu_width,
                ):
                    self.__menu_width_padding_cache.render_to_buffer(
                        buffer,
                        row + row_offset,
                        pc,
                        buffer_height,
                        buffer_width,
                    )
                row_offset += 1

    def select_next(self):
        """
        Select the next entry in the menu.

        The selected entry is rendered differently to give a visual feedback to the
        user. Please see the :class:`UiConfig` class for the styling option available to
        the Menu object.

        Example::

            menu.select_next()
        """
        self.entries[self.__current_index % len(self.entries)].selected = False
        self.__current_index += 1
        self.entries[self.__current_index % len(self.entries)].selected = True

    def select_previous(self):
        """
        Select the previous entry in the menu.

        The selected entry is rendered differently to give a visual feedback to the
        user. Please see the :class:`UiConfig` class for the styling option available to
        the Menu object.


        Example::

            menu.select_previous()
        """
        self.entries[self.__current_index % len(self.entries)].selected = False
        self.__current_index -= 1
        self.entries[self.__current_index % len(self.entries)].selected = True

    def activate(self):  # pragma: no cover
        """
        Activates the menu. This method contains its own event loop a bit like the
        show() methods of Dialogs. It expands the menu if it wasn't already the case and
        listen to keyboard key strokes.

         * SPACE or ENTER activates (i.e execute) menu actions.
         * DOWN select the next entry.
         * UP select the previous entry.
         * ESC or LEFT close the menu.
         * RIGHT activate (i.e expand) a submenu.

        Example::

            menu.activate()
        """
        screen = self.config.game.screen
        term = self.config.game.terminal
        inkey = ""
        self.__expanded = True
        if isinstance(self._parent, Menu) or isinstance(self._parent, MenuBar):
            for e in self.entries:
                e.selected = False
            self.__current_index = -1
            self.select_next()
        screen.force_update()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER" or inkey == " ":
                    if isinstance(self.current_entry(), MenuAction):
                        self.current_entry().activate()
                        break
                elif inkey.name == "KEY_DOWN":
                    self.select_next()
                    screen.force_update()
                elif inkey.name == "KEY_UP":
                    self.select_previous()
                    screen.force_update()
                elif inkey.name == "KEY_ESCAPE" or inkey.name == "KEY_LEFT":
                    break
                elif inkey.name == "KEY_RIGHT":
                    if isinstance(self.current_entry(), Menu):
                        self.current_entry().activate()
            elif not self.__expanded:
                break
            inkey = term.inkey(timeout=0.05)
        self.__expanded = False
        screen.force_update()

    def expand(self):
        """
        Expand the menu. A menu is automatically expanded when activated.

        Example::

            file_menu.expand()
        """
        self.__expanded = True

    def collapse(self):
        """
        Collapse the menu. A menu is automatically collapsed after activation.

        Example::

            file_menu.collapse()
        """
        self.__expanded = False
        for e in self.__entries:
            if isinstance(e, Menu):
                e.collapse()


class MenuBar(object):
    """
    The MenuBar widget is exactly that: an horizontal bar that can hold :class:`Menu` or
    :class:`MenuAction` objects.

    Contrary to these 2 classes, MenuBar does *not* have an activate() method. The
    reason is that the menubar cannot block rendering with its own event loop as it is
    supposed to be showned at all times. So the management of interactions are left to
    the programmer to implement.

    A typical implementation would look like this:

    Example::

        # First create a menubar
        menubar = MenuBar(config=UiConfig.instance(game=Game.instance()))

        # Then create a Menu
        file_menu = Menu(
            "File",
            [
                MenuAction("Open", open_file),
                MenuAction("Save", save_file),
                MenuAction("Save as", save_file_as),
                MenuAction("Quit", exit_application),
            ]
        )
        menubar.add_entry( file_menu )
        menubar.add_entry( MenuAction("Help", display_help) )

        # Place the menubar on screen
        screen.place(menubar, 0, 0)
        screen.update()

        # Then, somewhere in an event loop, manage the inputs for example in the user
        # update function
        def user_update(game, inkey, elapsed_time):
            if inkey == engine.key.DOWN:
                if menubar.current_entry() is not None:
                    menubar.current_entry().activate()
            elif inkey == engine.key.LEFT:
                menubar.select_previous()
            elif inkey == engine.key.RIGHT:
                menubar.select_next()
            elif inkey.name == "KEY_ENTER":
                if menubar.current_entry() is not None:
                    menubar.current_entry().activate()
            elif inkey.name == "KEY_ESCAPE":
                menubar.close()
    """

    def __init__(
        self, entries: list = None, spacing: int = 2, config: UiConfig = None
    ) -> None:
        """
        The constructor takes the following parameters.

        :param entries: A list of :class:`MenuAction` or :class:`Menu` objects.
        :type entries: list
        :param spacing: The horizontal spacing between entries.
        :type padding: int
        :param config: The configuration object.
        :type config: :class:`UiConfig`
        """
        super().__init__()
        self.__entries = []
        self.__config = config
        self.__cross_ref = {}
        self.__spacing = spacing
        if entries is not None:
            for entry in entries:
                if isinstance(entry, Menu) or isinstance(entry, MenuAction):
                    entry._parent = self
                    entry.config = self.config
                    entry.selected = False
                    self.__entries.append(entry)
                else:
                    raise base.PglInvalidTypeException(
                        "MenuBar(entries=list_of_entries): each entry must be a Menu or"
                        " a MenuAction object."
                    )
            self.__build_cross_ref()
        self.__current_index = -1

    def __build_cross_ref(self):
        self.__cross_ref = {}
        idx = 0
        for e in self.__entries:
            if hasattr(e, "title"):
                self.__cross_ref[e.title] = idx
            idx += 1

    @property
    def entries(self) -> list:
        """
        Get / set the entries of the MenuBar, it needs to be a list of
        :class:`MenuAction` or :class:`Menu` objects.
        """
        return self.__entries

    @entries.setter
    def entries(self, value: list) -> None:
        if type(value) is list:
            for entry in value:
                if not isinstance(entry, Menu) and not isinstance(entry, MenuAction):
                    raise base.PglInvalidTypeException(
                        "MenuBar.entries = value: value needs to be a list of Menu or "
                        "MenuAction objects"
                    )

            self.__entries = value
            self.__build_cross_ref()
        else:
            raise base.PglInvalidTypeException(
                "MenuBar.entries = value: value needs to be a list of Menu or "
                "MenuAction objects."
            )

    def add_entry(self, entry):
        """
        Add an entry to the menu bar. An entry can be a :class:`MenuAction` or a
        :class:`Menu`.
        Entries are displayed in the order of there additions from left to right.

        .. IMPORTANT:: The config of the entry is overwritten by the config of the
           MenuBar. That is why it's not mandatory for :class:`Menu` and
           :class:`MenuAction`.

        :param entry: The entry to add.
        :type entry: :class:`MenuAction` | :class:`Menu`

        Example::

            menubar.add_entry( Menu('File') )
            menubar.add_entry( MenuAction('Exit', quit_application) )
        """
        if not isinstance(entry, Menu) and not isinstance(entry, MenuAction):
            raise base.PglInvalidTypeException(
                "MenuBar.add_entry(value): value needs to be a Menu or MenuAction "
                "object"
            )
        entry.config = self.config
        entry._parent = self
        entry.selected = False
        self.__entries.append(entry)
        self.__build_cross_ref()

    @property
    def spacing(self):
        """
        Get / set the spacing between menu entries, it needs to be an int.
        """
        return self.__spacing

    @spacing.setter
    def spacing(self, value):
        if type(value) is int:
            self.__spacing = value
        else:
            raise base.PglInvalidTypeException(
                "Menu.spacing = value: value needs to be an int."
            )

    @property
    def config(self):
        """
        Get / set the config of the MenuBar, it needs to be a :class:`UiConfig`.

        .. IMPORTANT:: The MenuBar's config is imposed on the managed items (Menu and\
            MenuAction).
        """
        return self.__config

    @config.setter
    def config(self, value: UiConfig):
        if isinstance(value, UiConfig):
            self.__config = value
        else:
            raise base.PglInvalidTypeException(
                "Menu.config = value: value needs to be a UiConfig object."
            )

    @property
    def current_index(self):
        """
        Get / set the currently selected menu entry, it needs to be an int.
        When setting the current_index, if the previous index was corresponding to a
        selected entry, said entry is first unselected.
        """
        return self.__current_index

    @current_index.setter
    def current_index(self, value: int):
        if type(value) is int:
            if (
                self.__current_index >= 0
                and self.__entries[self.__current_index % len(self.__entries)].selected
            ):
                self.__entries[
                    self.__current_index % len(self.__entries)
                ].selected = False
            self.__current_index = value
            if (
                self.__current_index >= 0
                and not self.__entries[
                    self.__current_index % len(self.__entries)
                ].selected
            ):
                self.__entries[
                    self.__current_index % len(self.__entries)
                ].selected = True
        else:
            raise base.PglInvalidTypeException(
                "Menu.current_index = value: value needs to be an int."
            )

    def current_entry(self):
        """
        Return the currently selected menu entry.

        It can be either a :class:`Menu` object or a :class:`MenuAction` object.
        """
        if self.__current_index >= 0:
            return self.__entries[self.__current_index % len(self.__entries)]

    # def _recursive_build_entries(self, entry: list):
    #     # This function only deal with menu entries not top level entry
    #     # entry needs to be like that:
    #     # {
    #     #     "label": "Help",
    #     #     "entries": [
    #     #         {"label": "Quick help", "callback": None},
    #     #         {"label": "Documentation", "callback": None},
    #     #         {"label": "About", "callback": None},
    #     #     ],
    #     #     "callback": None,
    #     #     "expand_under": True,
    #     # }
    #     me = None
    #     if "label" in entry:
    #         me = MenuAction(entry["label"], config=self.config)
    #         if "callback" in entry and entry["callback"] is not None:
    #             me.callback = entry["callback"]
    #         if "expand_under" in entry and entry["expand_under"] is not None:
    #             me.expand_under = entry["expand_under"]
    #         if "is_active" in entry and entry["is_active"] is not None:
    #             me.is_active = entry["is_active"]
    #         if "entries" in entry and len(entry["entries"]) > 0:
    #             for e in entry["entries"]:
    #                 me.entries.append(self._recursive_build_entries(e))
    #     return me

    # def build_from_dict(self, entries: list):
    #     """
    #     .. IMPORTANT:: Top level menu entries are forced to expand under for the
    #        moment.

    #     menu = [
    #         {
    #             "label": "File",
    #             "entries": [
    #                 {"label": "Open", "callback": None},
    #                 {"label": "Save", "callback": None},
    #                 {"label": "Save As", "callback": None},
    #                 {"label": "Quit", "callback": None},
    #             ],
    #             "callback": None,
    #             "expand_under": True,
    #         },
    #         {
    #             "label": "Edit",
    #             "entries": [
    #                 {"label": "Copy", "callback": None},
    #                 {"label": "Paste", "callback": None},
    #                 {"label": "New sprite", "callback": None},
    #                 {"label": "New brush", "callback": None},
    #             ],
    #             "callback": None,
    #             "expand_under": True,
    #         },
    #         {
    #             "label": "Help",
    #             "entries": [
    #                 {"label": "Quick help", "callback": None},
    #                 {"label": "Documentation", "callback": None},
    #                 {"label": "About", "callback": None},
    #             ],
    #             "callback": None,
    #             "expand_under": True,
    #         },
    #     ]
    #     """

    #     self.entries = []
    #     for entry in entries:
    #         me = self._recursive_build_entries(entry)
    #         if me is not None:
    #             me.expand_under = True
    #             self.entries.append(me)
    #         else:
    #             raise base.PglInvalidTypeException(
    #                 "Menu.build_from_dict(entries): entries needs to be a "
    #                 "specifically formated dict. Please refer to the documentation."
    #             )

    def length(self) -> int:
        """
        Returns the total length of the menubar. This is computed everytime the method
        is called and it includes the spacing.
        """
        le = 0
        for e in self.entries:
            le += e.title_width() + self.spacing
        return le

    def select_next(self):
        """
        Select the next element in the menubar.

        Example ::

            if user_input.name == 'KEY_RIGHT':
                menubar.select_next()
        """
        self.entries[self.__current_index % len(self.entries)].selected = False
        self.__current_index += 1
        self.entries[self.__current_index % len(self.entries)].selected = True

    def select_previous(self):
        """
        Select the previous element in the menubar.

        Example ::

            if user_input.name == 'KEY_RIGHT':
                menubar.select_previous()
        """
        self.entries[self.__current_index % len(self.entries)].selected = False
        self.__current_index -= 1
        self.entries[self.__current_index % len(self.entries)].selected = True

    def render_to_buffer(
        self, buffer, row: int, column: int, buffer_height: int, buffer_width: int
    ) -> None:
        """Render the object from the display buffer to the frame buffer.

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
        offset = 0
        for entry in self.entries:
            # entry.label.render_to_buffer(
            #     buffer, row, column + offset, buffer_height, buffer_width
            # )
            entry.render_to_buffer(
                buffer,
                row,
                column + offset,
                buffer_height,
                buffer_width,
            )
            offset += entry.title_width() + self.spacing

    def close(self):
        """
        Close and unselect menu entries/submenu.

        Please call that method when the menu bar loses focus.
        """
        for e in self.entries:
            e.selected = False
            if isinstance(e, Menu):
                e.collapse()
        self.current_index = -1

    # def activate(self):
    #     screen = self.config.game.screen
    #     game = self.config.game
    #     term = game.terminal
    #     inkey = ""
    #     screen.force_update()
    #     while 1:
    #         if inkey != "":
    #             if inkey.name == "KEY_DOWN":
    #                 if self.current_entry() is not None:
    #                     self.current_entry().activate()
    #             elif inkey.name == "KEY_LEFT":
    #                 self.select_previous()
    #                 screen.force_update()
    #             elif inkey.name == "KEY_RIGHT":
    #                 self.select_next()
    #                 screen.force_update()
    #             elif inkey.name == "KEY_ENTER":
    #                 if self.current_entry() is not None:
    #                     self.current_entry().activate()
    #                     self.close()
    #                     break
    #             elif inkey.name == "KEY_ESCAPE":
    #                 self.close()
    #                 break
    #         inkey = term.inkey(timeout=0.05)
    #     screen.force_update()
