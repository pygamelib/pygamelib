from pygamelib import engine
from pygamelib.gfx.core import Sprite, SpriteCollection, Sprixel
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

    def test_clear(self):
        self.assertIsNone(self.screen.clear())

    def test_screen_dimension(self):
        self.assertEqual(self.term.width, self.screen.width)
        self.assertEqual(self.term.height, self.screen.height)

    def test_screen_display(self):
        self.assertIsNone(
            self.screen.display_at(
                "This is centered",
                int(self.screen.height / 2),
                int(self.screen.width / 2),
            )
        )

    def test_screen_display_sprite(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        self.assertIsNone(
            self.screen.display_sprite(sprites_panda["panda"], filler=Sprixel(" "))
        )

    def test_screen_display_sprite_at(self):
        sprites_panda = SpriteCollection.load_json_file("tests/panda.spr")
        self.assertIsNone(
            self.screen.display_sprite_at(
                sprites_panda["panda"],
                Sprixel(" "),
                int(self.screen.height / 2),
                int(self.screen.width / 2),
            )
        )

if __name__ == "__main__":
    unittest.main()
