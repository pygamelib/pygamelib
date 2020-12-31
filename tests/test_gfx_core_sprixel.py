import pygamelib.gfx.core as gfx_core
import pygamelib.base as pgl_base
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_sprixel_create(self):
        sprix = gfx_core.Sprixel()
        self.assertEqual(sprix.model, "")
        self.assertIsNone(sprix.bg_color)
        self.assertIsNone(sprix.fg_color)
        sprix = gfx_core.Sprixel("m", gfx_core.Color(0, 0, 0), gfx_core.Color(1, 1, 1))
        self.assertEqual(sprix.model, "m")
        self.assertEqual(sprix.bg_color, gfx_core.Color(0, 0, 0))
        self.assertEqual(sprix.fg_color, gfx_core.Color(1, 1, 1))
        t = pgl_base.Console.instance()
        self.assertEqual(
            sprix.__repr__(),
            "".join([t.on_color_rgb(0, 0, 0), t.color_rgb(1, 1, 1), "m", "\x1b[0m"]),
        )
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Sprixel(False, gfx_core.Color(0, 0, 0), gfx_core.Color(1, 1, 1))
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Sprixel("False", "nope", gfx_core.Color(1, 1, 1))
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            gfx_core.Sprixel("False", gfx_core.Color(0, 0, 0), "nope")
        sprix = gfx_core.Sprixel(is_bg_transparent=True)
        self.assertTrue(sprix.is_bg_transparent)

    def test_sprixel_cmp(self):
        s1 = gfx_core.Sprixel()
        s2 = gfx_core.Sprixel()
        s3 = gfx_core.Sprixel("m")
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertFalse(s1 == s3)
        self.assertFalse(s1 != s2)

    def test_sprixel_from_ansi(self):
        s = gfx_core.Sprixel.from_ansi(
            "\x1b[48;2;160;26;23m\x1b[38;2;120;18;15m▄\x1b[0m"
        )
        self.assertIsInstance(s, gfx_core.Sprixel)
        self.assertEqual(s.model, "▄")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m"))
        self.assertEqual(s.fg_color, gfx_core.Color.from_ansi("\x1b[38;2;120;18;15m"))
        s = gfx_core.Sprixel.from_ansi("\x1b[38;2;120;18;15m▄\x1b[0m")
        self.assertEqual(s.model, "▄")
        self.assertIsNone(s.bg_color)
        self.assertEqual(s.fg_color, gfx_core.Color.from_ansi("\x1b[38;2;120;18;15m"))
        s = gfx_core.Sprixel.from_ansi("\x1b[48;2;160;26;23m▄\x1b[0m")
        self.assertIsInstance(s, gfx_core.Sprixel)
        self.assertEqual(s.model, "▄")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m"))
        self.assertIsNone(s.fg_color)

    def test_sprixel_update(self):
        sprix = gfx_core.Sprixel()
        self.assertEqual(sprix.model, "")
        self.assertEqual(sprix.length, 0)
        self.assertIsNone(sprix.bg_color)
        self.assertIsNone(sprix.fg_color)
        sprix.model = "@"
        self.assertEqual(sprix.model, "@")
        self.assertIsNone(sprix.bg_color)
        self.assertIsNone(sprix.fg_color)
        sprix.bg_color = gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m")
        self.assertEqual(sprix.model, "@")
        self.assertEqual(
            sprix.bg_color, gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m")
        )
        self.assertIsNone(sprix.fg_color)
        sprix.fg_color = gfx_core.Color.from_ansi("\x1b[38;2;120;18;15m")
        self.assertEqual(sprix.model, "@")
        self.assertEqual(
            sprix.bg_color, gfx_core.Color.from_ansi("\x1b[48;2;160;26;23m")
        )
        self.assertEqual(
            sprix.fg_color, gfx_core.Color.from_ansi("\x1b[38;2;120;18;15m")
        )
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sprix.bg_color = 1
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sprix.fg_color = 1

    def test_sprixel_static_black(self):
        s = gfx_core.Sprixel.black_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color(0, 0, 0))
        s = gfx_core.Sprixel.black_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color(0, 0, 0))

    def test_sprixel_static_red(self):
        s = gfx_core.Sprixel.red_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[41m"))
        s = gfx_core.Sprixel.red_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[41m"))

    def test_sprixel_static_green(self):
        s = gfx_core.Sprixel.green_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[42m"))
        s = gfx_core.Sprixel.green_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[42m"))

    def test_sprixel_static_yellow(self):
        s = gfx_core.Sprixel.yellow_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[43m"))
        s = gfx_core.Sprixel.yellow_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[43m"))

    def test_sprixel_static_blue(self):
        s = gfx_core.Sprixel.blue_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[44m"))
        s = gfx_core.Sprixel.blue_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[44m"))

    def test_sprixel_static_magenta(self):
        s = gfx_core.Sprixel.magenta_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[45m"))
        s = gfx_core.Sprixel.magenta_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[45m"))

    def test_sprixel_static_cyan(self):
        s = gfx_core.Sprixel.cyan_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[46m"))
        s = gfx_core.Sprixel.cyan_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[46m"))

    def test_sprixel_static_white(self):
        s = gfx_core.Sprixel.white_rect()
        self.assertEqual(s.model, " ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[47m"))
        s = gfx_core.Sprixel.white_square()
        self.assertEqual(s.model, "  ")
        self.assertEqual(s.bg_color, gfx_core.Color.from_ansi("\x1b[47m"))


if __name__ == "__main__":
    unittest.main()
