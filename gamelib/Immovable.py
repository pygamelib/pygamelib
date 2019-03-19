from gamelib.BoardItem import BoardItem

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
            kwargs['action'] = None
        else:
            self.action = kwargs['action']
        Immovable.__init__(self,**kwargs)
    
    def activate(self):
        if self.action != None:
            self.action()