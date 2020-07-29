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
        v = self.vectors[0] * self.vectors[2]
        self.assertEqual(v, 0.0)
        v = (self.vectors[2] + self.vectors[1]) * self.vectors[2]
        self.assertEqual(v, -3.0)

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

    def test_text_repr(self):
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
        self.assertIn("34m", self.text.blue("TEST"))

    def test_text_to_sprite(self):
        self.assertTrue("Sprite" in str(type(self.text.to_sprite())))

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


if __name__ == "__main__":
    unittest.main()
