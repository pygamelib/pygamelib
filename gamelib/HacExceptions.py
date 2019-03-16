class HacInvalidTypeException(Exception):
    """
    Exception raised for invalid types.
    """
    def __init__(self,message):
        self.message = message

class HacException(Exception):
    """
    Exception raised for non specific errors in HAC-GAME-LIB.
    """
    def __init__(self,error,message):
        self.error = error 
        self.message = message

class HacOutOfBoardBoundException(Exception):
    """
    Exception for out of the board's boundaries operations.
    """
    def __init__(self,message):
        self.message = message