from pygamelib.gfx import core, particles
from pygamelib.assets import graphics
from pygamelib import base
import unittest

# Test cases for all classes in pygamelib.gfx.particles.
# WARNING: This module is under heavy work, it is not ready yet.
# Therefor tests cases are just covering the current state.


class TestBase(unittest.TestCase):
    def test_particle(self):
        p = particles.Particle(
            velocity=base.Vector2D(-1.0, 0.0),
            lifespan=10,
        )
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p.update()
        self.assertEqual(p.row, -1.0)
        self.assertEqual(p.column, 0)
        p.reset()
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p.reset(velocity=base.Vector2D(1.0, 0.0), lifespan=5)
        p.update()
        self.assertEqual(p.y, 1.0)
        self.assertEqual(p.x, 0)
        self.assertEqual(p.lifespan, 4)
        p.x = 1
        p.y = 1
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 1)
        p.reset_lifespan(None)
        self.assertEqual(p.lifespan, 20)
        p.apply_force(base.Vector2D(3.0, 0.0))
        self.assertEqual(p.acceleration.row, 3.0)
        self.assertEqual(p.acceleration.column, 0.0)
        sprix = p.render()
        self.assertEqual(sprix, p.sprixel)
        ps = particles.ParticleSprixel(graphics.Blocks.QUADRANT_UPPER_LEFT)
        p.sprixel.model = graphics.Blocks.QUADRANT_UPPER_RIGHT
        sprix = p.render(ps)
        self.assertNotEqual(sprix.model, graphics.Blocks.QUADRANT_UPPER_LEFT)
        s = core.Sprixel("+", core.Color(10, 20, 30))
        sprix = p.render(s)
        self.assertEqual(sprix.model, p.sprixel.model)
        self.assertEqual(sprix.bg_color, core.Color(10, 20, 30))

    def test_partition_particle(self):
        p = particles.PartitionParticle(
            velocity=base.Vector2D(1.0, 0.0),
            lifespan=10,
        )
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p.update()
        p.velocity.row = 0.6
        p.velocity.column = 0.6
        p.update()
        self.assertEqual(p.row, 1.0)
        # render test
        sprix = p.render()
        self.assertEqual(sprix, p.sprixel)
        ps = particles.ParticleSprixel("+")
        sprix = p.render(ps)
        self.assertEqual(sprix.model, "+")
        s = core.Sprixel("+", core.Color(10, 20, 30))
        sprix = p.render(s)
        self.assertEqual(sprix.model, p.sprixel.model)
        self.assertEqual(sprix.bg_color, core.Color(10, 20, 30))

    def test_emitter_properties(self):
        emt_props = particles.EmitterProperties(
            0,  # Position is not important as it will be updated by the
            0,  # ParticleEmitter.render_to_buffer method.
            lifespan=150,
            variance=0.3,
            emit_number=100,
            emit_rate=2.0,
            particle=particles.ColorPartitionParticle(
                start_color=core.Color(45, 151, 227),
                stop_color=core.Color(7, 2, 40),
            ),
            particle_lifespan=5,
            radius=0.4,
        )
        self.assertEqual(emt_props.lifespan, 150)
        self.assertEqual(emt_props.variance, 0.3)
        self.assertEqual(emt_props.emit_number, 100)
        self.assertEqual(emt_props.emit_rate, 2.0)
        self.assertEqual(emt_props.particle_lifespan, 5)
        self.assertEqual(emt_props.radius, 0.4)
        self.assertEqual(emt_props.particle.start_color, core.Color(45, 151, 227))
        self.assertEqual(emt_props.particle.stop_color, core.Color(7, 2, 40))

    def test_emitter(self):
        emt_props = particles.EmitterProperties(
            0,  # Position is not important as it will be updated by the
            0,  # ParticleEmitter.render_to_buffer method.
            lifespan=150,
            variance=0.3,
            emit_number=100,
            emit_rate=2.0,
            particle=particles.ColorPartitionParticle(
                start_color=core.Color(45, 151, 227),
                stop_color=core.Color(7, 2, 40),
            ),
            particle_lifespan=5,
            radius=0.4,
        )
        emt = particles.ParticleEmitter(emt_props)
        emt.emit()
        emt.apply_force(base.Vector2D(1.0, -0.6))
        emt.update()


if __name__ == "__main__":
    unittest.main()
