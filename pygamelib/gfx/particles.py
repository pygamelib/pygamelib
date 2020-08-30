import pygamelib.gfx.core as gfx_core
import pygamelib.board_items as board_items
import pygamelib.assets.graphics as graphics
import pygamelib.constants as constants
import pygamelib.base as base

import random
import uuid


class BaseParticle(board_items.Movable):
    """
    Particles are not ready. This is only an early early test.
    *you should not use it*. If you do, don't complain. And if you really want to help,
    interact on Github or Discord.
    Thank you ;)
    """

    def __init__(self, **kwargs):
        board_items.Movable.__init__(self, **kwargs)
        self.size = [1, 1]
        self.name = str(uuid.uuid4())
        self.type = "base_particle"
        self.sprixel = gfx_core.Sprixel(graphics.GeometricShapes.BULLET)
        if "bg_color" in kwargs:
            self.sprixel.bg_color = kwargs["bg_color"]
        if "fg_color" in kwargs:
            self.sprixel.fg_color = kwargs["fg_color"]
        if "model" in kwargs:
            self.sprixel.model = kwargs["model"]
        self.directions = [
            base.Vector2D.from_direction(constants.UP, 1),
            base.Vector2D.from_direction(constants.DLUP, 1),
            base.Vector2D.from_direction(constants.DRUP, 1),
        ]
        self.lifespan = 5
        if "velocity" in kwargs and isinstance(kwargs["velocity"], base.Vector2D):
            self.velocity = kwargs["velocity"]
        else:
            self.velocity = base.Vector2D()
        if "acceleration" in kwargs and isinstance(
            kwargs["acceleration"], base.Vector2D
        ):
            self.acceleration = kwargs["acceleration"]
        else:
            self.acceleration = base.Vector2D()

        for item in ["lifespan", "sprixel", "name", "type", "directions"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])

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
