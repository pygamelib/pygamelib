"""This module contains the basic board items classes.

.. autosummary::
   :toctree: .

   BoardItem
   BoardItemVoid
   BoardComplexItem
   BoardItemComplexComponent
   Movable
   Projectile
   Immovable
   Actionable
   Character
   Player
   ComplexPlayer
   NPC
   ComplexNPC
   TextItem
   Wall
   ComplexWall
   Treasure
   ComplexTreasure
   Door
   ComplexDoor
   GenericStructure
   GenericActionableStructure
   Tile
"""
from pygamelib import engine
from pygamelib import base
from pygamelib import constants
from pygamelib.gfx import core
from pygamelib import actuators


class BoardItem:
    """
    Base class for any item that will be placed on a Board.

    :param type: A type you want to give your item. It can be any string. You can then
        use the type for sorting or grouping for example.
    :type type: str
    :param name: A name for this item. For identification purpose.
    :type name: str
    :param pos: the position of this item. When the item is managed by the Board and
        Game engine this member hold the last updated position of the item. It is not
        updated if you manually move the item. It must be an array of
        2 integers [row,column]
    :type pos: array
    :param model: The model to use to display this item on the Board. Be mindful of the
        space it will require. Default value is '*'.
    :type model: str
    :param parent: The parent object of the board item. Usually a Board or Game object.

    .. important:: Starting with version 1.2.0 and introduction of complex items,
       BoardItems have a size. That size **CANNOT** be set. It is always 1x1.
       This is because a BoardItem always takes 1 cell, regardless of its actual number
       of characters. Python does not really provide a way to prevent changing that
       member but if you do, you'll break rendering. You have been warned.
    """

    def __init__(self, **kwargs):
        self.name = "Board item"
        self.type = "item"
        self.pos = [None, None]
        self.model = "*"
        self.animation = None
        self.parent = None
        self.sprixel = None
        self.size = [1, 1]
        # Setting class parameters
        for item in ["name", "type", "pos", "model", "parent", "sprixel"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])

    def __str__(self):
        if self.sprixel is not None:
            return self.sprixel.__repr__()
        else:
            return self.model

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def display(self):
        """
        Print the model WITHOUT carriage return.
        """
        print(self.model, end="")

    def debug_info(self):
        """
        Return a string with the list of the attributes and their current value.

        :rtype: str
        """
        string = "attrs: \n"
        for key in vars(self):
            if type(getattr(self, key)) is list:
                string += (
                    f"'{key}' = '"
                    + "".join(str(e) + " " for e in getattr(self, key))
                    + "'\n"
                )
            else:
                string += f"'{key}' = '{getattr(self, key)}'\n"
        return string

    def store_position(self, row, column):
        """Store the BoardItem position for self access.

        The stored position is used for consistency and quick access to the self
        postion. It is a redundant information and might not be synchronized.

        :param row: the row of the item in the :class:`~pygamelib.engine.Board`.
        :type row: int
        :param column: the column of the item in the :class:`~pygamelib.engine.Board`.
        :type column: int

        Example::

            item.store_position(3,4)
        """
        self.pos = [row, column]

    def position_as_vector(self):
        """Returns the current item position as a Vector2D

        :returns: The position as a 2D vector
        :rtype: :class:`~pygamelib.base.Vector2D`

        Example::

            gravity = Vector2D(9.81, 0)
            next_position = item.position_as_vector() + gravity.unit()
        """
        return base.Vector2D(self.pos[0], self.pos[1])

    @property
    def row(self):
        """Convenience method to get the current stored row of the item.

        This is absolutely equivalent to access to item.pos[0].

        :return: The row coordinate
        :rtype: int

        Example::

            if item.row != item.pos[0]:
                print('Something extremely unlikely just happened...')
        """
        return self.pos[0]

    @property
    def column(self):
        """Convenience method to get the current stored column of the item.

        This is absolutely equivalent to access to item.pos[1].

        :return: The column coordinate
        :rtype: int

        Example::

            if item.column != item.pos[1]:
                print('Something extremely unlikely just happened...')
        """
        return self.pos[1]

    @property
    def width(self):
        """Convenience method to get the width of the item.

        This is absolutely equivalent to access to item.size[0].

        :return: The width
        :rtype: int

        Example::

            if item.width > board.width:
                print('The item is too big for the board.')
        """
        return self.size[0]

    @property
    def height(self):
        """Convenience method to get the height of the item.

        This is absolutely equivalent to access to item.size[1].

        :return: The height
        :rtype: int

        Example::

            if item.height > board.height:
                print('The item is too big for the board.')
        """
        return self.size[1]

    def collides_with(self, other):
        """Tells if this item collides with another item.

        :param other: The item you want to check for collision.
        :type other: :class:`~pygamelib.board_items.BoardItem`
        :rtype: bool

        Example::

            if projectile.collides_with(game.player):
                game.player.hp -= 5
        """
        if isinstance(other, BoardItem):
            return base.Math.intersect(
                self.pos[0],
                self.pos[1],
                self.size[0],
                self.size[1],
                other.pos[0],
                other.pos[1],
                other.size[0],
                other.size[1],
            )
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.collides_with require a BoardItem as parameter."
            )

    def distance_to(self, other):
        """Calculates the distance with an item.

        :param other: The item you want to calculate the distance to.
        :type other: :class:`~pygamelib.board_items.BoardItem`
        :return: The distance between this item and the other.
        :rtype: float

        Example::

            if npc.distance_to(game.player) <= 2.0:
                npc.seek_and_destroy = True
        """
        if isinstance(other, BoardItem):
            return base.Math.distance(
                self.pos[0], self.pos[1], other.pos[0], other.pos[1],
            )
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.distance_to require a BoardItem as parameter."
            )

    def can_move(self):
        """
        This is a virtual method that must be implemented in deriving classes.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be moved by the Board.
        """
        raise NotImplementedError()

    def pickable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be pick-up by player or NPC.
        """
        raise NotImplementedError()

    def overlappable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a BoardItem to be overlapped by another
        BoardItem.
        """
        raise NotImplementedError()

    def inventory_space(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return an integer.
        This represent the size of the BoardItem for the
        :class:`~pygamelib.engine.Inventory`. It is used for example to evaluate
        the space taken in the inventory.

        .. important:: That abstract function was called size() before version 1.2.0.
           As it was exclusively used for inventory space management, it as been
           renamed. Particularly because now items do have a need for a size.
        """
        raise NotImplementedError()


class BoardItemVoid(BoardItem):
    """
    A class that represent a void cell.
    """

    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        self.name = "void_cell"

    def pickable(self):
        """
        A BoardItemVoid is not pickable, therefor this method return false.

        :return: False
        """
        return False

    def overlappable(self):
        """
        A BoardItemVoid is obviously overlappable (so player and NPC can walk over).

        :return: True
        """
        return True


class BoardItemComplexComponent(BoardItem):
    """The default component of a complex item.

    It is literrally just a BoardItem but is subclassed for easier identification.

    It is however scanning its parent for the item's basic properties (overlappable,
    restorable, etc.)

    A component can never be pickable by itself.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, "parent") and self.parent is not None:
            if hasattr(self.parent, "restorable") and callable(self.parent.restorable):
                self.__is_restorable = self.parent.restorable()
            else:
                self.__is_restorable = False
            if hasattr(self.parent, "overlappable") and callable(
                self.parent.overlappable
            ):
                self.__is_overlappable = self.parent.overlappable()
            else:
                self.__is_overlappable = False
            if hasattr(self.parent, "can_move") and callable(self.parent.can_move):
                self.__can_move = self.parent.can_move()
            else:
                self.__can_move = False
        else:
            self.__is_restorable = False
            self.__is_overlappable = False
            self.__can_move = False
        self.__is_pickable = False

    def restorable(self):
        """
        Returns True if the item is restorable, False otherwise.

        Example::

            if item.item(4,5).restorable():
                print('The item is restorable')
        """
        return self.__is_restorable

    def overlappable(self):
        """
        Returns True if the item is overlappable, False otherwise.

        Example::

            if item.item(4,5).overlappable():
                print('The item is overlappable')
        """
        return self.__is_overlappable

    def can_move(self):
        """
        Returns True if the item can move, False otherwise.

        Example::

            if item.item(4,5).can_move():
                print('The item can move')
        """
        return self.__can_move

    def pickable(self):
        """
        Returns True if the item is pickable, False otherwise.

        Example::

            if item.item(4,5).pickable():
                print('The item is pickable')
        """
        return self.__is_pickable


class BoardComplexItem(BoardItem):
    """
    .. versionadded:: 1.2.0

    A BoardComplexItem is the base item for multi cells elements. It inherits from
    :class:`BoardItem` and accepts all its parameters.

    The main difference is that a complex item can use
    :class:`~pygamelib.gfx.core.Sprite` as representation.

    You can see a complex item as a collection of other items that are ruled by the
    same laws. They behave as one but a complex item is actually made of complex
    components. At first it is not important but you may want to exploit that as a
    feature for your game.

    On top of :class:`BoardItem` the constructor accepts the following parameters:

    :param sprite: A sprite representing the item.
    :type sprite: :class:`~pygamelib.gfx.core.Sprite`
    :param size: The size of the item. It impact movement and collision detection
        amongst other things. If it is left empty the Sprite size is used. If no sprite
        is given to the constructor the default size is 2x2.
    :type size: array[int]
    :null_sprixel: The null_sprixel is a bit of a special parameter: during construction
        a null sprixel is replaced by a BoardItemVoid. This is a trick to show the
        background (i.e transparency). A sprixel can take the color of the background
        but a complex item with a null_sprixel that correspond to transparent zone of a
        sprite will really be transparent and show the background.
    :null_sprixel: :class:`~pygamelib.gfx.core.Sprixel`
    :param base_item_type: the building block of the complex item. The complex item is
        built from a 2D array of base items.
    :type base_item_type: :class:`BoardItemComplexComponent`

    """

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.name = "Board Multi Item"
        self.type = "multi_item"
        super().__init__(**kwargs)
        self.sprite = core.Sprite()
        self.null_sprixel = None
        self.size = None
        self._item_matrix = []
        # Not sure about that one
        self.hit_box = []
        self.base_item_type = BoardItemComplexComponent
        for item in ["sprite", "size", "null_sprixel", "base_item_type"]:
            if item in kwargs:
                setattr(self, item, kwargs[item])
        if self.size is None:
            self.size = self.sprite.size
        if isinstance(self.sprite, core.Sprite) and self.sprite.parent is None:
            self.sprite.parent = self
        self.update_sprite()

    def __repr__(self):  # pragma: no cover
        return self.sprite.__repr__()

    def __str__(self):  # pragma: no cover
        return self.sprite.__str__()

    def update_sprite(self):
        """
        Update the complex item with the current sprite.
        This method needs to be called everytime the sprite is changed.

        Example::

            item = BoardComplexItem(sprite=position_idle)
            for s in [walk_1, walk_2, walk_3, walk_4]:
                item.sprite = s
                item.update_sprite()
                board.move(item, constants.RIGHT, 1)
                time.sleep(0.2)
        """
        self._item_matrix = []
        # Update sprite size.
        self.sprite.calculate_size()
        for row in range(0, self.sprite.size[1]):
            self._item_matrix.append([])
            for col in range(0, self.sprite.size[0]):
                if (
                    self.null_sprixel is not None
                    and self.sprite.sprixel(row, col) == self.null_sprixel
                ):
                    self._item_matrix[row].append(BoardItemVoid())
                else:
                    self._item_matrix[row].append(self.base_item_type(**self.__kwargs))
                    self._item_matrix[row][col].name = f"{self.name}_{row}_{col}"
                    self._item_matrix[row][col].model = self.sprite.sprixel(
                        row, col
                    ).model
                    self._item_matrix[row][col].sprixel = self.sprite.sprixel(row, col)
                    self._item_matrix[row][col].parent = self
        self.size = self.sprite.size

    def item(self, row, column):
        """
        Return the item at the row, column position if it is within the item's
        boundaries.

        :rtype: pygamelib.board_items.BoardItem

        :raise PglOutOfBoardBoundException: if row or column are
            out of bound.
        """
        if row < self.size[1] and column < self.size[0]:
            return self._item_matrix[row][column]
        else:
            raise base.PglOutOfItemBoundException(
                (
                    f"There is no item at coordinates [{row},{column}] "
                    "because it's out of the board multi item boundaries "
                    f"({self.size[0]}x{self.size[1]})."
                )
            )


class Movable(BoardItem):
    """A class representing BoardItem capable of movements.

    Movable subclasses :class:`BoardItem`.

    :param step: the amount of cell a movable can cross in one turn. Default value: 1.
    :type step: int
    :param step_vertical: the amount of cell a movable can vertically cross in one turn.
       Default value: step value.
    :type step_vertical: int
    :param step_horizontal: the amount of cell a movable can horizontally cross in one
       turn. Default value: step value.
    :type step_horizontal: int
    :param movement_speed: The time (in seconds) between 2 movements of a Movable. It is
       used by all the Game's actuation methods to enforce move speed of NPC and
       projectiles.
    :type movement_speed: int|float

    The movement_speed parameter is only used when the Game is configured with MODE_RT.
    Additionally the dtmove property is used to accumulate time between frames. It is
    entirely managed by the Game object and most of the time you shouldn't mess up with
    it. Unless you want to manage movements by yourself. If so, have fun! That's the
    point of the pygamelib to let you do whatever you like.

    This class derive BoardItem and describe an object that can move or be
    moved (like a player or NPC).
    Thus this class implements BoardItem.can_move().
    However it does not implement BoardItem.pickable() or
    BoardItem.overlappable()
    """

    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        # We probably need the item to store its own velocity at some point
        # self.velocity = base.Vector2d(0,0)
        # Set default values
        for s in ["step", "step_vertical", "step_horizontal"]:
            if s not in kwargs.keys():
                # self.step = 1
                self.__setattr__(s, 1)
            else:
                # self.step = kwargs["step"]
                self.__setattr__(s, kwargs[s])
        # TODO: That's initial thought for physic i the pygamelib. For future reference.
        # if "velocity" in kwargs.keys():
        #     self.velocity = kwargs["velocity"]
        # else:
        #     self.velocity = base.Vector2D()
        # if "ignore_physic" in kwargs.keys():
        #     self.ignore_physic = kwargs["ignore_physic"]
        # else:
        #     self.ignore_physic = False
        # Now if only step is set and it's not 1, set the correct value for the 2 others
        if "step_vertical" not in kwargs.keys() and self.step != 1:
            self.step_vertical = self.step

        if "step_horizontal" not in kwargs.keys() and self.step != 1:
            self.step_horizontal = self.step
        if "movement_speed" not in kwargs.keys():
            self.movement_speed = 1.0
        else:
            self.movement_speed = kwargs["movement_speed"]
        self.__dtmove = 0.0
        self.__can_move = True

    @property
    def dtmove(self):
        return self.__dtmove

    @dtmove.setter
    def dtmove(self, value):
        if type(value) is float or type(value) is int:
            self.__dtmove = value
        else:
            raise base.PglInvalidTypeException(
                "Movable.dtmove(value): value needs to be an int or float."
            )

    def can_move(self):
        """
        Movable implements can_move().

        :return: True
        :rtype: Boolean
        """
        return self.__can_move

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
    :class:`~pygamelib.board_items.Movable` so you can use my_projectile.actuator).

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
    :type movement_animation: :class:`~pygamelib.gfx.core.Animation`
    :param hit_animation: the animation used when the projectile collide with something.
    :type hit_animation: :class:`~pygamelib.gfx.core.Animation`
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
    :param callback_parameters: A list of parameters to pass to hit_callback.
    :type callback_parameters: list
    :param movement_speed: The movement speed of the projectile
    :type movement_speed: int|float
    :param parent: The parent object (usually a Board object or some sort of BoardItem).

    .. important:: The effects of a Projectile are determined by the callback. No
        callback == no effect!

    Example::

        fireball = Projectile(
                                name="fireball",
                                model=Utils.red_bright(black_circle),
                                hit_model=Sprites.EXPLOSION,
                            )
        fireball.set_direction(constants.RIGHT)
        my_game.add_projectile(1, fireball,
                               my_game.player.pos[0], my_game.player.pos[1] + 1)


    """

    def __init__(
        self,
        name="projectile",
        direction=constants.RIGHT,
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
        callback_parameters=[],
        movement_speed=0.15,
    ):
        if range % step != 0:
            raise base.PglException(
                "incorrect_range_step",
                "range must be a factor of step" " in Projectile",
            )
        Movable.__init__(
            self,
            model=model,
            step=step,
            name=name,
            parent=parent,
            movement_speed=movement_speed,
        )
        self.direction = direction
        self.range = range
        self.movement_animation = movement_animation
        self._directional_animations = {}
        self._directional_models = {}
        self.hit_animation = hit_animation
        self.hit_model = hit_model
        self.hit_callback = hit_callback
        self.callback_parameters = callback_parameters
        self.actuator = actuators.UnidirectionalActuator(direction=direction)
        self.is_aoe = is_aoe
        self.aoe_radius = aoe_radius
        self.parent = parent

    def add_directional_animation(self, direction, animation):
        """Add an animation for a specific direction.

        :param direction: A direction from the constants module.
        :type direction: int
        :param animation: The animation for the direction
        :type animation: :class:`~pygamelib.gfx.core.Animation`

        Example::

            fireball.add_directional_animation(constants.UP, constants.UP, animation)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the constants module as"
                "direction."
            )
        if not isinstance(animation, core.Animation):
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires a pygamelib.gfx.core.Animation as "
                "animation"
            )
        self._directional_animations[direction] = animation

    def directional_animation(self, direction):
        """Return the animation for a specific direction.

        :param direction: A direction from the constants module.
        :type direction: int
        :rtype: :class:`~pygamelib.gfx.core.Animation`

        Example::

            # No more animation for the UP direction
            fireball.directional_animation(constants.UP)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the constants module as"
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

        :param direction: A direction from the constants module.
        :type direction: int

        Example::

            # No more animation for the UP direction
            fireball.remove_directional_animation(constants.UP)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_animation "
                "requires an int from the constants module as"
                "direction."
            )
        del self._directional_animations[direction]

    def add_directional_model(self, direction, model):
        """Add an model for a specific direction.

        :param direction: A direction from the constants module.
        :type direction: int
        :param model: The model for the direction
        :type model: str

        Example::

            fireball.add_directional_animation(constants.UP, updward_animation)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the constants module as"
                "direction."
            )
        if type(model) is not str:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_model " "requires a string as model."
            )
        self._directional_models[direction] = model

    def directional_model(self, direction):
        """Return the model for a specific direction.

        :param direction: A direction from the constants module.
        :type direction: int
        :rtype: str

        Example::

            fireball.directional_model(constants.UP)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the constants module as"
                "direction."
            )
        if direction in self._directional_models:
            return self._directional_models[direction]
        else:
            return self.model

    def remove_directional_model(self, direction):
        """Remove the model for a specific direction.

        :param direction: A direction from the constants module.
        :type direction: int

        Example::

            fireball.directional_model(constants.UP)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.add_directional_model "
                "requires an int from the constants module as"
                "direction."
            )
        del self._directional_models[direction]

    def set_direction(self, direction):
        """Set the direction of a projectile

        This method will set a UnidirectionalActuator with the direction.
        It will also take care of updating the model and animation for the given
        direction if they are specified.

        :param direction: A direction from the constants module.
        :type direction: int

        Example::

            fireball.set_direction(constants.UP)
        """
        if type(direction) is not int:
            raise base.PglInvalidTypeException(
                "Projectile.set_direction "
                "requires an int from the constants module as"
                "direction."
            )
        self.model = self.directional_model(direction)
        self.animation = self.directional_animation(direction)
        self.direction = direction
        self.actuator = actuators.UnidirectionalActuator(direction=direction)

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
        return True


class Immovable(BoardItem):
    """
    This class derive BoardItem and describe an object that cannot move or be
    moved (like a wall). Thus this class implements BoardItem.can_move().
    However it does not implement BoardItem.pickable() or
    BoardItem.overlappable()
    """

    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        if "inventory_space" not in kwargs.keys():
            self._inventory_space = 0
        else:
            self._inventory_space = kwargs["inventory_space"]

    def can_move(self):
        """ Return the capability of moving of an item.

        Obviously an Immovable item is not capable of moving. So that method
        always returns False.

        :return: False
        :rtype: bool
        """
        return False

    def inventory_space(self):
        """Return the size of the Immovable Item for the
        :class:`~pygamelib.engine.Inventory`.

        :return: The size of the item.
        :rtype: int
        """
        return self._inventory_space

    def restorable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for an Immovable BoardItem to be restored
        by the board if the item is overlappable and has been overlapped by
        another Movable (:class:`~pygamelib.board_items.Movable`) item.
        """
        raise NotImplementedError()


class Actionable(Immovable):
    """
    This class derives :class:`~pygamelib.board_items.Immovable`. It adds the
    ability to an Immovable BoardItem to be triggered and execute some code.

    :param action: the reference to a function (Attention: no parentheses at
        the end of the function name).
    :type action: function
    :param action_parameters: the parameters to the action function.
    :type action_parameters: list
    :param perm: The permission that defines what types of items can actually
        activate the actionable. The permission has to be one of the
        permissions defined in :mod:`~pygamelib.constants`
    :type perm: :mod:`~pygamelib.constants`

    On top of these parameters Actionable accepts all parameters from
    :class:`~pygamelib.board_items.Immovable` and therefor from
    :class:`~pygamelib.board_items.BoardItem`.

    .. note:: The common way to use this class is to use
        GenericActionableStructure. Please refer to
        :class:`~pygamelib.board_items.GenericActionableStructure`
        for more details.
    """

    def __init__(self, **kwargs):
        if "action" not in kwargs.keys():
            self.action = None
        else:
            self.action = kwargs["action"]
        if "action_parameters" not in kwargs.keys():
            kwargs["action_parameters"] = []
        else:
            self.action_parameters = kwargs["action_parameters"]
        if "perm" not in kwargs.keys():
            self.perm = constants.PLAYER_AUTHORIZED
        else:
            self.perm = kwargs["perm"]
        Immovable.__init__(self, **kwargs)

    def activate(self):
        """
        This function is calling the action function with the
        action_parameters.

        Usually it's automatically called by :meth:`~pygamelib.engine.Board.move`
        when a Player or NPC (see :mod:`~pygamelib.board_items`)
        """
        if self.action is not None:
            self.action(self.action_parameters)


class Character:
    """A base class for a character (playable or not)

    :param agility: Represent the agility of the character
    :type agility: int
    :param attack_power: Represent the attack power of the character.
    :type attack_power: int
    :param defense_power: Represent the defense_power of the character
    :type defense_power: int
    :param hp: Represent the hp (Health Point) of the character
    :type hp: int
    :param intelligence: Represent the intelligence of the character
    :type intelligence: int
    :param max_hp: Represent the max_hp of the character
    :type max_hp: int
    :param max_mp: Represent the max_mp of the character
    :type max_mp: int
    :param mp: Represent the mp (Mana/Magic Point) of the character
    :type mp: int
    :param remaining_lives: Represent the remaining_lives of the character. For a NPC
        it is generally a good idea to set that to 1. Unless the NPC is a multi phased
        boss.
    :type remaining_lives: int
    :param strength: Represent the strength of the character
    :type strength: int

    These characteristics are here to be used by the game logic but very few of them are
    actually used by the Game (`pygamelib.engine`) engine.


    """

    def __init__(self, **kwargs):
        self.max_hp = None
        self.hp = None
        self.max_mp = None
        self.mp = None
        self.remaining_lives = None
        self.attack_power = None
        self.defense_power = None
        self.strength = None
        self.intelligence = None
        self.agility = None
        for a in [
            "max_hp",
            "hp",
            "max_mp",
            "mp",
            "remaining_lives",
            "attack_power",
            "defense_power",
            "strength",
            "intelligence",
            "agility",
        ]:
            if a in kwargs.keys():
                setattr(self, a, kwargs[a])


class Player(Movable, Character):
    """
    A class that represent a player controlled by a human.
    It accepts all the parameters from :class:`~pygamelib.board_items.Character` and is
    a :class:`~pygamelib.board_items.Movable`.

    This class sets a couple of variables to default values:

     * max_hp: 100
     * hp: 100
     * remaining_lives: 3
     * attack_power: 10
     * movement_speed: 0.1 (one movement every 0.1 second). Only useful if the game mode
         is set to MODE_RT.

    .. note:: If no inventory is passed as parameter a default one is created.
    """

    def __init__(self, **kwargs):
        if "max_hp" not in kwargs.keys():
            kwargs["max_hp"] = 100
        if "hp" not in kwargs.keys():
            kwargs["hp"] = 100
        if "remaining_lives" not in kwargs.keys():
            kwargs["remaining_lives"] = 3
        if "attack_power" not in kwargs.keys():
            kwargs["attack_power"] = 10
        if "movement_speed" not in kwargs.keys():
            kwargs["movement_speed"] = 0.1
        Movable.__init__(self, **kwargs)
        Character.__init__(self, **kwargs)
        if "inventory" in kwargs.keys():
            self.inventory = kwargs["inventory"]
        else:
            self.inventory = engine.Inventory(parent=self)

    def pickable(self):
        """This method returns False (a player is obviously not pickable).
        """
        return False

    def has_inventory(self):
        """This method returns True (a player has an inventory).
        """
        return True

    def overlappable(self):
        """This method returns false (a player cannot be overlapped).

        .. note:: If you wish your player to be overlappable, you need to inherit from
            that class and re-implement overlappable().
        """
        return False


class ComplexPlayer(Player, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A complex player is nothing more than a :class:`~Player` mashed with a
    :class:`BoardComplexItem`.

    It supports all parameters of both with inheritance going first to Player and second
    to BoardComplexItem.

    The main interest is of course the multiple cell representation and the Sprites
    support.

    Example::

        player = ComplexPlayer(
                name='Mighty Wizard',
                sprite=sprite_collection['wizard_idle']
            )
    """

    def __init__(self, **kwargs):
        Player.__init__(self, **kwargs)
        BoardComplexItem.__init__(self, **kwargs)


class NPC(Movable, Character):
    """
    A class that represent a non playable character controlled by the computer.
    For the NPC to be successfully managed by the Game, you need to set an actuator.

    None of the parameters are mandatory, however it is advised to make good use of some
    of them (like type or name) for game design purpose.

    In addition to its own member variables, this class inherits all members from:
        * :class:`pygamelib.board_items.Character`
        * :class:`pygamelib.board_items.Movable`
        * :class:`pygamelib.board_items.BoardItem`

    This class sets a couple of variables to default values:

     * max_hp: 10
     * hp: 10
     * remaining_lives: 1
     * attack_power: 5
     * movement_speed: 0.25 (one movement every 0.25 second). Only useful if the game
         mode is set to MODE_RT.

    :param actuator: An actuator, it can be any class but it need to implement
        pygamelib.actuators.Actuator.
    :type actuator: pygamelib.actuators.Actuator

    Example::

        mynpc = NPC(name='Idiot McStupid', type='dumb_enemy')
        mynpc.step = 1
        mynpc.actuator = RandomActuator()
    """

    def __init__(self, **kwargs):
        if "max_hp" not in kwargs.keys():
            kwargs["max_hp"] = 10
        if "hp" not in kwargs.keys():
            kwargs["hp"] = 10
        if "remaining_lives" not in kwargs.keys():
            kwargs["remaining_lives"] = 1
        if "attack_power" not in kwargs.keys():
            kwargs["attack_power"] = 5
        if "movement_speed" not in kwargs.keys():
            kwargs["movement_speed"] = 0.25
        Movable.__init__(self, **kwargs)
        Character.__init__(self, **kwargs)
        if "actuator" not in kwargs.keys():
            self.actuator = None
        else:
            self.actuator = kwargs["actuator"]

        if "step" not in kwargs.keys():
            self.step = 1
        else:
            self.step = kwargs["step"]

    def pickable(self):
        """Define if the NPC is pickable.

        Obviously this method always return False.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.pickable():
                Utils.warn("Something is fishy, that NPC is pickable"
                    "but is not a Pokemon...")
        """
        return False

    def overlappable(self):
        """Define if the NPC is overlappable.

        Obviously this method also always return False.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.overlappable():
                Utils.warn("Something is fishy, that NPC is overlappable but"
                    "is not a Ghost...")
        """
        return False

    def has_inventory(self):
        """Define if the NPC has an inventory.

        This method returns false because the game engine doesn't manage NPC inventory
        yet but it could be in the future. It's a good habit to check the value returned
        by this function.

        :return: False
        :rtype: Boolean

        Example::

            if mynpc.has_inventory():
                print("Cool: we can pickpocket that NPC!")
            else:
                print("No pickpocketing XP for us today :(")
        """
        return False


class ComplexNPC(NPC, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A complex NPC is nothing more than a :class:`~NPC` mashed with a
    :class:`BoardComplexItem`.

    It supports all parameters of both with inheritance going first to NPC and second
    to BoardComplexItem.

    The main interest is of course the multiple cell representation and the Sprites
    support.

    Example::

        player = ComplexNPC(
                name='Idiot McComplexStupid',
                sprite=npc_sprite_collection['troll_licking_stones']
            )
    """

    def __init__(self, **kwargs):
        NPC.__init__(self, **kwargs)
        BoardComplexItem.__init__(self, **kwargs)


class TextItem(BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    The text item is a board item that can contains text. The text can then be
    manipulated and placed on a :class:`~pygamelib.engine.Board`.

    It is overall a :class:`BoardComplexItem` (so it takes all the parameters of that
    class). The big difference is that the first parameter is the text you want to
    display.

    The text parameter can be either a regular string or a :class:`~pygamelib.base.Text`
    object (in case you want formatting and colors).

    :param text: The text you want to display.
    :type text: str | :class:`~pygamelib.base.Text`

    Example::

        city_name = TextItem('Super City')
        fancy_city_name = TextItem(text=base.Text('Super City', base.Fore.GREEN,
            base.Back.BLACK,
            base.Style.BRIGHT
        ))
        my_board.place_item(city_name, 0, 0)
        my_board.place_item(fancy_city_name, 1, 0)
    """

    def __init__(self, text=None, **kwargs):
        BoardComplexItem.__init__(self, **kwargs)
        if text is not None and not isinstance(text, base.Text) and type(text) is str:
            self._text = base.Text(text)
        elif text is not None and not isinstance(text, base.Text):
            raise base.PglInvalidTypeException(
                f"TextItem: text parameter need to be either a str or a "
                f"pygamelib.base.Text object. Type {type(text)} is neither of these."
            )
        else:
            self._text = text
        self.sprite = core.Sprite.from_text(self._text)
        self.update_sprite()

    def __repr__(self):  # pragma: no cover
        return self._text.__repr__()

    @property
    def text(self):
        """The text within the item.

        TextItem.text can be set to either a string or a :class:`~pygamelib.base.Text`
        object.

        It will always return a :class:`~pygamelib.base.Text` object.

        Internally it translate the text to a :class:`~pygamelib.gfx.core.Sprite` to
        display it correctly on a :class:`~pygamelib.engine.Board`. If print()-ed it
        will do so like the :class:`~pygamelib.base.Text` object.
        """
        return self._text

    @text.setter
    def text(self, value):
        if type(value) is str:
            self._text = base.Text(value)
        elif isinstance(value, base.Text):
            self._text = value
        else:
            raise base.PglInvalidTypeException(
                "TextItem.text must be either a str or a pygamelib.base.Text object."
            )
        self.sprite = core.Sprite.from_text(self._text)
        self.update_sprite()


class Wall(Immovable):
    """
    A Wall is a specialized :class:`~pygamelib.board_items.Immovable` object that as
    unmodifiable characteristics:

    * It is not pickable (and cannot be).
    * It is not overlappable (and cannot be).
    * It is not restorable (and cannot be).

    As such it's an object that cannot be moved, cannot be picked up or modified by
    Player or NPC and block their ways. It is therefor advised to create one per board
    and reuse it in many places.

    :param model: The representation of the Wall on the Board.
    :type model: str
    :param name: The name of the Wall.
    :type name: str
    :param size: The size of the Wall. This parameter will probably be deprecated as
        size is only used for pickable objects.
    :type size: int
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "#"
        if "name" not in kwargs.keys():
            kwargs["name"] = "wall"
        if "size" not in kwargs.keys():
            kwargs["size"] = 1
        Immovable.__init__(self, **kwargs)

    def pickable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be pick-up by player or NPC.

        :return: False
        :rtype: bool

        Example::

            if mywall.pickable():
                print('Whoaa this wall is really light... and small...')
            else:
                print('Really? Trying to pick-up a wall?')
        """
        return False

    def overlappable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be overlapped by player or NPC.

        :return: False
        :rtype: bool
        """
        return False

    def restorable(self):
        """
        This represent the capacity for an :class:`~pygamelib.board_items.Immovable`
        :class:`~pygamelib.board_items.BoardItem`(in this case a Wall item) to be
        restored by the board if the item is overlappable and has been overlapped by
        another :class:`~pygamelib.board_items.Movable` item.
        A wall is not overlappable.

        :return: False
        :rtype: bool
        """
        return False


class ComplexWall(Wall, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A complex wall is nothing more than a :class:`~Wall` mashed with a
    :class:`BoardComplexItem`.

    It supports all parameters of both with inheritance going first to Wall and second
    to BoardComplexItem.

    The main interest is of course the multiple cell representation and the Sprites
    support.

    Example::

        wall = ComplexWall(
                sprite=sprite_brick_wall
            )
    """

    def __init__(self, **kwargs):
        Wall.__init__(self, **kwargs)
        BoardComplexItem.__init__(self, **kwargs)


class GenericStructure(Immovable):
    """
    A GenericStructure is as the name suggest, a generic object to create all kind of
    structures.

    It can be tweaked with all the properties of
    :class:`~pygamelib.board_items.BoardItem`, :class:`~pygamelib.board_items.Immovable`
    and it can be made pickable, overlappable or restorable or any combination of these.

    If you need an action to be done when a Player and/or a NPC touch the structure
    please have a look at
    :class:`pygamelib.board_items.GenericActionableStructure`.

    :param pickable: Define if the structure can be picked-up by a Player or NPC.
    :type pickable: bool
    :param overlappable: Define if the structure can be overlapped by a Player or NPC.
    :type overlappable: bool
    :param restorable: Define if the structure can be restored by the Board after a
        Player or NPC passed through. For example, you want a door or an activator
        structure (see GenericActionableStructure for that) to remain on the board after
        it's been overlapped by a player. But you could also want to develop some kind
        of Space Invaders game were the protection block are overlappable but not
        restorable.
    :type restorable: bool

    On top of these, this object takes all parameters of
    :class:`~pygamelib.board_items.BoardItem` and
    :class:`~pygamelib.board_items.Immovable`

    .. important:: If you need a structure with a permission system please have a look
        at :class:`~pygamelib.board_items.GenericActionableStructure`. This class
        has a permission system for activation.

    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "#"
        if "name" not in kwargs.keys():
            kwargs["name"] = "structure"
        Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs["value"]
        if "pickable" in kwargs.keys():
            self.__is_pickable = kwargs["pickable"]
        else:
            self.__is_pickable = False
        if "overlappable" in kwargs.keys():
            self.__is_overlappable = kwargs["overlappable"]
        else:
            self.__is_overlappable = False

        if "restorable" in kwargs.keys():
            self.__is_restorable = kwargs["restorable"]
        else:
            self.__is_restorable = False

    def pickable(self):
        """This represent the capacity for a BoardItem to be picked-up by player or NPC.

        To set this value please use :meth:`~.set_pickable`

        :return: True or False
        :rtype: bool

        .. seealso:: :meth:`~.set_pickable`
        """
        return self.__is_pickable

    def set_pickable(self, val):
        """Make the structure pickable or not.

        :param val: True or False depending on the pickability of the structure.
        :type val: bool

        Example::

            myneatstructure.set_pickable(True)
        """
        if type(val) is bool:
            self.__is_pickable = val

    def overlappable(self):
        """ This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
        be overlapped by player or NPC.

        To set this value please use :meth:`~.set_overlappable`

        :return: False
        :rtype: bool

        .. seealso:: :meth:`~.set_overlappable`
        """
        return self.__is_overlappable

    def set_overlappable(self, val):
        """Make the structure overlappable or not.

        :param val: True or False depending on the fact that the structure can be
            overlapped (i.e that a Player or NPC can step on it) or not.
        :type val: bool

        Example::

            myneatstructure.set_overlappable(True)
        """
        if type(val) is bool:
            self.__is_overlappable = val

    def restorable(self):
        """
        This represent the capacity for an :class:`~pygamelib.board_items.Immovable`
        :class:`~pygamelib.board_items.BoardItem` (in this case a GenericStructure item)
        to be restored by the board if the item is overlappable and has been overlapped
        by another :class:`~pygamelib.board_items.Movable` item.

        The value of this property is set with :meth:`~.set_restorable`

        :return: False
        :rtype: bool

        .. seealso:: :meth:`~.set_restorable`
        """
        return self.__is_restorable

    def set_restorable(self, val):
        """Make the structure restorable or not.

        :param val: True or False depending on the restorability of the structure.
        :type val: bool

        Example::

            myneatstructure.set_restorable(True)
        """
        if type(val) is bool:
            self.__is_restorable = val
        else:
            raise base.PglInvalidTypeException(
                "set_restorable(bool) takes a boolean as paramater."
            )


class GenericActionableStructure(GenericStructure, Actionable):
    """
    A GenericActionableStructure is the combination of a
    :class:`~pygamelib.board_items.GenericStructure` and an
    :class:`~pygamelib.board_items.Actionable`.
    It is only a helper combination.

    Please see the documentation for
    :class:`~pygamelib.board_items.GenericStructure` and
    :class:`~pygamelib.board_items.Actionable` for more information.
    """

    def __init__(self, **kwargs):
        GenericStructure.__init__(self, **kwargs)
        Actionable.__init__(self, **kwargs)


class Treasure(Immovable):
    """
    A Treasure is an :class:`~pygamelib.board_items.Immovable` that is pickable and
    with a non zero value. It is an helper class that allows to focus on game design and
    mechanics instead of small building blocks.

    :param model: The model that will represent the treasure on the map
    :type model: str
    :param value: The value of the treasure, it is usually used to calculate the score.
    :type value: int
    :param inventory_space: The space occupied by the treasure. It is used by
        :class:`~pygamelib.engine.Inventory` as a measure of space. If the treasure's
        size exceed the Inventory size (or the cumulated size of all items + the
        treasure exceed the inventory max_size()) the
        :class:`~pygamelib.base.Inventory` will refuse to add the treasure.
    :type inventory_space: int

    .. note:: All the options from :class:`~pygamelib.board_items.Immovable` are also
        available to this constructor.

    Example::

        money_bag = Treasure(model=Sprites.MONEY_BAG,value=100,inventory_space=2)
        print(f"This is a money bag {money_bag}")
        player.inventory.add_item(money_bag)
        print(f"The inventory value is {player.inventory.value()} and is at
            {player.inventory.size()}/{player.inventory.max_size}")
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "¤"
        Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 10
        else:
            self.value = kwargs["value"]
        if "inventory_space" not in kwargs.keys():
            self._inventory_space = 1
        else:
            self._inventory_space = kwargs["inventory_space"]

    def pickable(self):
        """ This represent the capacity for a Treasure to be picked-up by player or NPC.

        A treasure is obviously pickable by the player and potentially NPCs.
        :class:`~pygamelib.engine.Board` puts the Treasure in the
        :class:`~pygamelib.engine.Inventory` if the picker implements has_inventory()

        :return: True
        :rtype: bool
        """
        return True

    def overlappable(self):
        """ This represent the capacity for a Treasure to be overlapped by player or NPC.

        A treasure is not overlappable.

        :return: False
        :rtype: bool
        """
        return False

    def restorable(self):
        """ This represent the capacity for a Treasure to be restored after being overlapped.

        A treasure is not overlappable, therefor is not restorable.

        :return: False
        :rtype: bool
        """
        return False


class ComplexTreasure(Treasure, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A complex treasure is nothing more than a :class:`~Treasure` mashed with a
    :class:`BoardComplexItem`.

    It supports all parameters of both with inheritance going first to Treasure and
    second to BoardComplexItem.

    The main interest is of course the multiple cell representation and the Sprites
    support.

    Example::

        chest = ComplexTreasure(
                sprite=sprite_chest
            )
    """

    def __init__(self, **kwargs):
        Treasure.__init__(self, **kwargs)
        BoardComplexItem.__init__(self, **kwargs)


class Door(GenericStructure):
    """
    A Door is a :class:`~pygamelib.board_items.GenericStructure` that is not
    pickable, overlappable and restorable. It has a value of 0 and a size of 1 by
    default. It is an helper class that allows to focus on game design and mechanics
    instead of small building blocks.

    :param model: The model that will represent the door on the map
    :type model: str
    :param value: The value of the door, it is useless in that case. The default value
        is 0.
    :type value: int
    :param inventory_space: The size of the door in the inventory. Unless you make the
        door pickable (I have no idea why you would do that...), this parameter is not
        used.
    :type inventory_space: int
    :param type: The type of the door. It is often used as a type identifier for your
        game main loop. For example: unlocked_door or locked_door.
    :type type: str
    :param pickable: Is this door pickable by the player? Default value is False.
    :type pickable: Boolean
    :param overlappable: Is this door overlappable by the player? Default value is True.
    :type overlappable: Boolean
    :param restorable: Is this door restorable after being overlapped? Default value is
        True.
    :type restorable: Boolean

    .. note:: All the options from
       :class:`~pygamelib.board_items.GenericStructure` are also available to
       this constructor.

    Example::

        door1 = Door(model=Sprites.DOOR,type='locked_door')
    """

    def __init__(self, **kwargs):
        if "model" not in kwargs.keys():
            kwargs["model"] = "]"
        Immovable.__init__(self, **kwargs)
        if "value" not in kwargs.keys():
            self.value = 0
        else:
            self.value = kwargs["value"]
        if "inventory_space" not in kwargs.keys():
            self._inventory_space = 1
        else:
            self._inventory_space = kwargs["inventory_space"]
        if "name" not in kwargs.keys():
            self.name = "Door"
        else:
            self.name = kwargs["name"]
        if "type" not in kwargs.keys():
            self.type = "door"
        else:
            self.type = kwargs["type"]
        if "pickable" not in kwargs.keys():
            self.set_pickable(False)
        else:
            self.set_pickable(kwargs["pickable"])
        if "overlappable" not in kwargs.keys():
            self.set_overlappable(True)
        else:
            self.set_overlappable(kwargs["overlappable"])
        if "restorable" not in kwargs.keys():
            self.set_restorable(True)
        else:
            self.set_restorable(kwargs["restorable"])


class ComplexDoor(Door, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A complex door is nothing more than a :class:`~Door` mashed with a
    :class:`BoardComplexItem`.

    It supports all parameters of both with inheritance going first to Door and second
    to BoardComplexItem.

    The main interest is of course the multiple cell representation and the Sprites
    support.

    Example::

        castle_door = ComplexDoor(
                sprite=sprite_castle_door
            )
    """

    def __init__(self, **kwargs):
        Door.__init__(self, **kwargs)
        BoardComplexItem.__init__(self, **kwargs)


class GenericStructureComplexComponent(GenericStructure, BoardItemComplexComponent):
    """
    A ComplexComponent specifically for generic structures.
    """

    def __init__(self, **kwargs):
        GenericStructure.__init__(self, **kwargs)
        BoardItemComplexComponent.__init__(self, **kwargs)


class Tile(GenericStructure, BoardComplexItem):
    """
    .. versionadded:: 1.2.0

    A Tile is a standard :class:`BoardComplexItem` configured by default to:

     * be overlappable
     * be not pickable
     * be immovable.

    Aside from the movable attributes (it inherit from GenericStructure so it's an
    Immovable object), everything else is configurable.

    It is particularly useful to display a :class:`~pygamelib.gfx.core.Sprite` on the
    background or to create terrain.

    :param overlappable: Defines if the Tile can be overlapped.
    :type overlappable: bool
    :param restorable: Defines is the Tile should be restored after being overlapped.
    :type restorable: bool
    :param pickable: Defines if the Tile can be picked up by the Player or NPC.
    :type pickable: bool

    Please see :class:`BoardComplexItem` for additional parameters.

    Example::

        grass_sprite = Sprite.load_from_ansi_file('textures/grass.ans')
        for pos in grass_positions:
            outdoor_level.place_item( Tile(sprite=grass_sprite), pos[0], pos[1] )
    """

    def __init__(self, **kwargs):
        kwargs["parent"] = self
        kwargs["base_item_type"] = GenericStructureComplexComponent
        if "overlappable" not in kwargs:
            kwargs["overlappable"] = True
        if "restorable" not in kwargs:
            kwargs["restorable"] = True
        if "pickable" not in kwargs:
            kwargs["pickable"] = False
        GenericStructure.__init__(self, **kwargs)
        # kwargs["base_item_type"] = Door
        BoardComplexItem.__init__(self, **kwargs)

    def can_move(self):
        """A Tile cannot move.

        :returns: False
        :rtype: bool
        """
        return False
