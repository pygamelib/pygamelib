.. _gfx_particles-module:

particles
=========

.. versionadded:: 1.3.0

Starting with version 1.3.0, the pygamelib now provides a particle system. It is for now
a first limited version and it has a number of limitations.

First, the particles are "non interactive" objects. They are not affected by board items
or anything drawn on screen nor can they affect them. All particles are drawn on top of
an already rendered screen.

This means no fancy particle physics out of the box. It doesn't means that it is not
doable. It just means that it is not existing out of the box.

Second, although I did my best to make the particle system as efficient as possible,
drawing a lot of moving elements in the terminal is very slow. So be mindful of
the performances when using it.

Now despite the limitations, the particle system still allow to do some very cool stuff.
Here is a video example:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/KnBOzVpapNY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

This is the benchmark of the particle system, the code is available on 
`Ghithub <https://github.com/pygamelib/pygamelib/tree/master/examples/benchmark-particle-system>`_.

.. important:: Like the UI module, the particles system works exclusively with the
   screen buffer system (place, delete, render, update, etc.).
   It doesn't work with Screen functions tagged "direct display" like display_at().

.. toctree::

   pygamelib.gfx.particles.CircleEmitter.rst
   pygamelib.gfx.particles.ColorParticle.rst
   pygamelib.gfx.particles.ColorPartitionParticle.rst
   pygamelib.gfx.particles.EmitterProperties.rst
   pygamelib.gfx.particles.ParticleEmitter.rst
   pygamelib.gfx.particles.ParticlePool.rst
   pygamelib.gfx.particles.Particle.rst
   pygamelib.gfx.particles.ParticleSprixel.rst
   pygamelib.gfx.particles.PartitionParticle.rst
   pygamelib.gfx.particles.RandomColorParticle.rst
   pygamelib.gfx.particles.RandomColorPartitionParticle.rst

.. automodule:: pygamelib.gfx.particles
    :noindex: