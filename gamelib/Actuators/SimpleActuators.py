from gamelib.Actuators.Actuator import Actuator
import random

class RandomActuator(Actuator):
    def __init__(self,moveset=[]):
        Actuator.__init__(self)
        self.moveset = moveset
    
    def next_move(self):
        return random.choice(self.moveset)

class PathActuator(Actuator):
    def __init__(self,path=[]):
        Actuator.__init__(self)
        self.path = path
        self.index = 0
    
    def next_move(self):
        move = self.path[self.index]
        self.index += 1
        if self.index == len(self.path):
            self.index = 0
        return move

    def set_path(self,path):
        self.path = path
        self.index = 0
        
