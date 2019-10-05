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
        else:
            return None

class PathActuator(Actuator):
    """ 
    The path actuator is a subclass of :class:`~gamelib.Actuators.Actuator.Actuator`.  The move inside the function next_move 
    depends on path and index. If the state is not running it returns None otherwise it increments the index & then, further compares the index 
    with length of the path. If they both are same then, index is set to value zero and the move is returned back.
    :param path: A list of paths.
    :type path: list
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
        else:
            return None
            
    def set_path(self,path):
        self.path = path
        self.index = 0
        
