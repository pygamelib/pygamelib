"""
This file holds utility functions that belongs to nowhere else.
"""

import inspect


def pgl_isinstance(obj, obj_type):
    """Check if an object is instance of some type.

    This function is similar to Python isinstance() function except that it only look at
    the MRO to find a matching type name. Therefor it does not require importing a whole
    module just to check the type of a variable.

    .. Important:: You need to give the full type name string not just a part of it. For
       example, pgl_isinstance(board_items.Player(), 'Movable') will return False.
       pgl_isinstance(board_items.Player(), 'pygamelib.board_items.Movable') will
       return True.

    :param obj: The object to check.
    :type obj: object
    :param obj_type: The type to check **as a string**
    :type obj_type: str
    :rtype: bool

    Example::

        if pgl_isinstance(item, 'pygamelib.gfx.core.Color'):
            print('This is a color!')
    """
    # Adapted from:
    # https://stackoverflow.com/questions/16964467/isinstance-without-importing-candidates
    return obj_type in [
        x.__module__ + "." + x.__name__ for x in inspect.getmro(type(obj))
    ]


def clamp(minimum, maximum, value):
    """Return the value clamped between the min and max boundaries.

    If value is between min and max, this returns value. If it's outside, it returns the
    closer boundary (either min or max).

    :param minimum: The lower boundary.
    :type minimum: int|float
    :param maximum: The lower boundary.
    :type maximum: int|float
    :param value: The value to clamp.
    :type value: int|float
    :returns: The clamped value.
    :rtype: int|float

    Example::

        safe_row = clamp(0, board.height, projected_position.row)
    """
    return max(minimum, min(maximum, value))
