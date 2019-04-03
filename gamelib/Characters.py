from gamelib.Movable import Movable
from gamelib.Inventory import Inventory

class Character():
    def __init__(self, **kwargs):
        self.max_hp = None
        self.hp = None
        self.max_mp = None
        self.mp = None
        self.remaining_lives = None
        self.attack_power = None
        self.defense_power = None
        self.strength = None
        self.intelligence = None
        self.agility = None
        for a in ['max_hp','hp','max_mp','mp','remaining_lives','attack_power','defense_power','strength','intelligence','agility']:
            if a in kwargs.keys():
                setattr(self,a,kwargs[a])

class Player(Movable,Character):
    """
    A class that represent a player controlled by a human.
    """
    def __init__(self,**kwargs):
        if 'max_hp' not in kwargs.keys():
            kwargs['max_hp'] = 100
        if 'hp' not in kwargs.keys():
            kwargs['hp'] = 100
        if 'remaining_lives' not in kwargs.keys():
            kwargs['remaining_lives'] = 3
        if 'attack_power' not in kwargs.keys():
            kwargs['attack_power'] = 10
        Movable.__init__(self,**kwargs)
        Character.__init__(self,**kwargs)
        if 'inventory' in kwargs.keys():
            self.inventory = kwargs['inventory']
        else:
            self.inventory = Inventory()

    def pickable(self):
        return False

    def has_inventory(self):
        return True

    def overlappable(self):
        return False

class NPC(Movable,Character):
    """
    A class that represent a non playable character controlled by the computer.
    For the NPC to be successfully managed by the Game, you need to set an actuator.
    Ex: mynpc.actuator = RandomActuator()
    """
    def __init__(self,**kwargs):
        if 'max_hp' not in kwargs.keys():
            kwargs['max_hp'] = 10
        if 'hp' not in kwargs.keys():
            kwargs['hp'] = 10
        if 'remaining_lives' not in kwargs.keys():
            kwargs['remaining_lives'] = 1
        if 'attack_power' not in kwargs.keys():
            kwargs['attack_power'] = 5
        Movable.__init__(self,**kwargs)
        Character.__init__(self,**kwargs)
        if 'actuator' not in kwargs.keys():
            self.actuator= None
        else:
            self.actuator = kwargs['actuator']
        
        if 'step' not in kwargs.keys():
            self.step = 0
        else:
            self.step = kwargs['step']
    
    def pickable(self):
        return False
    
    def overlappable(self):
        return False
    
    def has_inventory(self):
        return False