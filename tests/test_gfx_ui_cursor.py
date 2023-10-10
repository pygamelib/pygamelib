from pygamelib.gfx.ui import UiConfig, Cursor, Widget
from pygamelib.gfx import core
from pygamelib import engine, base
import unittest


class TestCursor(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.game = engine.Game.instance()
        self.game.screen = engine.Screen(50, 50)
        self.ui_config = UiConfig.instance(game=self.game)

    # Create a Cursor object with default parameters.
    def test_create_cursor_with_default_parameters(self):
        cursor = Cursor()
        self.assertEqual(cursor.relative_row, 0)
        self.assertEqual(cursor.relative_column, 0)
        self.assertEqual(cursor.blink_time, 0.4)
        self.assertIsInstance(cursor.model, core.Sprixel)
        self.assertIsNone(cursor.parent)

    # Create a Cursor object with custom parameters.
    def test_create_cursor_with_custom_parameters(self):
        cursor = Cursor(relative_row=2, relative_column=5, blink_time=0.5)
        self.assertEqual(cursor.relative_row, 2)
        self.assertEqual(cursor.relative_column, 5)
        self.assertEqual(cursor.blink_time, 0.5)
        self.assertIsInstance(cursor.model, core.Sprixel)
        self.assertIsNone(cursor.parent)

    # Set the model of a Cursor object.
    def test_set_cursor_model(self):
        model = core.Sprixel(
            "|", bg_color=core.Color(255, 255, 255), fg_color=core.Color(0, 0, 0)
        )
        cursor = Cursor(model=model)
        self.assertEqual(cursor.model, model)

    # Create a Cursor object with a negative relative row.
    def test_create_cursor_with_negative_relative_row(self):
        cursor = Cursor(relative_row=-1)
        self.assertEqual(cursor.relative_row, 0)

    # Create a Cursor object with a negative relative column.
    def test_create_cursor_with_negative_relative_column(self):
        cursor = Cursor(relative_column=-1)
        self.assertEqual(cursor.relative_column, 0)

    # Set the model of a Cursor object with an invalid type.
    def test_set_cursor_model_with_invalid_type(self):
        cursor = Cursor()
        with self.assertRaises(base.PglInvalidTypeException):
            cursor.model = "invalid_model"

    # test the model property
    def test_model_property(self):
        # Create a cursor with default parameters
        cursor = Cursor()

        # Test that the default model is an instance of core.Sprixel
        self.assertIsInstance(cursor.model, core.Sprixel)

        # Create a new model
        new_model = core.Sprixel("X", bg_color=core.Color(255, 0, 0))

        # Set the new model as the cursor's model
        cursor.model = new_model

        # Test that the cursor's model has been updated
        self.assertEqual(cursor.model, new_model)

    # test the parent property
    def test_parent_property(self):
        # Create a cursor with default parameters
        cursor = Cursor()

        # Test that the default parent is None
        self.assertIsNone(cursor.parent)

        # Create a new parent widget
        new_parent = Widget()

        # Set the new parent as the cursor's parent
        cursor.parent = new_parent

        # Test that the cursor's parent has been updated
        self.assertEqual(cursor.parent, new_parent)

    # test the rendering loop
    def test_rendering_loop(self):
        # Create a cursor with default parameters
        cursor = Cursor(blink_time=0)

        # Set up the initial position of the cursor
        cursor.screen_row = 5
        cursor.screen_column = 5

        # Render the cursor to the buffer
        self.assertIsNone(
            cursor.render_to_buffer(
                self.game.screen.buffer,
                cursor.screen_row,
                cursor.screen_column,
                self.game.screen.height,
                self.game.screen.width,
            )
        )

        # Check that the cursor is rendered correctly in the buffer
        self.assertEqual(
            self.game.screen.buffer[cursor.screen_row, cursor.screen_column].model,
            cursor.model.model,
        )

        # Move the cursor to a new position
        cursor.screen_row = 6
        cursor.screen_column = 6

        # Render the cursor to the buffer again
        cursor.render_to_buffer(
            self.game.screen.buffer,
            cursor.screen_row,
            cursor.screen_column,
            self.game.screen.height,
            self.game.screen.width,
        )

        # Check that the previous position of the cursor is cleared in the buffer
        self.assertEqual(
            self.game.screen.buffer[
                cursor.screen_row - 1, cursor.screen_column - 1
            ].model,
            core.Sprixel(" ").model,
        )
