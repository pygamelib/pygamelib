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
        if 'size' not in kwargs.keys():
            self._size = 0
        else:
            self._size = kwargs['size']

    def can_move(self):
        return False
    
    def size(self):
        return self._size
    
    def restorable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for an Immovable BoardItem to be restored by the board if the item is overlappable and has been overlapped by another Movable (:class:`gamelib.Movable.Movable`) item.
        """
        raise NotImplementedError()

class Actionnable(Immovable):
    """
    .. TODO:: Documentation
    """
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