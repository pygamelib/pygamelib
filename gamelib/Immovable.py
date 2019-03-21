from gamelib.BoardItem import BoardItem
import gamelib.Constants as C

class Immovable(BoardItem):
    """
    This class derive BoardItem and describe an object that cannot move or be moved (like a wall).
    Thus this class implements BoardItem.can_move().
    However it does not impement BoardItem.pickable() or BoardItem.overlappable()
    """
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)

    def can_move(self):
        return False

class Actionnable(Immovable):
    def __init__(self,**kwargs):
        if 'action' not in kwargs.keys():
            self.action = None
        else:
            self.action = kwargs['action']
        if 'action_parameters' not in kwargs.keys():
            kwargs['action_parameters'] = []
        else:
            self.action_parameters = kwargs['action_parameters']
        if 'perm' not in kwargs.keys():
            self.perm = C.PLAYER_AUTHORIZED
        else:
            self.perm = kwargs['perm']
        Immovable.__init__(self,**kwargs)
    
    def activate(self):
        if self.action != None:
            self.action(self.action_parameters)