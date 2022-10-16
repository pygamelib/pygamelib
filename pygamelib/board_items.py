__docformat__ = "restructuredtext"
"""This module contains the basic board items classes.

.. autosummary::
   :toctree: .

   pygamelib.board_items.BoardItem
   pygamelib.board_items.BoardItemVoid
   pygamelib.board_items.BoardComplexItem
   pygamelib.board_items.BoardItemComplexComponent
   pygamelib.board_items.Movable
   pygamelib.board_items.Projectile
   pygamelib.board_items.Immovable
   pygamelib.board_items.Actionable
   pygamelib.board_items.Character
   pygamelib.board_items.Player
   pygamelib.board_items.ComplexPlayer
   pygamelib.board_items.NPC
   pygamelib.board_items.ComplexNPC
   pygamelib.board_items.TextItem
   pygamelib.board_items.Wall
   pygamelib.board_items.ComplexWall
   pygamelib.board_items.Treasure
   pygamelib.board_items.ComplexTreasure
   pygamelib.board_items.Door
   pygamelib.board_items.ComplexDoor
   pygamelib.board_items.GenericStructure
   pygamelib.board_items.GenericActionableStructure
   pygamelib.board_items.GenericStructureComplexComponent
   pygamelib.board_items.Tile
   pygamelib.board_items.ActionableTile
   pygamelib.board_items.Camera
"""
from pygamelib import engine
from pygamelib import base
from pygamelib import constants
from pygamelib.gfx import core
from pygamelib import actuators
from pygamelib.functions import pgl_isinstance


class BoardItem(base.PglBaseObject):
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
        space it will require. Default value is '*'. This parameter is now deprecated in
        favor of "sprixel". If both "sprixel" and "model" are specified, "model" is
        ignored.
    :type model: str
    :param parent: The parent object of the board item. Usually a Board or Game object.
    :param sprixel: The sprixel that will represent the item on the Board.
    :type sprixel: :class:`~pygamelib.gfx.core.Sprixel`
    :param pickable: Represent the capacity for a BoardItem to be pick-up by player or
       NPC. This parameter is True or False. If sets to None, it'll be set to False.
    :type pickable: bool
    :param overlappable: Represent to be overlapped by another BoardItem. This parameter
       is True or False. If sets to None, it'll be set to False.
    :type overlappable: bool
    :param restorable: Represent the capacity for an Immovable BoardItem to be restored
        by the board if the item is overlappable and has been overlapped by another
        BoardItem. This parameter is True or False. If sets to None, it'll be set to
        False.
    :type restorable: bool
    :param can_move: Represent the ability of the BoardItem to move on the Board. If
       this parameter is False, the Board.move() method will not allow the item to move.
       This parameter is True or False. If sets to None, it'll be set to False.
    :type can_move: bool
    :param pos: The position of the BoardItem on a :class:`~pygamelib.engine.Board`.
       Please make sure that you understand what you do before changing that parameter.
       The position of an item is managed by the Board object and will be updated. In
       most cases you don't need to use that parameter. The position is a list of 2 or 3
       int: [row, column, layer].
    :type pos: list
    :param value: The value of an item. It can be used for any game purpose: a score
       indicator, a trade value, the amount of XP to grant to a player on a kill, etc.
    :type value: int | float
    :param inventory_space: The space that the item takes in the
       :class:`pygamelib.engine.Inventory`. This parameter used to be available only for
       :class:`Immovable` items but since 1.3.0, every BoardItem can be configured to be
       pickable, so every BoardItem can now take space in the inventory. Default value
       is 1.
    :type inventory_space: int
    :param animation: An animation to animate the item sprixel.
    :type animation: :class:`~pygamelib.gfx.core.Animation`
    :param particle_emitter: A particle emitter that is attached to this item.
    :type particle_emitter: :class:`~pygamelib.gfx.particles.ParticleEmitter`

    .. note:: Starting with version 1.2.0 and introduction of complex items,
       BoardItems have a size. That size **CANNOT** be set. It is always 1x1.
       This is because a BoardItem always takes 1 cell, regardless of its actual number
       of characters. The size is a read-only property.

    .. important:: In version 1.3.0 the BoardItem object has been reworked to make sure
       that the pickable, restorable, overlappable and can_move properties are
       configurable for all items independently of their type. This fixes an issue with
       restorable: only :class:`~Immovable` objects could be restorable. Now all items
       can be any combination of these properties. As a developer you are now
       encouraged to use the corresponding functions to determine the abilities of an
       item.

    .. warning:: An item cannot be restorable and pickable at the same time. If it's
       pickable, it's put into the inventory of the item overlapping it. Therefor, it
       cannot be restored. If both restorable and pickable are set to True, one of the 2
       is set to False depending on the value of overlappable: if True restorable is set
       to True and pickable to False and the contrary if overlappable is False.
    """

    def __init__(
        self,
        sprixel=None,
        model=None,
        name=None,
        item_type=None,
        parent=None,
        pickable=False,
        overlappable=False,
        restorable=False,
        can_move=False,
        pos=None,
        value=None,
        inventory_space=1,
        animation: core.Animation = None,
        particle_emitter=None,
    ):
        super().__init__()
        self.name = "Board item"
        if name is not None:
            self.name = name
        self.type = "item"
        if item_type is not None:
            self.type = item_type
        self.pos = [None, None, None]
        if (
            pos is not None
            and len(pos) >= 2
            and pos[0] is not None
            and pos[1] is not None
        ):
            self.pos = pos
        # DEPRECATED
        # self.model = "*"
        self._particle_emitter = None
        if particle_emitter is not None and pgl_isinstance(
            particle_emitter, "pygamelib.gfx.particles.ParticleEmitter"
        ):
            self._particle_emitter = particle_emitter
            setattr(self._particle_emitter, "_board_item", self)
        self.__animation = None
        self.animation = animation
        self.parent = None
        if parent is not None:
            self.parent = parent
        self.sprixel = core.Sprixel("*")
        if sprixel is not None:
            self.sprixel = sprixel
        self._size = [1, 1]
        if model is not None and sprixel is None:
            self.sprixel.model = model
        if self.sprixel.bg_color is None and sprixel is None:
            self.sprixel.is_bg_transparent = True
        self.value = value
        self._inventory_space = inventory_space
        self.__heading = base.Vector2D(0, 0)
        self.__centroidcc = base.Vector2D(0, 0)
        # Init the pickable, overlappable and restorable states
        self.__is_pickable = pickable
        self.__is_overlappable = overlappable
        self.__is_restorable = restorable
        self.__can_move = can_move
        if self.__is_pickable is None:
            self.__is_pickable = False
        if self.__is_overlappable is None:
            self.__is_overlappable = False
        if self.__is_restorable is None:
            self.__is_restorable = False
        if self.__can_move is None:
            self.__can_move = False
        # Solving conflicts
        if pickable and restorable and overlappable:
            self.__is_pickable = False
        elif pickable and restorable and not overlappable:
            self.__is_restorable = False

    def serialize(self) -> dict:
        """Return a dictionary with all the attributes of this object.

        :return: A dictionary with all the attributes of this object.
        :rtype: dict
        """
        ret_data = dict()
        # self.parent cannot really be serialized (or more accurately I don't really
        # want to do it properly)
        ret_data["object"] = str(self.__class__)
        if self.sprixel is not None:
            ret_data["sprixel"] = self.sprixel.serialize()
        if self.animation is not None:
            ret_data["animation"] = self.animation.serialize()
        ret_data["restorable"] = self.restorable()
        ret_data["overlappable"] = self.overlappable()
        ret_data["pickable"] = self.pickable()
        ret_data["can_move"] = self.can_move()
        ret_data["inventory_space"] = self.inventory_space
        if self.particle_emitter is not None:
            ret_data["particle_emitter"] = self.particle_emitter.serialize()
        else:
            ret_data["particle_emitter"] = None
        keys = [
            "value",
            "name",
            "model",
            "type",
            "pos",
        ]
        for key in keys:
            ret_data[key] = getattr(self, key)
        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new BoardItem out of it.

        :param data: Data to create a new item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new item.
        :rtype: `~pygamelib.board_items.BoardItem`
        """
        fields = [
            "restorable",
            "overlappable",
            "pickable",
            "can_move",
            "inventory_space",
            "value",
            "name",
            "model",
            "type",
            "pos",
        ]
        for field in fields:
            if field not in data.keys():
                data[field] = None
        if "sprixel" not in data.keys():
            data["sprixel"] = {
                "model": "",
                "fg_color": None,
                "bg_color": None,
                "is_bg_transparent": True,
            }
        itm = cls(
            sprixel=core.Sprixel.load(data["sprixel"]),
            model=data["model"],
            name=data["name"],
            item_type=data["type"],
            pickable=data["pickable"],
            overlappable=data["overlappable"],
            restorable=data["restorable"],
            can_move=data["can_move"],
            pos=data["pos"],
            value=data["value"],
            inventory_space=data["inventory_space"],
        )
        if "animation" in data.keys() and data["animation"] is not None:
            itm.animation = core.Animation.load(data["animation"])
        if "particle_emitter" in data.keys() and data["particle_emitter"] is not None:
            import pygamelib  # noqa: F401

            pt = eval(data["particle_emitter"]["emitter_type"])
            itm.particle_emitter = pt.load(data["particle_emitter"])
        return itm

    @property
    def particle_emitter(self):
        return self._particle_emitter

    @particle_emitter.setter
    def particle_emitter(self, value):
        self._particle_emitter = value
        setattr(self._particle_emitter, "_board_item", self)

    @property
    def heading(self):
        """Return the heading of the item.

        This is a read only property that is updated by :py:meth:`store_position()`.

        The property represent the orientation and movement of the item in the board. It
        gives the difference between the item's centroid current and previous position.
        Thus, giving you both the direction and the distance of the movement. You can
        get the angle from here.

        One of the possible usage of that property is to set the sprite/sprixel/model of
        a moving item.

        :return: The heading of the item.
        :rtype: :class:`~pygamelib.base.Vector2D`

        Example::

            if my_item.heading.column > 0:
                my_item.sprixel.model = item_models["heading_right"]

        .. warning:: Just after placing an item on the board, and before moving it, the
           heading cannot be trusted! The heading represent the direction and
           orientation of the **movement**, therefore, it is not reliable before the
           item moved.
        """
        return self.__heading

    @property
    def animation(self):
        """A property to get and set an :class:`~pygamelib.gfx.core.Animation` for
        this item.

        .. Important:: When an animation is set, the item is setting the animation's
           parent to itself.
        """
        return self.__animation

    @animation.setter
    def animation(self, animation: core.Animation):
        if isinstance(animation, core.Animation):
            animation.parent = self
            self.__animation = animation

    @property
    def model(self):
        return self.sprixel.model

    @model.setter
    def model(self, value):
        self.sprixel.model = value

    @property
    def inventory_space(self):
        """A property to get and set the size that the BoardItem takes in the
        :class:`~pygamelib.engine.Inventory`.

        :return: The size of the item.
        :rtype: int
        """
        return self._inventory_space

    @inventory_space.setter
    def inventory_space(self, value):
        if type(value) is int:
            self._inventory_space = value
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.inventory_space.(value): value needs to be an int."
            )

    def __str__(self):
        if self.sprixel is not None:
            return self.sprixel.__repr__()
        return ""

    def __repr__(self):
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
            string += f"'model' = '{self.model}'"
        return string

    def store_position(self, row: int, column: int, layer: int = 0):
        """Store the BoardItem position for self access.

        The stored position is used for consistency and quick access to the self
        position. It is a redundant information and might not be synchronized.

        :param row: the row of the item in the :class:`~pygamelib.engine.Board`.
        :type row: int
        :param column: the column of the item in the :class:`~pygamelib.engine.Board`.
        :type column: int
        :param layer: the layer of the item in the :class:`~pygamelib.engine.Board`. By
           default layer is set to 0.
        :type column: int

        Example::

            item.store_position(3,4)
        """
        self.pos = [row, column, layer]
        if row is not None and column is not None:
            pcr = self.__centroidcc.row
            pcc = self.__centroidcc.column
            self.__centroidcc.row = row + self.height / 2
            self.__centroidcc.column = column + self.width / 2
            self.__heading.row = self.__centroidcc.row - pcr
            self.__heading.column = self.__centroidcc.column - pcc
        if self.particle_emitter is not None:
            self.particle_emitter.row = row
            self.particle_emitter.column = column

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
    def layer(self):
        """Convenience method to get the current stored layer number of the item.

        This is absolutely equivalent to access to item.pos[2].

        :return: The layer number
        :rtype: int

        Example::

            if item.layer != item.pos[2]:
                print('Something extremely unlikely just happened...')
        """
        return self.pos[2]

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

    @property
    def size(self):
        """A read-only property that gives the size of the item as a 2 dimensions list.
        The first element is the width and the second the height.

        :return: The size.
        :rtype: list

        Example::

            # This is a silly example because the Board object does not allow
            # that use case.
            if item.column + item.size[0] >= board.width:
                Game.instance().screen.display_line(
                    f"{item.name} cannot be placed at {item.pos}."
                )
        """
        return self._size

    def collides_with(self, other, projection_offset: base.Vector2D = None):
        """Tells if this item collides with another item.

        .. Important:: collides_with() does not take the layer into account! It is not
           desirable for the pygamelib to assume that 2 items on different layers wont
           collide. For example, if a player is over a door, they are on different
           layers, but logically speaking they are colliding. The player is overlapping
           the door. Therefor, it is the responsibility of the developer to check for
           layers in collision, if it is important to the game logic.

        :param other: The item you want to check for collision.
        :type other: :class:`~pygamelib.board_items.BoardItem`
        :param projection_offset: A vector to offset this board item's position (not the
           position of the `other` item). Use this to detect a collision before moving
           the board item. You can pass the movement vector before moving to check if
           a collision will occur when moving.
        :type projection_offset: :class:`~pygamelib.base.Vector2D`
        :rtype: bool

        Example::

            if projectile.collides_with(game.player):
                game.player.hp -= 5
        """
        offset_row = offset_col = 0
        if isinstance(projection_offset, base.Vector2D):
            offset_row = round(projection_offset.row)
            offset_col = round(projection_offset.column)
        if isinstance(other, BoardItem):
            return base.Math.intersect(
                # self.pos[0] + round(offset_row),
                # self.pos[1] + round(offset_col),
                self.pos[0] + offset_row,
                self.pos[1] + offset_col,
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
                self.pos[0],
                self.pos[1],
                other.pos[0],
                other.pos[1],
            )
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.distance_to require a BoardItem as parameter."
            )

    def render_to_buffer(self, buffer, row, column, height, width):
        """Render the board item into a display buffer (not a screen buffer).

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
        buffer[row][column] = self.sprixel.__repr__()
        incr = self.sprixel.length
        if incr > 1:
            end = min(column + incr, width)
            for idx in range(column + 1, end):
                buffer[row][idx] = ""

    def restorable(self):
        """
        Returns True if the item is restorable, False otherwise.

        Example::

            if board.item(4,5).restorable():
                print('The item is restorable')
        """
        return self.__is_restorable

    def set_restorable(self, value):
        """
        Set the value of the restorable property to value.

        :param value: The value to set.
        :type value: bool

        Example::

            item.set_restorable(False)
        """
        if type(value) is bool:
            self.__is_restorable = value
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.set_restorable(value): 'value' needs to be a bool."
            )

    def overlappable(self):
        """
        Returns True if the item is overlappable, False otherwise.

        Example::

            if board.item(4,5).overlappable():
                print('The item is overlappable')
        """
        return self.__is_overlappable

    def set_overlappable(self, value):
        """
        Set the value of the overlappable property to value.

        :param value: The value to set.
        :type value: bool

        Example::

            item.set_overlappable(False)
        """
        if type(value) is bool:
            self.__is_overlappable = value
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.set_overlappable(value): 'value' needs to be a bool."
            )

    def can_move(self):
        """
        Returns True if the item can move, False otherwise.

        Example::

            if board.item(4,5).can_move():
                print('The item can move')
        """
        return self.__can_move

    def set_can_move(self, value):
        """
        Set the value of the can_move property to value.

        :param value: The value to set.
        :type value: bool

        Example::

            item.set_can_move(False)
        """
        if type(value) is bool:
            self.__can_move = value
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.set_can_move(value): 'value' needs to be a bool."
            )

    def pickable(self):
        """
        Returns True if the item is pickable, False otherwise.

        Example::

            if board.item(4,5).pickable():
                print('The item is pickable')
        """
        return self.__is_pickable

    def set_pickable(self, value):
        """
        Set the value of the pickable property to value.

        :param value: The value to set.
        :type value: bool

        Example::

            item.set_pickable(False)
        """
        if type(value) is bool:
            self.__is_pickable = value
        else:
            raise base.PglInvalidTypeException(
                "BoardItem.set_pickable(value): 'value' needs to be a bool."
            )


class BoardItemVoid(BoardItem):
    """
    A class that represent a void cell.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    It is literally just a BoardItem but is subclassed for easier identification.

    It is however scanning its parent for the item's basic properties (overlappable,
    restorable, etc.)

    A component can never be pickable by itself.
    """

    def __init__(self, **kwargs):
        valid_kwargs_opts = [
            "sprixel",
            "model",
            "name",
            "item_type",
            "parent",
            "pickable",
            "overlappable",
            "restorable",
            "can_move",
            "pos",
            "value",
            "inventory_space",
            "animation",
            "particle_emitter",
        ]
        valid_kwargs = {}
        for opt in valid_kwargs_opts:
            if opt in kwargs:
                valid_kwargs[opt] = kwargs[opt]
        super().__init__(**valid_kwargs)
        self.__is_restorable = False
        self.__is_overlappable = False
        self.__can_move = False
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
        self.__is_pickable = False

    def pickable(self):
        """
        Returns False. A component is never pickable by itself (either the whole complex
        item is pickable or not, but not partially)

        Example::

            if item.item(4,5).pickable():
                print('The item is pickable')
        """
        return False


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
    :param size: The size of the item as [WIDTH, HEIGHT]. It impact movement and
       collision detection amongst other things. If it is left empty the Sprite size is
       used. If no sprite is given to the constructor the default size is 2x2.
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

    def __init__(
        self, sprite=None, size=None, null_sprixel=None, base_item_type=None, **kwargs
    ):
        self.__kwargs = kwargs
        self.name = "Board Multi Item"
        self.type = "multi_item"
        valid_kwargs_opts = [
            "sprixel",
            "model",
            "name",
            "item_type",
            "parent",
            "pickable",
            "overlappable",
            "restorable",
            "can_move",
            "pos",
            "value",
            "inventory_space",
            "animation",
            "particle_emitter",
        ]
        valid_kwargs = {}
        for opt in valid_kwargs_opts:
            if opt in kwargs:
                valid_kwargs[opt] = kwargs[opt]
        super().__init__(**valid_kwargs)
        self.__sprite = core.Sprite()
        if sprite is not None:
            self.__sprite = sprite
        self.null_sprixel = null_sprixel
        if self.null_sprixel is None:
            self.null_sprixel = core.Sprixel()
        self._size = size
        self._item_matrix = []
        # Not sure about that one
        # self.hit_box = []
        self.base_item_type = BoardItemComplexComponent
        if base_item_type is not None:
            self.base_item_type = base_item_type
        self.particle_emitter_position = [0, 0]
        # for item in ["sprite", "size", "null_sprixel", "base_item_type"]:
        #     if item in kwargs:
        #         setattr(self, item, kwargs[item])
        if self._size is None:
            self._size = self.__sprite.size
        if isinstance(self.__sprite, core.Sprite) and self.__sprite.parent is None:
            self.__sprite.parent = self
        self.update_sprite()

    def __repr__(self):  # pragma: no cover
        return self.__sprite.__repr__()

    def __str__(self):  # pragma: no cover
        return self.__sprite.__str__()

    @property
    def sprite(self):
        """A property to easily access and update a complex item's sprite.

        :param new_sprite: The sprite to set
        :type new_sprite: :class:`~pygamelib.gfx.core.Sprite`

        Example::

            npc1 = board_items.ComplexNpc(
                                            sprite=npc_sprite_collection['npc1_idle']
                                        )
            # to access the sprite:
            if npc1.sprite.width * npc1.sprite.height > CONSTANT_BIG_GUY:
                game.screen.place(
                    base.Text(
                        'Big boi detected!!!',
                        core.Color(255,0,0),
                        style=constants.BOLD,
                    ),
                    notifications.row,
                    notifications.column,
                )
            # And to set it:
            if game.player in game.neighbors(3, npc1):
                npc1.sprite = npc_sprite_collection['npc1_fight']
        """
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: core.Sprite):
        if isinstance(new_sprite, core.Sprite):
            self.__sprite = new_sprite
            self.update_sprite()

    def update_sprite(self):
        """
        Update the complex item with the current sprite.

        .. note:: This method use to need to be called every time the sprite was
           changed. Starting with version 1.3.0, it is no longer a requirement as
           BoardComplexItem.sprite was turned into a property that takes care of calling
           update_sprite().

        Example::

            item = BoardComplexItem(sprite=position_idle)
            for s in [walk_1, walk_2, walk_3, walk_4]:
                # This is not only no longer required but also wasteful as
                # update_sprite() is called twice here.
                item.sprite = s
                item.update_sprite()
                board.move(item, constants.RIGHT, 1)
                time.sleep(0.2)
        """
        self._item_matrix = []
        # Update sprite size.
        self.__sprite.calculate_size()
        for row in range(0, self.__sprite.size[1]):
            self._item_matrix.append([])
            for col in range(0, self.__sprite.size[0]):
                if (
                    self.null_sprixel is not None
                    and self.__sprite.sprixel(row, col) == self.null_sprixel
                ):
                    self._item_matrix[row].append(BoardItemVoid())
                    self._item_matrix[row][col].name = f"{self.name}_{row}_{col}"
                    self._item_matrix[row][col].parent = self
                else:
                    self._item_matrix[row].append(self.base_item_type(**self.__kwargs))
                    self._item_matrix[row][col].name = f"{self.name}_{row}_{col}"
                    self._item_matrix[row][col].model = self.__sprite.sprixel(
                        row, col
                    ).model
                    self._item_matrix[row][col].sprixel = self.__sprite.sprixel(
                        row, col
                    )
                    self._item_matrix[row][col].parent = self
        self._size = self.__sprite.size

    def item(self, row, column):
        """
        Return the item component at the row, column position if it is within the
        complex item's boundaries.

        :rtype: `~pygamelib.board_items.BoardItem`

        :raise `~pygamelib.base.PglOutOfBoardBoundException`: if row or column are
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

    def render_to_buffer(self, buffer, row, column, height, width):
        """Render the complex board item from the display buffer to the frame buffer.

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
        # For optimization's sakes we directly loop through the right places in the
        # buffer and simply translate the coordinates back to the sprite.
        # The loops takes clamped value to not render anything out of the buffer.
        for sr in range(row, min(self.__sprite.size[1] + row, height)):
            for sc in range(column, min(self.__sprite.size[0] + column, width)):
                # TODO: If the Sprite has sprixels with length > 1 this is going to be
                # A mess.
                buffer[sr][sc] = self.__sprite.sprixel(sr - row, sc - column).__repr__()

    def serialize(self) -> dict:
        """Return a dictionary with all the attributes of this object.

        :return: A dictionary with all the attributes of this object.
        :rtype: dict
        """
        ret_data = super().serialize()
        ret_data["sprite"] = self.sprite.serialize()
        ret_data["size"] = self.size
        if self.null_sprixel is not None and isinstance(
            self.null_sprixel, core.Sprixel
        ):
            ret_data["null_sprixel"] = self.null_sprixel.serialize()
        ret_data["base_item_type"] = str(self.base_item_type)
        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new BoardComplexItem out of it.

        :param data: Data to create a new complex item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex item.
        :rtype: `~pygamelib.board_items.BoardComplexItem`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        fields = ["sprite", "size", "base_item_type"]
        for field in fields:
            if field not in data.keys():
                data[field] = None
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


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

    def __init__(
        self,
        step: int = None,
        step_vertical: int = None,
        step_horizontal: int = None,
        movement_speed: float = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # We probably need the item to store its own velocity at some point
        # self.velocity = base.Vector2d(0,0)
        # Set default values
        self.step_horizontal = 1
        if step_horizontal is not None:
            self.step_horizontal = step_horizontal
        self.step_vertical = 1
        if step_vertical is not None:
            self.step_vertical = step_vertical
        self.step = 1
        if step is not None:
            self.step = step
        self.movement_speed = 1.0
        if movement_speed is not None:
            self.movement_speed = movement_speed

        self._movement_vector = base.Vector2D(self.step_vertical, self.step_horizontal)
        self._accumulator = base.Vector2D(0.0, 0.0)

        # TODO: That's initial thought for physic i the pygamelib. For future reference.
        # if velocity is not None:
        #     self.velocity = velocity
        # else:
        #     self.velocity = base.Vector2D()
        # if ignore_physic is not None:
        #     self.ignore_physic = ignore_physic
        # else:
        #     self.ignore_physic = False

        # Now if only step is set and it's not 1, set the correct value for the 2 others
        if step_vertical is None and self.step != 1:
            self.step_vertical = self.step

        if step_horizontal is None and self.step != 1:
            self.step_horizontal = self.step
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

    def serialize(self) -> dict:
        """Serialize the Immovable object.

        This returns a dictionary that contains all the key/value pairs that makes up
        the object.

        """
        ret_data = super().serialize()
        ret_data["step"] = self.step
        ret_data["step_horizontal"] = self.step_horizontal
        ret_data["step_vertical"] = self.step_vertical
        ret_data["movement_speed"] = self.movement_speed

        if hasattr(self, "has_inventory"):
            try:
                ret_data["has_inventory"] = self.has_inventory()
            except NotImplementedError:
                pass

        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new Movable out of it.

        :param data: Data to create a new movable item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex item.
        :rtype: `~pygamelib.board_items.Movable`
        """
        itm = super().load(data)
        itm.step = data["step"]
        itm.step_horizontal = data["step_horizontal"]
        itm.step_vertical = data["step_vertical"]
        itm.movement_speed = data["movement_speed"]
        return itm

    def can_move(self) -> bool:
        """
        Movable implements can_move().

        :return: True
        :rtype: Boolean
        """
        return True

    def has_inventory(self) -> bool:
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
    :param collision_exclusions: A list of **TYPES** of objects that should not collides
       with that projectile. It is usually a good idea to put the projectile type in the
       exclusion list. This prevent the projectile to collide with other instances of
       itself. Adding the projectile's emitter is also a valid idea.
    :type collision_exclusions: list
    :param parent: The parent object (usually a Board object or some sort of BoardItem).

    .. important:: The effects of a Projectile are determined by the callback. No
        callback == no effect!

    Example::

        fireball = Projectile(
                                name="fireball",
                                model=Utils.red_bright(black_circle),
                                hit_model=graphics.Models.EXPLOSION,
                                # won't collide with other projectiles.
                                collision_exclusions = [Projectile],
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
        callback_parameters=None,
        movement_speed=0.15,
        collision_exclusions=None,
        **kwargs,
    ):
        if range % step != 0:
            raise base.PglException(
                "incorrect_range_step",
                "Range must be a factor of step in Projectile (or else it might never "
                "reach its target).",
            )
        super().__init__(
            model=model,
            step=step,
            name=name,
            parent=parent,
            movement_speed=movement_speed,
            **kwargs,
        )
        self._direction = direction
        self.range = range
        self.movement_animation = movement_animation
        self._directional_animations = {}
        self._directional_models = {}
        self.hit_animation = hit_animation
        self.hit_model = hit_model
        self.hit_callback = hit_callback
        if callback_parameters is None:
            callback_parameters = []
        self.callback_parameters = callback_parameters
        if collision_exclusions is None:
            collision_exclusions = []
        self.collision_exclusions = collision_exclusions
        self.actuator = actuators.UnidirectionalActuator(direction=direction)
        self.is_aoe = is_aoe
        self.aoe_radius = aoe_radius
        self.parent = parent

    @property
    def direction(self):
        """The direction of the projectile.

        Updating this property also updates the UnidirectionalActuator's direction.

        :param value: some param
        :type value: int | :class:`~pygamelib.base.Vector2D`

        .. warning:: If your projectile uses directional model and/or animation you
           should use :py:meth:`set_direction` to set the projectile direction.

        Example::

            bullet.direction = Vector2D(0, 1)
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self.actuator.direction = value

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

            fireball.add_directional_animation(constants.UP, upward_animation)
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
        if type(direction) is not int and not isinstance(direction, base.Vector2D):
            raise base.PglInvalidTypeException(
                "Projectile.set_direction(direction): "
                "requires an int from the constants module or a Vector2D as direction."
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
    This class derive :class:`BoardItem` and describe an object that cannot move or be
    moved (like a wall).
    :func:`~BoardItem.can_move` cannot be configured and return False. The other
    properties can be configured. They have the same default values than
    :class:`BoardItem`.

    :param inventory_space: The space the immovable item takes into an
       :class:`~pygamelib.engine.Inventory` (in case the item is pickable). By default
       it is 0.
    :type inventory_space: int
    """

    def __init__(self, inventory_space: int = None, **kwargs):
        super().__init__(**kwargs)
        if inventory_space is None:
            self._inventory_space = 0
        else:
            self._inventory_space = inventory_space

    def can_move(self):
        """Return the capability of moving of an item.

        Obviously an Immovable item is not capable of moving. So that method
        always returns False.

        :return: False
        :rtype: bool
        """
        return False

    @property
    def inventory_space(self):
        """Return the size that the Immovable item takes
        in the :class:`~pygamelib.engine.Inventory`.

        :return: The size of the item.
        :rtype: int
        """
        return self._inventory_space

    @inventory_space.setter
    def inventory_space(self, value):
        if type(value) is int:
            self._inventory_space = value
        else:
            raise base.PglInvalidTypeException(
                "Immovable.inventory_space.(value): value needs to be an int."
            )


class Actionable(Immovable):
    """
    This class derives :class:`~pygamelib.board_items.Immovable`. It adds the
    ability to an Immovable BoardItem to be triggered and execute some code.

    If an actionable board item is activated by an item (this mechanism is taken care of
    by the Board class), the function passed as the `action` parameter is called with
    `action_parameters` as parameters. Subclass may implement a different mechanism for
    activation so please read their documentations.

    :param action: the reference to a function (Attention: no parentheses at
        the end of the function name). It needs to be callable.
    :type action: function
    :param action_parameters: the parameters to the action function.
    :type action_parameters: list
    :param perm: The permission that defines what types of items can actually
        activate the actionable. The permission has to be one of the
        permissions defined in :mod:`~pygamelib.constants`. By default it is set to
        constants.PLAYER_AUTHORIZED.
    :type perm: :mod:`~pygamelib.constants`

    On top of these parameters Actionable accepts all parameters from
    :class:`~pygamelib.board_items.Immovable` and therefor from
    :class:`~pygamelib.board_items.BoardItem`.

    .. note:: The common way to use this class is to use
        GenericActionableStructure. Please refer to
        :class:`~pygamelib.board_items.GenericActionableStructure`
        for more details.

    .. important:: There's a complete tutorial about Actionable items on the pygamelib
       `wiki <https://github.com/pygamelib/pygamelib/wiki/Actionable-Items>`_
    """

    def __init__(self, action=None, action_parameters=None, perm=None, **kwargs):
        super().__init__(**kwargs)
        self.action = None
        if action is not None and callable(action):
            self.action = action
        self.action_parameters = []
        if action_parameters is not None:
            self.action_parameters = action_parameters
        self.perm = constants.PLAYER_AUTHORIZED
        if perm is not None:
            self.perm = perm

    def activate(self):
        """
        This function is calling the action function with the
        action_parameters.

        The `action` callback function should therefor have a signature like:

            ``def my_callback_function(actionable, action_parameters)``

        With `actionable` being the Actionable current reference to `self`.

        Usually it's automatically called by :meth:`~pygamelib.engine.Board.move`
        when a Player or NPC (see :mod:`~pygamelib.board_items`)
        """
        if self.action is not None:
            self.action(self.action_parameters)


class Character(Movable):
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

    def __init__(
        self,
        max_hp=None,
        hp=None,
        max_mp=None,
        mp=None,
        remaining_lives=None,
        attack_power=None,
        defense_power=None,
        strength=None,
        intelligence=None,
        agility=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_hp = None
        if max_hp is not None:
            self.max_hp = max_hp
        self.hp = None
        if hp is not None:
            self.hp = hp
        elif max_hp is not None:
            self.hp = max_hp
        self.max_mp = None
        if max_mp is not None:
            self.max_mp = max_mp
        self.mp = None
        if mp is not None:
            self.mp = mp
        self.remaining_lives = None
        if remaining_lives is not None:
            self.remaining_lives = remaining_lives
        self.attack_power = None
        if attack_power is not None:
            self.attack_power = attack_power
        self.defense_power = None
        if defense_power is not None:
            self.defense_power = defense_power
        self.strength = None
        if strength is not None:
            self.strength = strength
        self.intelligence = None
        if intelligence is not None:
            self.intelligence = intelligence
        self.agility = None
        if agility is not None:
            self.agility = agility

    def serialize(self) -> dict:
        """Serialize the Character object.

        This returns a dictionary that contains all the key/value pairs that makes up
        the object.

        """
        ret_data = super().serialize()
        keys = [
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
        ]
        for key in keys:
            ret_data[key] = getattr(self, key)

        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new Character out of it.

        :param data: Data to create a new character item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new character item.
        :rtype: `~pygamelib.board_items.Character`
        """
        itm = super().load(data)
        keys = [
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
        ]
        for key in keys:
            if key in data.keys():
                setattr(itm, key, data[key])
        return itm


class Player(Character):
    """
    A class that represent a player controlled by a human.

    This can take all parameter from :class:`~pygamelib.board_items.Character`,
    :class:`~pygamelib.board_items.Movable` and obviously
    :class:`~pygamelib.board_items.BoardItem`.

    It is a specific board item as the whole Game class assumes only one player. Aside
    from the wrapper functions (like Game.move_player for example), there is no reel
    limitations to use more than one player.

    The player also has a couple of attributes that are added for your convenience. You
    are free to use them or not. They are (name and default value):

     * max_hp: 100
     * hp: 100
     * remaining_lives: 3
     * attack_power: 10
     * movement_speed: 0.1 (one movement every 0.1 second). Only useful if the game mode
         is set to MODE_RT.
     * inventory: A :class:`~pygamelib.engine.Inventory` object. If none is provided,
          one is created automatically.

    A player can be animated by providing a :class:`~pygamelib.gfx.core.Animation`
    object to its `animation` attribute.

    Like all other board items, you can specify a `sprixel` attribute that will be the
    representation of the player on the board.

    Example::

        player = Player(
            name="Player",
            # A sprixel with "@" as the model, no background color, a cyan foreground
            # color and we set the background to be transparent.
            sprixel=core.Sprixel("@", None, core.Color(0, 255, 255), True),
            max_hp=200,
        )

    """

    def __init__(self, inventory=None, **kwargs):
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
        super().__init__(**kwargs)
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = engine.Inventory(parent=self)

    def pickable(self):
        """This method returns False (a player is obviously not pickable)."""
        return False

    def has_inventory(self):
        """This method returns True (a player has an inventory)."""
        return True

    # NOTE: This is an arbitrary decision, there is no reason for a player object to
    #       behave like that.
    # def overlappable(self):
    #     """This method returns false (a player cannot be overlapped).

    #     .. note:: If you wish your player to be overlappable, you need to inherit from
    #         that class and re-implement overlappable().
    #     """
    #     return False


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
        super().__init__(**kwargs)

    @classmethod
    def load(cls, data):
        """Load data and create a new ComplexPlayer out of it.

        :param data: Data to create a new complex player (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.ComplexPlayer`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


class NPC(Character):
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

    def __init__(self, actuator=None, **kwargs):
        if "max_hp" not in kwargs.keys():
            kwargs["max_hp"] = 10
        if "hp" not in kwargs.keys():
            kwargs["hp"] = 10
        if "remaining_lives" not in kwargs.keys():
            kwargs["remaining_lives"] = 1
        if "attack_power" not in kwargs.keys():
            kwargs["attack_power"] = 5
        if "movement_speed" not in kwargs.keys():
            kwargs["movement_speed"] = 0.2
        super().__init__(**kwargs)
        # TODO: actuator should be a property that sets automatically the
        # parent/actuated_object
        self.actuator = None
        if actuator is not None:
            self.actuator = actuator

        # NOTE: Useless, it is done in Movable
        # if "step" not in kwargs.keys():
        #     self.step = 1
        # else:
        #     self.step = kwargs["step"]

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

    def serialize(self) -> dict:
        """
        Serialize the NPC object.

        This returns a dictionary that contains all the key/value pairs that makes up
        the object.
        """
        ret_data = super().serialize()
        if self.actuator is not None:
            ret_data["actuator"] = self.actuator.serialize()
        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new NPC out of it.

        :param data: Data to create a new npc (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new npc.
        :rtype: `~pygamelib.board_items.NPC`
        """
        fields = [
            "restorable",
            "overlappable",
            "pickable",
            "can_move",
            "inventory_space",
            "value",
            "name",
            "model",
            "type",
            "pos",
            "step",
            "step_horizontal",
            "step_vertical",
            "movement_speed",
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
        ]
        for field in fields:
            if field not in data.keys():
                data[field] = None
        if "sprixel" not in data.keys():
            data["sprixel"] = {
                "model": "",
                "fg_color": None,
                "bg_color": None,
                "is_bg_transparent": True,
            }
        itm = cls(
            restorable=data["restorable"],
            overlappable=data["overlappable"],
            pickable=data["pickable"],
            can_move=data["can_move"],
            inventory_space=data["inventory_space"],
            value=data["value"],
            name=data["name"],
            model=data["model"],
            item_type=data["type"],
            pos=data["pos"],
            step=data["step"],
            step_horizontal=data["step_horizontal"],
            step_vertical=data["step_vertical"],
            movement_speed=data["movement_speed"],
            max_hp=data["max_hp"],
            hp=data["hp"],
            max_mp=data["max_mp"],
            mp=data["mp"],
            remaining_lives=data["remaining_lives"],
            attack_power=data["attack_power"],
            defense_power=data["defense_power"],
            strength=data["strength"],
            intelligence=data["intelligence"],
            agility=data["agility"],
            sprixel=core.Sprixel.load(data["sprixel"]),
        )
        if "actuator" in data.keys() and data["actuator"]["type"] in dir(actuators):
            act = eval(f"actuators.{data['actuator']['type']}")
            itm.actuator = act.load(data["actuator"])
        return itm


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
        super().__init__(**kwargs)

    @classmethod
    def load(cls, data):
        """Load data and create a new ComplexNPC out of it.

        :param data: Data to create a new complex npc (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.ComplexNPC`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        if "actuator" in data.keys() and data["actuator"]["type"] in dir(actuators):
            act = eval(f"actuators.{data['actuator']['type']}")
            itm.actuator = act.load(data["actuator"])
        return itm


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
        super().__init__(**kwargs)
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

    def __repr__(self):  # pragma: no cover
        return self._text.__repr__()

    def serialize(self) -> dict:
        """Return a dictionary with all the attributes of this object.

        :return: A dictionary with all the attributes of this object.
        :rtype: dict
        """
        ret_data = super().serialize()
        ret_data["text"] = self._text.serialize()
        return ret_data

    @classmethod
    def load(cls, data):
        """Load data and create a new TextItem out of it.

        :param data: Data to create a new text item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.TextItem`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "text" in data.keys():
            data["text"] = base.Text.load(data["text"])
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm

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
        if "sprixel" not in kwargs and "model" in kwargs:
            kwargs["sprixel"] = core.Sprixel(kwargs["model"])
        elif "sprixel" not in kwargs.keys():
            kwargs["sprixel"] = core.Sprixel("#")
        if "name" not in kwargs.keys():
            kwargs["name"] = "wall"
        # Deprecated (size is 1 for BoardItems)
        # if "size" not in kwargs.keys():
        #     kwargs["size"] = 1
        super().__init__(**kwargs)

    def pickable(self):
        """This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
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
        """This represent the capacity for a :class:`~pygamelib.board_items.BoardItem` to
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
        super().__init__(**kwargs)

    @classmethod
    def load(cls, data):
        """Load data and create a new ComplexWall out of it.

        :param data: Data to create a new complex wall item (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.ComplexWall`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


class GenericStructure(Immovable):
    """
    A GenericStructure is as the name suggest, a generic object to create all kind of
    structures.

    It can be tweaked with all the properties of
    :class:`~pygamelib.board_items.BoardItem`, :class:`~pygamelib.board_items.Immovable`
    and it can be made pickable, overlappable or restorable or any combination of these.

    If you need an action to be done when a Player and/or a NPC touch the structure
    please have a look at :class:`pygamelib.board_items.GenericActionableStructure`.

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
    :param value: The value of the structure. It can be used for scoring, resource
       spending, etc.
    :type value: int|float

    On top of these, this object takes all parameters of
    :class:`~pygamelib.board_items.BoardItem` and
    :class:`~pygamelib.board_items.Immovable`

    .. important:: If you need a structure with a permission system please have a look
        at :class:`~pygamelib.board_items.GenericActionableStructure`. This class
        has a permission system for activation.

    """

    def __init__(self, value=0, **kwargs):
        if "sprixel" not in kwargs and "model" in kwargs:
            kwargs["sprixel"] = core.Sprixel(kwargs["model"])
        elif "sprixel" not in kwargs.keys():
            kwargs["sprixel"] = core.Sprixel("#")
        if "name" not in kwargs.keys():
            kwargs["name"] = "structure"
        if "pickable" not in kwargs.keys():
            kwargs["pickable"] = False
        if "restorable" not in kwargs.keys():
            kwargs["restorable"] = False
        if "overlappable" not in kwargs.keys():
            kwargs["overlappable"] = False

        super().__init__(**kwargs)
        self.value = value


class GenericActionableStructure(GenericStructure, Actionable):
    """
    A GenericActionableStructure is the combination of a
    :class:`~pygamelib.board_items.GenericStructure` and an
    :class:`~pygamelib.board_items.Actionable`.
    It is only a helper combination.

    Please see the documentation for
    :class:`~pygamelib.board_items.GenericStructure` and
    :class:`~pygamelib.board_items.Actionable` for more information.

    .. important:: There's a complete tutorial about Actionable items on the pygamelib
       `wiki <https://github.com/pygamelib/pygamelib/wiki/Actionable-Items>`_
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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

        money_bag = Treasure(
            model=graphics.Models.MONEY_BAG,value=100,inventory_space=2
        )
        print(f"This is a money bag {money_bag}")
        player.inventory.add_item(money_bag)
        print(f"The inventory value is {player.inventory.value()} and is at
            {player.inventory.size()}/{player.inventory.max_size}")
    """

    def __init__(self, value=10, **kwargs):
        if "sprixel" not in kwargs:
            if "model" in kwargs:
                kwargs["sprixel"] = core.Sprixel(kwargs["model"])
            else:
                kwargs["sprixel"] = core.Sprixel("¤")
        if "inventory_space" not in kwargs.keys():
            kwargs["inventory_space"] = 1
        super().__init__(**kwargs)
        self.value = value

    def pickable(self):
        """This represent the capacity for a Treasure to be picked-up by player or NPC.

        A treasure is obviously pickable by the player and potentially NPCs.
        :class:`~pygamelib.engine.Board` puts the Treasure in the
        :class:`~pygamelib.engine.Inventory` if the picker implements has_inventory()

        :return: True
        :rtype: bool
        """
        return True

    def overlappable(self):
        """This represent the capacity for a Treasure to be overlapped by player or NPC.

        A treasure is not overlappable.

        :return: False
        :rtype: bool
        """
        return False

    def restorable(self):
        """This represent the capacity for a Treasure to be restored after being overlapped.

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
        super().__init__(**kwargs)

    @classmethod
    def load(cls, data):
        """Load data and create a new ComplexTreasure out of it.

        :param data: Data to create a new complex treasure (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.ComplexTreasure`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


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

        door1 = Door(model=graphics.Models.DOOR,type='locked_door')
    """

    def __init__(self, **kwargs):
        if "sprixel" not in kwargs and "model" in kwargs:
            kwargs["sprixel"] = core.Sprixel(kwargs["model"])
        elif "sprixel" not in kwargs:
            kwargs["sprixel"] = core.Sprixel("]")
        if "value" not in kwargs.keys():
            kwargs["value"] = 0
        if "inventory_space" not in kwargs:
            kwargs["inventory_space"] = 1
        if "name" not in kwargs:
            kwargs["name"] = "Door"
        if "item_type" not in kwargs:
            kwargs["item_type"] = "door"
        if "pickable" not in kwargs:
            kwargs["pickable"] = False
        if "overlappable" not in kwargs:
            kwargs["overlappable"] = True
        if "restorable" not in kwargs:
            kwargs["restorable"] = True
        super().__init__(**kwargs)


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
        super().__init__(**kwargs)

    @classmethod
    def load(cls, data):
        """Load data and create a new ComplexDoor out of it.

        :param data: Data to create a new complex door (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.ComplexDoor`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


class GenericStructureComplexComponent(GenericStructure, BoardItemComplexComponent):
    """
    A ComplexComponent specifically for generic structures.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Tile(BoardComplexItem, GenericStructure):
    """
    .. versionadded:: 1.2.0

    A Tile is a standard :class:`BoardComplexItem` configured by default to:

     * be overlappable
     * be restorable
     * be not pickable
     * be immovable.

    Aside from the movable attributes (it inherit from GenericStructure so it's an
    Immovable object), everything else is configurable.

    It is particularly useful to display a :class:`~pygamelib.gfx.core.Sprite` on the
    background or to create terrain.

    Example::

        grass_sprite = Sprite.load_from_ansi_file('textures/grass.ans')
        for pos in grass_positions:
            outdoor_level.place_item( Tile(sprite=grass_sprite), pos[0], pos[1] )
    """

    def __init__(self, **kwargs):
        """
        :param overlappable: Defines if the Tile can be overlapped.
        :type overlappable: bool
        :param restorable: Defines is the Tile should be restored after being
           overlapped.
        :type restorable: bool
        :param pickable: Defines if the Tile can be picked up by the Player or NPC.
        :type pickable: bool

        Please see :class:`BoardComplexItem` for additional parameters.
        """
        kwargs["parent"] = self
        kwargs["base_item_type"] = GenericStructureComplexComponent
        if "overlappable" not in kwargs:
            kwargs["overlappable"] = True
        if "restorable" not in kwargs:
            kwargs["restorable"] = True
        if "pickable" not in kwargs:
            kwargs["pickable"] = False
        super().__init__(**kwargs)
        # kwargs["base_item_type"] = Door

    def can_move(self):
        """A Tile cannot move.

        :returns: False
        :rtype: bool
        """
        return False

    @classmethod
    def load(cls, data):
        """Load data and create a new Tile out of it.

        :param data: Data to create a new tile (usually generated by
           :meth:`serialize()`)
        :type data: dict

        :return: A new complex npc.
        :rtype: `~pygamelib.board_items.Tile`
        """
        obj = data["base_item_type"].split("'")[-2]
        del data["object"]
        del data["base_item_type"]
        if "type" in data.keys():
            data["item_type"] = data["type"]
            del data["type"]
        if "has_inventory" in data.keys():
            del data["has_inventory"]
        if "sprixel" in data.keys():
            data["sprixel"] = core.Sprixel.load(data["sprixel"])
        if "sprite" in data.keys() and data["sprite"] is not None:
            data["sprite"] = core.Sprite.load(data["sprite"])
        if "null_sprixel" in data.keys():
            data["null_sprixel"] = core.Sprixel.load(data["null_sprixel"])
        else:
            data["null_sprixel"] = None
        itm = cls(**data)
        exec("import pygamelib")
        itm.base_item_type = eval(f"{obj}")
        return itm


class ActionableTile(Actionable, Tile):
    """
    The ActionableTile is the complex (i.e: multi-cells items) version of the
    :class:`GenericActionableStructure`. It allows you to create any type of in game
    object that is represented with more than one character in the terminal and that is
    :class:`Actionable`.
    Actionable object have a callback system that is automatically called when the
    player collide with the object.

    .. important:: There's a complete tutorial about Actionable items on the pygamelib
       `wiki <https://github.com/pygamelib/pygamelib/wiki/Actionable-Items>`_
    """

    def __init__(self, **kwargs):
        """
        Please have a look at the documentation for :class:`Tile` and
        :class:`Actionable` for the list of possible constructor's parameters.
        """
        super().__init__(**kwargs)


class Camera(Movable):
    """
    .. versionadded:: 1.3.0

    A Camera is a special item: it does not appear on the Board and actually is not even
    registered on it. It is only an item that you can center the board on (when using
    partial display). It helps for cut scenes for example.

    The main difference with a regular BoardItem is that the row and column properties
    are writable. This means that you can directly manipulate its coordinates and
    partially render a huge board around that focal point.

    The :class:`~pygamelib.engine.Screen` buffer rendering system introduced in version
    1.3.0 require a board item to be declared as the focus point of the
    board if partial display is enabled.

    The Camera object inherits from Movable and can accept an actuator parameter.
    However, it is up to the developer to activate the actuators mechanics as the
    Camera object does not register as a NPC or a Player.
    The support for actuators is mainly thought for pre-scripted cut-scenes.

    Example::

        # This example leverage the Screen buffer system introduced in v1.3.0.
        # It pans the camera over a huge map. The Screen.update() method automatically
        # uses the Board.partial_display_focus coordinates to adjust the displayed area.
        camera = Camera()
        huge_board.partial_display_focus = camera
        while camera.column < huge_board.width:
            camera.column += 1
            game.screen.update()
    """

    def __init__(self, actuator=None, **kwargs):
        super().__init__(**kwargs)
        self.model = ""
        self.sprixel = core.Sprixel("", None, None, True)
        self.actuator = None
        if actuator is not None:
            self.actuator = actuator

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

    @row.setter
    def row(self, val):
        if type(val) is int:
            self.store_position(val, self.pos[1])

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

    @column.setter
    def column(self, val):
        if type(val) is int:
            self.store_position(self.pos[0], val)

    def has_inventory(self) -> bool:
        return False
