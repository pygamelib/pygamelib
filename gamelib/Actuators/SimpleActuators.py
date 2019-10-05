from gamelib.Actuators.Actuator import Actuator
from gamelib.Constants import PAUSED,RUNNING,STOPPED
import random

class RandomActuator(Actuator):
    """A class that implements a random choice of movement.

    The random actuator is a subclass of :class:`~gamelib.Actuators.Actuator.Actuator`. It is simply implementing a random choice in a predefined move set.

    :param moveset: A list of movements.
    :type moveset: list

    ..todo:: finish the doc.
    """
    def __init__(self,moveset=[]):
        Actuator.__init__(self)
        self.moveset = moveset
    
    def next_move(self):
        if self.state == RUNNING:
            return random.choice(self.moveset)

class PathActuator(Actuator):
    """A class that follows a given path of movement.

    The path actuator is a subclass of :class:`~gamelib.Actuators.Actuator.Actuator`.
    When the Actuator is created it receives a list with a path.
    while the state it's running it will move trough the values of that list.
    Once the lists finishes the path is reset and starts all over again.

    :param path: A list of moves
    :type path: list
    each move is a tuple of two integer from the grid.

    Example: PathActuator(path=[(1,1), (1,2), (2,2), (2,1)])
    """
    def __init__(self,path=[]):
        Actuator.__init__(self)
        self.path = path
        self.index = 0

    
    def next_move(self):
        if self.state == RUNNING:
            move = self.path[self.index]
            self.index += 1
            if self.index == len(self.path):
                self.index = 0
            return move

    def set_path(self,path):
        self.path = path
        self.index = 0
