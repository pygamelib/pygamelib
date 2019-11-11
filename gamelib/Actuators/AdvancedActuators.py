"""This module contains the more advanced actuators.
AdvancedActuators allow for more actions and not only movement.
It can also be more advanced movement classes.
"""


from gamelib.Actuators.Actuator import Behavioral
from gamelib.HacExceptions import HacInvalidTypeException, HacException
from gamelib.Movable import Movable
import gamelib.Constants as Constants
import collections


class PathFinder(Behavioral):
    """
    .. important:: This module assume a one step movement.
        If you need more than one step, you will need to sub-class
        this module and re-implement next_waypoint().

    This actuator is a bit different than the simple actuators
    (:mod:`~gamelib.Actuators.SimpleActuators`) as it requires
    the knowledge of both the game object and the actuated object.

    The constructor takes the following parameters:

    :param game: A reference to the instanciated game engine.
    :type game: gamelib.Game.Game
    :param actuated_object: The object to actuate.
    :type actuated_object: gamelib.BoardItem.BoardItem
    :param circle_waypoints: If True the next_waypoint()
        method is going to circle between the waypoints
        (when the last is visited, go back to the first)
    :type circle_waypoints: bool

    """
    def __init__(self, game=None, actuated_object=None, circle_waypoints=True):
        super().__init__()
        self.actuated_object = actuated_object
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
        :raises HacInvalidTypeException: if row or column are not int.

        Example::

            mykillernpc.actuator.set_destination(
                mygame.player.pos[0], mygame.player.pos[1]
            )
        """
        if type(row) is not int or type(column) is not int:
            raise HacInvalidTypeException(
                "In Actuator.PathFinder.set_destination(x,y) \
                both x and y must be integer."
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
            raise HacException(
                'actuated_object is not defined',
                'PathFinder.actuated_object has to be defined.'
            )
        if not isinstance(self.actuated_object, Movable):
            raise HacException(
                'actuated_object not a Movable object',
                'PathFinder.actuated_object has to be an instance \
                of a Movable object.'
            )
        if self.destination is None:
            raise HacException(
                'destination is not defined',
                'PathFinder.destination has to be defined.'
            )

        queue = collections.deque([[
                (
                    self.actuated_object.pos[0],
                    self.actuated_object.pos[1]
                )
            ]])
        seen = set([(
            self.actuated_object.pos[0],
            self.actuated_object.pos[1]
        )])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if (x, y) == self.destination:
                self._current_path = path
                # We return only a copy of the path as we need to keep the
                # real one untouched for our own needs.
                return path.copy()
            # r = row c = column
            for r, c in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (0 <= c < self.game.current_board().size[0]
                        and 0 <= r < self.game.current_board().size[1]
                        and self.game.current_board().item(r, c).overlappable()
                        and (r, c) not in seen):
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

    def next_move(self):
        """This method return the next move calculated by this actuator.

        In the case of this PathFinder actuator, next move does the following:

         - If the destination is not set return NO_DIR \
            (see :py:mod:`~gamelib.Constants`) \
         - If the destination is set, but the path is empty and actuated \
            object's position is different from destination: \
            call :meth:`find_path()`
         - Look at the current waypoint, if the actuated object is not at \
            that position return a direction from the \
            :mod:`~gamelib.Constants` module. The direction is calculated \
            from the difference betwen actuated object's position and \
            waypoint's position.
         - If the actuated object is at the waypoint position, then call \
            next_waypoint(), set the destination and return a direction. \
            In this case, also call :meth:`find_path()`.
         - In any case, if there is no more waypoints in the path this method \
            returns NO_DIR (see :py:mod:`~gamelib.Constants`)

        Example::

            seeker = NPC(model=Sprites.SKULL)
            seeker.actuator = PathFinder(game=mygame,actuated_object=seeker)
            while True:
                seeker.actuator.set_destination(mygame.player.pos[0],mygame.player.pos[1])
                # next_move() will call find_path() for us.
                next_move = seeker.actuator.next_move()
                if next_move == Constants.NO_DIR:
                    seeker.actuator.set_destination(mygame.player.pos[0],mygame.player.pos[1])
                else:
                    mygame.current_board().move(seeker,next_move,1)
        """
        # If one of destination coordinate is None, return NO_DIR
        if self.destination[0] is None or self.destination[1] is None:
            return Constants.NO_DIR

        # If path is empty and actuated_object is not at destination,
        # try to find a path to destination
        if (len(self._current_path) == 0
                and (self.actuated_object.pos[0] != self.destination[0]
                     or self.actuated_object.pos[1] != self.destination[1])):
            self.find_path()

        # If path is still empty return NO_DIR (destination is unreachable or
        # the current waypoint is reached)
        if len(self._current_path) == 0:
            # First we check if we already are at current waypoint
            (cwr, cwc) = self.current_waypoint()
            if (self.actuated_object.pos[0] == cwr
                    and self.actuated_object.pos[1] == cwc):
                # If so, we get the next waypoint
                (r, c) = self.next_waypoint()
                # If there are no more waypoints, then we return NO_DIR
                if r is None or c is None:
                    return Constants.NO_DIR
                else:
                    # Else we set the new destination and calculate the path
                    self.set_destination(r, c)
                    self.find_path()
            else:
                return Constants.NO_DIR

        if len(self._current_path) == 0:
            return Constants.NO_DIR

        # Get the next position from the path
        next_position = self._current_path.pop(0)
        # If actuated object is already there check if the path is empty, if so
        # return NO_DIR, else get the next position from the path.
        if (next_position[0] == self.actuated_object.pos[0]
                and next_position[1] == self.actuated_object.pos[1]):
            if len(self._current_path) == 0:
                return Constants.NO_DIR
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
            return Constants.DOWN
        elif dr == 1 and dc == 0:
            return Constants.UP
        elif dr == 0 and dc == 1:
            return Constants.LEFT
        elif dr == 0 and dc == -1:
            return Constants.RIGHT
        elif dr == -1 and dc == -1:
            return Constants.DRDOWN
        elif dr == 1 and dc == -1:
            return Constants.DRUP
        elif dr == -1 and dc == 1:
            return Constants.DLDOWN
        elif dr == 1 and dc == 1:
            return Constants.DLUP
        elif dr > 1 or dr < -1 or dc > 1 or dc < -1:
            # If we are here it means that something is blocking the movement
            self.find_path()
            return self.next_move()
        else:
            return Constants.NO_DIR

    def add_waypoint(self, row, column):
        """Add a waypoint to the list of waypoints.

        Waypoints are used one after the other on a FIFO basis
        (First In, First Out).

        :param row: The "row" part of the waypoint's coordinate.
        :type row: int
        :param column: The "column" part of the waypoint's coordinate.
        :type row: int
        :raise HacInvalidTypeException: If any of the parameters is not an int.

        Example::

            pf = PathFinder(game=mygame, actuated_object=npc1)
            pf.add_waypoint(3,5)
            pf.add_waypoint(12,15)

        """
        if type(row) is not int:
            raise HacInvalidTypeException(
                                         '"row" is not an integer. It must be.'
            )
        if type(column) is not int:
            raise HacInvalidTypeException(
                                         '"column" is not an integer.\
                                         It must be.'
            )
        self.waypoints.append((row, column))

    def clear_waypoints(self):
        """Empty the waypoints stack.

        Example::

            pf.clear_waypoints()
        """
        self.waypoints.clear()

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
        HacInvalidTypeException is raised.

        :param row: The "row" part of the waypoint's coordinate.
        :type row: int
        :param column: The "column" part of the waypoint's coordinate.
        :type row: int
        :raise HacInvalidTypeException: If any of the parameters is not an int.
        :raise ValueError: If the waypoint is not found in the stack.

        Example::

            method()
        """
        if type(row) is not int:
            raise HacInvalidTypeException(
                                        '"row" is not an integer. It must be.'
                                        )
        if type(column) is not int:
            raise HacInvalidTypeException(
                                        '"column" is not an integer.\
                                         It must be.'
                                        )
        try:
            idx = self.waypoints.index((row, column))
            self.waypoints.pop(idx)
        except ValueError as e:
            print(e)
