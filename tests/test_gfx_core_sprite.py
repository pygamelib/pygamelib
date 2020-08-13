import pygamelib.gfx.core as gfx_core
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_screen_create_empty(self):
        spr = gfx_core.Sprite()
        self.assertEqual(spr.size[0], 2)
        self.assertEqual(spr.size[1], 2)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel())

    def test_screen_create1(self):
        spr = gfx_core.Sprite(size=[4, 4])
        self.assertEqual(spr.size[0], 4)
        self.assertEqual(spr.size[1], 4)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel())

    def test_screen_create2(self):
        spr = gfx_core.Sprite(default_sprixel=gfx_core.Sprixel.cyan_rect())
        self.assertEqual(spr.size[0], 2)
        self.assertEqual(spr.size[1], 2)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel.cyan_rect())

    def test_screen_create3(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        self.assertEqual(spr.size[0], 3)
        self.assertEqual(spr.size[1], 2)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel.blue_rect())

    def test_screen_flip_horiz(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        spr_flipped = spr.flip_horizontally()
        self.assertEqual(spr.sprixel(1, 0), gfx_core.Sprixel.yellow_rect())
        self.assertEqual(spr_flipped.sprixel(1, 0), gfx_core.Sprixel.white_rect())

    def test_screen_flip_vert(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        spr_flipped = spr.flip_vertically()
        self.assertEqual(spr.sprixel(1, 0), gfx_core.Sprixel.yellow_rect())
        self.assertEqual(spr_flipped.sprixel(1, 0), gfx_core.Sprixel.cyan_rect())

    def test_screen_empty(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        self.assertEqual(spr.sprixel(1, 0), gfx_core.Sprixel.yellow_rect())
        spr.empty()
        self.assertEqual(spr.sprixel(1, 0), spr.default_sprixel)

    def test_collection(self):
        spr = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel.cyan_rect(),
                    gfx_core.Sprixel.red_rect(),
                    gfx_core.Sprixel.green_rect(),
                ],
                [
                    gfx_core.Sprixel.yellow_rect(),
                    gfx_core.Sprixel.blue_rect(),
                    gfx_core.Sprixel.white_rect(),
                ],
            ]
        )
        spr2 = spr.flip_horizontally()
        spr3 = spr.flip_vertically()
        sc = gfx_core.SpriteCollection()
        sc.add(spr)
        sc.add(spr2)
        sc.add(spr3)
        self.assertEqual(spr.name, sc[spr.name].name)
        self.assertEqual(spr.name, sc.get(spr.name).name)
        self.assertEqual(spr2.name, sc[spr2.name].name)
        self.assertEqual(spr2.name, sc.get(spr2.name).name)
        self.assertEqual(spr3.name, sc[spr3.name].name)
        self.assertEqual(spr3.name, sc.get(spr3.name).name)
        self.assertIsNone(sc.to_json_file("test.pgs"))
        sc2 = gfx_core.SpriteCollection.load_json_file("test.pgs")
        self.assertIsInstance(sc2, gfx_core.SpriteCollection)
        self.assertEqual(spr3.sprixel(1, 1), sc2.get(spr3.name).sprixel(1, 1))


if __name__ == "__main__":
    unittest.main()
