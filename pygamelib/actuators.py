"""This module contains the base classes for simple and advanced actuators.
These classes are the base contract for actuators.
If you wish to create your own one, you need to inheritate from one of these base class.

This module contains the simple actuators classes.
Simple actuators are movement related one. They allow for predetermined movements
patterns.

.. autosummary::
   :toctree: .

    Actuator
    Behavioral
    RandomActuator
    PathActuator
    PatrolActuator
    UnidirectionalActuator
    PathFinder

"""
from pygamelib import board_items
from pygamelib import base
from pygamelib import constants
import random
import collections


class Actuator:
    """
    Actuator is the base class for all Actuators. It is mainly a contract class with
    some utility methods.

    By default, all actuators are considered movement actuators. So the base class only
    require next_move() to be implemented.

    :param parent: the item parent.

    """

    def __init__(self, parent):
        """
        The constructor take only one (positional) parameter: the parent object.

        .. important:: The default state of ALL actuators is RUNNING. If you want your
            actuator to be in a different state (PAUSED for example), you have to do it
            yourself.
        """
        self.type = None
        self.state = constants.RUNNING
        self.parent = parent

    def start(self):
        """Set the actuator state to RUNNING.

        If the actuator state is not RUNNING, actuators' next_move() function
        (and all derivatives) should not return anything.

        Example::

            mygame.start()
        """
        self.state = constants.RUNNING

    def pause(self):
        """Set the actuator state to PAUSED.

        Example::

            mygame.pause()
        """
        self.state = constants.PAUSED

    def stop(self):
        """Set the actuator state to STOPPED.

        Example::

            mygame.stop()
        """
        self.state = constants.STOPPED

    def next_move(self):
        """
        That method needs to be implemented by all actuators or a NotImplementedError
        exception will be raised.

        :raises: NotImplementedError
        """
        raise NotImplementedError()


class Behavioral(Actuator):
    """
    The behavioral actuator is inheriting from Actuator and is adding a next_action()
    method.
    The actual actions are left to the actuator that implements Behavioral.

    :param parent: the item parent.

    """

    def __init__(self, parent):
        """
        The constructor simply construct an Actuator. It takes on positional paraneter:
        the parent object.
        """
        Actuator.__init__(self, parent)

    def next_action(self):
        """
        That method needs to be implemented by all behavioral actuators or a
        NotImplementedError exception will be raised.

        :raises: NotImplementedError
        """
        raise NotImplementedError()


class RandomActuator(Actuator):
    """A class that implements a random choice of movement.

    The random actuator is a subclass of
    :class:`~pygamelib.actuators.Actuator`.
    It is simply implementing a random choice in a predefined move set.

    :param moveset: A list of movements.
    :type moveset: list
    :param parent: The parent object to actuate.
    :type parent: pygamelib.board_items.BoardItem
    """

    def __init__(self, moveset=None, parent=None):
        if moveset is None:
            moveset = []
        super().__init__(parent)
        self.moveset = moveset

    def next_move(self):
        """Return a randomly selected movement

        The movement is randomly selected from moveset if state is RUNNING,
        otherwise it should return None.

        :return: The next movement
        :rtype: int | None

        Example::

            randomactuator.next_move()
        """
        if self.state == constants.RUNNING:
            return random.choice(self.moveset)


class PathActuator(Actuator):
    """
    The path actuator is a subclass of
    :class:`~pygamelib.actuators.Actuator`.
    The move inside the function next_move
    depends on path and index. If the state is not running it returns None
    otherwise it increments the index & then, further compares the index
    with length of the path. If they both are same then, index is set to
    value zero and the move is returned back.

    :param path: A list of paths.
    :type path: list
    :param parent: The parent object to actuate.
    :type parent: pygamelib.board_items.BoardItem
    """

    def __init__(self, path=None, parent=None):
        if path is None:
            path = []  # pragma: no cover
        super().__init__(parent)
        self.path = path
        self.index = 0

    def next_move(self):
        """Return the movement based on current index

        The movement is selected from path if state is RUNNING, otherwise
        it should return None. When state is RUNNING, the movement is selected
        before incrementing the index by 1. When the index equal the length of
        path, the index should return back to 0.

        :return: The next movement
        :rtype: int | None

        Example::

            pathactuator.next_move()
        """
        if self.state == constants.RUNNING:
            move = self.path[self.index]
            self.index += 1
            if self.index == len(self.path):
                self.index = 0
            return move

    def set_path(self, path):
        """Defines a new path

        This will also reset the index back to 0.

        :param path: A list of movements.
        :type path: list

        Example::

            pathactuator.set_path([constants.UP,constants.DOWN,constants.LEFT,constants.RIGHT])
        """
        self.path = path
        self.index = 0


class PatrolActuator(PathActuator):
    """
    The patrol actuator is a subclass of
    :class:`~pygamelib.actuators.PathActuator`.  The move inside the function
    next_move depends on path and index and the mode. Once it reaches the end
    of the move list it will start cycling back to the beggining of the list.
    Once it reaches the beggining it will start moving forwards
    If the state is not running it returns None otherwise it increments the
    index & then, further compares the index with length of the path.
    If they both are same then, index is set to value zero and the move is
    returned back.

    :param path: A list of directions.
    :type path: list
    """

    def next_move(self):
        """Return the movement based on current index

        The movement is selected from path if state is RUNNING, otherwise it
        should return None. When state is RUNNING, the movement is selected
        before incrementing the index by 1. When the index equals the length
        of path, the index should return back to 0 and the path list should be
        reversed before the next call.

        :return: The next movement
        :rtype: int | None

        Example::

            patrolactuator.next_move()
        """
        if self.state == constants.RUNNING:
            move = self.path[self.index]
            self.index += 1
            if self.index == len(self.path):
                self.index = 0
                self.path.reverse()
                for i in range(0, len(self.path)):
                    if self.path[i] == constants.UP:
                        self.path[i] = constants.DOWN
                    elif self.path[i] == constants.DOWN:
                        self.path[i] = constants.UP
                    elif self.path[i] == constants.LEFT:
                        self.path[i] = constants.RIGHT
                    elif self.path[i] == constants.RIGHT:
                        self.path[i] = constants.LEFT
                    elif self.path[i] == constants.DLDOWN:
                        self.path[i] = constants.DRUP
                    elif self.path[i] == constants.DLUP:
                        self.path[i] = constants.DRDOWN
                    elif self.path[i] == constants.DRDOWN:
                        self.path[i] = constants.DLUP
                    elif self.path[i] == constants.DRUP:
                        self.path[i] = constants.DLDOWN
            return move


class UnidirectionalActuator(Actuator):
    """A class that implements a single movement.

    The unidirectional actuator is a subclass of
    :class:`~pygamelib.actuators.Actuator`.
    It is simply implementing a mono directional movement. It is primarily target at
    projectiles.

    :param direction: A single direction from the Constants module.
    :type direction: int
    :param parent: The parent object to actuate.
    :type parent: pygamelib.board_items.BoardItem
    """

    def __init__(self, direction=constants.RIGHT, parent=None):
        if direction is None:
            direction = constants.RIGHT
        super().__init__(parent)
        self.direction = direction

    def next_move(self):
        """Return the direction.

        The movement is always direction if state is RUNNING,
        otherwise it returns None.

        :return: The next movement
        :rtype: int | None

        Example::

            unidirectional_actuator.next_move()
        """
        if self.state == constants.RUNNING:
            return self.direction


class PathFinder(Behavioral):
    """
    .. important:: This module assume a one step movement.
        If you need more than one step, you will need to sub-class
        this module and re-implement next_waypoint().

    This actuator is a bit different than the simple actuators
    (:mod:`~pygamelib.actuators.SimpleActuators`) as it requires
    the knowledge of both the game object and the actuated object.

    The constructor takes the following parameters:

    :param game: A reference to the instanciated game engine.
    :type game: pygamelib.engine.Game
    :param actuated_object: The object to actuate. Deprecated in favor of parent.
        Only kept for backward compatibility.
    :type actuated_object: pygamelib.board_items.BoardItem
    :param parent: The parent object to actuate.
    :type parent: pygamelib.board_items.BoardItem
    :param circle_waypoints: If True the next_waypoint()
        method is going to circle between the waypoints
        (when the last is visited, go back to the first)
    :type circle_waypoints: bool

    """

    def __init__(
        self, game=None, actuated_object=None, circle_waypoints=True, parent=None
    ):
        if actuated_object is not None and parent is None:
            self.actuated_object = actuated_object
            self.parent = actuated_object
        elif parent is not None:
            self.actuated_object = parent
            self.parent = parent
        super().__init__(self.parent)
        self.destination = (None, None)
        self.game = game
        self._current_path = []
        self.waypoints = []
        self._waypoint_index = 0
        self.circle_waypoints = circle_waypoints

    def set_destination(self, row=0, column=0):
        """Set the targeted destination.

        :param row: "row" coordinate on the board grid
        :type row: int
        :param column: "column" coordinate on the board grid
        :type column: int
        :raises PglInvalidTypeException: if row or column are not int.

        Example::

            mykillernpc.actuator.set_destination(
                mygame.player.pos[0], mygame.player.pos[1]
            )
        """
        if type(row) is not int or type(column) is not int:
            raise base.PglInvalidTypeException(
                "In Actuator.PathFinder.set_destination(x,y) both x and y must be "
                "integer."
            )
        self.destination = (row, column)

    def find_path(self):
        """Find a path to the destination.

        Destination (PathFinder.destination) has to be set beforehand.
        This method implements a Breadth First Search algorithm
        (`Wikipedia <https://en.wikipedia.org/wiki/Breadth-first_search>`_)
        to find the shortest path to destination.

        Example::

            mykillernpc.actuator = PathFinder(
                    game=mygame, actuated_object=mykillernpc
                )
            mykillernpc.actuator.set_destination(
                    mygame.player.pos[0], mygame.player.pos[1]
                )
            mykillernpc.actuator.find_path()

        .. warning:: PathFinder.destination is a tuple!
            Please use PathFinder.set_destination(x,y) to avoid problems.

        """
        if self.actuated_object is None:
            raise base.PglException(
                "actuated_object is not defined",
                "PathFinder.actuated_object has to be defined.",
            )
        if not isinstance(self.actuated_object, board_items.Movable):
            raise base.PglException(
                "actuated_object not a Movable object",
                "PathFinder.actuated_object has to be an instance \
                of a Movable object.",
            )
        if self.destination is None:
            raise base.PglException(
                "destination is not defined",
                "PathFinder.destination has to be defined.",
            )

        queue = collections.deque(
            [[(self.actuated_object.pos[0], self.actuated_object.pos[1])]]
        )
        seen = set([(self.actuated_object.pos[0], self.actuated_object.pos[1])])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if (x, y) == self.destination:
                self._current_path = path
                # We return only a copy of the path as we need to keep the
                # real one untouched for our own needs.
                return path.copy()
            # r = row c = column
            for r, c in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (
                    0 <= c < self.game.current_board().size[0]
                    and 0 <= r < self.game.current_board().size[1]
                    and self.game.current_board().item(r, c).overlappable()
                    and (r, c) not in seen
                ):
                    queue.append(path + [(r, c)])
                    seen.add((r, c))
        return []

    def current_path(self):
        """This method simply return a copy of the current path of the actuator.

        The current path is to be understood as: the list of positions still
        remaining. All positions that have already been gone through are
        removed from the stack.

        .. important:: A copy of the path is returned for every call to that
            function so be wary of the performances impact.

        Example::

            mykillernpc.actuator = PathFinder(
                                    game=mygame,
                                    actuated_object=mykillernpc
                                )
            mykillernpc.actuator.set_destination(
                                    mygame.player.pos[0],
                                    mygame.player.pos[1]
                                )
            mykillernpc.actuator.find_path()
            for i in mykillernpc.actuator.current_path():
                print(i)

        """
        return self._current_path.copy()

    # That function is actually covered in tests but some cases are too edgy to test.
    def next_move(self):  # pragma: no cover
        """This method return the next move calculated by this actuator.

        In the case of this PathFinder actuator, next move does the following:

         - If the destination is not set return NO_DIR \
            (see :py:mod:`~pygamelib.constants`) \
         - If the destination is set, but the path is empty and actuated \
            object's position is different from destination: \
            call :meth:`find_path()`
         - Look at the current waypoint, if the actuated object is not at \
            that position return a direction from the \
            :mod:`~pygamelib.constants` module. The direction is calculated \
            from the difference betwen actuated object's position and \
            waypoint's position.
         - If the actuated object is at the waypoint position, then call \
            next_waypoint(), set the destination and return a direction. \
            In this case, also call :meth:`find_path()`.
         - In any case, if there is no more waypoints in the path this method \
            returns NO_DIR (see :py:mod:`~pygamelib.constants`)

        Example::

            seeker = NPC(model=Sprites.SKULL)
            seeker.actuator = PathFinder(game=mygame,actuated_object=seeker)
            while True:
                seeker.actuator.set_destination(mygame.player.pos[0],mygame.player.pos[1])
                # next_move() will call find_path() for us.
                next_move = seeker.actuator.next_move()
                if next_move == constants.NO_DIR:
                    seeker.actuator.set_destination(mygame.player.pos[0],mygame.player.pos[1])
                else:
                    mygame.current_board().move(seeker,next_move,1)
        """
        # If one of destination coordinate is None, return NO_DIR
        if self.destination[0] is None or self.destination[1] is None:
            return constants.NO_DIR

        # If path is empty and actuated_object is not at destination,
        # try to find a path to destination
        if len(self._current_path) == 0 and (
            self.actuated_object.pos[0] != self.destination[0]
            or self.actuated_object.pos[1] != self.destination[1]
        ):
            self.find_path()

        # If path is still empty return NO_DIR (destination is unreachable or
        # the current waypoint is reached)
        if len(self._current_path) == 0:
            # First we check if we already are at current waypoint
            (cwr, cwc) = self.current_waypoint()
            if (
                self.actuated_object.pos[0] == cwr
                and self.actuated_object.pos[1] == cwc
            ):
                # If so, we get the next waypoint
                (r, c) = self.next_waypoint()
                # If there are no more waypoints, then we return NO_DIR
                if r is None or c is None:
                    return constants.NO_DIR
                else:
                    # Else we set the new destination and calculate the path
                    self.set_destination(r, c)
                    self.find_path()
            else:
                return constants.NO_DIR

        if len(self._current_path) == 0:
            return constants.NO_DIR

        # Get the next position from the path
        next_position = self._current_path.pop(0)
        # If actuated object is already there check if the path is empty, if so
        # return NO_DIR, else get the next position from the path.
        if (
            next_position[0] == self.actuated_object.pos[0]
            and next_position[1] == self.actuated_object.pos[1]
        ):
            if len(self._current_path) == 0:
                return constants.NO_DIR
            next_position = self._current_path.pop(0)

        # print(f'Next position is: {next_position} and object position is
        # {self.actuated_object.pos} _current_path length
        # is {len(self._current_path)}')
        dr = self.actuated_object.pos[0] - next_position[0]
        dc = self.actuated_object.pos[1] - next_position[1]

        # Look at the difference between the current position and next position
        # and return the correct direction.
        # If the coordinates are impossible to resolve return NO_DIR
        # NOTE: We could use a comparison with 0
        #   (dr < 0 instead of dr == -1 for example) but the sides effects are
        #   numerous in case the user use a step higher than 1 in Board.move().
        #   The actuated object could end up going into a wall or out of bound.
        if dr == -1 and dc == 0:
            return constants.DOWN
        elif dr == 1 and dc == 0:
            return constants.UP
        elif dr == 0 and dc == 1:
            return constants.LEFT
        elif dr == 0 and dc == -1:
            return constants.RIGHT
        elif dr == -1 and dc == -1:
            return constants.DRDOWN
        elif dr == 1 and dc == -1:
            return constants.DRUP
        elif dr == -1 and dc == 1:
            return constants.DLDOWN
        elif dr == 1 and dc == 1:
            return constants.DLUP
        elif dr > 1 or dr < -1 or dc > 1 or dc < -1:
            # If we are here it means that something is blocking the movement
            self.find_path()
            return self.next_move()
        else:
            return constants.NO_DIR

    def add_waypoint(self, row, column):
        """Add a waypoint to the list of waypoints.

        Waypoints are used one after the other on a FIFO basis
        (First In, First Out).

        If not destination (i.e destination == (None, None)) have been set yet, that
        method sets it.

        :param row: The "row" part of the waypoint's coordinate.
        :type row: int
        :param column: The "column" part of the waypoint's coordinate.
        :type row: int
        :raise PglInvalidTypeException: If any of the parameters is not an int.

        Example::

            pf = PathFinder(game=mygame, actuated_object=npc1)
            pf.add_waypoint(3,5)
            pf.add_waypoint(12,15)

        """
        if type(row) is not int:
            raise base.PglInvalidTypeException('"row" is not an integer. It must be.')
        if type(column) is not int:
            raise base.PglInvalidTypeException(
                '"column" is not an integer. It must be.'
            )
        self.waypoints.append((row, column))
        if self.destination == (None, None):
            self.destination = (row, column)

    def clear_waypoints(self):
        """Empty the waypoints stack.

        Example::

            pf.clear_waypoints()
        """
        self.waypoints.clear()
        self._waypoint_index = -1

    def current_waypoint(self):
        """Return the currently active waypoint.

        If no waypoint have been added, this function return None.

        :return: Either a None tuple or the current waypoint.
        :rtype: A None tuple or a tuple of integer.

        Example::

            (row,column) = pf.current_waypoint()
            pf.set_destination(row,column)

        """
        if len(self.waypoints) == 0:
            return (None, None)
        return self.waypoints[self._waypoint_index]

    def next_waypoint(self):
        """Return the next active waypoint.

        If no waypoint have been added, this function return None.
        If there is no more waypoint in the stack:

        - if PathFinder.circle_waypoints is True this function reset the \
        waypoints stack and return the first one.
        - else, return None.

        :return: Either a None tuple or the next waypoint.
        :rtype: A None tuple or a tuple of integer.

        Example::

            pf.circle_waypoints = True
            (row,column) = pf.next_waypoint()
            pf.set_destination(row,column)

        """
        if len(self.waypoints) == 0:
            return (None, None)
        self._waypoint_index += 1
        if self._waypoint_index >= len(self.waypoints):
            if self.circle_waypoints:
                self._waypoint_index = 0
            else:
                return (None, None)
        return self.waypoints[self._waypoint_index]

    def remove_waypoint(self, row, column):
        """ Remove a waypoint from the stack.

        This method removes the first occurrence of a waypoint in the stack.

        If the waypoint cannot be found, it raises a ValueError exception.
        If the row and column parameters are not int, an
        PglInvalidTypeException is raised.

        :param row: The "row" part of the waypoint's coordinate.
        :type row: int
        :param column: The "column" part of the waypoint's coordinate.
        :type row: int
        :raise PglInvalidTypeException: If any of the parameters is not an int.
        :raise ValueError: If the waypoint is not found in the stack.

        Example::

            method()
        """
        if type(row) is not int:
            raise base.PglInvalidTypeException('"row" is not an integer. It must be.')
        if type(column) is not int:
            raise base.PglInvalidTypeException(
                '"column" is not an integer. It must be.'
            )
        try:
            idx = self.waypoints.index((row, column))
            self.waypoints.pop(idx)
        except ValueError:
            raise base.PglException(
                "invalid_waypoint",
                f"Waypoint ({row},{column}) does not exist in the waypoints stack.",
            )
