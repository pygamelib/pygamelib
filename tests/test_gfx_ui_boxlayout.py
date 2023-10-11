from pygamelib.gfx.ui import Widget, UiConfig, BoxLayout
from pygamelib import engine, constants, base
import unittest


class TestBoxLayout(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Create a BoxLayout object with default parameters
    def test_default_parameters(self):
        layout = BoxLayout()
        self.assertEqual(layout.orientation, constants.Orientation.HORIZONTAL)
        self.assertEqual(layout.size_constraint, constants.SizeConstraint.DEFAULT_SIZE)
        self.assertEqual(layout.count(), 0)
        self.assertEqual(layout.width, 0)
        self.assertEqual(layout.height, 0)

    # Create a BoxLayout object with specified orientation and size constraint
    def test_specified_orientation_and_size_constraint(self):
        layout = BoxLayout(
            orientation=constants.Orientation.VERTICAL,
            size_constraint=constants.SizeConstraint.MINIMUM_SIZE,
        )
        self.assertEqual(layout.orientation, constants.Orientation.VERTICAL)
        self.assertEqual(layout.size_constraint, constants.SizeConstraint.MINIMUM_SIZE)
        self.assertEqual(layout.count(), 0)
        self.assertEqual(layout.width, 0)
        self.assertEqual(layout.height, 0)

    # Add a widget to the BoxLayout
    def test_add_widget(self):
        layout = BoxLayout()
        widget = Widget(width=10, height=5)
        self.assertTrue(layout.add_widget(widget))
        self.assertEqual(layout.count(), 1)
        self.assertEqual(layout.width, 10)
        self.assertEqual(layout.height, 5)

    # Create a BoxLayout object with invalid orientation
    def test_invalid_orientation(self):
        with self.assertRaises(base.PglInvalidTypeException):
            BoxLayout(orientation="invalid")

    # Create a BoxLayout object with invalid size constraint policy
    def test_invalid_size_constraint(self):
        with self.assertRaises(base.PglInvalidTypeException):
            BoxLayout(size_constraint="invalid")

    # Add a non-widget object to the BoxLayout
    def test_add_non_widget(self):
        layout = BoxLayout()
        non_widget = "not a widget"
        self.assertFalse(layout.add_widget(non_widget))
        self.assertEqual(layout.count(), 0)
        self.assertEqual(layout.width, 0)
        self.assertEqual(layout.height, 0)

    # test the orientation property
    def test_orientation_property(self):
        # Create a BoxLayout with default parameters
        layout = BoxLayout()

        # Check that the default orientation is HORIZONTAL
        self.assertEqual(layout.orientation, constants.Orientation.HORIZONTAL)

        # Change the orientation to VERTICAL
        layout.orientation = constants.Orientation.VERTICAL

        # Check that the orientation has been updated
        self.assertEqual(layout.orientation, constants.Orientation.VERTICAL)

        # Change the orientation to an invalid value
        layout.orientation = "invalid"

        # Check that the orientation remains unchanged
        self.assertEqual(layout.orientation, constants.Orientation.VERTICAL)

    # test the size_constraint property
    def test_size_constraint_property(self):
        # Create a BoxLayout with default parameters
        layout = BoxLayout()

        # Check that the default size_constraint is DEFAULT_SIZE
        self.assertEqual(layout.size_constraint, constants.SizeConstraint.DEFAULT_SIZE)

        # Create a widget and add it to the layout
        widget = Widget()
        layout.add_widget(widget)

        # Check that the widget's size_constraint is set to the layout's size_constraint
        self.assertEqual(widget.size_constraint, layout.size_constraint)

        # Change the layout's size_constraint
        layout.size_constraint = constants.SizeConstraint.EXPAND

        # Check that the widget's size_constraint is updated
        self.assertEqual(widget.size_constraint, layout.size_constraint)

        # Change the layout's size_constraint to an invalid value
        layout.size_constraint = "invalid"

        # Check that the widget's size_constraint is not changed
        self.assertEqual(widget.size_constraint, constants.SizeConstraint.EXPAND)

    # test the width property
    def test_width_property(self):
        # Create a BoxLayout object
        layout = BoxLayout()

        # Create two widgets with different widths
        widget1 = Widget(10, 20)
        widget2 = Widget(15, 25)

        # Add the widgets to the layout
        layout.add_widget(widget1)
        layout.add_widget(widget2)

        # Check that the width property returns the correct value
        self.assertEqual(layout.width, widget1.width + widget2.width + layout.spacing)

        # Create a BoxLayout object with a vertical layout
        layout = BoxLayout(orientation=constants.Orientation.VERTICAL)

        # Create two widgets with different heights
        widget1 = Widget(10, 20)
        widget2 = Widget(15, 25)

        # Add the widgets to the layout
        layout.add_widget(widget1)
        layout.add_widget(widget2)

        # Check that the width property returns the correct value
        expected_width = max(widget1.width, widget2.width)
        expected_width += layout.spacing * (layout.count() - 1)
        self.assertEqual(layout.width, expected_width)

    # test the height property
    def test_height_property(self):
        # Create a BoxLayout with vertical orientation
        layout = BoxLayout(orientation=constants.Orientation.VERTICAL)

        # Create two widgets with different heights
        widget1 = Widget(10, 20)
        widget2 = Widget(15, 20)

        # Add the widgets to the layout
        layout.add_widget(widget1)
        layout.add_widget(widget2)

        # Check that the height property returns the correct value
        self.assertEqual(
            layout.height, widget1.height + widget2.height + layout.spacing
        )

    # test the render loop
    def test_render_loop(self):
        layout = BoxLayout()
        widget1 = Widget(10, 10)
        widget2 = Widget(20, 20)
        layout.add_widget(widget1)
        layout.add_widget(widget2)

        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 30, 30)
        )

        self.assertEqual(widget1.screen_row, 0)
        self.assertEqual(widget1.screen_column, 0)
        self.assertEqual(widget2.screen_row, 0)
        self.assertEqual(widget2.screen_column, 10)
        self.assertEqual(layout.width, 30)
        self.assertEqual(layout.height, 20)

        # Test widget culling by giving a smaller area to render into
        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 10, 10)
        )

        # Test rendering in a different orientation
        layout.orientation = constants.Orientation.VERTICAL
        self.assertIsNone(
            layout.render_to_buffer(self.game.screen.buffer, 0, 0, 30, 30)
        )
