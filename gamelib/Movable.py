from gamelib.BoardItem import BoardItem

class Movable(BoardItem):
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)
    
    def can_move(self):
        return True