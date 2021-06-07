from pygamelib.gfx import core
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_font_create(self):
        font = core.Font("8bits")
        self.assertEqual(font.name(), "8bits")
        with self.assertRaises(FileNotFoundError):
            core.Font("42")

    def test_accessors(self):
        font = core.Font("8bits")
        self.assertEqual(font.name(), "8bits")
        self.assertEqual(font.height(), 4)
        self.assertEqual(font.horizontal_spacing(), 1)
        self.assertEqual(font.vertical_spacing(), 1)

    def test_glyph(self):
        font = core.Font("8bits")
        g = font.glyph("42")
        self.assertEqual(g, font.glyph("default"))
        g = font.glyph("a", core.Color(255, 0, 0))
        self.assertIsInstance(g, core.Sprite)
        font = core.Font()
        self.assertIsNone(font.glyph("a"))


if __name__ == "__main__":
    unittest.main()
