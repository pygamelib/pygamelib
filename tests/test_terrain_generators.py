"""
Unit tests for the terrain generators in pygamelib.assets.terrain_generators.
"""

import unittest

from pygamelib import base, board_items
from pygamelib.assets import graphics, terrain_generators
from pygamelib.gfx import core


class TestTerrainFeature(unittest.TestCase):
    def test_defaults(self):
        feature = terrain_generators.TerrainFeature(name="plain")
        self.assertEqual(feature.name, "plain")
        self.assertEqual(feature.model, " ")
        self.assertIsNone(feature.fg_color)
        self.assertIsNone(feature.bg_color)
        self.assertIsNone(feature.sprite)

    def test_equality_and_hash(self):
        a = terrain_generators.TerrainFeature(name="plain", model='"')
        b = terrain_generators.TerrainFeature(name="plain", model=".")
        c = terrain_generators.TerrainFeature(name="forest", model='"')
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(hash(a), hash(b))
        # Comparing to something else than a feature is not supported
        self.assertNotEqual(a, "plain")

    def test_repr(self):
        feature = terrain_generators.TerrainFeature(name="plain", model='"')
        self.assertEqual(repr(feature), "TerrainFeature('plain', model='\"')")

    def test_make_item_with_model(self):
        color = core.Color(10, 20, 30)
        feature = terrain_generators.TerrainFeature(
            name="plain", model="#", fg_color=color
        )
        item = feature.make_item()
        self.assertIsInstance(item, board_items.Tile)
        self.assertEqual(item.sprite.default_sprixel.model, "#")
        self.assertEqual(item.sprite.default_sprixel.fg_color, color)

    def test_make_item_with_sprite(self):
        sprite = core.Sprite(
            size=[2, 1],
            default_sprixel=core.Sprixel(model="T"),
        )
        feature = terrain_generators.TerrainFeature(name="forest", sprite=sprite)
        item = feature.make_item()
        self.assertIsInstance(item, board_items.Tile)
        self.assertIs(item.sprite, sprite)

    def test_serialization(self):
        feature = terrain_generators.TerrainFeature(
            name="plain",
            model="#",
            fg_color=core.Color(1, 2, 3),
            bg_color=core.Color(4, 5, 6),
        )
        loaded = terrain_generators.TerrainFeature.load(feature.serialize())
        self.assertEqual(loaded, feature)
        self.assertEqual(loaded.model, "#")
        self.assertEqual(loaded.fg_color, core.Color(1, 2, 3))
        self.assertEqual(loaded.bg_color, core.Color(4, 5, 6))
        self.assertIsNone(loaded.sprite)

    def test_serialization_with_sprite(self):
        feature = terrain_generators.TerrainFeature(
            name="forest",
            sprite=core.Sprite(size=[2, 1], default_sprixel=core.Sprixel(model="T")),
        )
        loaded = terrain_generators.TerrainFeature.load(feature.serialize())
        self.assertEqual(loaded.serialize(), feature.serialize())


class TestTerrainPalette(unittest.TestCase):
    def test_default_features(self):
        palette = terrain_generators.TerrainPalette()
        for name in (
            "deep_water",
            "water",
            "shore",
            "plain",
            "forest",
            "hill",
            "mountain",
            "snow",
        ):
            self.assertEqual(palette.feature(name).name, name)

    def test_default_models(self):
        palette = terrain_generators.TerrainPalette()
        self.assertEqual(palette.feature("water").model, "~")
        self.assertEqual(
            palette.feature("forest").model, graphics.MiscTechnicals.EARTH_GROUND
        )

    def test_set_feature(self):
        palette = terrain_generators.TerrainPalette()
        palette.set_feature(
            "plain",
            terrain_generators.TerrainFeature(name="ignored", model="^"),
        )
        self.assertEqual(palette.feature("plain").model, "^")
        # The name is forced to the key
        self.assertEqual(palette.feature("plain").name, "plain")

    def test_set_feature_with_custom_name(self):
        palette = terrain_generators.TerrainPalette()
        palette.set_feature(
            "swamp", terrain_generators.TerrainFeature(name="swamp", model="%")
        )
        self.assertEqual(palette.feature("swamp").model, "%")

    def test_set_feature_invalid_type(self):
        palette = terrain_generators.TerrainPalette()
        with self.assertRaises(base.PglInvalidTypeException):
            palette.set_feature("plain", "not a feature")

    def test_unknown_feature(self):
        palette = terrain_generators.TerrainPalette()
        with self.assertRaises(base.PglException):
            palette.feature("swamp")

    def test_constructor_features(self):
        palette = terrain_generators.TerrainPalette(
            features={
                "plain": terrain_generators.TerrainFeature(name="plain", model="#"),
            }
        )
        self.assertEqual(palette.feature("plain").model, "#")

    def test_serialization(self):
        palette = terrain_generators.TerrainPalette()
        palette.set_feature(
            "plain",
            terrain_generators.TerrainFeature(
                name="plain", model="#", fg_color=core.Color(9, 9, 9)
            ),
        )
        loaded = terrain_generators.TerrainPalette.load(palette.serialize())
        self.assertEqual(loaded.feature("plain").model, "#")
        self.assertEqual(loaded.feature("plain").fg_color, core.Color(9, 9, 9))
        self.assertEqual(loaded.serialize(), palette.serialize())


class TestTerrainGenerator(unittest.TestCase):
    def test_defaults(self):
        generator = terrain_generators.TerrainGenerator()
        self.assertEqual(generator.width, 40)
        self.assertEqual(generator.height, 20)
        self.assertIsInstance(generator.palette, terrain_generators.TerrainPalette)
        self.assertEqual(generator.scale, 12.0)
        self.assertEqual(generator.octaves, 3)
        self.assertFalse(generator.island)

    def test_generate_dimensions_and_name(self):
        generator = terrain_generators.TerrainGenerator(width=12, height=7, seed=1)
        board = generator.generate()
        self.assertEqual(board.size, [12, 7])
        self.assertEqual(board.name, "Terrain")

    def test_custom_name(self):
        board = terrain_generators.TerrainGenerator(width=4, height=4, seed=1).generate(
            name="World"
        )
        self.assertEqual(board.name, "World")

    def test_every_cell_is_a_tile(self):
        generator = terrain_generators.TerrainGenerator(width=8, height=6, seed=2)
        board = generator.generate()
        for row in range(6):
            for column in range(8):
                self.assertEqual(len(board._matrix[row][column]), 1)

    def test_reproducible_with_seed(self):
        first = terrain_generators.TerrainGenerator(width=20, height=10, seed=42)
        second = terrain_generators.TerrainGenerator(width=20, height=10, seed=42)
        for row in range(10):
            for column in range(20):
                self.assertEqual(
                    first.feature_at(row, column).name,
                    second.feature_at(row, column).name,
                )

    def test_altitude_in_range(self):
        generator = terrain_generators.TerrainGenerator(width=30, height=15, seed=3)
        for row in range(15):
            for column in range(30):
                value = generator.altitude(row, column)
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

    def test_feature_at_is_consistent_with_altitude(self):
        generator = terrain_generators.TerrainGenerator(width=20, height=10, seed=4)
        for row in range(10):
            for column in range(20):
                name = generator.feature_at(row, column).name
                value = generator.altitude(row, column)
                if value < generator.water_level * 0.5:
                    self.assertEqual(name, "deep_water")
                elif value < generator.water_level:
                    self.assertEqual(name, "water")
                else:
                    self.assertNotIn(name, ("deep_water", "water"))

    def test_island_edges_are_water(self):
        generator = terrain_generators.TerrainGenerator(
            width=30, height=30, seed=5, island=True
        )
        for column in range(30):
            self.assertEqual(generator.feature_at(0, column).name, "deep_water")
            self.assertEqual(generator.feature_at(29, column).name, "deep_water")
        for row in range(30):
            self.assertEqual(generator.feature_at(row, 0).name, "deep_water")
            self.assertEqual(generator.feature_at(row, 29).name, "deep_water")

    def test_island_has_land_in_the_middle(self):
        generator = terrain_generators.TerrainGenerator(
            width=40, height=40, seed=5, island=True
        )
        middle = generator.feature_at(20, 20).name
        self.assertNotIn(middle, ("deep_water", "water"))

    def test_non_island_can_reach_water_level(self):
        # A continental map is not forced to be surrounded by water, so it should
        # produce at least one non water cell with a small board.
        generator = terrain_generators.TerrainGenerator(width=10, height=10, seed=6)
        names = {
            generator.feature_at(row, column).name
            for row in range(10)
            for column in range(10)
        }
        self.assertTrue(names - {"deep_water", "water"})

    def test_water_level_changes_result(self):
        low = terrain_generators.TerrainGenerator(
            width=20, height=20, seed=7, water_level=0.2
        )
        high = terrain_generators.TerrainGenerator(
            width=20, height=20, seed=7, water_level=0.6
        )
        low_water = sum(
            1
            for row in range(20)
            for column in range(20)
            if low.feature_at(row, column).name in ("deep_water", "water")
        )
        high_water = sum(
            1
            for row in range(20)
            for column in range(20)
            if high.feature_at(row, column).name in ("deep_water", "water")
        )
        self.assertGreater(high_water, low_water)

    def test_feature_at_high_altitude_is_snow(self):
        generator = terrain_generators.TerrainGenerator(width=4, height=4, seed=1)
        # Force a high altitude to exercise the snow classification, which the noise
        # field rarely reaches on its own.
        generator.altitude = lambda row, column: 0.99
        self.assertEqual(generator.feature_at(0, 0).name, "snow")

    def test_custom_palette_is_used(self):
        palette = terrain_generators.TerrainPalette()
        palette.set_feature(
            "plain", terrain_generators.TerrainFeature(name="plain", model="#")
        )
        generator = terrain_generators.TerrainGenerator(
            width=20, height=20, seed=8, palette=palette, water_level=0.0
        )
        self.assertIs(generator.palette, palette)
        board = generator.generate()
        models = {
            board._matrix[row][column][-1].sprixel.model
            for row in range(20)
            for column in range(20)
        }
        self.assertIn("#", models)

    def test_serialization(self):
        generator = terrain_generators.TerrainGenerator(
            width=25,
            height=12,
            seed=9,
            scale=8.0,
            octaves=2,
            persistence=0.4,
            water_level=0.3,
            island=True,
        )
        loaded = terrain_generators.TerrainGenerator.load(generator.serialize())
        self.assertEqual(loaded.width, 25)
        self.assertEqual(loaded.height, 12)
        self.assertEqual(loaded.seed, 9)
        self.assertEqual(loaded.scale, 8.0)
        self.assertEqual(loaded.octaves, 2)
        self.assertEqual(loaded.persistence, 0.4)
        self.assertEqual(loaded.water_level, 0.3)
        self.assertTrue(loaded.island)
        self.assertEqual(loaded.serialize(), generator.serialize())


class TestTerrainGeneratorValidation(unittest.TestCase):
    def test_invalid_dimensions(self):
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(width=0, height=10)
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(width=10, height=0)

    def test_invalid_scale(self):
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(scale=0)

    def test_invalid_octaves(self):
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(octaves=0)

    def test_invalid_persistence(self):
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(persistence=0)
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(persistence=1.5)

    def test_invalid_water_level(self):
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(water_level=-0.1)
        with self.assertRaises(base.PglInvalidTypeException):
            terrain_generators.TerrainGenerator(water_level=1.0)

    def test_missing_opensimplex(self):
        generator = terrain_generators.TerrainGenerator(width=2, height=2, seed=1)
        saved = terrain_generators.opensimplex
        try:
            terrain_generators.opensimplex = None
            with self.assertRaises(base.PglException):
                generator.altitude(0, 0)
        finally:
            terrain_generators.opensimplex = saved
