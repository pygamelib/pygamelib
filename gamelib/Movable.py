"""This module contains the Movable class.
It can potentially hold more movement related classes.
"""

from gamelib.BoardItem import BoardItem


class Movable(BoardItem):
    """A class representing BoardItem capable of movements.

    Movable subclasses :class:`BoardItem`.

    :param step: the amount of cell a movable can cross in one turn.
    :type step: int

    This class derive BoardItem and describe an object that can move or be
    moved (like a player or NPC).
    Thus this class implements BoardItem.can_move().
    However it does not implement BoardItem.pickable() or
    BoardItem.overlappable()

    This class contains a private member called _overlapping.
    This private member is used to store the reference to an overlappable
    object while a movable occupy its position. The Board then restore the
    overlapped object. You should let the Board class take care of that.
    """
    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        if 'step' not in kwargs.keys():
            self.step = 1
        else:
            self.step = kwargs['step']
        self._overlapping = None
        self._overlapping_buffer = None

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
