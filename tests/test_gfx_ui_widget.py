import unittest
from pygamelib.gfx.ui import Widget, UiConfig, BoxLayout
from pygamelib.gfx.core import Color
from pygamelib import engine, base, constants


class TestWidget(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Create a Widget object with default parameters.
    def test_create_widget_with_default_parameters(self):
        widget = Widget()
        self.assertEqual(widget.width, 0)
        self.assertEqual(widget.height, 0)
        self.assertIsNone(widget.bg_color)
        self.assertIsNone(widget.parent)
        self.assertEqual(widget.maximum_width, 20)
        self.assertEqual(widget.maximum_height, 10)
        self.assertEqual(widget.minimum_width, 0)
        self.assertEqual(widget.minimum_height, 0)
        self.assertIsNone(widget.layout)
        self.assertEqual(widget.size_constraint, constants.SizeConstraint.DEFAULT_SIZE)
        self.assertFalse(widget.focus)

    # Create a Widget object with width and heigh outside of the max and min values.
    def test_create_widget_with_default_parameters_outside_of_max_and_min(self):
        widget = Widget(
            width=0,
            height=0,
            minimum_width=2,
            minimum_height=2,
            maximum_width=15,
            maximum_height=8,
        )
        self.assertEqual(widget.width, 2)
        self.assertEqual(widget.height, 2)
        self.assertIsNone(widget.bg_color)
        self.assertIsNone(widget.parent)
        self.assertEqual(widget.maximum_width, 15)
        self.assertEqual(widget.maximum_height, 8)
        self.assertEqual(widget.minimum_width, 2)
        self.assertEqual(widget.minimum_height, 2)
        self.assertIsNone(widget.layout)
        self.assertEqual(widget.size_constraint, constants.SizeConstraint.DEFAULT_SIZE)
        self.assertFalse(widget.focus)

    # Set the parent of a Widget object to another Widget or BoxLayout object.
    def test_set_parent_widget(self):
        widget = Widget()
        parent_widget = Widget()
        layout = BoxLayout()

        widget.parent = parent_widget
        self.assertEqual(widget.parent, parent_widget)

        widget.parent = layout
        self.assertEqual(widget.parent, layout)

    # Test the layout parameter of the constructor.
    def test_set_layout_parameter(self):
        widget = Widget(layout=BoxLayout())
        self.assertIsInstance(widget.layout, BoxLayout)

    # Set the background color of a Widget object.
    def test_set_background_color(self):
        widget = Widget()
        color = Color(255, 255, 255)

        widget.bg_color = color
        self.assertEqual(widget.bg_color, color)

    # Create a Widget object with maximum width less than its width.
    def test_create_widget_with_maximum_width_less_than_width(self):
        widget = Widget(width=10, maximum_width=5)
        self.assertEqual(widget.width, 10)

    # Create a Widget object with height less than its minimum height.
    def test_create_widget_with_height_less_than_minimum_height(self):
        widget = Widget(height=2, minimum_height=5)
        self.assertEqual(widget.height, 5)

    # Set the maximum width of a Widget object to less than its width.
    def test_set_maximum_width_less_than_width(self):
        widget = Widget(width=10)
        widget.maximum_width = 5
        self.assertEqual(widget.width, 5)

    # Test that children widgets added to a widget's layout are returned when using the
    # Widget.children property
    def test_children_widgets_added_to_layout_are_returned(self):
        widget = Widget()
        layout = BoxLayout()
        widget.layout = layout
        child_widget = Widget()
        layout.add_widget(child_widget)
        self.assertIn(widget.children[0], [child_widget])

    # Test that when the maximum and minimum width and height are adjusted through their
    # properties, the width and height are updated accordingly when they are outside of
    # the defined values.
    def test_adjust_width_and_height(self):
        widget = Widget()
        widget.width = 10
        widget.height = 5
        self.assertEqual(widget.width, 10)
        self.assertEqual(widget.height, 5)

        widget.maximum_width = 15
        widget.maximum_height = 8
        self.assertEqual(widget.maximum_width, 15)
        self.assertEqual(widget.maximum_height, 8)
        self.assertEqual(widget.width, 10)
        self.assertEqual(widget.height, 5)

        widget.height = 8
        widget.width = 15
        widget.maximum_height = 5
        self.assertEqual(widget.height, 5)
        widget.maximum_width = 10
        self.assertEqual(widget.width, 10)

        widget.maximum_width = 15
        widget.maximum_height = 8

        widget.minimum_width = 3
        widget.minimum_height = 2
        self.assertEqual(widget.minimum_width, 3)
        self.assertEqual(widget.minimum_height, 2)
        self.assertEqual(widget.width, 10)
        self.assertEqual(widget.height, 5)

        widget.width = 20
        widget.height = 12
        self.assertEqual(widget.width, 15)
        self.assertEqual(widget.height, 8)

        widget.width = 1
        widget.height = 1
        self.assertEqual(widget.width, 3)
        self.assertEqual(widget.height, 2)

    # Test that  the Widget.layout setter raise an exception if we try to set it with
    # something else than a Layout
    def test_layout_setter_exception(self):
        widget = Widget()
        with self.assertRaises(base.PglInvalidTypeException):
            widget.layout = "not_a_layout"

    # Test that changing the Widget.size_constraint property has the appropriate effect
    # on maximum and minimum width and height
    def test_size_constraint_property(self):
        widget = Widget(
            width=10,
            height=5,
            minimum_width=2,
            minimum_height=2,
            maximum_width=15,
            maximum_height=8,
        )
        widget.size_constraint = constants.SizeConstraint.MINIMUM_SIZE
        self.assertEqual(widget.width, widget.minimum_width)
        self.assertEqual(widget.height, widget.minimum_height)

        widget.size_constraint = constants.SizeConstraint.MAXIMUM_SIZE
        self.assertEqual(widget.width, widget.maximum_width)
        self.assertEqual(widget.height, widget.maximum_height)

    # Test the rendering loop
    def test_empty_lineinput_rendering_loop(self):
        widget = Widget(width=5, height=2, layout=BoxLayout())
        screen = engine.Screen(50, 50)
        screen.place(widget, 10, 10)
        self.assertIsNone(screen.update())
