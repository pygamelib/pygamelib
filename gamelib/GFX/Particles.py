from gamelib.GFX import Core
from gamelib.Movable import Movable
from gamelib.Assets import Graphics
from gamelib import Constants
import random
import uuid


class BaseParticle(Movable):
    def __init__(self, **kwargs):
        Movable.__init__(self, **kwargs)
        self.dimension = [1, 1]
        self.name = str(uuid.uuid4())
        self.type = "base_particle"
        self.sprixel = Core.Sprixel(Graphics.GeometricShapes.BULLET)
        if "bg_color" in kwargs:
            self.sprixel.bg_color = kwargs["bg_color"]
        if "fg_color" in kwargs:
            self.sprixel.fg_color = kwargs["fg_color"]
        if "model" in kwargs:
            self.sprixel.model = kwargs["model"]
        self.directions = [Constants.UP, Constants.DLUP, Constants.DRUP]
        self.ttl = 5
        for item in ["ttl", "sprixel", "name", "type", "directions"]:
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

    def size(self):
        """
        The size of a particle is the result of dimesion[0]*dimension[1].
        """
        return self.dimension[0] * self.dimension[1]
