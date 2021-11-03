from copy import deepcopy
from pygamelib.gfx import core
import pygamelib.board_items as board_items
import pygamelib.assets.graphics as graphics
import pygamelib.constants as constants
import pygamelib.base as base

import time
import random
import uuid

__docformat__ = "restructuredtext"


class ParticleSprixel(core.Sprixel):
    def __init__(self, model="", bg_color=None, fg_color=None, is_bg_transparent=None):
        super().__init__(
            model=model,
            bg_color=bg_color,
            fg_color=fg_color,
            is_bg_transparent=is_bg_transparent,
        )


class Particle(base.PglBaseObject):
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        sprixel: ParticleSprixel = None,
    ) -> None:
        super().__init__()
        self.__pos_x = self._initial_column = column
        self.__pos_y = self._initial_row = row
        self.velocity = velocity
        # print(f"Particle constructor: self.velocity={self.velocity}")
        if self.velocity is None:
            self.velocity = base.Vector2D(random.uniform(-1, 1), random.uniform(-1, 1))
            # print(
            #     f"Particle constructor: created a velocity vector so self.velocity={self.velocity}"
            # )
        self.acceleration = base.Vector2D(0.0, 0.0)
        self.lifespan = lifespan
        if self.lifespan is None:
            self.lifespan = 20
        self._initial_lifespan = self.lifespan
        self.sprixel = sprixel
        if sprixel is None:
            self.sprixel = core.Sprixel(graphics.GeometricShapes.BULLET)

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

    def apply_force(self, force: base.Vector2D):
        if force is not None and isinstance(force, base.Vector2D):
            self.acceleration += force

    def update(self):
        # print(f"\tParticle.update() CURRENT position={self.row}x{self.column}")
        # print(
        #     f"\tParticle.update() CURRENT acceleration={self.acceleration} velocity={self.velocity}"
        # )
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
        self.row = int(self._initial_row + self.velocity.row)
        self.column = int(self._initial_column + self.velocity.column)

        #     print(f"\tivr: {self.velocity.row} - {int(self.velocity.row)} = {ivr}")
        #     print(
        #         f"\tivc: {self.velocity.column} - {int(self.velocity.column)} = {ivc}"
        #     )
        # print(f"\tParticle.update() NEW position={self.row}x{self.column}\n")
        self.acceleration *= 0
        self.lifespan -= 1

    def render(self, sprixel: core.Sprixel = None):
        return self.sprixel

    def finished(self):
        return self.lifespan <= 0

    def terminate(self):
        self.lifespan = -1


class PartitionParticle(Particle):
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        partition: list = None,
        partition_blending_table: list = None,
        sprixel: ParticleSprixel = None,
    ) -> None:
        super().__init__(
            row=row,
            column=column,
            velocity=velocity,
            lifespan=lifespan,
            sprixel=sprixel,
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
        # If you override this method, it's your responsibility to return a copy of
        # yourself (or just use super().render(sprixel) as it already returns a copy).
        if isinstance(sprixel, ParticleSprixel):
            # A particle has already been rendered here.
            # print(
            #     f"sprix='{self.sprixel}' param='{sprixel}' combi='{self.sprixel.model + sprixel.model}'"
            # )
            # print("self.partition_blending_table:")
            # print(self.partition_blending_table)

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
            # # TODO: DEV
            # return None
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
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        sprixel: ParticleSprixel = None,
        color: core.Color = None,
    ) -> None:
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
        elif sprixel is None and color is not None:
            self.sprixel.fg_color = core.Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        else:
            self.sprixel.fg_color = color


class RandomColorPartitionParticle(PartitionParticle):
    def __init__(
        self,
        row: int = 0,
        column: int = 0,
        velocity: base.Vector2D = None,
        lifespan: int = None,
        partition: list = None,
        partition_blending_table: list = None,
        sprixel: ParticleSprixel = None,
        color: core.Color = None,
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
        if sprixel is None and color is None:
            self.sprixel = ParticleSprixel(
                graphics.GeometricShapes.BULLET,
                fg_color=core.Color(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            )
        elif sprixel is None and color is not None:
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

    def update(self):
        super().update()
        lp = self.lifespan if self.lifespan >= 0 else 0
        self.sprixel.fg_color = self.start_color.blend(
            self.stop_color, 1 - (lp / self._initial_lifespan)
        )


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

    def update(self):
        super().update()
        lp = self.lifespan if self.lifespan >= 0 else 0
        self.sprixel.fg_color = self.start_color.blend(
            self.stop_color, 1 - (lp / self._initial_lifespan)
        )


class ParticleEmitter(base.PglBaseObject):
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
        particle=Particle,
        particle_lifespan=5,
    ) -> None:
        super().__init__()
        self.__pos_x = column
        self.__pos_y = row
        self.particles = list()
        self.variance = variance
        self.emit_number = emit_number
        self.emit_rate = emit_rate
        self.lifespan = lifespan
        self.parent = parent
        self.particle_velocity = particle_velocity
        self.particle = particle
        self.particle_lifespan = particle_lifespan
        self.particle_acceleration = particle_acceleration

        # if particle is not callable it is an instance of a particle. So we adjust its
        # values.
        if not callable(self.particle):
            if self.particle_velocity is not None:
                self.particle.velocity = self.particle_velocity
            self.particle.lifespan = self.particle_lifespan
            self.particle._initial_lifespan = self.particle_lifespan

        self.__last_emit = time.time()

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

    def emit(self, number_particle: int = None):
        if time.time() - self.__last_emit >= self.emit_rate:
            if number_particle is None:
                number_particle = self.emit_number
            # Poor attempt at optimization: test outside the loop.
            # dbg_idx = 0
            if callable(self.particle):
                for _ in range(number_particle):
                    self.particles.append(
                        self.particle(
                            row=self.row,
                            column=self.column,
                            velocity=self.particle_velocity,
                            lifespan=self.particle_lifespan,
                        )
                    )
                    # print(
                    #     f"\t{dbg_idx} Emitter.emit() particle INITIAL velocity: {self.particles[-1].velocity}"
                    # )
                    self.particles[-1].velocity *= random.uniform(
                        -self.variance, self.variance
                    )
                    # print(
                    #     f"\t{dbg_idx} Emitter.emit() particle VARIATED velocity: {self.particles[-1].velocity}"
                    # )
                    # dbg_idx += 1
            else:
                for _ in range(number_particle):
                    p = deepcopy(self.particle)
                    p.row = p._initial_row = self.row
                    p.column = p._initial_column = self.column
                    p.velocity = base.Vector2D(
                        random.uniform(-1, 1), random.uniform(-1, 1)
                    )
                    # print(
                    #     f"\t{dbg_idx} Emitter.emit() particle INITIAL velocity: {p.velocity}"
                    # )
                    p.velocity *= random.uniform(-self.variance, self.variance)
                    # print(
                    #     f"\t{dbg_idx} Emitter.emit() particle VARIATED velocity: {p.velocity}"
                    # )
                    self.particles.append(p)
                    # dbg_idx += 1
            t = time.time()
            if self.lifespan is not None:
                self.lifespan -= t - self.__last_emit
            self.__last_emit = t

    def apply_force(self, force: base.Vector2D):
        for p in self.particles:
            p.apply_force(force)

    def update(self):
        particles = self.particles
        # for p in particles:
        #     p.apply_force(self.particle_acceleration)
        #     p.update()

        for i in range(len(particles) - 1, -1, -1):
            p = particles[i]
            p.apply_force(self.particle_acceleration)
            p.update()
            if p.finished():
                del particles[i]

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
        for p in self.particles:
            if (
                p.row < buffer_height
                and p.column < buffer_width
                and p.row >= 0
                and p.column >= 0
            ):
                buffer[p.row][p.column] = p.render(buffer[p.row][p.column])
            else:
                p.terminate()

        # # Attempt at optimization.
        # null_sprixel = Sprixel()
        # get_sprixel = self.sprixel
        # for sr in range(row, min(self.size[1] + row, buffer_height)):
        #     for sc in range(column, min(self.size[0] + column, buffer_width)):
        #         sprix = get_sprixel(sr - row, sc - column)
        #         # Need to check the empty/null sprixel in the sprite
        #         # because for the sprite we just skip and leave the
        #         # sprixel that is behind but when it comes to screen we
        #         # cannot leave a blank cell.
        #         if sprix == null_sprixel:
        #             continue
        #         # TODO: If the Sprite has sprixels with length > 1 this
        #         # is going to be a mess.
        #         buffer[sr][sc] = sprix.__repr__()
        #         for c in range(sc + 1, sc + sprix.length):
        #             buffer[sr][c] = Sprixel()


# NOTE: OUTDATED DO NOT USE!!!
class BaseParticle(board_items.Movable):
    """
    Particles are not ready. This is only an early early test.
    *you should not use it*. If you do, don't complain. And if you really want to help,
    interact on Github or Discord.
    Thank you ;)
    """

    def __init__(
        self,
        model=None,
        bg_color=None,
        fg_color=None,
        acceleration=None,
        velocity=None,
        lifespan=None,
        directions=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # NOTE: this cannot be done anymore for BoardItems
        # self.size = [1, 1]
        self.name = str(uuid.uuid4())
        self.type = "base_particle"
        self.sprixel = core.Sprixel(graphics.GeometricShapes.BULLET)
        if bg_color is not None and isinstance(bg_color, core.Color):
            self.sprixel.bg_color = bg_color
        if fg_color is not None and isinstance(fg_color, core.Color):
            self.sprixel.fg_color = fg_color
        if model is not None:
            self.sprixel.model = model
        self.directions = [
            base.Vector2D.from_direction(constants.UP, 1),
            base.Vector2D.from_direction(constants.DLUP, 1),
            base.Vector2D.from_direction(constants.DRUP, 1),
        ]
        self.lifespan = 5
        if velocity is not None and isinstance(velocity, base.Vector2D):
            self.velocity = velocity
        else:
            self.velocity = base.Vector2D()
        if acceleration is not None and isinstance(acceleration, base.Vector2D):
            self.acceleration = acceleration
        else:
            self.acceleration = base.Vector2D()
        if lifespan is not None:
            self.lifespan = lifespan
        if directions is not None and type(directions) is list:
            self.directions = directions
        # for item in ["lifespan", "sprixel", "name", "type", "directions"]:
        #     if item in kwargs:
        #         setattr(self, item, kwargs[item])

    def direction(self):
        return random.choice(self.directions)

    def pickable(self):
        """
        A particle is not pickable by default. So that method returns False.
        """
        return False

    def overlappable(self):
        """
        Overlapable always return true. As by definition a particle is overlapable.
        """
        return True
