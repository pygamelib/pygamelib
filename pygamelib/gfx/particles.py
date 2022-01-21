from copy import deepcopy, copy
from pygamelib.gfx import core
import pygamelib.board_items as board_items
import pygamelib.assets.graphics as graphics
import pygamelib.base as base

# from dataclasses import dataclass

# DEBUG ONLY
# from pygamelib import engine

import time
import random
import math

__docformat__ = "restructuredtext"

"""
The particle module contains everything related to particles.

This includes utility classes like the ParticleSprixel, EmitterProperties or
ParticlePool, as well as all type of particles and particle emitters.

.. Important:: Most objects i the particle system have a position that can be referred
   to and manipulated using the regular x/y coordinates system or the pygamelib's
   row/column system. They are exactly equivalent.

.. autosummary::
   :toctree: .

   pygamelib.gfx.particles.CircleEmitter
   pygamelib.gfx.particles.ColorParticle
   pygamelib.gfx.particles.ColorPartitionParticle
   pygamelib.gfx.particles.EmitterProperties
   pygamelib.gfx.particles.Particle
   pygamelib.gfx.particles.ParticleSprixel
   pygamelib.gfx.particles.ParticlePool
   pygamelib.gfx.particles.ParticleEmitter
   pygamelib.gfx.particles.PartitionParticle
   pygamelib.gfx.particles.RandomColorParticle
   pygamelib.gfx.particles.RandomColorPartitionParticle

"""


class ParticleSprixel(core.Sprixel):
    """
    The ParticleSprixel is nothing more than a :class:`~pygamelib.gfx.core.Sprixel`.
    Its only role is to help differentiate rendered sprixels for Partition Particles.
    """

    def __init__(self, model="", bg_color=None, fg_color=None, is_bg_transparent=None):
        super().__init__(
            model=model,
            bg_color=bg_color,
            fg_color=fg_color,
            is_bg_transparent=is_bg_transparent,
        )


class Particle(base.PglBaseObject):
    """
    The Particle class is the base class that is inherited from by all other particles.
    It is mostly a "data class" in the sense that it is a class used for calculations
    but is not able to render on screen by itsefl. All operations are pure data
    operations until the emitter draw the particles.

    Altought the Particle class can be used on its own, it is most likely to be used as
    a template for a particle emitter.
    """

    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        sprixel: ParticleSprixel = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param row: The initial row position of the particle on the screen.
        :type row: int
        :param column: The initial column position of the particle on the screen.
        :type column: int
        :param velocity: The initial velocity of the particle.
        :type velocity: :class:`~pygamelib.base.Vector2D`
        :param lifespan: The particle lifespan in number of movements/turns. A particle
           with a lifespan of 3 will move for 3 turns before being finished.
        :type lifespan: int
        :param sprixel: The sprixel that represent the particle when drawn on screen.
        :type sprixel: :class:`~pygamelib.gfx.core.Sprixel`

        Example::

            single_particle = Particle(
                row=5,
                column=5,
                velocity=base.Vector2D(-0.5, 0.0),
                lifespan=10,
                sprixel=core.Sprixel(graphics.GeometricShapes.BLACK_CIRCLE)
            )
        """
        super().__init__()
        self.__pos_x = self._initial_column = column
        self.__pos_y = self._initial_row = row
        self.velocity = velocity
        # print(f"Particle constructor: self.velocity={self.velocity}")
        if self.velocity is None:
            self.velocity = base.Vector2D(
                random.uniform(-1, 1), 2 * random.uniform(-1, 1)
            )
            if abs(self.velocity.column) < abs(self.velocity.row) * 2:
                self.velocity.column = (
                    self.velocity.column / abs(self.velocity.column)
                ) * (abs(self.velocity.row) * 2)
        self.__velocity_accumulator = base.Vector2D(0.0, 0.0)
        self.acceleration = base.Vector2D(0.0, 0.0)
        self.lifespan = lifespan
        if self.lifespan is None:
            self.lifespan = 20
        self._initial_lifespan = self.lifespan
        self.sprixel = sprixel
        if sprixel is None:
            self.sprixel = core.Sprixel(graphics.GeometricShapes.BULLET)
        self.__last_update = time.time()

    def reset(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
    ):
        """
        Reset a particle in its initial state. This is particularly useful for the reuse
        of particles.

        This method takes almost the same parameters than the constructor.

        :param row: The initial row position of the particle on the screen.
        :type row: int
        :param column: The initial column position of the particle on the screen.
        :type column: int
        :param velocity: The initial velocity of the particle.
        :type velocity: :class:`~pygamelib.base.Vector2D`
        :param lifespan: The particle lifespan in number of movements/turns. A particle
           with a lifespan of 3 will move for 3 turns before being finished.
        :type lifespan: int

        Example::

            single_particle.reset(
                row=5,
                column=5,
                velocity=base.Vector2D(-0.5, 0.0),
                lifespan=10,
            )
        """
        self.__pos_x = self._initial_column = column
        self.__pos_y = self._initial_row = row
        if velocity is not None:
            self.velocity = velocity
        # if self.velocity is None:
        #     self.velocity = base.Vector2D(
        #         random.uniform(-1, 1), 2 * random.uniform(-1, 1)
        #     )
        #     if abs(self.velocity.column) < abs(self.velocity.row) * 2:
        #         self.velocity.column = (
        #             self.velocity.column / abs(self.velocity.column)
        #         ) * (abs(self.velocity.row) * 2)
        self.__velocity_accumulator = base.Vector2D(0.0, 0.0)
        self.acceleration = base.Vector2D(0.0, 0.0)
        if lifespan is not None:
            self.reset_lifespan(lifespan)

        # if sprixel is not None:
        #     self.sprixel = sprixel
        self.__last_update = time.time()

    @property
    def x(self):
        """
        Access and set the x property. Equivalent to the column property.
        """
        return self.__pos_x

    @x.setter
    def x(self, value: int):
        if type(value) is int:
            self.__pos_x = value

    @property
    def column(self):
        """
        Access and set the column property. Equivalent to the x property.
        """
        return self.__pos_x

    @column.setter
    def column(self, value: int):
        if type(value) is int:
            self.__pos_x = value

    @property
    def y(self):
        """
        Access and set the y property. Equivalent to the row property.
        """
        return self.__pos_y

    @y.setter
    def y(self, value: int):
        if type(value) is int:
            self.__pos_y = value

    @property
    def row(self):
        """
        Access and set the row property. Equivalent to the y property.
        """
        return self.__pos_y

    @row.setter
    def row(self, value: int):
        if type(value) is int:
            self.__pos_y = value

    def apply_force(self, force: base.Vector2D) -> None:
        """
        Apply a force to the particle acceleration vector.

        You are more likely to apply forces to all particles of an emitter through the
        :py:meth:`~pygamelib.gfx.particles.Emitter.apply_force` method of the emitter
        class.

        :param force: The force to apply.
        :type force: :class:`~pygamelib.base.Vector2D`

        Example::

            gravity = Vector2D(-0.2, 0.0)
            my_particle.apply_force(gravity)
        """
        if force is not None and isinstance(force, base.Vector2D):
            self.acceleration += force

    def reset_lifespan(self, lifespan: int) -> None:
        """
        Reset the particle lifespan (including the initial lifespan).

        :param lifespan: The particle lifespan in number of movements/turns.
        :type lifespan: int

        Example::

            my_particle.reset_lifespan(10)
        """
        self.lifespan = lifespan
        if self.lifespan is None:
            self.lifespan = 20
        self._initial_lifespan = self.lifespan

    def update(self) -> None:
        """
        The update method perform the calculations required to process the new particle
        position.
        It mainly adds the acceleration to the velocity vector and update the position
        accordingly.

        After calling update() the accelertion is "consummed" in the velocity and
        therefor resetted'

        The update() method takes no parameters and returns nothing.

        Example::

            my_particle.update()
        """
        now = time.time()
        self.velocity += self.acceleration
        # print(f"\tParticle.update() NEW velocity={self.velocity}")
        # sign_c = sign_r = 1.0
        # if self.velocity.row != 0.0 and self.velocity.row != 0:
        #     sign_r = self.velocity.row / abs(self.velocity.row)
        # if self.velocity.column != 0.0 and self.velocity.column != 0:
        #     sign_c = self.velocity.column / abs(self.velocity.column)
        # if abs(self.velocity.row) >= 1.0:
        #     self.velocity.row -= sign_r * 1.0
        #     self.row += sign_r * 1.0
        # else:
        #     self.row += round(self.velocity.row)
        # if abs(self.velocity.column) >= 1.0:
        #     self.velocity.column -= sign_c * 1.0
        #     self.column += sign_c * 1.0
        # else:
        #     self.column += round(self.velocity.column)

        # self.row += round(self.velocity.row)
        # self.column += round(self.velocity.column)

        self.__velocity_accumulator += self.velocity
        # self.__velocity_accumulator.row += self.velocity.row * (
        #     now - self.__last_update
        # )
        # self.__velocity_accumulator.column += self.velocity.column * (
        #     now - self.__last_update
        # )

        # V1
        # self.row = int(self._initial_row + self.velocity.row)
        # self.column = int(self._initial_column + self.velocity.column)

        # V2
        self.row = int(self._initial_row + self.__velocity_accumulator.row)
        self.column = int(self._initial_column + self.__velocity_accumulator.column)

        #     print(f"\tivr: {self.velocity.row} - {int(self.velocity.row)} = {ivr}")
        #     print(
        #         f"\tivc: {self.velocity.column} - {int(self.velocity.column)} = {ivc}"
        #     )
        # print(f"\tParticle.update() NEW position={self.row}x{self.column}\n")
        self.acceleration *= 0
        self.lifespan -= 1
        self.__last_update = now

    def render(self, sprixel: core.Sprixel = None):
        """
        Render the particle as a :class:`~pygamelib.gfx.core.Sprixel`. This method is
        called by the :class:`~pygamelib.gfx.particles.ParticleEmitter` render_to_buffer
        method.

        It takes a :class:`~pygamelib.gfx.core.Sprixel` as a parameter. This Sprixel is
        given by the ParticleEmitter.render_to_buffer() method and if it is not None,
        the particle will render itself into that :class:`~pygamelib.gfx.core.Sprixel`
        and return it.

        .. important:: This method must be called after everything else as rendered or
           else there will be :class:`~pygamelib.gfx.core.Sprixel` that will be
           overwritten during their rendering cycle. Other elements could also have
           their :class:`~pygamelib.gfx.core.Sprixel` corrupted and replaced by the
           particle one.

        :param sprixel: A sprixel already rendered in the screen buffer.
        :type sprixel: :class:`~pygamelib.gfx.core.Sprixel`

        Example::

            p = my_particle
            buffer[p.row][p.column] = p.render(buffer[p.row][p.column])
        """
        # If you override this method, it's your responsibility to return a copy of
        # yourself (or just use super().render(sprixel) as it already returns a copy).
        if isinstance(sprixel, ParticleSprixel):
            sprixel.model = self.sprixel.model
            return sprixel
        elif isinstance(sprixel, core.Sprixel):
            # This sprixel might be modified later in the rendering cycle so we want to
            # make sure that the next particle will only overide the rendered sprixel,
            # not our live one. While preserving the
            # NOTE: on the other hand, the model is overwritten at each update... I need
            # to test to see if I could save the copy...
            # ret = deepcopy(self.sprixel)
            ret = copy(self.sprixel)
            ret.bg_color = sprixel.bg_color
            return ret
        else:
            # This sprixel might be modified later in the rendering cycle so we want to
            # make sure that the next particle will only overide the rendered sprixel,
            # not our live one.
            # NOTE: on the other hand, the model is overwritten at each update... I need
            # to test to see if I could save the copy...
            # return deepcopy(self.sprixel)
            return copy(self.sprixel)

    def finished(self) -> bool:
        """
        Return True if the particle is done living (i.e its lifespan is lesser or equal
        to 0). It returns False otherwise.

        :rtype: bool

        Example::

            if not my_particle.finished():
                my_particle.update()
        """
        return self.lifespan <= 0

    def terminate(self) -> None:
        """
        Terminate a particle, i.e sets its lifespan to -1.

        In that case the ParticleEmitter and ParticlePool will recycle it. That is *IF*
        you are managing the particle through an emitter and/or a pool of course.

        Example::

            p = my_particle
            if p.row >= screen,height or p.column >= screen.width:
                p.terminate()
        """
        self.lifespan = -1


class PartitionParticle(Particle):
    """
    The PartitionParticle is a more precise :class:`~pygamelib.gfx.particles.Particle`.
    Its main difference is that it is additive. This means that the PartitionParticle
    posess the ability to complement a sprixel that is already drawn. Or to add to a
    sprixel that is already drawn.

    As a matter of facts, the primary goal of the PartitionParticle is to modify an
    already drawn sprixel to improve the visuals/graphical effects.

    For example, if two particles occupy the sane space on screen, with a regular
    :class:`~pygamelib.gfx.particles.Particle` the last to render is the one that will
    be displayed. If one particle is represented by '▘' and the other by '▗', only the
    second will be displayed.

    In the case of PartitionParticles, an addition of the 2 sprixels will be displayed!
    So in the previous example the addition of the 2 particles would result in '▚'
    because '▘' + '▗' = '▚'.

    It comes at a cost though as the PartitionParticle is slower to render than the
    :class:`~pygamelib.gfx.particles.Particle` class.

    The partition particle achieve that by using a partition and a blending table. The
    blending table is crucial for the performances to be not too catastrophic. The size
    of the blending table is directly linked to the performances of the
    PartitionParticle (the bigger the blending table the slower the rendering).

    The blending table is a dictionnary of strings that covers all possible operations.

    Example::
       partition_blending_table = {
            gb.QUADRANT_UPPER_LEFT
            + gb.QUADRANT_UPPER_RIGHT: gb.UPPER_HALF_BLOCK,
            gb.QUADRANT_UPPER_LEFT + gb.QUADRANT_LOWER_LEFT: gb.LEFT_HALF_BLOCK,
            gb.QUADRANT_UPPER_LEFT
            + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
            # it goes on for many lines...
        }

    By default, the PartitionParticle has a blending table that is using the UTF8
    Blocks.QUADRANT_* characters. If you want to use a different one, you need to define
    a new blending table and pass it as parameter to the constructor.

    The partition itself is a 2x2 array that contains the 4 quadrants of a character
    displayed in the terminal.

    As an example, if a full character were a block: '█' the partition would be:
    [['▘', '▝'], ['▖', '▗']].

    You can conceive the partition as the exploded version of the character/sprixel and
    the blending table as the rules to blend them together.

    The PartitionParticle can also be used to create reinforcement effects. For example,
    if the partition is composed solely of '■' and the partition table only define one
    rule: '■' + '■' = '⬛'.
    It is a powerful particle that can be used to create a lot of different effects.

    """

    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        partition: list = None,
        partition_blending_table: list = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param row: The initial row position of the particle on the screen.
        :type row: int
        :param column: The initial column position of the particle on the screen.
        :type column: int
        :param velocity: The initial velocity of the particle.
        :type velocity: :class:`~pygamelib.base.Vector2D`
        :param lifespan: The particle lifespan in number of movements/turns. A particle
           with a lifespan of 3 will move for 3 turns before being finished.
        :type lifespan: int
        :param partition: The 2x2 array that defines the partition of the sprixel.
        :type partition: list
        :param partition_blending_table: The blending table that defines the rules to
           blend the 2 sprixels.
        :type partition_blending_table: list

        Example::

            # Here we'll use the default blending table
            single_particle = PartitionParticle(
                row=5,
                column=5,
                velocity=base.Vector2D(-0.5, 0.0),
                lifespan=10,
                self.partition = [
                    [
                        graphics.Blocks.QUADRANT_UPPER_LEFT,
                        graphics.Blocks.QUADRANT_UPPER_RIGHT,
                    ],
                    [
                        graphics.Blocks.QUADRANT_LOWER_LEFT,
                        graphics.Blocks.QUADRANT_LOWER_RIGHT,
                    ],
                ]
            )
        """
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
        )
        self.partition = partition
        self.partition_blending_table = partition_blending_table
        self._spx_row = 0
        self._spx_column = 0
        if partition is None and sprixel is None:
            self.partition = [
                [
                    graphics.Blocks.QUADRANT_UPPER_LEFT,
                    graphics.Blocks.QUADRANT_UPPER_RIGHT,
                ],
                [
                    graphics.Blocks.QUADRANT_LOWER_LEFT,
                    graphics.Blocks.QUADRANT_LOWER_RIGHT,
                ],
            ]
            self.sprixel = ParticleSprixel(self.partition[0][0])

            if partition_blending_table is None:
                gb = graphics.Blocks
                # I don't think anyone is going to willingly go through that...
                # So first I coded a way to dynamically recognize the addition to do,
                # but crappy performances got me to build a "cached version".
                self.partition_blending_table = {
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT: gb.UPPER_HALF_BLOCK,
                    gb.QUADRANT_UPPER_LEFT + gb.QUADRANT_LOWER_LEFT: gb.LEFT_HALF_BLOCK,
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
                    gb.QUADRANT_UPPER_LEFT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT + gb.LEFT_HALF_BLOCK: gb.LEFT_HALF_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.UPPER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT + gb.QUADRANT_UPPER_LEFT: gb.LEFT_HALF_BLOCK,
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK + gb.QUADRANT_UPPER_LEFT: gb.LEFT_HALF_BLOCK,
                    #
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.RIGHT_HALF_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.UPPER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT + gb.QUADRANT_UPPER_LEFT: gb.LEFT_HALF_BLOCK,
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.LOWER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT + gb.RIGHT_HALF_BLOCK: gb.RIGHT_HALF_BLOCK,
                    gb.RIGHT_HALF_BLOCK + gb.QUADRANT_UPPER_RIGHT: gb.RIGHT_HALF_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.LOWER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.RIGHT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_LOWER_RIGHT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.RIGHT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_UPPER_RIGHT: gb.RIGHT_HALF_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.QUADRANT_LOWER_RIGHT: gb.RIGHT_HALF_BLOCK,
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.QUADRANT_LOWER_LEFT: gb.LOWER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT
                    + gb.QUADRANT_LOWER_RIGHT: gb.LOWER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_RIGHT + gb.RIGHT_HALF_BLOCK: gb.RIGHT_HALF_BLOCK,
                    gb.RIGHT_HALF_BLOCK + gb.QUADRANT_LOWER_RIGHT: gb.RIGHT_HALF_BLOCK,
                    gb.QUADRANT_LOWER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_RIGHT + gb.LOWER_HALF_BLOCK: gb.LOWER_HALF_BLOCK,
                    gb.LOWER_HALF_BLOCK + gb.QUADRANT_LOWER_RIGHT: gb.LOWER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_LOWER_LEFT + gb.LEFT_HALF_BLOCK: gb.LEFT_HALF_BLOCK,
                    gb.LEFT_HALF_BLOCK + gb.QUADRANT_LOWER_LEFT: gb.LEFT_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT + gb.LOWER_HALF_BLOCK: gb.LOWER_HALF_BLOCK,
                    gb.LOWER_HALF_BLOCK + gb.QUADRANT_LOWER_LEFT: gb.LOWER_HALF_BLOCK,
                    gb.QUADRANT_LOWER_LEFT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK + gb.LEFT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.LEFT_HALF_BLOCK + gb.RIGHT_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.RIGHT_HALF_BLOCK
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.RIGHT_HALF_BLOCK
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.RIGHT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.LEFT_HALF_BLOCK
                    + gb.LOWER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK
                    + gb.LEFT_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.LOWER_HALF_BLOCK + gb.UPPER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.UPPER_HALF_BLOCK + gb.LOWER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT: gb.FULL_BLOCK,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.UPPER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT
                    + gb.UPPER_HALF_BLOCK: gb.FULL_BLOCK,
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_LEFT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK + gb.QUADRANT_UPPER_RIGHT: gb.UPPER_HALF_BLOCK,
                    gb.QUADRANT_UPPER_RIGHT + gb.UPPER_HALF_BLOCK: gb.UPPER_HALF_BLOCK,
                    gb.UPPER_HALF_BLOCK + gb.QUADRANT_UPPER_LEFT: gb.UPPER_HALF_BLOCK,
                    gb.QUADRANT_UPPER_LEFT + gb.UPPER_HALF_BLOCK: gb.UPPER_HALF_BLOCK,
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.UPPER_HALF_BLOCK
                    + gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                    gb.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + gb.UPPER_HALF_BLOCK: gb.QUADRANT_UPPER_LEFT_AND_UPPER_RIGHT_AND_LOWER_RIGHT,  # noqa: E501
                }

    def update(self):
        """
        This method first calls the Particle.update() method, then calculates the
        quadrant position, i.e: the actual position of the particle within a console
        character. It then updates the particle's model based on this internal position.

        Example::

            my_particle.update()
        """
        super().update()
        f_row = self._initial_row + self.velocity.row
        f_column = self._initial_column + self.velocity.column
        if self.partition is not None:
            ivr = f_row - int(f_row)
            ivc = f_column - int(f_column)
            spx_c = 0
            spx_r = 0
            if ivr > 0.5:
                spx_r = 1
            if ivc > 0.5:
                spx_c = 1
            self.sprixel.model = self.partition[spx_r][spx_c]
            self._spx_row = spx_r
            self._spx_column = spx_c

    def render(self, sprixel: core.Sprixel = None):
        """
        This method first calls the Particle.render() method. Then it updates the
        rendered particle's model based on the blending table.

        :param sprixel: A sprixel already rendered in the screen buffer.
        :type sprixel: :class:`~pygamelib.gfx.core.Sprixel`

        Example::

            p = my_particle
            buffer[p.row][p.column] = p.render(buffer[p.row][p.column])
        """
        # If you override this method, it's your responsibility to return a copy of
        # yourself (or just use super().render(sprixel) as it already returns a copy).
        if isinstance(sprixel, ParticleSprixel):
            if self.sprixel.model + sprixel.model in self.partition_blending_table:
                sprixel.model = self.partition_blending_table[
                    self.sprixel.model + sprixel.model
                ]
                return sprixel
            # If we have no match we don't change the sprixel already rendered.
            # TODO: DEV
            # return None
            return sprixel
        elif isinstance(sprixel, core.Sprixel):
            # This sprixel might be modified later in the rendering cycle so we want to
            # make sure that the next particle will only overide the rendered sprixel,
            # not our live one. While preserving the
            # NOTE: on the other hand, the model is overwritten at each update... I need
            # to test to see if I could save the copy...
            ret = deepcopy(self.sprixel)
            ret.bg_color = sprixel.bg_color
            return ret
        else:
            # This sprixel might be modified later in the rendering cycle so we want to
            # make sure that the next particle will only overide the rendered sprixel,
            # not our live one.
            # NOTE: on the other hand, the model is overwritten at each update... I need
            # to test to see if I could save the copy...
            return deepcopy(self.sprixel)


class RandomColorParticle(Particle):
    """
    This class is a :class:`~pygamelib.gfx.particles.Particle` that has a random
    foreground color.

    By default, if both the sprixel and color parameters are not specified, the model
    of the :class:`~pygamelib.gfx.core.Sprixel` is going to be '•' and the color will be
    randomly chosen.

    You can also specify a color and a model.
    """

    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        sprixel: ParticleSprixel = None,
        color: core.Color = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param row: The initial row position of the particle on the screen.
        :type row: int
        :param column: The initial column position of the particle on the screen.
        :type column: int
        :param velocity: The initial velocity of the particle.
        :type velocity: :class:`~pygamelib.base.Vector2D`
        :param lifespan: The particle lifespan in number of movements/turns. A particle
           with a lifespan of 3 will move for 3 turns before being finished.
        :type lifespan: int
        :param sprixel: The sprixel that represent the particle when drawn on screen.
        :type sprixel: :class:`~pygamelib.gfx.core.Sprixel`
        :param color: The color of the particle.
        :type color: :class:`~pygamelib.gfx.core.Color`

        Example::

            single_particle = RandomColorParticle(
                row=5,
                column=5,
                velocity=base.Vector2D(-0.5, 0.0),
                lifespan=10,
            )
        """
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
            sprixel=sprixel,
        )
        self.partition = None
        if sprixel is None and color is None:
            self.sprixel = ParticleSprixel(
                graphics.GeometricShapes.BULLET,
                fg_color=core.Color(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            )
        elif sprixel is not None and color is None:
            self.sprixel.fg_color = core.Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        else:
            self.sprixel.fg_color = color


class RandomColorPartitionParticle(PartitionParticle):
    """
    This class is basically the same as
    :class:`~pygamelib.gfx.particles.RandomColorParticle` but its base class is
    :class:`~pygamelib.gfx.particles.PartitionParticle` instead of
    :class:`~pygamelib.gfx.particles.Particle`. Everything else is the same.
    """

    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        partition: list = None,
        partition_blending_table: list = None,
        color: core.Color = None,
    ) -> None:
        """
        The constructor takes the following parameters.

        :param row: The initial row position of the particle on the screen.
        :type row: int
        :param column: The initial column position of the particle on the screen.
        :type column: int
        :param velocity: The initial velocity of the particle.
        :type velocity: :class:`~pygamelib.base.Vector2D`
        :param lifespan: The particle lifespan in number of movements/turns. A particle
           with a lifespan of 3 will move for 3 turns before being finished.
        :type lifespan: int
        :param partition: The partition of the particle.
        :type partition: list
        :param partition_blending_table: The blending table of the particle.
        :type partition_blending_table: list
        :param color: The color of the particle.
        :type color: :class:`~pygamelib.gfx.core.Color`

        Example::

            single_particle = RandomColorPartitionParticle(
                row=5,
                column=5,
                velocity=base.Vector2D(-0.5, 0.0),
                lifespan=10,
            )
        """
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
            partition=partition,
            partition_blending_table=partition_blending_table,
        )
        if color is None:
            self.sprixel.fg_color = core.Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        else:
            self.sprixel.fg_color = color


class ColorParticle(Particle):
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        sprixel: ParticleSprixel = None,
        start_color: core.Color = None,
        stop_color: core.Color = None,
    ) -> None:
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
            sprixel=sprixel,
        )
        self.start_color = start_color
        if self.start_color is None:
            self.start_color = core.Color(255, 0, 0)
        self.stop_color = stop_color
        if self.stop_color is None and self.start_color is None:
            self.stop_color = core.Color(0, 0, 0)
        elif self.stop_color is None and self.start_color is not None:
            self.stop_color = self.start_color
        self.sprixel.fg_color = deepcopy(self.start_color)
        self.__color_cache = {}

    def update(self):
        super().update()
        lp = self.lifespan if self.lifespan >= 0 else 0
        coeff = 1 - (lp / self._initial_lifespan)
        if coeff not in self.__color_cache.keys():
            self.__color_cache[coeff] = self.start_color.blend(self.stop_color, coeff)
        self.sprixel.fg_color = self.__color_cache[coeff]


class ColorPartitionParticle(PartitionParticle):
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        partition: list = None,
        partition_blending_table: list = None,
        sprixel: ParticleSprixel = None,
        start_color: core.Color = None,
        stop_color: core.Color = None,
    ) -> None:
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
            partition=partition,
            partition_blending_table=partition_blending_table,
            sprixel=sprixel,
        )
        self.start_color = start_color
        if self.start_color is None:
            self.start_color = core.Color(255, 0, 0)
        self.stop_color = stop_color
        if self.stop_color is None and self.start_color is None:
            self.stop_color = core.Color(0, 0, 0)
        elif self.stop_color is None and self.start_color is not None:
            self.stop_color = self.start_color
        self.sprixel.fg_color = deepcopy(self.start_color)
        self.__color_cache = {}

    def update(self):
        super().update()
        lp = self.lifespan if self.lifespan >= 0 else 0
        # self.sprixel.fg_color = self.start_color.blend(
        #     self.stop_color, 1 - (lp / self._initial_lifespan)
        # )
        coeff = 1 - (lp / self._initial_lifespan)
        if coeff not in self.__color_cache.keys():
            self.__color_cache[coeff] = self.start_color.blend(self.stop_color, coeff)
        self.sprixel.fg_color = self.__color_cache[coeff]


# Emitters


# Ideally that would be a @dataclass, but support for KW_ONLY is restricted to
# Python 3.10+. Too bad.
class EmitterProperties:
    """
    EmitterProperties is a class that hold configuration variables for a particle
    emitter. The idea is that it's easier to carry around for multiple emitters with the
    same configuration than multiple values in the emitter's constructor.

    It holds all possible parmeters for all types of emitters. Emitters uses only the
    ones that they really need.

    .. Important:: In most cases these values are copied by the emitter's constructor.
       So changing the values during an emitter's alive cycle is not going to do
       anything.

    .. Note:: This class should be a @dataclass. However, support for keyword only
       data classes is specific to python 3.10+. So for now, it is a regular class.
    """

    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        variance: float = 2.0,
        emit_number: int = 1,
        emit_rate: float = 0.1,
        lifespan=200,
        parent: board_items.BoardItem = None,
        particle_velocity=None,
        particle_acceleration=None,
        particle_lifespan=5.0,
        radius=1.0,
        particle: Particle = Particle,
    ) -> None:
        """

        :param row: The row where the emitter is. It is only important for the first
           rendering cycle. After that, the emitter will know its position on screen.
        :type row: int
        :param column: The row where the emitter is. It is only important for the first
           rendering cycle. After that, the emitter will know its position on screen.
        :type column: int
        :param variance: The variance is the amount of randomness that is allowed when
           emitting a particle. The exact use of this parameter is specific to each
           emitter.
        :type variance: float
        :param emit_number: The number of particle emitted at each timer tick.
        :type emit_number: int
        :param emit_rate: The rate of emission in seconds. This value needs to be
           understood as "the emitter will emit **emit_number** particles every
           **emit_rate** seconds".
        :type emit_rate: float
        :param lifespan: The lifespan of the emitter in number of emission cycle. If
           lifespan is set to 1 for example, the emitter will only emit one burst of
           particles.
        :type lifespan: int
        :param parent: A parent board item. If you do that manually, you will probably
           want to set it specifically for each emitter.
        :type parent: :class:`~pygamelib.board_items.BoardItem`
        :param particle_velocity: The initial particle velocity. Please read the
           documentation of each emitter for the specific use of particle velocity.
        :type particle_velocity: :class:`~pygamelib.base.Vector2D`
        :param particle_acceleration: The initial particle acceleration. Please read the
           documentation of each emitter for the specific use of particle acceleration.
        :type particle_acceleration: :class:`~pygamelib.base.Vector2D`
        :param particle_lifespan: The lifespan of the particle in number of cycles.
        :type particle_lifespan: int
        :param radius: For emitter that supports it (like the CircleEmitter), sets the
           radius of emission (which translate into a velocity vector for each
           particle).
        :type radius: float
        :param particle: The particle that the emitter will emit. This can be a class
           reference or a fully instanciated particle. Emitters will copy it in the
           particle pool.
        :type particle: :class:`Particle`

        Example::

            method()
        """
        self.row = row
        self.column = column
        self.variance = variance
        self.emit_number = emit_number
        self.emit_rate = emit_rate
        self.lifespan = lifespan
        self.parent = parent
        self.particle_velocity = particle_velocity
        self.particle_acceleration = particle_acceleration
        self.particle_lifespan = particle_lifespan
        self.radius = radius
        self.particle = particle


class ParticlePool:
    def __init__(
        self, size: int = None, emitter_properties: EmitterProperties = None
    ) -> None:

        if size is None:
            self.size = (
                emitter_properties.emit_number * emitter_properties.particle_lifespan
            )
        elif type(size) is int:
            self.size = size
        elif type(size) is float:
            self.size = int(size)
        else:
            self.size = 100
        if self.size % emitter_properties.emit_number != 0:
            self.size += emitter_properties.emit_number - (
                self.size % emitter_properties.emit_number
            )
        self.emitter_properties = None
        if isinstance(emitter_properties, EmitterProperties):
            self.emitter_properties = emitter_properties
        else:
            self.emitter_properties = EmitterProperties()
        self.current_idx = 0

        # Init the particle pool. Beware: it's a tuple, therefore it's immutable.
        self.__particle_pool = ()
        # Here we don't care about the particles configuration (position, velocity,
        # variance, etc.) because the emitter will reset it when it actually emit the
        # particles.
        if callable(self.emitter_properties.particle):
            self.__particle_pool = tuple(
                self.emitter_properties.particle() for _ in range(self.size)
            )
        else:
            self.__particle_pool = tuple(
                deepcopy(self.emitter_properties.particle) for _ in range(self.size)
            )
        # Finally, we make sure that all are terminated.
        for p in self.__particle_pool:
            p.terminate()

    @property
    def pool(self) -> tuple:
        """
        A read-only property that returns the particle pool tuple.
        """
        return self.__particle_pool

    def get_particles(self, amount):
        if amount is None:
            amount = self.emitter_properties.emit_number
        lp = self.size
        # We cannot return more particles than there is in the pool
        if amount > lp:
            amount = lp - 1

        idx = self.current_idx

        # If there's still enough unused particles in the pool we return them.
        if idx + amount < lp:
            self.current_idx += amount
            # I have no idea why VSCode/black keeps adding a space here!
            return self.pool[idx : idx + amount - 1]  # noqa: E203
        # If not, but there's enough dead particle at the beginning of the pool we
        # return these.
        elif self.pool[amount - 1].finished():
            self.current_idx = amount
            # I have no idea why VSCode/black keeps adding a space here!
            return self.pool[idx : (idx + amount)]  # noqa: E203
        # Else we return what we have left and reset the index. It is highly probable
        # that we have not enough particle left...
        else:
            self.current_idx = 0
            return self.pool[idx:]

    def count_active_particles(self) -> int:
        """Returns the number of active particle (i.e not finished) in the pool.

        .. Important:: The only way to know the amount of alive particles is to go
           through the entire pool. Be aware of the performance impact on large particle
           pools.

        :returns: the number of active particles.
        :rtype: int

        Example::

            if emitter.particles.count_active_particles() > 0:
                emitter.apply_force(gravity)
        """
        np = 0
        for p in self.__particle_pool:
            if not p.finished():
                np += 1
        return np

    def resize(self, new_size: int):
        if new_size is not None:
            if new_size > self.size:
                new_pool = ()
                tmpl = self.emitter_properties.particle
                if callable(tmpl):
                    new_pool = tuple(tmpl() for _ in range(new_size - self.size))
                else:
                    new_pool = tuple(
                        deepcopy(tmpl) for _ in range(new_size - self.size)
                    )
                for p in new_pool:
                    p.terminate()
                self.__particle_pool = self.__particle_pool + new_pool
            elif new_size < self.size:
                self.__particle_pool = self.__particle_pool[0:new_size]
                if self.current_idx >= new_size - 1:
                    self.current_idx = 0


class ParticleEmitter(base.PglBaseObject):
    def __init__(self, emitter_properties=None) -> None:
        super().__init__()
        if emitter_properties is None:
            emitter_properties = EmitterProperties()
        self.__pos_x = emitter_properties.column
        self.__pos_y = emitter_properties.row
        self.variance = emitter_properties.variance
        self.emit_number = emitter_properties.emit_number
        self.emit_rate = emitter_properties.emit_rate
        self.lifespan = emitter_properties.lifespan
        self.parent = emitter_properties.parent
        self.particle_velocity = emitter_properties.particle_velocity
        self.particle = emitter_properties.particle
        self.particle_lifespan = emitter_properties.particle_lifespan
        self.particle_acceleration = emitter_properties.particle_acceleration

        # if particle is not callable it is an instance of a particle. So we adjust its
        # values.
        if not callable(self.particle):
            if self.particle_velocity is not None:
                self.particle.velocity = self.particle_velocity
            self.particle.lifespan = self.particle_lifespan
            self.particle._initial_lifespan = self.particle_lifespan

        self.__particle_pool = ParticlePool(
            size=self.emit_number * self.particle_lifespan,
            emitter_properties=emitter_properties,
        )

        self.__last_emit = time.time()
        self.__active = True

    @property
    def particle_pool(self):
        # return self.__particles
        return self.__particle_pool

    @property
    def x(self):
        return self.__pos_x

    @x.setter
    def x(self, value: int):
        if type(value) is int:
            self.__pos_x = value

    @property
    def column(self):
        return self.__pos_x

    @column.setter
    def column(self, value: int):
        if type(value) is int:
            self.__pos_x = value

    @property
    def y(self):
        return self.__pos_y

    @y.setter
    def y(self, value: int):
        if type(value) is int:
            self.__pos_y = value

    @property
    def row(self):
        return self.__pos_y

    @row.setter
    def row(self, value: int):
        if type(value) is int:
            self.__pos_y = value

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, state: bool):
        if type(state) is bool:
            self.__active = state
        else:
            raise base.PglInvalidTypeException(
                "ParticleEmitter.active = state: state needs to be a boolean not a "
                f"{type(state)}."
            )

    def resize_pool(self, new_size: int = None):
        if new_size is None:
            # If no size is specified we only resize up. Never down.
            new_size = self.emit_number * self.particle_lifespan
            if self.__particle_pool.size < new_size:
                self.__particle_pool.resize(new_size)
        else:
            # if new_size is set, we consider that the programer knows what he is doing
            # and we let him set whatever size he wants.
            self.__particle_pool.resize(new_size)

    def toggle_active(self):
        self.__active = not self.__active

    def emit(self, amount: int = None):
        if (
            self.__active
            and (self.lifespan is not None and self.lifespan > 0)
            and time.time() - self.__last_emit >= self.emit_rate
        ):
            if amount is None:
                amount = self.emit_number
            # Poor attempt at optimization: test outside the loop.
            if callable(self.particle):
                for p in self.__particle_pool.get_particles(amount):
                    p.reset(
                        row=self.row,
                        column=self.column,
                        velocity=self.particle_velocity,
                        lifespan=self.particle_lifespan,
                    )
                    dv = random.uniform(-self.variance, self.variance)
                    p.velocity.row *= dv
                    p.velocity.column *= 2 * dv
            else:
                for p in self.__particle_pool.get_particles(amount):
                    p.reset(
                        row=self.row,
                        column=self.column,
                        velocity=base.Vector2D(
                            random.uniform(-1, 1), random.uniform(-2, 2)
                        ),
                        lifespan=self.particle_lifespan,
                    )
                    p.velocity *= random.uniform(-self.variance, self.variance)
            if self.lifespan is not None:
                self.lifespan -= 1
            self.__last_emit = time.time()

    def apply_force(self, force: base.Vector2D):
        for p in self.particle_pool.pool:
            p.apply_force(force)

    def update(self):
        particles = self.particle_pool

        for i in range(particles.size - 1, -1, -1):
            p = particles.pool[i]
            if not p.finished():
                p.apply_force(self.particle_acceleration)
                p.update()

    def finished(self):
        return self.lifespan <= 0 and self.particle_pool.count_active_particles() == 0

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        """Render all the particles of that emitter in the display buffer.

        This method is automatically called by :func:`pygamelib.engine.Screen.render`.

        :param buffer: A screen buffer to render the item into.
        :type buffer: numpy.array
        :param row: The row to render in.
        :type row: int
        :param column: The column to render in.
        :type column: int
        :param height: The total height of the display buffer.
        :type height: int
        :param width: The total width of the display buffer.
        :type width: int

        """
        # In real life the emitter will be associated to a BoardItem most of the time.
        # So, it needs to maintain a coherent screen coordinate.
        self.row = row
        self.column = column
        # g = engine.Game.instance()
        for p in self.particle_pool.pool:
            if (
                not p.finished()
                and p.row < buffer_height
                and p.column < buffer_width
                and p.row >= 0
                and p.column >= 0
            ):
                buffer[p.row][p.column] = p.render(buffer[p.row][p.column])
            else:
                p.terminate()


class CircleEmitter(ParticleEmitter):
    def __init__(
        self,
        emitter_properties: EmitterProperties = None,
    ) -> None:
        if emitter_properties is None:
            emitter_properties = EmitterProperties()
        super().__init__(emitter_properties)
        self.radius = emitter_properties.radius
        self.__last_emit = time.time()
        # self.__active = True

    def emit(self, amount: int = None):
        if (
            self.active
            and (self.lifespan is not None and self.lifespan > 0)
            and time.time() - self.__last_emit >= self.emit_rate
        ):
            if amount is None:
                amount = self.emit_number
            # Poor attempt at optimization: test outside the loop.
            if callable(self.particle):
                i = 0
                for p in self.particle_pool.get_particles(amount):
                    theta = 2.0 * math.pi * i / (amount - 1)
                    x = self.x + self.radius * 2 * math.cos(theta)
                    y = self.y + self.radius * math.sin(theta)
                    p.reset(
                        row=y,
                        column=x,
                        velocity=base.Vector2D(y - self.y, x - self.x),
                        lifespan=self.particle_lifespan,
                    )
                    i += 1
            else:
                i = 0
                for p in self.particle_pool.get_particles(amount):
                    theta = 2.0 * math.pi * i / (amount - 1)
                    # the 2 coefficient is to account for console's characters being
                    # twice higher than larger.
                    x = self.x + self.radius * 2 * math.cos(theta)
                    y = self.y + self.radius * math.sin(theta)
                    p.reset(
                        row=y,
                        column=x,
                        velocity=base.Vector2D(y - self.y, x - self.x),
                        lifespan=self.particle_lifespan,
                    )
                    if self.variance > 0.0:
                        p.velocity *= random.uniform(0.1, self.variance)
                    i += 1
            if self.lifespan is not None:
                self.lifespan -= 1
            self.__last_emit = time.time()
