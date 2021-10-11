import pygamelib.gfx.particles as particles
import pygamelib.gfx.core as core
from pygamelib import constants
import unittest

# Test cases for all classes in pygamelib.gfx.particles.
# WARNING: This module is under heavy work, it is not ready yet.
# Therefor tests cases are just covering the current state.


class TestBase(unittest.TestCase):
    def test_create(self):
        p = particles.BaseParticle()
        self.assertEqual(p.type, "base_particle")
        self.assertEqual(p.size, [1, 1])
        p = particles.BaseParticle(
            bg_color=core.Color(0, 0, 255),
            fg_color=core.Color(255, 0, 0),
            model="*",
            velocity=particles.base.Vector2D(),
            acceleration=particles.base.Vector2D(),
            directions=[constants.UP],
            lifespan=8,
        )
        self.assertEqual(p.sprixel.bg_color, core.Color(0, 0, 255))
        self.assertEqual(p.sprixel.fg_color, core.Color(255, 0, 0))
        self.assertEqual(p.sprixel.model, "*")
        self.assertEqual(p.directions, [constants.UP])

    def test_accessors(self):
        p = particles.BaseParticle()
        self.assertIn(
            p.direction(),
            [
                particles.base.Vector2D.from_direction(constants.UP, 1),
                particles.base.Vector2D.from_direction(constants.DLUP, 1),
                particles.base.Vector2D.from_direction(constants.DRUP, 1),
            ],
        )
        self.assertFalse(p.pickable())
        self.assertTrue(p.overlappable())


if __name__ == "__main__":
    unittest.main()
