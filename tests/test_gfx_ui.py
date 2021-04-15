import pygamelib.base as pgl_base
from pygamelib.gfx import core, ui
from pygamelib import constants, engine
import unittest
from pathlib import Path


class FakeText:
    def __init__(self, text) -> None:
        self.text = text

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        pass


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()

    def test_uiconfig(self):
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.UiConfig()
        conf = ui.UiConfig.instance(game=self.game)
        self.assertIsInstance(conf, ui.UiConfig)

    def test_dialog(self):
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.Dialog()
        d = ui.Dialog(config=ui.UiConfig.instance())
        self.assertIsInstance(d, ui.Dialog)
        d.config = ui.UiConfig.instance()
        self.assertIsInstance(d.config, ui.UiConfig)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            d.config = "bork"
        with self.assertRaises(pgl_base.PglInvalidTypeException):
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
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            b.config = 2
        self.assertEqual(b.width, 20)
        b.width = 30
        self.assertEqual(b.width, 30)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            b.width = "20"
        self.assertEqual(b.height, 10)
        b.height = 20
        self.assertEqual(b.height, 20)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            b.height = "20"
        b.title = ""
        self.assertEqual(b.title, "")
        self.game.screen.place(b, 0, 0)
        self.game.screen.update()
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            b.title = 2

    def test_progressbar(self):
        conf = ui.UiConfig.instance(game=self.game)
        conf.borderless_dialog = False
        pb = ui.ProgressDialog(
            pgl_base.Text("test"),
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
        pb.label = pgl_base.Text("Test text")
        self.assertEqual(pb.label, "Test text")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.label = 2
        self.assertEqual(pb.value, 0)
        pb.value = 2
        self.assertEqual(pb.value, 2)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.value = "3"
        self.assertEqual(pb.maximum, 100)
        pb.maximum = 20
        self.assertEqual(pb.maximum, 20)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
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
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.config = 3
        self.assertIsInstance(pb.progress_marker, core.Sprixel)
        self.assertIsInstance(pb.empty_marker, core.Sprixel)
        pb.progress_marker = "#"
        self.assertEqual(pb.progress_marker, "#")
        pb.progress_marker = pgl_base.Text("#")
        self.assertEqual(pb.progress_marker, "#")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.progress_marker = 3
        pb.empty_marker = "#"
        self.assertEqual(pb.empty_marker, "#")
        pb.empty_marker = pgl_base.Text("#")
        self.assertEqual(pb.empty_marker, "#")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.empty_marker = 3
        self.assertEqual(pb.value, 0)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.value = "10"
        self.assertEqual(pb.maximum, 100)
        pb.maximum = 10
        self.assertEqual(pb.maximum, 10)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pb.maximum = "10"

    def test_message_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        # Test when height is none and adpatative_height is False (it will be tuned on)
        md = ui.MessageDialog(
            [
                "Test",
                "Message dialog",
                FakeText("fake"),
                pgl_base.Text("Another test"),
                core.Sprixel("!"),
            ],
            adaptive_height=False,
            config=conf,
        )
        self.game.screen.place(md, 0, 0)
        self.game.screen.update()
        md.add_line("test 2", constants.ALIGN_RIGHT)
        md.add_line("test 3", constants.ALIGN_CENTER)
        md.add_line(pgl_base.Text("test 4"), constants.ALIGN_RIGHT)
        md.add_line(pgl_base.Text("test 5"), constants.ALIGN_CENTER)
        self.game.screen.force_update()
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            md.add_line(1, constants.ALIGN_CENTER)
        self.assertIs(type(md.height), int)
        # Now test with fixed height
        md = ui.MessageDialog(
            [
                "Test",
                "Message dialog",
                FakeText("fake"),
                pgl_base.Text("Another test"),
                core.Sprixel("!"),
            ],
            adaptive_height=False,
            height=10,
            config=conf,
        )
        self.assertEqual(md.height, 10)
        md.height = 6
        self.assertEqual(md.height, 6)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            md.height = "6"

    def test_lineinput_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.LineInputDialog(123, config=conf)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.LineInputDialog(default=12, config=conf)
        ld = ui.LineInputDialog("test line input", config=conf)
        self.assertEqual(ld.label.text, "test line input")
        ld.label = "test 2"
        self.assertEqual(ld.label.text, "test 2")
        ld.label = pgl_base.Text("test 3")
        self.assertEqual(ld.label.text, "test 3")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ld.label = 3
        self.game.screen.place(ld, 0, 0)
        self.game.screen.update()

    def test_multiline_input_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.MultiLineInputDialog(fields=1, config=conf)
        mld = ui.MultiLineInputDialog(config=conf)
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
        mld.fields = [
            {
                "label": pgl_base.Text("Input a value:"),
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
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            mld.fields = 42

        self.game.screen.place(mld, 0, 0)
        self.game.screen.update()

    def test_file_dialog(self):
        conf = ui.UiConfig.instance(game=self.game)
        fd = ui.FileDialog(Path("tests"), config=conf)
        self.assertEqual(fd.path, Path("tests"))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            fd.path = 42

        fd.path = Path()
        self.assertEqual(fd.path, Path())
        self.assertEqual(fd.filter, "*")
        fd.filter = "*.spr"
        self.assertEqual(fd.filter, "*.spr")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            fd.filter = 42
        self.assertFalse(fd.show_hidden_files)
        fd.show_hidden_files = True
        self.assertTrue(fd.show_hidden_files)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            fd.show_hidden_files = 42

        fd.user_input = "Some input but not just any input, a very very long user input"

        self.game.screen.place(fd, 0, 0)
        self.game.screen.update()
        fd.user_input = "Some input"
        self.game.screen.force_update()

    def test_gridselector(self):
        conf = ui.UiConfig.instance(game=self.game)
        gd = ui.GridSelectorDialog(["a", "b", "c", "##"], 10, 20, "test", config=conf)
        self.assertEqual(gd.grid_selector.current_page, 0)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            ui.GridSelectorDialog(
                ["a", "b", pgl_base.Text("c"), "##"], 10, 20, "test", config=conf
            )

        self.assertEqual(gd.title, "test")
        gd.title = "test 2"
        self.assertEqual(gd.title, "test 2")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.title = 42
        self.assertIsInstance(gd.grid_selector, ui.GridSelector)
        self.assertEqual(len(gd.grid_selector.choices), 4)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.grid_selector.choices = 3

        gd.grid_selector.choices = ["a", "b", "c"]
        self.assertEqual(len(gd.grid_selector.choices), 3)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.grid_selector.choices = "42"
        gd.grid_selector.max_height = 20
        self.assertEqual(gd.grid_selector.max_height, 20)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.grid_selector.max_height = "42"
        gd.grid_selector.max_width = 20
        self.assertEqual(gd.grid_selector.max_width, 20)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.grid_selector.max_width = "42"
        self.assertEqual(gd.grid_selector.current_choice, 0)
        gd.grid_selector.current_choice = 1
        self.assertEqual(gd.grid_selector.current_choice, 1)
        self.assertIsInstance(gd.grid_selector.current_sprixel(), core.Sprixel)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
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
        with self.assertRaises(pgl_base.PglInvalidTypeException):
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
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            gd.grid_selector = 42

    def test_colorpickers(self):
        conf = ui.UiConfig.instance(game=self.game)
        cpd = ui.ColorPickerDialog(conf)
        cpd.set_color(core.Color(1, 2, 3))
        cd = ui.ColorPicker(config=conf)
        self.assertEqual(cd.selection, 0)
        cd.selection = 1
        self.assertEqual(cd.selection, 1)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            cd.selection = "42"
        self.assertIsInstance(cd.color, core.Color)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            cd.color = "42"
        cd.color = core.Color(4, 5, 6)
        self.assertEqual(cd.color.r, 4)
        self.assertEqual(cd.color.g, 5)
        self.assertEqual(cd.color.b, 6)
        self.assertEqual(cd.red, 4)
        self.assertEqual(cd.green, 5)
        self.assertEqual(cd.blue, 6)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            cd.red = "42"
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            cd.green = "42"
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            cd.blue = "42"

        self.game.screen.place(cpd, 0, 0)
        self.game.screen.update()


if __name__ == "__main__":
    unittest.main()
