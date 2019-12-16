"""This module regroup all the specific exceptions of the library.
The idea behind most exceptions is to provide more context and info that the standard
exceptions.
"""


class HacInvalidTypeException(Exception):
    """
    Exception raised for invalid types.
    """

    def __init__(self, message):
        self.message = message


class HacException(Exception):
    """
    Exception raised for non specific errors in HAC-GAME-LIB.
    """

    def __init__(self, error, message):
        self.error = error
        self.message = message


class HacOutOfBoardBoundException(Exception):
    """
    Exception for out of the board's boundaries operations.
    """

    def __init__(self, message):
        self.message = message


class HacObjectIsNotMovableException(Exception):
    """
    Exception raised if the object that is being moved is not a subclass of Movable.
    """

    def __init__(self, message):
        self.message = message


class HacInvalidLevelException(Exception):
    """
    Exception raised if a level is not associated to a board in Game().
    """

    def __init__(self, message):
        self.message = message


class HacInventoryException(Exception):
    """
    Exception raised for issue related to the inventory.
    The error is an explicit string, and the message explains the error.
    """

    def __init__(self, error, message):
        self.error = error
        self.message = message
