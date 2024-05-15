from pygamelib.gfx.ui import Widget, UiConfig, FormLayout
from pygamelib import engine
from pygamelib.base import Text
import unittest


class TestFormLayout(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Add a widget to the form layout
    def test_add_row_to_form_layout(self):
        layout = FormLayout()
        widget = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertEqual(layout.count_rows(), 1)
        self.assertEqual(layout.widgets(), [widget])
        self.assertTrue(layout.add_row("Test 2", widget))
        self.assertEqual(layout.count_rows(), 2)

    # Add a wrong type of widget to the form layout
    def test_add_row_to_form_layout_wrong_widget(self):
        layout = FormLayout()
        self.assertFalse(layout.add_row(Text("Test 1"), None))
        self.assertFalse(layout.add_row(Text("Test 1"), "Invalid"))

    # Add a wrong type of label to the form layout
    def test_add_row_to_form_layout_wrong_label(self):
        widget = Widget()
        layout = FormLayout()
        self.assertFalse(layout.add_row(None, widget))
        self.assertFalse(layout.add_row(widget, widget))

    # insert a widget to the form layout
    def test_insert_row_to_form_layout(self):
        layout = FormLayout()
        widget = Widget()
        widget2 = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.insert_row(0, Text("Test 2"), widget2))
        self.assertEqual(layout.count_rows(), 2)
        self.assertEqual(layout.widgets()[1], widget)
        self.assertEqual(layout.widgets()[0], widget2)
        self.assertTrue(layout.insert_row(999, "Test 3", widget))
        self.assertEqual(layout.count_rows(), 3)
        self.assertTrue(layout.insert_row(1, "Test 4", widget))
        self.assertEqual(layout.count_rows(), 4)
        self.assertTrue(layout.insert_row(0, Text("Test 5 (which is longer)"), widget))
        self.assertEqual(layout.count(), 5)

    # insert a wrong type of widget to the form layout
    def test_insert_row_to_form_layout_wrong_widget(self):
        layout = FormLayout()
        self.assertFalse(layout.insert_row(0, Text("Test 1"), None))
        self.assertFalse(layout.insert_row(0, Text("Test 1"), "Invalid"))

    # insert a wrong type of label to the form layout
    def test_insert_row_to_form_layout_wrong_label(self):
        widget = Widget()
        layout = FormLayout()
        self.assertFalse(layout.insert_row(0, None, widget))
        self.assertFalse(layout.insert_row(0, widget, widget))

    def test_remove_row(self):
        layout = FormLayout()
        widget = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget))
        self.assertEqual(layout.count_rows(), 4)
        self.assertTrue(layout.remove_row(1))
        self.assertFalse(layout.remove_row(99))
        self.assertEqual(layout.count_rows(), 3)

    def test_remove_row_bad_input(self):
        layout = FormLayout()
        widget = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget))
        self.assertEqual(layout.count_rows(), 4)
        self.assertFalse(layout.remove_row(99))
        self.assertEqual(layout.count_rows(), 4)
        self.assertTrue(layout.remove_row())
        self.assertEqual(layout.count_rows(), 3)

    def test_set_label(self):
        layout = FormLayout()
        widget = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget))
        layout.set_label(1, "Another test")
        (l, w) = layout.get_row(1)
        self.assertEqual(l.text, "Another test")
        self.assertEqual(w, widget)

    def test_set_widget(self):
        layout = FormLayout()
        widget = Widget(10, 10)
        widget2 = Widget(20, 20)
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget))
        layout.set_widget(1, widget2)
        (l, w) = layout.get_row(1)
        self.assertEqual(l.text, "Test 2")
        self.assertEqual(w, widget2)

    def test_get_row(self):
        layout = FormLayout()
        widget = Widget()
        widget2 = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget2))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget2))
        (l, w) = layout.get_row(1)
        self.assertEqual(l.text, "Test 2")
        self.assertEqual(w, widget2)
        (l, w) = layout.get_row(2)
        self.assertEqual(l.text, "Test 3")
        self.assertEqual(w, widget)

    def test_get_row_bad_input(self):
        layout = FormLayout()
        widget = Widget()
        widget2 = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget2))
        (l, w) = layout.get_row("Wrong answer only!")
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget2)
        (l, w) = layout.get_row(None)
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget2)
        (l, w) = layout.get_row(-1)
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget2)
        (l, w) = layout.get_row(999)
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget2)

    def test_take_row(self):
        layout = FormLayout()
        widget = Widget()
        widget2 = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget2))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget2))

        (l, w) = layout.take_row(2)
        self.assertEqual(l.text, "Test 3")
        self.assertEqual(w, widget)
        self.assertEqual(layout.count_rows(), 3)

        (l, w) = layout.get_row(2)
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget2)
        self.assertEqual(layout.count_rows(), 3)

    def test_take_row_bad_input(self):
        layout = FormLayout()
        widget = Widget()
        widget2 = Widget()
        self.assertTrue(layout.add_row(Text("Test 1"), widget))
        self.assertTrue(layout.add_row(Text("Test 2"), widget))
        self.assertTrue(layout.add_row(Text("Test 3"), widget))
        self.assertTrue(layout.add_row(Text("Test 4"), widget))
        self.assertTrue(layout.add_row(Text("Test 5"), widget))
        self.assertTrue(layout.add_row(Text("Test 6"), widget2))
        (l, w) = layout.take_row("Wrong answer only!")
        self.assertEqual(l.text, "Test 6")
        self.assertEqual(w, widget2)
        (l, w) = layout.take_row(None)
        self.assertEqual(l.text, "Test 5")
        self.assertEqual(w, widget)
        (l, w) = layout.take_row(-1)
        self.assertEqual(l.text, "Test 4")
        self.assertEqual(w, widget)
        (l, w) = layout.take_row(999)
        self.assertEqual(l.text, "Test 3")
        self.assertEqual(w, widget)

    # test the rendering loop
    def test_render_loop(self):
        layout = FormLayout(parent=Widget(30, 30))
        widget1 = Widget(10, 10)
        widget2 = Widget(20, 20)
        layout.add_row(Text("Test 1"), widget1)
        layout.add_row(Text("Test 2"), widget2)

        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 30, 30)
        )

        # self.assertEqual(widget1.screen_row, 0)
        # self.assertEqual(widget1.screen_column, layout.get_row(0)[0].length)
        # self.assertEqual(widget2.screen_row, 10)
        # self.assertEqual(widget2.screen_column, layout.get_row(0)[0].length)
        # self.assertEqual(layout.width, 20)
        # self.assertEqual(layout.height, 30)

        # Test widget culling by giving a smaller area to render into
        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 10, 10)
        )
