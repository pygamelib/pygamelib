from gamelib.Movable import Movable

class Player(Movable):
    """
    A class that represent a player controlled by a human.
    """
    def __init__(self,**kwargs):
        Movable.__init__(self,**kwargs)

    def pickable(self):
        return False

    def has_inventory(self):
        return True

    def overlappable(self):
        return False

class NPC(Movable):
    """
    A class that represent a non playable character controlled by the computer.
    For the NPC to be successfully managed by the Game, you need to set an actuator.
    Ex: mynpc.actuator = RandomActuator()
    """
    def __init__(self,**kwargs):
        Movable.__init__(self,**kwargs)
        if 'actuator' not in kwargs.keys():
            self.actuator= None
        else:
            self.actuator = kwargs['actuator']
        
        if 'step' not in kwargs.keys():
            self.step = None
        else:
            self.step = kwargs['step']
    
    def pickable(self):
        return False
    
    def overlappable(self):
        return False
    
    def has_inventory(self):
        return False