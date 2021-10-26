import pygamelib.gfx.core as gfx_core
import unittest

# Test cases for all classes in pygamelib.gfx.core except for Animation.


class TestBase(unittest.TestCase):
    def test_sprite_create_empty(self):
        spr = gfx_core.Sprite()
        self.assertEqual(spr.size[0], 2)
        self.assertEqual(spr.size[1], 2)
        self.assertEqual(spr.width, 2)
        self.assertEqual(spr.height, 2)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel())
        self.assertEqual(spr.__repr__(), "\x1b[0m\x1b[0m\n\x1b[0m\x1b[0m")
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            spr.sprixel("crash", 1)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            spr.sprixel(1, "crash")
        with self.assertRaises(gfx_core.base.PglException) as e:
            spr.sprixel(1, 10)
            self.assertEqual(e.error, "out_of_sprite_boundaries")
        self.assertTrue(type(spr.sprixel(1)) is list)
        with self.assertRaises(gfx_core.base.PglException) as e:
            spr.sprixel(10, 1)
            self.assertEqual(e.error, "out_of_sprite_boundaries")
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            spr.set_sprixel(1, "crash", "bork")
        with self.assertRaises(gfx_core.base.PglException) as e:
            spr.set_sprixel(1, 10, "bork")
            self.assertEqual(e.error, "out_of_sprite_boundaries")
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            spr.set_sprixel(1, 1, "bork")

    def test_sprite_create1(self):
        spr = gfx_core.Sprite(size=[4, 4])
        self.assertEqual(spr.size[0], 4)
        self.assertEqual(spr.size[1], 4)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel())

    def test_sprite_create2(self):
        spr = gfx_core.Sprite(default_sprixel=gfx_core.Sprixel.cyan_rect())
        self.assertEqual(spr.size[0], 2)
        self.assertEqual(spr.size[1], 2)
        self.assertEqual(spr.sprixel(1, 1), gfx_core.Sprixel.cyan_rect())

    def test_sprite_create3(self):
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

    def test_sprite_flip_horiz(self):
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

    def test_sprite_flip_vert(self):
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
        spr = gfx_core.Sprite(
            sprixels=[
                [gfx_core.Sprixel("▄"), gfx_core.Sprixel("▄")],
                [gfx_core.Sprixel("▀"), gfx_core.Sprixel("▀")],
            ]
        )
        spr_flipped = spr.flip_vertically()
        self.assertEqual(spr.sprixel(0, 0).model, "▀")
        self.assertIsNone(spr.set_transparency(True))

    def test_sprite_empty(self):
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

    def test_load(self):
        with self.assertRaises(gfx_core.base.PglException) as e:
            gfx_core.Sprite.load_from_ansi_file("tests/house-red-borked.ans")
            self.assertEqual(e.error, "sprite_file_format_not_supported")
        spr = gfx_core.Sprite.load_from_ansi_file("tests/house-red-double.ans")
        self.assertEqual(spr.width, 17)
        gfx_core.Sprite.load_from_ansi_file("tests/house-red.ans")
        with self.assertRaises(gfx_core.base.PglException) as e:
            gfx_core.Sprite.load(
                {
                    "size": [2, 3],
                    "name": "villager",
                    "default_sprixel": {
                        "bg_color": "",
                        "fg_color": "",
                        "model": "",
                        "is_bg_transparent": True,
                    },
                    "sprixels": [
                        [
                            {
                                "bg_color": "\x1b[48;2;139;22;19m",
                                "fg_color": "\x1b[38;2;160;26;23m",
                                "model": "▄",
                                "is_bg_transparent": True,
                            },
                            {
                                "bg_color": "\x1b[48;2;139;22;19m",
                                "fg_color": "\x1b[38;2;160;26;23m",
                                "model": "▄",
                                "is_bg_transparent": True,
                            },
                        ],
                        [
                            {
                                "bg_color": "\x1b[48;2;139;22;19m",
                                "fg_color": "\x1b[38;2;160;26;23m",
                                "model": "▄",
                                "is_bg_transparent": False,
                            },
                            {
                                "bg_color": "\x1b[48;2;139;22;19m",
                                "fg_color": "\x1b[38;2;160;26;23m",
                                "model": "▄",
                                "is_bg_transparent": False,
                            },
                        ],
                    ],
                }
            )
            self.assertEqual(e.error, "invalid_sprite_size")

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
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sc.add(1)
        self.assertEqual(spr.name, sc[spr.name].name)
        self.assertEqual(spr.name, sc.get(spr.name).name)
        self.assertEqual(spr2.name, sc[spr2.name].name)
        self.assertEqual(spr2.name, sc.get(spr2.name).name)
        self.assertEqual(spr3.name, sc[spr3.name].name)
        self.assertEqual(spr3.name, sc.get(spr3.name).name)
        self.assertIsNone(sc.rename(spr.name, "test_rename"))
        self.assertEqual(sc["test_rename"].sprixel(0, 0), spr.sprixel(0, 0))
        self.assertIsNone(sc.to_json_file("test.pgs"))
        sc2 = gfx_core.SpriteCollection.load_json_file("test.pgs")
        self.assertIsInstance(sc2, gfx_core.SpriteCollection)
        self.assertEqual(spr3.sprixel(1, 1), sc2.get(spr3.name).sprixel(1, 1))
        with self.assertRaises(gfx_core.base.PglException) as e:
            gfx_core.SpriteCollection.load({})
            self.assertEqual(e.error, "invalid_sprite_data")
        with self.assertRaises(gfx_core.base.PglException) as e:
            gfx_core.SpriteCollection.load({"sprites_count": 2, "sprites": {}})
            self.assertEqual(e.error, "corrupted_sprite_data")

    def test_scale(self):
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
        self.assertEqual(spr.width, 3)
        self.assertEqual(spr.height, 2)
        spr2 = spr.scale(2)
        self.assertEqual(spr2.width, 6)
        self.assertEqual(spr2.height, 4)
        spr3 = spr2.scale(0.5)
        self.assertEqual(spr3.width, 3)
        self.assertEqual(spr3.height, 2)
        self.assertEqual(spr3.width, spr.width)
        self.assertEqual(spr3.height, spr.height)
        self.assertEqual(spr, spr.scale(1))
        self.assertIsNone(spr.scale(0))

    def test_color(self):
        c = gfx_core.Color(1, 2, 3)
        self.assertEqual(c.r, 1)
        self.assertEqual(c.g, 2)
        self.assertEqual(c.b, 3)

    def test_tinting(self):
        sp = gfx_core.Sprite(
            sprixels=[
                [
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                ],
                [
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                    gfx_core.Sprixel(
                        " ",
                        gfx_core.Color(255, 255, 255),
                        gfx_core.Color(255, 255, 255),
                    ),
                ],
            ]
        )
        spr = sp.tint(gfx_core.Color(0, 255, 0), 0.2)
        self.assertEqual(spr.sprixel(0, 0).bg_color.r, 204)
        self.assertEqual(spr.sprixel(0, 0).bg_color.g, 255)
        self.assertEqual(spr.sprixel(0, 0).bg_color.b, 204)
        # Original sprite should not be modified by tint
        self.assertEqual(sp.sprixel(0, 0).bg_color.r, 255)
        self.assertEqual(sp.sprixel(0, 0).bg_color.g, 255)
        self.assertEqual(sp.sprixel(0, 0).bg_color.b, 255)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sp.tint(gfx_core.Color(0, 255, 0), 1.2)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sp.tint(gfx_core.Color(0, 255, 0), -1.2)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sp.modulate(gfx_core.Color(0, 255, 0), 1.2)
        with self.assertRaises(gfx_core.base.PglInvalidTypeException):
            sp.modulate(gfx_core.Color(0, 255, 0), -1.2)

        sp.modulate(gfx_core.Color(0, 255, 0), 0.2)
        # Original sprite should be modified by modulate
        self.assertEqual(sp.sprixel(0, 0).bg_color.r, 204)
        self.assertEqual(sp.sprixel(0, 0).bg_color.g, 255)
        self.assertEqual(sp.sprixel(0, 0).bg_color.b, 204)


if __name__ == "__main__":
    unittest.main()
