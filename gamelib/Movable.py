from gamelib.BoardItem import BoardItem

class Movable(BoardItem):
    """A class representing BoardItem capable of movements.

    Movable subclasses :class:`BoardItem`.

    This class derive BoardItem and describe an object that can move or be moved (like a player or NPC).
    Thus this class implements BoardItem.can_move().
    However it does not impement BoardItem.pickable() or BoardItem.overlappable()
    """
    def __init__(self,**kwargs):
        BoardItem.__init__(self,**kwargs)
    
    def can_move(self):
        """
        Movable implements can_move().

        :return: True
        :rtype: Boolean
        """
        return True
    
    def has_inventory(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for a Movable to have an inventory.
        """
        pass