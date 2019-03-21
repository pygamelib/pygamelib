from gamelib.Actuators.Actuator import Actuator
import random

class RandomActuator(Actuator):
    def __init__(self,moveset=[]):
        Actuator.__init__(self)
        self.moveset = moveset
    
    def next_move(self):
        return random.choice(self.moveset)
        
