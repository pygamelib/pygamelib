from pygamelib.gfx.ui import Widget, UiConfig, Layout
from pygamelib import engine
import unittest


class TestLayout(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Creating a Layout object with a parent widget sets the parent's layout to the
    # Layout object
    def test_parent_layout_set(self):
        parent_widget = Widget()
        layout = Layout(parent_widget)
        self.assertEqual(parent_widget.layout, layout)

    # Implementing the width and height properties in a child class returns the total
    # width and height of the layout
    def test_width_and_height_properties(self):
        class ChildLayout(Layout):
            @property
            def width(self):
                return 10

            @property
            def height(self):
                return 8

        layout = ChildLayout()
        self.assertEqual(layout.width, 10)
        self.assertEqual(layout.height, 8)

    # Creating a Layout object without a parent widget sets the parent property to None
    def test_parent_property_none(self):
        layout = Layout()
        self.assertIsNone(layout.parent)

    # Setting the spacing property to 0 does not raise any errors
    def test_spacing_zero(self):
        layout = Layout()
        layout.spacing = 0

    # Adding a widget to a full layout using add_widget() method returns False
    def test_add_widget_full_layout(self):
        class FullLayout(Layout):
            def add_widget(self, w):
                return False

        layout = FullLayout()
        widget = Widget()
        self.assertFalse(layout.add_widget(widget))

    # test that the parent is correctly set when using Layout.parent
    def test_parent_property_set(self):
        parent_widget = Widget()
        layout = Layout()
        layout.parent = parent_widget
        self.assertEqual(parent_widget.layout, layout)

    # Test the spacing property
    def test_spacing_property(self):
        layout = Layout()
        layout.spacing = 10
        self.assertEqual(layout.spacing, 10)

    # test all the functions that are raising a NotImplementedError
    def test_not_implemented_error(self):
        layout = Layout()
        with self.assertRaises(NotImplementedError):
            layout.width
        with self.assertRaises(NotImplementedError):
            layout.height
        with self.assertRaises(NotImplementedError):
            layout.add_widget(Widget())
        with self.assertRaises(NotImplementedError):
            layout.count()
        with self.assertRaises(NotImplementedError):
            layout.widgets()
        with self.assertRaises(NotImplementedError):
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 0, 0)
