from gamelib.BoardItem import BoardItem

class Immovable(BoardItem):
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)

    def can_move(self):
        return False