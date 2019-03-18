from gamelib.BoardItem import BoardItem

class Immovable(BoardItem):
    """
    This class derive BoardItem and describe an object that cannot move or be moved (like a wall).
    Thus this class implements BoardItem.can_move().
    However it does not impement BoardItem.pickable()
    """
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)

    def can_move(self):
        return False