from pygamelib.gfx import core
import pygamelib.board_items as board_items
import pygamelib.assets.graphics as graphics
import pygamelib.constants as constants
import pygamelib.base as base

import random
import uuid

__docformat__ = "restructuredtext"


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
        **kwargs
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
