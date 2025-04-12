from pygamelib.gfx import core, particles
from pygamelib.assets import graphics
from pygamelib import base, engine
import unittest
import time

# Test cases for all classes in pygamelib.gfx.particles.
# WARNING: This module is under heavy work, it is not ready yet.
# Therefor tests cases are just covering the current state.


def create_sprite(h: int, w: int) -> core.Sprite:
    new_sprite = core.Sprite(size=[w, h])
    for r in range(0, h):
        for c in range(0, w):
            new_sprite.set_sprixel(
                r, c, particles.ParticleSprixel(" ", core.Color.random())
            )
    return new_sprite


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
        ps = particles.ParticleSprixel("+")
        sprix = p.render(ps)
        self.assertNotEqual(sprix.model, "+")
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
        ps = particles.ParticleSprixel(graphics.Blocks.QUADRANT_UPPER_LEFT)
        sprix = p.render(ps)
        self.assertNotEqual(sprix.model, graphics.Blocks.QUADRANT_UPPER_LEFT)
        ps = particles.ParticleSprixel("+")
        sprix = p.render(ps)
        self.assertEqual(sprix.model, "+")
        s = core.Sprixel("+", core.Color(10, 20, 30))
        sprix = p.render(s)
        self.assertEqual(sprix.model, p.sprixel.model)
        self.assertEqual(sprix.bg_color, core.Color(10, 20, 30))

    def test_random_color_particle(self):
        p = particles.RandomColorParticle()
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p = particles.RandomColorParticle(sprixel=particles.ParticleSprixel("+"))
        self.assertEqual(p.sprixel.model, "+")
        p = particles.RandomColorParticle(
            sprixel=particles.ParticleSprixel("+"), color=core.Color(10, 20, 30)
        )
        self.assertEqual(p.sprixel.fg_color, core.Color(10, 20, 30))

    def test_random_color_partition_particle(self):
        p = particles.RandomColorPartitionParticle()
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p = particles.RandomColorPartitionParticle(color=core.Color(10, 20, 30))
        self.assertEqual(p.sprixel.fg_color, core.Color(10, 20, 30))

    def test_color_particle(self):
        p = particles.ColorParticle()
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p = particles.ColorParticle(
            start_color=core.Color(255, 0, 0),
            stop_color=core.Color(0, 255, 0),
        )
        self.assertEqual(p.sprixel.fg_color, core.Color(255, 0, 0))
        p.update()
        self.assertNotEqual(p.sprixel.fg_color, core.Color(255, 0, 0))
        p = particles.ColorParticle()
        self.assertEqual(p.stop_color, core.Color(0, 0, 0))
        p = particles.ColorParticle(start_color=core.Color(255, 0, 0))
        self.assertEqual(p.stop_color, core.Color(255, 0, 0))

    def test_color_partition_particle(self):
        p = particles.ColorPartitionParticle()
        self.assertEqual(p.row, 0)
        self.assertEqual(p.column, 0)
        p = particles.ColorPartitionParticle(
            start_color=core.Color(255, 0, 0),
            stop_color=core.Color(0, 255, 0),
        )
        self.assertEqual(p.sprixel.fg_color, core.Color(255, 0, 0))
        p.update()
        self.assertNotEqual(p.sprixel.fg_color, core.Color(255, 0, 0))
        p = particles.ColorPartitionParticle()
        self.assertEqual(p.stop_color, core.Color(0, 0, 0))
        p = particles.ColorPartitionParticle(start_color=core.Color(255, 0, 0))
        self.assertEqual(p.stop_color, core.Color(255, 0, 0))
        p.update()
        self.assertEqual(p.x, int(p.velocity.x))
        self.assertEqual(p.y, int(p.velocity.y))

    def test_particle_pool(self):
        pp = particles.ParticlePool()
        self.assertEqual(pp.size, 5.0)
        pp = particles.ParticlePool(size=10.0)
        self.assertEqual(pp.size, 10)
        self.assertIsInstance(pp.size, int)
        pp = particles.ParticlePool(size="bork")
        self.assertEqual(pp.size, 100)
        self.assertIsInstance(pp.size, int)

        pp = particles.ParticlePool(
            size=11,
            emitter_properties=particles.EmitterProperties(
                emit_number=10, particle_lifespan=5
            ),
        )
        self.assertEqual(pp.count_active_particles(), 0)
        # By itself the particle pool does not initialize the particles. This is left
        # to the ParticleEmitter. So we have to temper with the particles properties
        # manually.
        pp.pool[0].lifespan = 5
        self.assertEqual(pp.count_active_particles(), 1)
        self.assertEqual(pp.size, 20)
        self.assertIsInstance(pp.size, int)
        parts = pp.get_particles()
        self.assertEqual(len(parts), 10)
        parts = pp.get_particles(200)
        self.assertEqual(len(parts), 20)
        parts = pp.get_particles(20)
        self.assertEqual(len(parts), 20)
        pp.resize(5)
        self.assertEqual(pp.size, 5)
        pp.resize(40)
        self.assertEqual(pp.size, 40)
        parts = pp.get_particles(30)
        for p in parts:
            p.lifespan = 5
        parts = pp.get_particles(30)
        # There's not enough particles in the pool to satisfy the request. So it returns
        # the number of particles that it can get.
        self.assertEqual(len(parts), 10)
        # Test with an instanciated particle.
        p = particles.ColorPartitionParticle(
            start_color=core.Color(255, 0, 0),
            stop_color=core.Color(0, 255, 0),
        )
        pp = particles.ParticlePool(
            size=11,
            emitter_properties=particles.EmitterProperties(
                emit_number=10, particle_lifespan=5, particle=p
            ),
        )
        pp.resize(40)
        self.assertEqual(pp.size, 40)

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
        emt = particles.ParticleEmitter()
        time.sleep(0.1)
        emt.emit()
        emt.row = 5
        emt.column = 4
        self.assertEqual(emt.x, 4)
        self.assertEqual(emt.y, 5)
        emt.x = 10
        emt.y = 20
        self.assertEqual(emt.row, 20)
        self.assertEqual(emt.column, 10)
        emt_props = particles.EmitterProperties(
            0,  # Position is not important as it will be updated by the
            0,  # ParticleEmitter.render_to_buffer method.
            lifespan=50,
            variance=0.3,
            emit_number=100,
            emit_rate=0.05,
            particle=particles.ColorPartitionParticle(
                start_color=core.Color(45, 151, 227),
                stop_color=core.Color(7, 2, 40),
            ),
            particle_lifespan=5,
            particle_velocity=base.Vector2D(0.5, 0.5),
            radius=0.4,
        )
        emt = particles.ParticleEmitter(emt_props)
        emt.update()
        self.assertEqual(emt.active, True)
        emt.active = False
        self.assertEqual(emt.active, False)
        emt.active = True
        with self.assertRaises(base.PglInvalidTypeException):
            emt.active = "True"
        emt.toggle_active()
        self.assertEqual(emt.active, False)
        emt.toggle_active()
        self.assertEqual(emt.active, True)
        pps = emt.particle_pool.size
        emt.resize_pool()
        self.assertEqual(emt.particle_pool.size, pps)
        emt.emit_number *= 2
        emt.resize_pool()
        self.assertEqual(emt.particle_pool.size, pps * 2)
        emt.resize_pool(pps)
        self.assertEqual(emt.particle_pool.size, pps)
        self.assertFalse(emt.finished())

        screen = engine.Screen(50, 50)
        screen.place(emt, 25, 25)
        while not emt.finished():
            time.sleep(0.05)
            emt.emit()
            emt.apply_force(base.Vector2D(1.0, -0.6))
            emt.update()
            screen.update()
        self.assertTrue(emt.finished())

    def test_circle_emitter(self):
        emt_props = particles.EmitterProperties(
            0,  # Position is not important as it will be updated by the
            0,  # ParticleEmitter.render_to_buffer method.
            lifespan=50,
            variance=0.3,
            emit_number=100,
            emit_rate=0.05,
            particle=particles.ColorPartitionParticle(
                start_color=core.Color(45, 151, 227),
                stop_color=core.Color(7, 2, 40),
            ),
            particle_lifespan=5,
            particle_velocity=base.Vector2D(0.5, 0.5),
            radius=0.4,
        )
        emt = particles.CircleEmitter(emt_props)
        self.assertEqual(emt.active, True)
        time.sleep(0.1)
        emt.emit()
        self.assertEqual(emt.particle_pool.count_active_particles(), 100)
        emt = particles.CircleEmitter()
        emt.emit_number = 2
        self.assertEqual(emt.active, True)
        time.sleep(0.1)
        emt.emit()
        self.assertEqual(emt.particle_pool.count_active_particles(), 2)

    def test_serialization(self):
        ep = particles.EmitterProperties(emit_number=99, emit_rate=0.5)
        ep2 = particles.EmitterProperties.load(ep.serialize())
        self.assertEqual(ep.emit_number, ep2.emit_number)
        self.assertEqual(ep.emit_rate, ep2.emit_rate)
        self.assertEqual(ep.serialize(), ep2.serialize())
        p = particles.Particle(lifespan=42)
        p2 = particles.Particle.load(p.serialize())
        self.assertEqual(p.lifespan, p2.lifespan)
        self.assertEqual(p.serialize(), p2.serialize())
        p = particles.ColorPartitionParticle()
        p2 = particles.ColorPartitionParticle.load(p.serialize())
        self.assertEqual(p.serialize(), p2.serialize())
        p = particles.ColorParticle()
        p2 = particles.ColorParticle.load(p.serialize())
        self.assertEqual(p.serialize(), p2.serialize())
        p = particles.PartitionParticle()
        p2 = particles.PartitionParticle.load(p.serialize())
        self.assertEqual(p.serialize(), p2.serialize())
        p = particles.RandomColorParticle()
        p2 = particles.RandomColorParticle.load(p.serialize())
        self.assertEqual(p.serialize(), p2.serialize())
        p = particles.RandomColorPartitionParticle()
        p2 = particles.RandomColorPartitionParticle.load(p.serialize())
        self.assertEqual(p.serialize(), p2.serialize())
        pe = particles.ParticleEmitter(ep)
        pe2 = particles.ParticleEmitter.load(pe.serialize())
        self.assertEqual(pe.serialize(), pe2.serialize())
        self.assertEqual(pe2.emit_number, 99)
        self.assertEqual(pe2.emit_rate, 0.5)
        pe = particles.CircleEmitter(ep)
        pe2 = particles.CircleEmitter.load(pe.serialize())
        self.assertEqual(pe.serialize(), pe2.serialize())
        self.assertEqual(pe2.emit_number, 99)
        self.assertEqual(pe2.emit_rate, 0.5)
        ep.particle = particles.ColorPartitionParticle(4, 2, lifespan=24)
        pe = particles.ParticleEmitter(ep)
        pe2 = particles.ParticleEmitter.load(pe.serialize())
        self.assertEqual(pe.serialize(), pe2.serialize())
        self.assertEqual(pe2.emit_number, 99)
        self.assertEqual(pe2.emit_rate, 0.5)

    def test_sprite_emitter(self):
        emt_props = particles.EmitterProperties(
            0,  # Position is not important as it will be updated by the
            0,  # ParticleEmitter.render_to_buffer method.
            lifespan=1,
            variance=0.3,
            emit_number=100,
            emit_rate=0.05,
            particle=particles.ColorPartitionParticle(
                start_color=core.Color(45, 151, 227),
                stop_color=core.Color(7, 2, 40),
            ),
            particle_lifespan=5.0,
            particle_velocity=base.Vector2D(0.5, 0.5),
            radius=0.4,
        )
        # NOTE: For future maintainers, I scratched my head as to why the number of
        #       particles was different when omitting the emitter properties and
        #       obviously it is because emit_number and particle_lifespan are different.
        (sprite_height, sprite_width) = (2, 4)
        test_sprite = create_sprite(sprite_height, sprite_width)
        emt = particles.SpriteEmitter(test_sprite, emt_props)
        self.assertEqual(emt.active, True)
        time.sleep(0.1)
        emt.emit()
        emt.update()
        print(
            f"Test 1, # of active particles: {emt.particle_pool.count_active_particles()}"
        )
        self.assertEqual(
            emt.particle_pool.count_active_particles(), sprite_height * sprite_width
        )
        time.sleep(0.1)
        emt.emit(2)
        emt.update()
        print(
            f"Test 2, # of active particles: {emt.particle_pool.count_active_particles()}"
        )
        self.assertEqual(
            emt.particle_pool.count_active_particles(), sprite_height * sprite_width
        )
        emt = particles.SpriteEmitter(test_sprite)
        self.assertEqual(emt.active, True)
        time.sleep(0.1)
        emt.emit()
        emt.update()
        print(
            f"Test 3, # of active particles: {emt.particle_pool.count_active_particles()}"
        )
        self.assertEqual(
            emt.particle_pool.count_active_particles(), sprite_height * sprite_width
        )
        time.sleep(2)
        emt.emit(2)
        emt.update()
        print(
            f"Test 4, # of active particles: {emt.particle_pool.count_active_particles()}"
        )
        self.assertEqual(
            emt.particle_pool.count_active_particles(), sprite_height * sprite_width
        )


if __name__ == "__main__":
    unittest.main()
