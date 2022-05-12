import pygamelib.base as pgl_base
import pygamelib.gfx.core as core
import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.vectors = []
        self.vectors.append(pgl_base.Vector2D())
        self.vectors.append(pgl_base.Vector2D(1.0, 1.0))
        self.vectors.append(pgl_base.Vector2D(2, 2))
        self.text = pgl_base.Text(
            "Test case",
            core.Color(0, 0, 0),
            core.Color(255, 255, 0),
            pgl_base.Style.BRIGHT,
        )
        self.math = pgl_base.Math()

    def test_v2d_assert_values(self):
        self.assertEqual(self.vectors[0].row, 0)
        self.assertEqual(self.vectors[0].column, 0)
        self.assertEqual(self.vectors[1].row, 1.0)
        self.assertEqual(self.vectors[1].column, 1.0)
        self.assertEqual(self.vectors[2].row, 2)
        self.assertEqual(self.vectors[2].column, 2)
        self.assertEqual(self.vectors[1].__repr__(), "Vector2D (1.0, 1.0)")
        self.assertTrue(self.vectors[0] == pgl_base.Vector2D())
        self.assertFalse(self.vectors[0] == pgl_base.Vector2D(1, 2))
        self.assertEqual(self.vectors[0].__eq__("nope"), NotImplemented)

    def test_v2d_add(self):
        v = self.vectors[0] + self.vectors[1]
        self.assertEqual(v.row, 1.0)
        self.assertEqual(v.column, 1.0)
        v = self.vectors[0] + self.vectors[2]
        self.assertEqual(v.row, 2)
        self.assertEqual(v.column, 2)
        v = self.vectors[2] + self.vectors[1]
        self.assertEqual(v.row, 3.0)
        self.assertEqual(v.column, 3.0)
        self.assertEqual(v.__str__(), v.__repr__())

    def test_v2d_sub(self):
        v = self.vectors[0] - self.vectors[1]
        self.assertEqual(v.row, -1.0)
        self.assertEqual(v.column, -1.0)
        v = self.vectors[0] - self.vectors[2]
        self.assertEqual(v.row, -2)
        self.assertEqual(v.column, -2)
        v = self.vectors[2] - self.vectors[1]
        self.assertEqual(v.row, 1.0)
        self.assertEqual(v.column, 1.0)

    def test_v2d_mult(self):
        v = self.vectors[0] * self.vectors[1]
        self.assertEqual(v, 0.0)
        v = self.vectors[1] * self.vectors[2]
        self.assertEqual(v, 0.0)
        v = (self.vectors[2] + self.vectors[1]) * self.vectors[2]
        self.assertEqual(v, 0.0)
        self.assertEqual(self.vectors[2] * pgl_base.Vector2D(2, 5.0), 6.0)
        v = self.vectors[1] * 2
        self.assertEqual(v.row, 2.0)
        self.assertEqual(v.column, 2.0)

    def test_v2d_unit(self):
        self.assertEqual(self.vectors[0].unit(), pgl_base.Vector2D())
        v = self.vectors[2] + self.vectors[1]
        self.assertEqual(v.unit(), pgl_base.Vector2D(0.71, 0.71))

    def test_v2d_length(self):
        self.assertEqual(self.vectors[0].length(), 0.0)
        self.assertEqual(self.vectors[1].length(), 1.41)
        v = self.vectors[2] + self.vectors[1]
        v.rounding_precision = None
        self.assertEqual(v.length(), 4)

    def test_v2d_props(self):
        v = self.vectors[1]
        self.assertEqual(v.row, v.y)
        self.assertEqual(v.column, v.x)
        v.x = 9.0
        v.y = 9.0
        self.assertEqual(v.row, v.y)
        self.assertEqual(v.column, v.x)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            v.row = "2"
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            v.column = "2"
        v.row = 1.0
        v.column = 1.0

    def test_v2d_create(self):
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.NO_DIR, 1)
        self.assertEqual(v, pgl_base.Vector2D(0, 0))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.UP, 1)
        self.assertEqual(v, pgl_base.Vector2D(-1, 0))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.DOWN, 1)
        self.assertEqual(v, pgl_base.Vector2D(1, 0))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.LEFT, 1)
        self.assertEqual(v, pgl_base.Vector2D(0, -1))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.RIGHT, 1)
        self.assertEqual(v, pgl_base.Vector2D(0, 1))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.DRUP, 1)
        self.assertEqual(v, pgl_base.Vector2D(-1, 1))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.DRDOWN, 1)
        self.assertEqual(v, pgl_base.Vector2D(1, 1))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.DLUP, 1)
        self.assertEqual(v, pgl_base.Vector2D(-1, -1))
        v = pgl_base.Vector2D.from_direction(pgl_base.constants.DLDOWN, 1)
        self.assertEqual(v, pgl_base.Vector2D(1, -1))

    def test_text(self):
        text = pgl_base.Text(
            "Test case",
            core.Color(0, 0, 0),
            core.Color(255, 255, 0),
            pgl_base.Style.BRIGHT,
        )
        self.assertEqual(text.length, 9)
        t = pgl_base.Console.instance()
        self.assertEqual(
            text.__repr__(),
            "".join(
                [
                    t.on_color_rgb(255, 255, 0),
                    t.color_rgb(0, 0, 0),
                    pgl_base.Style.BRIGHT,
                    "Test case",
                    "\x1b[0m",
                ]
            ),
        )
        self.assertEqual(text.__str__(), text.__repr__())
        self.assertIn("TEST", text.black("TEST"))
        self.assertIn("30m", text.black("TEST"))
        self.assertIn("TEST", text.red("TEST"))
        self.assertIn("31m", text.red("TEST"))
        self.assertIn("TEST", text.green("TEST"))
        self.assertIn("32m", text.green("TEST"))
        self.assertIn("TEST", text.yellow("TEST"))
        self.assertIn("33m", text.yellow("TEST"))
        self.assertIn("TEST", text.blue("TEST"))
        self.assertIn("34m", text.blue_bright("TEST"))
        self.assertIn("TEST", text.red_bright("TEST"))
        self.assertIn("TEST", text.green_bright("TEST"))
        self.assertIn("TEST", text.yellow_bright("TEST"))
        self.assertIn("TEST", text.magenta_bright("TEST"))
        self.assertIn("TEST", text.cyan_bright("TEST"))
        self.assertIn("TEST", text.white_bright("TEST"))
        self.assertIn("TEST", text.black_bright("TEST"))
        self.assertIn("TEST", text.magenta("TEST"))
        self.assertIn("TEST", text.cyan("TEST"))
        self.assertIn("TEST", text.white("TEST"))
        self.assertIn("TEST", text.red_dim("TEST"))
        self.assertIn("TEST", text.blue_dim("TEST"))
        self.assertIn("TEST", text.green_dim("TEST"))
        self.assertIn("TEST", text.yellow_dim("TEST"))
        self.assertIn("TEST", text.magenta_dim("TEST"))
        self.assertIn("TEST", text.cyan_dim("TEST"))
        self.assertIn("TEST", text.white_dim("TEST"))
        self.assertIn("TEST", text.black_dim("TEST"))
        self.assertIsNone(text.warn("test"))
        self.assertIsNone(text.fatal("test"))
        self.assertIsNone(text.info("test"))
        self.assertIsNone(text.debug("test"))
        self.assertIsNone(text.print_white_on_red("test"))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pgl_base.Text("breaking", "pink")
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pgl_base.Text("breaking", None, "pink")
        text.text = pgl_base.Text("Another test")
        self.assertEqual(text.text, "Another test")
        text.text = 12
        self.assertEqual(text.text, "Another test")
        text.bg_color = core.Color(12, 34, 56)
        self.assertEqual(text.bg_color, core.Color(12, 34, 56))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            text.bg_color = "pink"
        text.fg_color = core.Color(56, 78, 90)
        self.assertEqual(text.fg_color, core.Color(56, 78, 90))
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            text.fg_color = "definitely not pink! (because tests are not copy/pasted)"
        text.bg_color = None
        self.assertIsNone(text.bg_color)
        text.fg_color = None
        self.assertIsNone(text.fg_color)

        text = pgl_base.Text("This is a test", font=core.Font("8bits"))
        self.assertIsNone(text.handle_notification(None))
        self.assertIsInstance(text, pgl_base.Text)
        with self.assertRaises(pgl_base.PglInvalidTypeException):
            pgl_base.Text("This is a test", font=42)
        self.assertEqual(text.length, 126)
        text = pgl_base.Text(
            "Serialization test",
            core.Color(255, 0, 0),
            core.Color(0, 200, 200),
            "",
            font=core.Font("8bits"),
        )
        text2 = pgl_base.Text.load(text.serialize())
        self.assertEqual(text.text, text2.text)
        self.assertEqual(text.bg_color, text2.bg_color)
        self.assertEqual(text.fg_color, text2.fg_color)
        self.assertEqual(text.style, text2.style)
        text = pgl_base.Text("Serialization test", style=None)
        text2 = pgl_base.Text.load(text.serialize())
        self.assertEqual(text.text, text2.text)
        self.assertEqual(text.bg_color, text2.bg_color)
        self.assertEqual(text.fg_color, text2.fg_color)
        self.assertEqual(text.style, None)

    def test_pgl_base_object(self):
        o1 = pgl_base.PglBaseObject()
        o2 = pgl_base.PglBaseObject()
        o3 = pgl_base.PglBaseObject()
        self.assertTrue(o2.attach(o1))
        self.assertTrue(o2.attach(o3))
        self.assertFalse(o2.attach(o2))
        self.assertIsNone(o2.notify())
        self.assertIsNone(o2.notify(o3))
        self.assertTrue(o2.detach(o1))
        self.assertFalse(o2.detach(o2))
        self.assertFalse(o1.store_screen_position(1, "2"))

    def test_math_distance(self):
        self.assertEqual(self.math.distance(0, 0, 0, 0), 0)
        self.assertEqual(self.math.distance(0, 0, 0, 1), 1)
        self.assertAlmostEqual(self.math.distance(1, 0, 0, 1), 1.414213562)
        self.assertEqual(self.math.distance(0, 1, 0, 0), 1)
        self.assertAlmostEqual(self.math.distance(1, 4, 3, 9), 5.385164807)

    def test_math_intersect(self):
        self.assertTrue(self.math.intersect(0, 0, 1, 1, 0, 0, 2, 2))
        self.assertTrue(self.math.intersect(0, 0, 2, 2, 1, 1, 2, 2))
        self.assertFalse(self.math.intersect(0, 0, 2, 2, 3, 1, 2, 2))

    def test_math_lerp(self):
        self.assertEqual(self.math.lerp(0, 1, 0), 0)
        self.assertEqual(self.math.lerp(0, 1, 1), 1)
        self.assertEqual(self.math.lerp(0, 1, 0.5), 0.5)

    def test_exceptions(self):
        e = pgl_base.PglException("error", "message")
        self.assertEqual(e.error, "error")
        self.assertEqual(e.message, "message")
        e = pgl_base.PglInvalidLevelException("message")
        self.assertEqual(e.message, "message")
        e = pgl_base.PglInvalidTypeException("message")
        self.assertEqual(e.message, "message")
        e = pgl_base.PglObjectIsNotMovableException("message")
        self.assertEqual(e.message, "message")
        e = pgl_base.PglInventoryException("error", "message")
        self.assertEqual(e.error, "error")
        self.assertEqual(e.message, "message")


if __name__ == "__main__":
    unittest.main()
