import pygamelib.gfx.core as gfx_core
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_color_create(self):
        color = gfx_core.Color()
        self.assertEqual(color.r, 0)
        self.assertEqual(color.g, 0)
        self.assertEqual(color.b, 0)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Color(False, 0, 0)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Color(0, False, 0)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Color(0, 0, False)
        self.assertEqual(color.__repr__(), "Color(0, 0, 0)")
        random_color = gfx_core.Color.random()
        self.assertIsInstance(random_color, gfx_core.Color)

    def test_color_cmp(self):
        c1 = gfx_core.Color()
        c2 = gfx_core.Color()
        c3 = gfx_core.Color(1, 2, 3)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertFalse(c1 == c3)
        self.assertFalse(c1 != c2)

    def test_color_from_ansi(self):
        c1 = gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m")
        self.assertIsInstance(c1, gfx_core.Color)
        self.assertEqual(c1.r, 160)
        self.assertEqual(c1.g, 26)
        self.assertEqual(c1.b, 23)
        c2 = gfx_core.Color.from_ansi("\x1b[38;2;160;26;23m")
        self.assertIsInstance(c2, gfx_core.Color)
        self.assertEqual(c2.r, 160)
        self.assertEqual(c2.g, 26)
        self.assertEqual(c2.b, 23)
        self.assertEqual(c1, c2)
        self.assertIsNone(gfx_core.Color.from_ansi("should fail"))

    def test_color_update(self):
        color = gfx_core.Color()
        color.r = 1
        self.assertEqual(color.r, 1)
        color.g = 1
        self.assertEqual(color.g, 1)
        color.b = 1
        self.assertEqual(color.b, 1)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            color.r = "1"
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            color.g = "1"
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            color.b = "1"

    def test_color_blend(self):
        c1 = gfx_core.Color(10, 10, 10)
        c2 = gfx_core.Color(20, 20, 20)
        c3 = c1.blend(c2)
        self.assertEqual(c3.r, 15)
        self.assertEqual(c3.g, 15)
        self.assertEqual(c3.b, 15)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            c1.blend(c2, 2)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            c1.blend(c2, "2.0")
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            c1.blend("this is not going to work...")

    def test_color_load(self):
        c = gfx_core.Color.load({"red": 25, "green": 35})
        self.assertEqual(c.r, 25)
        self.assertEqual(c.g, 35)
        self.assertEqual(c.b, 0)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Color.load({"red": 25, "green": "nope"})

    def test_color_randomize(self):
        # Let's keep this simple: most often than not,
        # the randomized value should be different from the default one
        # and the previous one
        default_color = gfx_core.Color()
        c = gfx_core.Color()
        criteria_match_count = 0
        total_rolls = 100
        for i in range(total_rolls):
            previous_color = gfx_core.Color(c.r, c.g, c.b)
            c.randomize()
            if c != default_color and c != previous_color:
                criteria_match_count += 1
        self.assertGreater(criteria_match_count, total_rolls // 2)


if __name__ == "__main__":
    unittest.main()
