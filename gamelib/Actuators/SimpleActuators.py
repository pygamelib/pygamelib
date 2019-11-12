"""This module contains the simple actuators classes.
Simple actuators are movement related one. They allow for predetermined movements
patterns.
"""

from gamelib.Actuators.Actuator import Actuator
from gamelib.Constants import RUNNING
import random


class RandomActuator(Actuator):
    """A class that implements a random choice of movement.

    The random actuator is a subclass of
    :class:`~gamelib.Actuators.Actuator.Actuator`.
    It is simply implementing a random choice in a predefined move set.

    :param moveset: A list of movements.
    :type moveset: list
    """
    def __init__(self, moveset=None):
        if moveset is None:
            moveset = []
        super().__init__()
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
        if self.state == RUNNING:
            return random.choice(self.moveset)


class PathActuator(Actuator):
    """
    The path actuator is a subclass of
    :class:`~gamelib.Actuators.Actuator.Actuator`.
    The move inside the function next_move
    depends on path and index. If the state is not running it returns None
    otherwise it increments the index & then, further compares the index
    with length of the path. If they both are same then, index is set to
    value zero and the move is returned back.

    :param path: A list of paths.
    :type path: list
    """
    def __init__(self, path=None):
        if path is None:
            path = []
        super().__init__()
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
        if self.state == RUNNING:
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

            pathactuator.set_path([Constants.UP,Constants.DOWN,Constants.LEFT,Constants.RIGHT])
        """
        self.path = path
        self.index = 0


class PatrolActuator(PathActuator):
    """
    The patrol actuator is a subclass of
    :class:`~gamelib.Actuators.PathActuator`.  The move inside the function
    next_move depends on path and index and the mode. Once it reaches the end
    of the move list it will start cycling back to the beggining of the list.
    Once it reaches the beggining it will start moving forwards
    If the state is not running it returns None otherwise it increments the
    index & then, further compares the index with length of the path.
    If they both are same then, index is set to value zero and the move is
    returned back.

    :param path: A list of paths.
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
        if self.state == RUNNING:
            move = self.path[self.index]
            self.index += 1
            if self.index == len(self.path):
                self.index = 0
                self.path = self.path.reverse()
            return move
