"""This module contains the Immovable and Actionable classes.
"""

from gamelib.BoardItem import BoardItem
import gamelib.Constants as Constants


class Immovable(BoardItem):
    """
    This class derive BoardItem and describe an object that cannot move or be
    moved (like a wall). Thus this class implements BoardItem.can_move().
    However it does not implement BoardItem.pickable() or
    BoardItem.overlappable()
    """
    def __init__(self, **kwargs):
        BoardItem.__init__(self, **kwargs)
        if 'size' not in kwargs.keys():
            self._size = 0
        else:
            self._size = kwargs['size']

    def can_move(self):
        """ Return the capability of moving of an item.

        Obviously an Immovable item is not capable of moving. So that method
        always returns False.

        :return: False
        :rtype: bool
        """
        return False

    def size(self):
        """Return the size of the Immovable Item.

        :return: The size of the item.
        :rtype: int
        """
        return self._size

    def restorable(self):
        """
        This is a virtual method that must be implemented in deriving class.
        This method has to return True or False.
        This represent the capacity for an Immovable BoardItem to be restored
        by the board if the item is overlappable and has been overlapped by
        another Movable (:class:`~gamelib.Movable.Movable`) item.
        """
        raise NotImplementedError()


class Actionable(Immovable):
    """
    This class derives :class:`~gamelib.Immovable.Immovable`. It adds the
    ability to an Immovable BoardItem to be triggered and execute some code.

    :param action: the reference to a function (Attention: no parentheses at
        the end of the function name).
    :type action: function
    :param action_parameters: the parameters to the action function.
    :type action_parameters: list
    :param perm: The permission that defines what types of items can actually
        activate the actionable. The permission has to be one of the
        permissions defined in :mod:`~gamelib.Constants`
    :type perm: :mod:`~gamelib.Constants`

    On top of these parameters Actionable accepts all parameters from
    :class:`~gamelib.Immovable.Immovable` and therefor from
    :class:`~gamelib.BoardItem.BoardItem`.

    .. note:: The common way to use this class is to use
        GenericActionableStructure. Please refer to
        :class:`~gamelib.Structures.GenericActionableStructure`
        for more details.
    """
    def __init__(self, **kwargs):
        if 'action' not in kwargs.keys():
            self.action = None
        else:
            self.action = kwargs['action']
        if 'action_parameters' not in kwargs.keys():
            kwargs['action_parameters'] = []
        else:
            self.action_parameters = kwargs['action_parameters']
        if 'perm' not in kwargs.keys():
            self.perm = Constants.PLAYER_AUTHORIZED
        else:
            self.perm = kwargs['perm']
        Immovable.__init__(self, **kwargs)

    def activate(self):
        """
        This function is calling the action function with the
        action_parameters.

        Usually it's automatically called by :meth:`~gamelib.Board.Board.move`
        when a Player or NPC (see :mod:`~gamelib.Characters`)
        """
        if self.action is not None:
            self.action(self.action_parameters)
