import pygamelib.base as base
from pygamelib.gfx import core, ui
from pygamelib import constants, engine
import unittest
from pathlib import Path


def fake_callback():
    pass


class FakeText:
    def __init__(self, text) -> None:
        self.text = text

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        pass


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)

    def test_uiconfig(self):
        with self.assertRaises(base.PglInvalidTypeException):
            ui.UiConfig()
        conf = ui.UiConfig.instance(game=self.game)
        self.assertIsInstance(conf, ui.UiConfig)

    def test_dialog(self):
        with self.assertRaises(base.PglInvalidTypeException):
            ui.Dialog()
        d = ui.Dialog(config=ui.UiConfig.instance())
        self.assertIsInstance(d, ui.Dialog)
        d.config = ui.UiConfig.instance()
        self.assertIsInstance(d.config, ui.UiConfig)
        with self.assertRaises(base.PglInvalidTypeException):
            d.config = "bork"
        with self.assertRaises(base.PglInvalidTypeException):
            d.user_input = 12
        d.user_input = "test"
        self.assertEqual(d.user_input, "test")
        with self.assertRaises(NotImplementedError):
            d.show()

    def test_box(self):
        conf = ui.UiConfig.instance(game=self.game)
        conf.borderless_dialog = False
        b = ui.Box(
            20, 10, "test box", conf, True, core.Sprixel(" "), constants.ALIGN_LEFT
        )
        self.game.screen.place(b, 0, 0)
        self.game.screen.update()
        b.config = ui.UiConfig.instance()
        self.assertIsInstance(b.config, ui.UiConfig)
        self.assertEqual(b.title, "test box")
        b.title = "test 2"
        self.assertEqual(b.title, "test 2")
        with self.assertRaises(base.PglInvalidTypeException):
            b.config = 2
        self.assertEqual(b.width, 20)
        b.width = 30
        self.assertEqual(b.width, 30)
        with self.assertRaises(base.PglInvalidTypeException):
            b.width = "20"
        self.assertEqual(b.height, 10)
        b.height = 20
        self.assertEqual(b.height, 20)
        with self.assertRaises(base.PglInvalidTypeException):
            b.height = "20"
        b.title = ""
        self.assertEqual(b.title, "")
        self.game.screen.place(b, 0, 0)
        self.game.screen.update()
        with self.assertRaises(base.PglInvalidTypeException):
            b.title = 2
        self.game.screen.place(
            b, self.game.screen.height - 5, self.game.screen.width - 5
        )
        self.game.screen.update()

    def test_progressbar(self):
        conf = ui.UiConfig.instance(game=self.game)
        conf.borderless_dialog = False
        pb = ui.ProgressDialog(
            base.Text("test"),
            0,
            100,
            20,
            core.Sprixel("="),
            core.Sprixel("-"),
            True,
            True,
            conf,
        )
        pb.label = "test"
        self.assertEqual(pb.label, "test")
        pb.label = base.Text("Test text")
        self.assertEqual(pb.label, "Test text")
        with self.assertRaises(base.PglInvalidTypeException):
            pb.label = 2
        self.assertEqual(pb.value, 0)
        pb.value = 2
        self.assertEqual(pb.value, 2)
        with self.assertRaises(base.PglInvalidTypeException):
            pb.value = "3"
        self.assertEqual(pb.maximum, 100)
        pb.maximum = 20
        self.assertEqual(pb.maximum, 20)
        with self.assertRaises(base.PglInvalidTypeException):
            pb.maximum = "3"
        self.game.screen.place(pb, 0, 0)
        self.game.screen.update()
        pb.value = 20
        self.game.screen.force_update()
        self.game.screen.force_update()
        pb = ui.ProgressBar(
            0,
            100,
            20,
            core.Sprixel("="),
            core.Sprixel("-"),
            conf,
        )
        self.assertIsInstance(pb.config, ui.UiConfig)
        pb.config = ui.UiConfig.instance()
        self.assertIsInstance(pb.config, ui.UiConfig)
        with self.assertRaises(base.PglInvalidTypeException):
            pb.config = 3
        self.assertIsInstance(pb.progress_marker, core.Sprixel)
        self.assertIsInstance(pb.empty_marker, core.Sprixel)
        pb.progress_marker = "#"
        self.assertEqual(pb.progress_marker, "#")
        pb.progress_marker = base.Text("#")
        self.assertEqual(pb.progress_marker, "#")
        with self.assertRaises(base.PglInvalidTypeException):
            pb.progress_marker = 3
        pb.empty_marker = "#"
        self.assertEqual(pb.empty_marker, "#")
        pb.empty_marker = base.Text("#")
        self.assertEqual(pb.empty_marker, "#")
        with self.assertRaises(base.PglInvalidTypeException):
            pb.empty_marker = 3
        pb.progress_marker = core.Sprixel("=")
        pb.empty_marker = core.Sprixel("-")
        self.assertIsInstance(pb.progress_marker, core.Sprixel)
        self.assertIsInstance(pb.empty_marker, core.Sprixel)
        self.assertEqual(pb.value, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            pb.value = "10"
        self.assertEqual(pb.maximum, 100)
        pb.maximum = 10
        self.assertEqual(pb.maximum, 10)
        with self.assertRaises(base.PglInvalidTypeException):
            pb.maximum = "10"

    def test_message_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        # Test when height is none and adpatative_height is False (it will be tuned on)
        md = ui.MessageDialog(
            [
                "Test",
                "Message dialog",
                FakeText("fake"),
                base.Text("Another test"),
                core.Sprixel("!"),
            ],
            adaptive_height=False,
            config=conf,
        )
        self.assertEqual(md.title, "")
        md.title = "test"
        self.assertEqual(md.title, "test")
        md.title = base.Text("test")
        self.assertEqual(md.title, "test")
        with self.assertRaises(base.PglInvalidTypeException):
            md.title = 42
        self.game.screen.place(md, 0, 0)
        self.game.screen.update()
        md.add_line("test 2", constants.ALIGN_RIGHT)
        md.add_line("test 3", constants.ALIGN_CENTER)
        md.add_line(base.Text("test 4"), constants.ALIGN_RIGHT)
        md.add_line(base.Text("test 5"), constants.ALIGN_CENTER)
        self.game.screen.force_update()
        with self.assertRaises(base.PglInvalidTypeException):
            md.add_line(1, constants.ALIGN_CENTER)
        self.assertIs(type(md.height), int)
        # Now test with fixed height
        md = ui.MessageDialog(
            [
                "Test",
                "Message dialog",
                FakeText("fake"),
                base.Text("Another test"),
                core.Sprixel("!"),
            ],
            adaptive_height=False,
            height=10,
            config=conf,
        )
        self.assertEqual(md.height, 10)
        md.height = 6
        self.assertEqual(md.height, 6)
        with self.assertRaises(base.PglInvalidTypeException):
            md.height = "6"
        md = ui.MessageDialog(title=base.Text("test"), config=conf)
        self.assertEqual(md.title, "test")
        with self.assertRaises(base.PglInvalidTypeException):
            ui.MessageDialog(title=42, config=conf)

    def test_lineinput_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.LineInputDialog("123", 123, config=conf)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.LineInputDialog(123, "123", config=conf)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.LineInputDialog(default=12, config=conf)
        ld = ui.LineInputDialog("title", "test line input", config=conf)
        self.assertEqual(ld.label.text, "test line input")
        self.assertEqual(ld.title, "title")
        ld.label = "test 2"
        self.assertEqual(ld.label.text, "test 2")
        ld.label = base.Text("test 3")
        self.assertEqual(ld.label.text, "test 3")
        with self.assertRaises(base.PglInvalidTypeException):
            ld.label = 3
        ld.title = "test"
        self.assertEqual(ld.title, "test")
        ld.title = base.Text("test")
        self.assertEqual(ld.title, "test")
        with self.assertRaises(base.PglInvalidTypeException):
            ld.title = 3
        self.game.screen.place(ld, 0, 0)
        self.game.screen.update()
        ld = ui.LineInputDialog(base.Text("title"), "test line input", config=conf)
        self.assertEqual(ld.title, "title")

    def test_multiline_input_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.MultiLineInputDialog(fields=1, title="test", config=conf)
        mld = ui.MultiLineInputDialog(title="test", config=conf)
        self.assertListEqual(
            mld.fields,
            [
                {
                    "label": "Input a value:",
                    "default": "",
                    "filter": constants.PRINTABLE_FILTER,
                    "user_input": "",
                }
            ],
        )
        fields = [
            {
                "label": base.Text("Input a value:"),
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
                "user_input": "",
            },
            {
                "label": "test",
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
                "user_input": "",
            },
            {
                "label": "test longer very much longer. for sure.",
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
                "user_input": "",
            },
        ]
        mld.fields = fields
        with self.assertRaises(base.PglInvalidTypeException):
            mld.fields = 42

        self.game.screen.place(mld, 0, 0)
        self.game.screen.update()
        mld.title = "test change"
        self.assertEqual(mld.title, "test change")
        mld.title = base.Text("test change")
        self.assertEqual(mld.title, "test change")
        mld = ui.MultiLineInputDialog(fields, title="test", config=conf)
        self.assertEqual(mld.title, "test")
        mld = ui.MultiLineInputDialog(fields, title=base.Text("test"), config=conf)
        self.assertEqual(mld.title, "test")
        with self.assertRaises(base.PglInvalidTypeException):
            mld = ui.MultiLineInputDialog(fields, title=42, config=conf)
        with self.assertRaises(base.PglInvalidTypeException):
            mld.title = 42
        mld = ui.MultiLineInputDialog(fields, title=None, config=conf)
        self.assertEqual(mld.title, "")

    def test_file_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        fd = ui.FileDialog(Path("tests"), config=conf)
        self.assertEqual(fd.path, Path("tests").resolve())
        with self.assertRaises(base.PglInvalidTypeException):
            fd.path = 42

        fd.path = Path()
        self.assertEqual(fd.path, Path())
        self.assertEqual(fd.filter, "*")
        fd.filter = "*.spr"
        self.assertEqual(fd.filter, "*.spr")
        with self.assertRaises(base.PglInvalidTypeException):
            fd.filter = 42
        self.assertFalse(fd.show_hidden_files)
        fd.show_hidden_files = True
        self.assertTrue(fd.show_hidden_files)
        with self.assertRaises(base.PglInvalidTypeException):
            fd.show_hidden_files = 42

        fd.user_input = "Some input but not just any input, a very very long user input"

        self.game.screen.place(fd, 0, 0)
        self.game.screen.update()
        fd.user_input = "Some input"
        self.game.screen.force_update()

        # tentative
        # fd.path = Path("/var/log/audit")
        # self.assertIsNone(fd._build_file_cache())

    def test_gridselector(self):
        conf = ui.UiConfig.instance(game=self.game)
        gd = ui.GridSelectorDialog(["a", "b", "c", "##"], 10, 20, "test", config=conf)
        self.assertEqual(gd.grid_selector.current_page, 0)
        gd.grid_selector.current_page = 1
        self.assertEqual(gd.grid_selector.current_page, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.GridSelectorDialog(
                ["a", "b", base.Text("c"), "##"],
                10,
                20,
                "test",
                config=conf,
            )

        self.assertEqual(gd.title, "test")
        gd.title = "test 2"
        self.assertEqual(gd.title, "test 2")
        with self.assertRaises(base.PglInvalidTypeException):
            gd.title = 42
        self.assertIsInstance(gd.grid_selector, ui.GridSelector)
        self.assertEqual(len(gd.grid_selector.choices), 4)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.choices = 3

        gd.grid_selector.choices = ["a", "b", "c"]
        self.assertEqual(len(gd.grid_selector.choices), 3)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.choices = "42"
        gd.grid_selector.max_height = 20
        self.assertEqual(gd.grid_selector.max_height, 20)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.max_height = "42"
        gd.grid_selector.max_width = 20
        self.assertEqual(gd.grid_selector.max_width, 20)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.max_width = "42"
        self.assertEqual(gd.grid_selector.current_choice, 0)
        gd.grid_selector.current_choice = 1
        self.assertEqual(gd.grid_selector.current_choice, 1)
        self.assertIsInstance(gd.grid_selector.current_sprixel(), core.Sprixel)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.current_choice = "42"

        gd.grid_selector.cursor_down()
        self.assertEqual(gd.grid_selector.current_choice, 1)
        gd.grid_selector.cursor_up()
        self.assertEqual(gd.grid_selector.current_choice, 1)
        gd.grid_selector.cursor_right()
        self.assertEqual(gd.grid_selector.current_choice, 2)
        gd.grid_selector.cursor_left()
        self.assertEqual(gd.grid_selector.current_choice, 1)
        gd.grid_selector.max_width = 3
        gd.grid_selector.max_height = 3
        gd.grid_selector.page_down()
        self.assertEqual(gd.grid_selector.current_page, 1)
        gd.grid_selector.page_up()
        self.assertEqual(gd.grid_selector.current_page, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector.current_page = "42"

        self.game.screen.place(gd, 0, 0)
        self.game.screen.update()

        conf.borderless_dialog = not conf.borderless_dialog
        self.assertIsInstance(
            ui.GridSelectorDialog(["a", "b", "c", "##"], 10, 20, "test", config=conf),
            ui.GridSelectorDialog,
        )
        conf.borderless_dialog = not conf.borderless_dialog
        gd.grid_selector = gd.grid_selector
        self.assertIsInstance(gd.grid_selector, ui.GridSelector)
        with self.assertRaises(base.PglInvalidTypeException):
            gd.grid_selector = 42
        gd.grid_selector.choices = ["a" for _ in range(30)]
        self.assertEqual(gd.grid_selector.nb_pages(), 15)
        # gd.grid_selector.choices.append("aa")
        # input(gd.grid_selector.choices)
        # gd.grid_selector.render_to_buffer(
        #     np.array([[" " for i in range(0, 50, 1)] for j in range(0, 50, 1)]),
        #     0,
        #     0,
        #     50,
        #     50,
        # )

    def test_colorpickers(self):
        conf = ui.UiConfig.instance(game=self.game)
        cpd = ui.ColorPickerDialog(config=conf)
        with self.assertRaises(base.PglInvalidTypeException):
            cpd.set_selection("42")
        self.assertEqual(cpd.title, "Pick a color")
        cpd.title = "Test"
        self.assertEqual(cpd.title, "Test")
        with self.assertRaises(base.PglInvalidTypeException):
            cpd.title = 42
        cpd.set_color(core.Color(1, 2, 3))
        cd = ui.ColorPicker(config=conf)
        self.assertEqual(cd.selection, 0)
        cd.selection = 1
        self.assertEqual(cd.selection, 1)
        with self.assertRaises(base.PglInvalidTypeException):
            cd.selection = "42"
        self.assertIsInstance(cd.color, core.Color)
        with self.assertRaises(base.PglInvalidTypeException):
            cd.color = "42"
        cd.color = core.Color(4, 5, 6)
        self.assertEqual(cd.color.r, 4)
        self.assertEqual(cd.color.g, 5)
        self.assertEqual(cd.color.b, 6)
        self.assertEqual(cd.red, 4)
        self.assertEqual(cd.green, 5)
        self.assertEqual(cd.blue, 6)
        with self.assertRaises(base.PglInvalidTypeException):
            cd.red = "42"
        with self.assertRaises(base.PglInvalidTypeException):
            cd.green = "42"
        with self.assertRaises(base.PglInvalidTypeException):
            cd.blue = "42"

        self.game.screen.place(cpd, 0, 0)
        self.game.screen.update()

    def test_menus(self):
        screen = self.game.screen
        conf = ui.UiConfig.instance(game=self.game)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.MenuBar([42], config=conf)
        menubar = ui.MenuBar([ui.MenuAction("Default", fake_callback)], config=conf)
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.add_entry(42)
        menubar.spacing = 0
        self.assertEqual(menubar.spacing, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.spacing = "42"
        menubar.config = conf
        self.assertIsInstance(menubar.config, ui.UiConfig)
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.config = "42"
        menubar.current_index = 0
        self.assertEqual(menubar.current_index, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.current_index = "42"
        file_menu = ui.Menu(
            "File",
            [
                ui.MenuAction("Open", fake_callback),
                ui.MenuAction(base.Text("Save"), fake_callback),
                ui.MenuAction("Save as", fake_callback),
                ui.MenuAction("Quit", fake_callback),
            ],
            config=conf,
        )
        edit_menu = ui.Menu(
            base.Text("Edit", core.Color(0, 255, 255)),
            [ui.MenuAction("Copy", fake_callback)],
        )
        menubar.add_entry(file_menu)
        menubar.add_entry(edit_menu)
        help_action = ui.MenuAction("Help", fake_callback)
        menubar.add_entry(help_action)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.Menu(42)
        with self.assertRaises(base.PglInvalidTypeException):
            edit_menu.add_entry(42)
        edit_menu.add_entry(ui.MenuAction("Paste", fake_callback))
        with self.assertRaises(base.PglInvalidTypeException):
            ui.Menu("42", ["this", "is", "not going to", "work"])
        with self.assertRaises(base.PglInvalidTypeException):
            ui.MenuAction(42, fake_callback)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.MenuAction("42", 42)

        edit_menu.title = "*E*dit"
        self.assertEqual(edit_menu.title.text, "*E*dit")
        edit_menu.title = base.Text("Edit")
        self.assertEqual(edit_menu.title.text, "Edit")
        with self.assertRaises(base.PglInvalidTypeException):
            edit_menu.title = 42

        help_action.title = "Help (Shift+H)"
        self.assertEqual(help_action.title.text, "Help (Shift+H)")
        help_action.title = base.Text("Help")
        self.assertEqual(help_action.title.text, "Help")
        with self.assertRaises(base.PglInvalidTypeException):
            help_action.title = 42

        help_action.action = fake_callback
        self.assertTrue(callable(help_action.action))
        with self.assertRaises(base.PglInvalidTypeException):
            help_action.action = 42
        with self.assertRaises(base.PglInvalidTypeException):
            help_action.config = 42
        with self.assertRaises(base.PglInvalidTypeException):
            help_action.padding = "42"
        help_action.padding = 2
        self.assertEqual(help_action.padding, 2)
        with self.assertRaises(base.PglInvalidTypeException):
            help_action.selected = 42
        help_action.selected = True
        self.assertTrue(help_action.selected)

        edit_menu.padding = 0
        self.assertEqual(edit_menu.padding, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            edit_menu.padding = "42"
        with self.assertRaises(base.PglInvalidTypeException):
            edit_menu.config = "42"
        edit_menu.selected = True
        self.assertTrue(edit_menu.selected)
        with self.assertRaises(base.PglInvalidTypeException):
            edit_menu.selected = 42
        export_menu = ui.Menu(
            "Export",
            [
                ui.MenuAction("Sprite (.spr)", fake_callback),
                ui.MenuAction("PNG (.png)", fake_callback),
                ui.MenuAction("Animation as a GIF (.gif)", fake_callback),
            ],
        )
        edit_menu.add_entry(export_menu)
        export_menu.selected = True
        self.assertTrue(export_menu.selected)
        self.assertTrue(type(export_menu.entries) is list)
        export_menu.entries = [
            ui.MenuAction("Sprite (.spr)", fake_callback),
            ui.MenuAction("PNG (.png)", fake_callback),
            ui.MenuAction("Animation as a GIF (.gif)", fake_callback),
        ]
        self.assertEqual(len(export_menu.entries), 3)
        with self.assertRaises(base.PglInvalidTypeException):
            export_menu.entries = 42
        with self.assertRaises(base.PglInvalidTypeException):
            export_menu.entries = [42]
        edit_menu.select_next()
        self.assertIsInstance(edit_menu.current_entry(), ui.MenuAction)
        edit_menu.select_previous()
        self.assertIsNone(edit_menu.current_entry())

        menubar.select_next()
        entry = menubar.current_entry()
        self.assertTrue(entry.selected)
        menubar.current_index += 1
        self.assertTrue(menubar.current_entry().selected)
        menubar.select_previous()
        self.assertTrue(menubar.current_entry().selected)
        self.assertTrue(type(menubar.length()) is int)
        menubar.close()
        self.assertEqual(menubar.current_index, -1)

        self.assertIsNone(edit_menu.expand())
        # Screen update
        screen.place(menubar, 0, 0)
        screen.update()
        self.assertIsNone(edit_menu.collapse())
        help_action.padding = 0
        screen.force_update()

        menubar.entries = [
            ui.MenuAction("Sprite (.spr)", fake_callback),
            ui.MenuAction("PNG (.png)", fake_callback),
            ui.MenuAction("Animation as a GIF (.gif)", fake_callback),
        ]
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.entries = 42
        with self.assertRaises(base.PglInvalidTypeException):
            menubar.entries = [42]

    def test_widget(self):
        w = ui.Widget()
        self.assertEqual(w.maximum_height, 10)
        self.assertEqual(w.minimum_height, 0)
        self.assertEqual(w.maximum_width, 20)
        self.assertEqual(w.minimum_width, 0)
        self.assertEqual(w.width, 0)
        self.assertEqual(w.height, 0)
        w.maximum_height = 10
        w.minimum_height = 2
        self.assertEqual(w.maximum_height, 10)
        self.assertEqual(w.minimum_height, 2)
        w.height = 5
        self.assertEqual(w.height, 5)
        w.height = 15
        self.assertEqual(w.height, 10)
        w.height = 0
        self.assertEqual(w.height, 2)
        w.maximum_width = 10
        w.minimum_width = 2
        self.assertEqual(w.maximum_width, 10)
        self.assertEqual(w.minimum_width, 2)
        w.width = 5
        self.assertEqual(w.width, 5)
        w.width = 15
        self.assertEqual(w.width, 10)
        w.width = 0
        self.assertEqual(w.width, 2)

        w = ui.Widget(4, 2, 0, 0, 3, 1)
        self.assertEqual(w.maximum_height, 2)
        self.assertEqual(w.maximum_width, 4)

        self.assertIsNone(w.parent)
        self.assertEqual(len(w.children), 0)

        parent = ui.Widget()
        w.parent = parent
        self.assertEqual(w.parent, parent)

        self.game.screen.place(w, 0, 0)
        self.game.screen.render()

        w.y = 5
        w.x = 10
        self.assertEqual(w.y, w.screen_row)
        self.assertEqual(w.x, w.screen_column)

        w.store_screen_position(6, 11)
        self.assertEqual(w.screen_row, w.y)
        self.assertEqual(w.screen_column, w.x)


class TestLineInput(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = ui.UiConfig.instance(game=self.game)

    def lineInputCreation(self):
        li = ui.LineInput()
        self.assertIsInstance(li, ui.LineInput)

    def test_default_values(self):
        li = ui.LineInput()
        self.assertEqual(li.text, "")
        self.assertEqual(li.ui_config, ui.UiConfig.instance())
        self.assertEqual(li.minimum_height, 1)
        self.assertEqual(li.minimum_width, 0)
        self.assertEqual(li.maximum_height, 1)
        self.assertEqual(li.maximum_width, 20)

    def test_line_input_long_input(self):
        li = ui.LineInput()
        long_input = "a" * 1000
        li.text = long_input
        self.assertEqual(li.text, long_input)

    # Set text to a valid string with PRINTABLE_FILTER.
    def test_set_valid_string_printable_filter(self):
        line_input = ui.LineInput(filter=constants.InputValidator.PRINTABLE_FILTER)
        line_input.text = "Hello, World!"
        self.assertEqual(line_input.text, "Hello, World!")

    # Test that setting the text of the LineInput object works correctly
    def test_setting_text(self):
        # Create a LineInput instance
        li = ui.LineInput()

        # Set the text of the LineInput object
        li.text = "Hello, World!"

        # Check if the text is set correctly
        self.assertEqual(li.text, "Hello, World!")

    # Set text to an empty string.
    def test_set_empty_string(self):
        line_input = ui.LineInput()
        line_input.text = ""
        self.assertEqual(line_input.text, "")

    # Test that creating a LineInput object with a non-default size works correctly
    def test_create_line_input_with_non_default_size(self):
        # Create a LineInput instance with non-default size
        li = ui.LineInput()
        li.minimum_height = 2
        li.minimum_width = 5
        li.maximum_height = 4
        li.maximum_width = 10

        # Check if the LineInput object has the correct size
        self.assertEqual(li.minimum_height, 2)
        self.assertEqual(li.minimum_width, 5)
        self.assertEqual(li.maximum_height, 4)
        self.assertEqual(li.maximum_width, 10)

        # Check if the LineInput object is an instance of LineInput class
        self.assertIsInstance(li, ui.LineInput)

    # Test that the LineInput object can handle input strings with non-ASCII characters
    def test_line_input_with_non_ascii_characters(self):
        # Create a LineInput instance
        li = ui.LineInput()

        # Set the text of the LineInput object with non-ASCII characters
        li.text = "Привет, мир!"

        # Check if the text is set correctly
        self.assertEqual(li.text, "Привет, мир!")

    # Test that when the filter property is set to INTEGER_FILTER it only accepts digits
    def test_filter_property_integer_filter_accepts_only_digits(self):
        # Create a LineInput instance
        li = ui.LineInput()

        # Set the filter property to INTEGER_FILTER
        li.filter = constants.InputValidator.INTEGER_FILTER

        # Test that only digits are accepted
        li.text = "123"
        self.assertEqual(li.text, "123")

        li.text = "abc"
        self.assertEqual(li.text, "123")

        li.text = "1a2b3c"
        self.assertEqual(li.text, "123")

        li.text = "12.34"
        self.assertEqual(li.text, "123")

    # Insert a character at the end of the content.
    def test_insert_character_end_of_content(self):
        line_input = ui.LineInput()
        line_input.insert_character("a")
        self.assertEqual(line_input.text, "a")

    # Insert a character at the cursor's position.
    def test_insert_character_cursor_position(self):
        line_input = ui.LineInput()
        line_input.insert_character("a", 0)
        line_input.insert_character("b", 1)
        line_input.insert_character("c", 2)
        self.assertEqual(line_input.text, "abc")

    # Insert a character at a specific position in the content.
    def test_insert_character_specific_position(self):
        line_input = ui.LineInput("abc")
        line_input.insert_character("d", 1)
        self.assertEqual(line_input.text, "adbc")

    # Insert a character at position 0 of an empty content.
    def test_insert_character_position_zero_empty_content(self):
        line_input = ui.LineInput()
        line_input.insert_character("a", 0)
        self.assertEqual(line_input.text, "a")

    # Insert a character at a position greater than the size of the content.
    def test_insert_character_position_greater_than_content_size(self):
        line_input = ui.LineInput("abc")
        line_input.insert_character("d", 5)
        self.assertEqual(line_input.text, "abcd")

    # Insert a non-printable character when the filter is set to printable.
    def test_insert_character_non_printable_character(self):
        line_input = ui.LineInput(filter=constants.InputValidator.PRINTABLE_FILTER)
        line_input.insert_character("\x00")
        self.assertEqual(line_input.text, "")

    # Insert a character at position -1.
    def test_insert_character_position_minus_1(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.insert_character("a", -1)
        self.assertEqual(line_input.text, "aHello")

    # Move cursor left when direction is LEFT and cursor is not at the beginning of the
    # content.
    def test_move_cursor_left(self):
        import pygamelib.gfx.ui as ui

        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.move_cursor(constants.Direction.LEFT)
        self.assertEqual(line_input.cursor.relative_column, 4)

    # Move cursor right when direction is RIGHT and cursor is not at the end of the
    # content.
    def test_move_cursor_right(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.move_cursor(constants.Direction.RIGHT)
        self.assertEqual(line_input.cursor.relative_column, len(line_input.text))

    # Do nothing when direction is not LEFT or RIGHT.
    def test_do_nothing_invalid_direction(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        cursor_position = line_input.cursor.relative_column
        line_input.move_cursor(constants.Direction.UP)
        self.assertEqual(line_input.cursor.relative_column, cursor_position)

    # Do nothing when cursor is at the beginning of the content and direction is LEFT.
    def test_do_nothing_left_at_beginning(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.cursor.relative_column = 0
        line_input.move_cursor(constants.Direction.LEFT)
        self.assertEqual(line_input.cursor.relative_column, 0)

    # Do nothing when cursor is at the end of the content and direction is RIGHT.
    def test_do_nothing_right_at_end(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.move_cursor(constants.Direction.RIGHT)
        self.assertEqual(line_input.cursor.relative_column, 5)

    # test that the cursor move correctly left and right if it is in the middle of the
    # text
    def test_cursor_moves_correctly_in_middle_of_sentence(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.move_cursor(constants.Direction.LEFT)
        self.assertEqual(line_input.cursor.relative_column, 4)
        line_input.move_cursor(constants.Direction.LEFT)
        self.assertEqual(line_input.cursor.relative_column, 3)
        line_input.move_cursor(constants.Direction.RIGHT)
        self.assertEqual(line_input.cursor.relative_column, 4)
        line_input.move_cursor(constants.Direction.RIGHT)
        self.assertEqual(line_input.cursor.relative_column, 5)

    # Test manipulation of the cursor through LineInput's specific methods.
    def test_set_cursor_relative_column_to_length_of_content(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.home()
        self.assertEqual(line_input.cursor.relative_column, 0)
        line_input.end()
        self.assertEqual(line_input.cursor.relative_column, len(line_input.text))

    # Delete character before cursor
    def test_delete_character_before_cursor(self):
        line_input = ui.LineInput(default="Hello")
        line_input.move_cursor(constants.Direction.LEFT)
        line_input.backspace()
        self.assertEqual(line_input.text, "Helo")

    # History is updated
    def test_history_updated(self):
        line_input = ui.LineInput(default="Hello")
        line_input.backspace()
        self.assertEqual(line_input.text, "Hell")
        self.assertEqual(line_input._LineInput__history.current, "Hell")

    # Cursor is at the beginning of the line
    def test_cursor_at_beginning(self):
        line_input = ui.LineInput(default="Hello")
        line_input.home()
        line_input.backspace()
        self.assertEqual(line_input.text, "Hello")

    # Line is empty
    def test_line_empty(self):
        line_input = ui.LineInput()
        line_input.backspace()
        self.assertEqual(line_input.text, "")

    # Line has only one character
    def test_line_one_character(self):
        line_input = ui.LineInput(default="H")
        line_input.backspace()
        self.assertEqual(line_input.text, "")

    # Delete character under cursor
    def test_delete_character_under_cursor(self):
        line_input = ui.LineInput()
        line_input.text = "Hello World"
        line_input.cursor.relative_column = 5
        line_input.delete()
        self.assertEqual(line_input.text, "HelloWorld")

    # Delete last character
    def test_delete_last_character(self):
        line_input = ui.LineInput()
        line_input.text = "Hello World"
        line_input.cursor.relative_column = len(line_input.text) - 1
        line_input.delete()
        self.assertEqual(line_input.text, "Hello Worl")

    # Delete first character
    def test_delete_first_character(self):
        line_input = ui.LineInput()
        line_input.text = "Hello World"
        line_input.cursor.relative_column = 0
        line_input.delete()
        self.assertEqual(line_input.text, "ello World")

    # Delete character when cursor is at the end of the line
    def test_delete_character_at_end_of_line(self):
        line_input = ui.LineInput()
        line_input.text = "Hello World"
        line_input.cursor.relative_column = len(line_input.text)
        line_input.delete()
        self.assertEqual(line_input.text, "Hello World")

    # Delete character when cursor is at the beginning of the line
    def test_delete_character_at_beginning_of_line(self):
        line_input = ui.LineInput()
        line_input.text = "Hello World"
        line_input.cursor.relative_column = 0
        line_input.delete()
        self.assertEqual(line_input.text, "ello World")

    # Delete character when line is empty
    def test_delete_character_when_line_is_empty(self):
        line_input = ui.LineInput()
        line_input.text = ""
        line_input.cursor.relative_column = 0
        line_input.delete()
        self.assertEqual(line_input.text, "")

    # Test that undo() method works when there is a history available and there is a
    # previous state to undo to.
    def test_undo_with_previous_state(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.insert_character(" World")
        line_input.undo()
        self.assertEqual(line_input.text, "Hello")

    # Test that undo() method does nothing when there is a history available but no
    # previous state to undo to.
    def test_undo_with_no_previous_state(self):
        line_input = ui.LineInput(history=base.History())
        line_input.undo()
        self.assertEqual(line_input.text, "")

    # Test that undo() method works when there is a history available and the previous
    # state is a string of length greater than 1.
    def test_undo_with_multiple_character_previous_state(self):
        line_input = ui.LineInput(history=base.History())
        line_input.text = "Hello"
        line_input.insert_character(" World")
        line_input.insert_character("!")
        line_input.undo()
        line_input.undo()
        self.assertEqual(line_input.text, "Hello")

    # Redo the last undone change when history is not None and current is not None.
    def test_redo_last_undone_change_with_history_and_current(self):
        line_input = ui.LineInput(history=base.History())
        line_input.insert_character("Hello")
        line_input.insert_character(" ")
        line_input.insert_character("World")
        line_input.undo()
        self.assertEqual(line_input.text, "Hello ")
        line_input.redo()
        self.assertEqual(line_input.text, "Hello World")

    # Clearing a LineInput with no text.
    def test_clear_with_no_text(self):
        line_input = ui.LineInput()
        line_input.clear()
        self.assertEqual(line_input.text, "")

    # Clearing a LineInput with some text.
    def test_clear_with_text(self):
        line_input = ui.LineInput(default="Hello")
        line_input.clear()
        self.assertEqual(line_input.text, "")

    # Clearing a LineInput with a history object.
    def test_clear_with_history(self):
        history = base.History()
        history.add("Hello")
        line_input = ui.LineInput(history=history)
        line_input.clear()
        self.assertEqual(line_input.text, "")
        self.assertIsNone(history.current)

    # Clearing a LineInput with a very long text.
    def test_clear_with_very_long_text(self):
        line_input = ui.LineInput(default="a" * 1000)
        line_input.clear()
        self.assertEqual(line_input.text, "")

    # Clearing a LineInput with a very short text.
    def test_clear_with_very_short_text(self):
        line_input = ui.LineInput(default="a")
        line_input.clear()
        self.assertEqual(line_input.text, "")

    # Clearing a LineInput with a history object and no text.
    def test_clear_with_history_and_no_text(self):
        history = base.History()
        history.add("Hello")
        line_input = ui.LineInput(history=history)
        line_input.text = ""
        line_input.clear()
        self.assertEqual(line_input.text, "")
        self.assertIsNone(history.current)

    # Test that length returns the correct length of the content when content is empty
    def test_length_empty_content(self):
        li = ui.LineInput()
        self.assertEqual(li.length(), 0)

    # Test that length returns the correct length of the content when content is not
    # empty
    def test_length_not_empty_content(self):
        li = ui.LineInput()
        li.text = "Hello, World!"
        self.assertEqual(li.length(), 13)

    # Test that length returns the correct length of the content when content is a
    # single character
    def test_length_single_character_content(self):
        li = ui.LineInput()
        li.text = "a"
        self.assertEqual(li.length(), 1)

    # Test that length returns 0 when content is None
    def test_length_none_content(self):
        li = ui.LineInput()
        li.text = None
        self.assertEqual(li.length(), 0)

    # Test that length returns 0 when content is not a string
    def test_length_non_string_content(self):
        li = ui.LineInput()
        li.text = 123
        self.assertEqual(li.length(), 0)

    # Test that length returns 0 when content is an empty list
    def test_length_empty_list_content(self):
        li = ui.LineInput()
        li.text = []
        self.assertEqual(li.length(), 0)

    # Test the rendering loop
    def test_empty_lineinput_rendering_loop(self):
        li = ui.LineInput()
        screen = engine.Screen(50, 50)
        screen.place(li, 10, 10)
        self.assertIsNone(screen.update())

    # Test the rendering loop with something in the LineInput
    def test_lineinput_rendering_loop(self):
        li = ui.LineInput()
        li.text = "Not empty"
        screen = engine.Screen(50, 50)
        screen.place(li, 10, 10)
        self.assertIsNone(screen.update())

    # Test the rendering loop while LineInput has the focus
    def test_focused_lineinput_rendering_loop(self):
        li = ui.LineInput()
        li.focus = True
        screen = engine.Screen(50, 50)
        screen.place(li, 10, 10)
        self.assertIsNone(screen.update())

    # Set filter to PRINTABLE_FILTER
    def test_set_filter_to_printable_filter(self):
        line_input = ui.LineInput()
        line_input.filter = constants.InputValidator.PRINTABLE_FILTER
        self.assertEqual(line_input.filter, constants.InputValidator.PRINTABLE_FILTER)

    # Set filter to INTEGER_FILTER
    def test_set_filter_to_integer_filter(self):
        line_input = ui.LineInput()
        line_input.filter = constants.InputValidator.INTEGER_FILTER
        self.assertEqual(line_input.filter, constants.InputValidator.INTEGER_FILTER)

    # Set filter to None
    def test_set_filter_to_none(self):
        line_input = ui.LineInput()
        with self.assertRaises(base.PglInvalidTypeException):
            line_input.filter = None

    # Set filter to an invalid value
    def test_set_filter_to_invalid_value(self):
        line_input = ui.LineInput()
        with self.assertRaises(base.PglInvalidTypeException):
            line_input.filter = "invalid_value"

    # Set filter to an invalid value
    def test_wrong_default_value_constructor(self):
        with self.assertRaises(base.PglInvalidTypeException):
            ui.LineInput(default=123)


if __name__ == "__main__":
    unittest.main()
