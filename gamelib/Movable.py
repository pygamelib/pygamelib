"""This module contains the Movable class.
It can potentially hold more movement related classes.

.. autosummary::
   :toctree: .

   Movable
   Projectile
"""

from gamelib.BoardItem import BoardItem
from gamelib.HacExceptions import HacInvalidTypeException, HacException
from gamelib.Animation import Animation
from gamelib.Actuators.SimpleActuators import UnidirectionalActuator
import gamelib.Constants as Constants


class Movable(BoardItem):
    """A class representing BoardItem capable of movements.

    Movable subclasses :class:`BoardItem`.

    :param step: the amount of cell a movable can cross in one turn.
    :type step: int

    This class derive BoardItem and describe an object that can move or be
    moved (like a player or NPC).
    Thus this class implements BoardItem.can_move().
    However it does not implement BoardItem.pickable() or
    BoardItem.overlappable()

    This class contains a private member called _overlapping.
    This private member is used to store the reference to an overlappable
    object while a movable occupy its position. The Board then restore the
    overlapped object. You should let the Board class take care of that.
    """

    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        if "step" not in kwargs.keys():
            self.step = 1
        else:
            self.step = kwargs["step"]
        self._overlapping = None
        self._overlapping_buffer = None

    def can_move(self):
        """
        Movable implements can_move().

        :return: True
        :rtype: Boolean
        """
        return True

    def has_inventory(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a Movable to have an inventory.
        """
        raise NotImplementedError()


class Projectile(Movable):
    """A class representing a projectile type board item.
    That class can be sub-classed to represent all your needs (fireballs,
    blasters shots, etc.).

    That class support the 2 types of representations: model and animations.
    The animation cases are slightly more evolved than the regular item.animation.
    It does use the item.animation but with more finesse as a projectile can travel in
    many directions. So it also keeps track of models and animation per travel
    direction.

    You probably want to subclass Projectile. It is totally ok to use it as it, but it
    is easier to create a subclass that contains all your Projectile information and let
    the game engine deal with orientation, range keeping, etc.
    Please see examples/07_projectiles.py for a good old fireball example.

    By default, Projectile travels in straight line in one direction. This behavior can
    be overwritten by setting a specific actuator (a projectile is a
    :class:`~gamelib.Movable.Movable` so you can use my_projectile.actuator).

    The general way to use it is as follow:

    - Create a factory object with your static content (usually the static models,
      default direction and hit callback)
    - Add the direction related models and/or animation (keep in mind that animation
      takes precedence over static models)
    - deep copy that object when needed and add it to the projectiles stack of the game
      object.
    - use Game.actuate_projectiles(level) to let the Game engine do the heavy lifting.

    The Projectile constructor takes the following parameters:

    :param direction: A direction from the :ref:`constants-module` module
    :type direction: int
    :param range: The maximum range of the projectile in number of cells that can be
        crossed. When range is attained the hit_callback is called with a BoardItemVoid
        as a collision object.
    :type range: int
    :param step: the amount of cells a projectile can cross in one turn
    :type step: int
    :param model: the default model of the projectile.
    :type model: str
    :param movement_animation: the default animation of a projectile. If a projectile is
        sent in a direction that has no explicit and specific animation, then
        movement_animation is used if defined.
    :type movement_animation: :class:`~gamelib.Animation.Animation`
    :param hit_animation: the animation used when the projectile collide with something.
    :type hit_animation: :class:`~gamelib.Animation.Animation`
    :param hit_model: the model used when the projectile collide with something.
    :type hit_model: str
    :param hit_callback: A reference to a function that will be called upon collision.
        The hit_callback is receiving the object it collides with as first parameter.
    :type hit_callback: function
    :param is_aoe: Is this an 'area of effect' type of projectile? Meaning, is it doing
        something to everything around (mass heal, exploding rocket, fireball, etc.)?
        If yes, you must set that parameter to True and set the aoe_radius. If not, the
        Game object will only send the colliding object in front of the projectile.
    :type is_aoe: bool
    :param aoe_radius: the radius of the projectile area of effect. This will force the
        Game object to send a list of all objects in that radius.
    :type aoe_radius: int
    :param args: extra parameters to pass to hit_callback.
    :param parent: The parent object (usually a Board object or some sort of BoardItem).

    .. important:: The effects of a Projectile are determined by the callback. No
        callback == no effect!

    Example::

        fireball = Projectile(
                                name="fireball",
                                model=Utils.red_bright(black_circle),
                                hit_model=Sprites.EXPLOSION,
                            )
        fireball.set_direction(Constants.RIGHT)
        my_game.add_projectile(1, fireball,
                               my_game.player.pos[0], my_game.player.pos[1] + 1)


    """

    def __init__(
        self,
        name="projectile",
        direction=Constants.RIGHT,
        step=1,
        range=5,
        model="\U00002301",
        movement_animation=None,
        hit_animation=None,
        hit_model=None,
        hit_callback=None,
        is_aoe=False,
        aoe_radius=0,
        parent=None,
        *args
    ):
        if range % step != 0:
            raise HacException(
                "incorrect_range_step",
                "range must be a factor of step" " in Projectile",
            )
        Movable.__init__(self, model=model, step=step, name=name, parent=parent)
        self.direction = direction
        self.range = range
        self.movement_animation = movement_animation
        self._directional_animations = {}
        self._directional_models = {}
        self.hit_animation = hit_animation
        self.hit_model = hit_model
        self.hit_callback = hit_callback
        self.callback_parameters = args
        self.actuator = UnidirectionalActuator(direction=direction)
        self.is_aoe = is_aoe
        self.aoe_radius = aoe_radius
        self.parent = parent

    def add_directional_animation(self, direction, animation):
        """Add an animation for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int
        :param animation: The animation for the direction
        :type animation: :class:`~gamelib.Animation.Animation`

        Example::

            fireball.add_directional_animation(Constants.UP, updward_animation)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the Constants module as"
                "direction."
            )
        if not isinstance(animation, Animation):
            raise HacInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires a gamelib.Animation.Animation as "
                "animation"
            )
        self._directional_animations[direction] = animation

    def directional_animation(self, direction):
        """Return the animation for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int
        :rtype: :class:`~gamelib.Animation.Animation`

        Example::

            # No more animation for the UP direction
            fireball.directional_animation(Constants.UP)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the Constants module as"
                "direction."
            )
        if direction in self._directional_animations:
            return self._directional_animations[direction]
        elif self.movement_animation is not None:
            return self.movement_animation
        else:
            return self.animation

    def remove_directional_animation(self, direction):
        """Remove an animation for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int

        Example::

            # No more animation for the UP direction
            fireball.remove_directional_animation(Constants.UP)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the Constants module as"
                "direction."
            )
        del self._directional_animations[direction]

    def add_directional_model(self, direction, model):
        """Add an model for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int
        :param model: The model for the direction
        :type model: str

        Example::

            fireball.add_directional_animation(Constants.UP, updward_animation)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the Constants module as"
                "direction."
            )
        if type(model) is not str:
            raise HacInvalidTypeException(
                "Projectile.add_directional_model " "requires a string as model."
            )
        self._directional_models[direction] = model

    def directional_model(self, direction):
        """Return the model for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int
        :rtype: str

        Example::

            fireball.directional_model(Constants.UP)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the Constants module as"
                "direction."
            )
        if direction in self._directional_models:
            return self._directional_models[direction]
        else:
            return self.model

    def remove_directional_model(self, direction):
        """Remove the model for a specific direction.

        :param direction: A direction from the Constants module.
        :type direction: int

        Example::

            fireball.directional_model(Constants.UP)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the Constants module as"
                "direction."
            )
        del self._directional_models[direction]

    def set_direction(self, direction):
        """Set the direction of a projectile

        This method will set a UnidirectionalActuator with the direction.
        It will also take care of updating the model and animation for the given
        direction if they are specified.

        :param direction: A direction from the Constants module.
        :type direction: int

        Example::

            fireball.set_direction(Constants.UP)
        """
        if type(direction) is not int:
            raise HacInvalidTypeException(
                "Projectile.set_direction "
                "requires an int from the Constants module as"
                "direction."
            )
        self.model = self.directional_model(direction)
        self.animation = self.directional_animation(direction)
        self.direction = direction
        self.actuator = UnidirectionalActuator(direction=direction)

    def hit(self, objects):
        """A method that is called when the projectile hit something.

        That method is automatically called by the Game object when the Projectile
        collide with another object or is at the end of its range.

        Here are the call cases covered by the Game object:

         - range is reached without collision and projectile IS NOT an AoE type: hit()
           is called with a single BoardItemVoid in the objects list.
         - range is reached without collision and projectile IS an AoE type: hit()
           is called with the list of all objects within aoe_radius (including
           structures).
         - projectile collide with something and IS NOT an AoE type: hit() is called
           with the single colliding object in the objects list.
         - projectile collide with something and IS an AoE type: hit() is called with
           the list of all objects within aoe_radius (including structures).

        In turn, that method calls the hit_callback with the following parameters (in
        that order):

         1. the projectile object
         2. the list of colliding objects (that may contain only one object)
         3. the callback parameters (from the constructor callback_parameters)

        :param objects: A list of objects hit by or around the projectile.
        :type name: list

        Example::

            my_projectile.hit([npc1])

        """
        if self.hit_model is not None:
            self.model = self.hit_model
        if self.hit_animation is not None:
            self.animation = self.hit_animation
            self.animation.play_all()
        else:
            if self.animation is not None:
                self.animation.stop()
                self.animation = None
        self.actuator.stop()
        if self.hit_callback is not None:
            self.hit_callback(self, objects, self.callback_parameters)

    def has_inventory(self):
        """
        Projectile cannot have inventory by default.

        :return: False
        :rtype: Boolean
        """
        return False

    def overlappable(self):
        """
        Projectile are overlappable by default.

        :return: True
        :rtype: Boolean
        """
        return True

    def restorable(self):
        """
        We assume that by default, Projectiles are restorable.

        :return: True
        :rtype: bool
        """
