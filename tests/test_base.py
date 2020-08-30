import pygamelib.base as pgl_base
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
            pgl_base.Fore.WHITE,
            pgl_base.Back.YELLOW,
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
        self.assertEqual(
            self.text.__repr__(), "\x1b[43m\x1b[37m\x1b[1mTest case\x1b[0m"
        )
        self.assertIn("TEST", self.text.black("TEST"))
        self.assertIn("30m", self.text.black("TEST"))
        self.assertIn("TEST", self.text.red("TEST"))
        self.assertIn("31m", self.text.red("TEST"))
        self.assertIn("TEST", self.text.green("TEST"))
        self.assertIn("32m", self.text.green("TEST"))
        self.assertIn("TEST", self.text.yellow("TEST"))
        self.assertIn("33m", self.text.yellow("TEST"))
        self.assertIn("TEST", self.text.blue("TEST"))
        self.assertIn("34m", self.text.blue_bright("TEST"))
        self.assertIn("TEST", self.text.red_bright("TEST"))
        self.assertIn("TEST", self.text.green_bright("TEST"))
        self.assertIn("TEST", self.text.yellow_bright("TEST"))
        self.assertIn("TEST", self.text.magenta_bright("TEST"))
        self.assertIn("TEST", self.text.cyan_bright("TEST"))
        self.assertIn("TEST", self.text.white_bright("TEST"))
        self.assertIn("TEST", self.text.black_bright("TEST"))
        self.assertIn("TEST", self.text.magenta("TEST"))
        self.assertIn("TEST", self.text.cyan("TEST"))
        self.assertIn("TEST", self.text.white("TEST"))
        self.assertIn("TEST", self.text.red_dim("TEST"))
        self.assertIn("TEST", self.text.blue_dim("TEST"))
        self.assertIn("TEST", self.text.green_dim("TEST"))
        self.assertIn("TEST", self.text.yellow_dim("TEST"))
        self.assertIn("TEST", self.text.magenta_dim("TEST"))
        self.assertIn("TEST", self.text.cyan_dim("TEST"))
        self.assertIn("TEST", self.text.white_dim("TEST"))
        self.assertIn("TEST", self.text.black_dim("TEST"))
        self.assertIsNone(self.text.warn("test"))
        self.assertIsNone(self.text.fatal("test"))
        self.assertIsNone(self.text.info("test"))
        self.assertIsNone(self.text.debug("test"))
        self.assertIsNone(self.text.print_white_on_red("test"))

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
