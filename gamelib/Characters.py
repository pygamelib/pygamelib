from gamelib.Movable import Movable

class Player(Movable):
    """
    A class that represent a player controlled by a human.
    """
    def __init__(self,**kwargs):
        Movable.__init__(self,**kwargs)

    def pickable(self):
        return False
    
    def overlappable(self):
        return False

class NPC(Movable):
    """
    A class that represent a non playable character controlled by the computer.
    """
    def __init__(self,**kwargs):
        Movable.__init__(self,**kwargs)
    
    def pickable(self):
        return False
    
    def overlappable(self):
        return False