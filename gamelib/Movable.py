from gamelib.BoardItem import BoardItem

class Movable(BoardItem):
    """
    This class derive BoardItem and describe an object that can move or be moved (like a player or NPC).
    Thus this class implements BoardItem.can_move().
    However it does not impement BoardItem.pickable() or BoardItem.overlappable()
    """
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)
    
    def can_move(self):
        return True