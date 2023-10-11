import pygamelib.base as base
from pygamelib.gfx import ui
from pygamelib import constants, engine
import unittest


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
        line_input.insert_characters("a")
        self.assertEqual(line_input.text, "a")

    # Insert a character at the cursor's position.
    def test_insert_character_cursor_position(self):
        line_input = ui.LineInput()
        line_input.insert_characters("a", 0)
        line_input.insert_characters("b", 1)
        line_input.insert_characters("c", 2)
        self.assertEqual(line_input.text, "abc")

    # Insert a character at a specific position in the content.
    def test_insert_character_specific_position(self):
        line_input = ui.LineInput("abc")
        line_input.insert_characters("d", 1)
        self.assertEqual(line_input.text, "adbc")

    # Insert a character at position 0 of an empty content.
    def test_insert_character_position_zero_empty_content(self):
        line_input = ui.LineInput()
        line_input.insert_characters("a", 0)
        self.assertEqual(line_input.text, "a")

    # Insert a character at a position greater than the size of the content.
    def test_insert_character_position_greater_than_content_size(self):
        line_input = ui.LineInput("abc")
        line_input.insert_characters("d", 5)
        self.assertEqual(line_input.text, "abcd")

    # Insert a non-printable character when the filter is set to printable.
    def test_insert_character_non_printable_character(self):
        line_input = ui.LineInput(filter=constants.InputValidator.PRINTABLE_FILTER)
        line_input.insert_characters("\x00")
        self.assertEqual(line_input.text, "")

    # Insert a character at position -1.
    def test_insert_character_position_minus_1(self):
        line_input = ui.LineInput()
        line_input.text = "Hello"
        line_input.insert_characters("a", -1)
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
        line_input.insert_characters(" World")
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
        line_input.insert_characters(" World")
        line_input.insert_characters("!")
        line_input.undo()
        line_input.undo()
        self.assertEqual(line_input.text, "Hello")

    # Redo the last undone change when history is not None and current is not None.
    def test_redo_last_undone_change_with_history_and_current(self):
        line_input = ui.LineInput(history=base.History())
        line_input.insert_characters("Hello")
        line_input.insert_characters(" ")
        line_input.insert_characters("World")
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
