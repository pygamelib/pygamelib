from pygamelib import engine
import unittest
from blessed import Terminal

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.term = Terminal()
        self.screen = engine.Screen(self.term)

    def test_screen_create_empty(self):
        with self.assertRaises(Exception) as context:
            engine.Screen()

        self.assertTrue("terminal_is_missing" in str(context.exception))

    def test_screen_create_bad(self):
        with self.assertRaises(Exception) as context:
            engine.Screen("Terminal")

        self.assertTrue("terminal_not_blessed" in str(context.exception))

    def test_screen_create_good(self):
        scr = engine.Screen(self.term)
        self.assertIsInstance(scr, engine.Screen)

    def test_screen_dimension(self):
        self.assertEqual(self.term.width, self.screen.width)
        self.assertEqual(self.term.height, self.screen.height)


if __name__ == "__main__":
    unittest.main()
