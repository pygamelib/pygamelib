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
        conf_init = ui.UiConfig()
        self.assertIsInstance(conf_init, ui.UiConfig)
        self.assertIsInstance(conf_init.game, engine.Game)
        conf = ui.UiConfig.instance(game=self.game)
        self.assertIsInstance(conf, ui.UiConfig)

    def test_dialog(self):
        d = ui.Dialog()
        self.assertIsInstance(d.config, ui.UiConfig)
        d = ui.Dialog(config=ui.UiConfig.instance())
        self.assertIsInstance(d, ui.Dialog)
        d.config = ui.UiConfig.instance()
        self.assertIsInstance(d.config, ui.UiConfig)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.Dialog(config="bork")
        with self.assertRaises(base.PglInvalidTypeException):
            d.config = "bork"
        with self.assertRaises(base.PglInvalidTypeException):
            d.user_input = 12
        d.user_input = "test"
        self.assertEqual(d.user_input, "test")
        with self.assertRaises(NotImplementedError):
            d.show()

    def test_box(self):
        b = ui.Box(
            20, 10, "test box", None, True, core.Sprixel(" "), constants.ALIGN_LEFT
        )
        self.assertIsInstance(b.config, ui.UiConfig)
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
            None,
        )
        self.assertIsInstance(pb.config, ui.UiConfig)

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
        ld = ui.LineInputDialog("title", base.Text("test line input"), config=conf)
        self.assertEqual(ld.label.text, "test line input")
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
        gd = ui.GridSelectorDialog()
        self.assertEqual(gd.config, ui.UiConfig.instance())
        grid_selector = ui.GridSelector()
        self.assertEqual(grid_selector.height, grid_selector.maximum_height)
        self.assertEqual(grid_selector.width, grid_selector.maximum_width)
        self.assertEqual(grid_selector.minimum_height, grid_selector.maximum_height)
        self.assertEqual(grid_selector.minimum_width, grid_selector.maximum_width)

        conf = ui.UiConfig.instance(game=self.game)
        gd = ui.GridSelectorDialog(
            ["a", "b", "c", "##"],
            maximum_height=10,
            maximum_width=20,
            title="test",
            config=conf,
        )
        self.assertEqual(gd.grid_selector.current_page, 0)
        gd.grid_selector.current_page = 1
        self.assertEqual(gd.grid_selector.current_page, 0)
        with self.assertRaises(base.PglInvalidTypeException):
            ui.GridSelectorDialog(
                ["a", "b", base.Text("c"), "##"],
                maximum_height=10,
                maximum_width=20,
                title="test",
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
        gd.grid_selector.maximum_height = 20
        self.assertEqual(gd.grid_selector.maximum_height, 20)
        gd.grid_selector.maximum_height = "42"
        self.assertEqual(
            gd.grid_selector.maximum_height, 20
        )  # #Tests to ensure that improper assignment fails silently as in Widget class
        gd.grid_selector.maximum_width = 20
        self.assertEqual(gd.grid_selector.maximum_width, 20)
        gd.grid_selector.maximum_width = "42"
        self.assertEqual(
            gd.grid_selector.maximum_width, 20
        )  # #Tests to ensure that improper assignment fails silently as in Widget class
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
        gd.grid_selector.maximum_width = 3
        gd.grid_selector.maximum_height = 3
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
            ui.GridSelectorDialog(
                ["a", "b", "c", "##"],
                maximum_height=10,
                maximum_width=20,
                title="test",
                config=conf,
            ),
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
        cp = ui.ColorPicker(config=conf, orientation=constants.Orientation.VERTICAL)
        self.assertEqual(cp._ColorPicker__orientation, constants.Orientation.VERTICAL)
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


if __name__ == "__main__":
    unittest.main()
