from gamelib.Utils import warn, debug
from gamelib.HacExceptions import HacException, HacOutOfBoardBoundException, HacInvalidTypeException
from gamelib.BoardItem import BoardItem
from gamelib.Movable import Movable
from gamelib.Immovable import Immovable

class Board():
    """
    A class that represent a game board.
    The board is being represented by a square matrix.
    Board can have the following parameters:
    name: str
    size: array [x,y]
    ui_border_left: str
    ui_border_right: str
    ui_border_top: str
    ui_border_bottom: str
    ui_board_void_cell: str
    """
    
    def __init__(self,**kwargs):
        self.name = "Board"
        self.size = [10,10]
        self.ui_border_left = '|'
        self.ui_border_right = '|'
        self.ui_border_top = '-'
        self.ui_border_bottom = '-'
        self.ui_board_void_cell = ' '
        # Setting class parameters
        for item in ['name','size','ui_border_bottom','ui_border_top','ui_border_left','ui_border_right','ui_board_void_cell']:
            if item in kwargs:
                setattr(self,item,kwargs[item])
        # Now checking for board's data sanity
        try:
            self.check_sanity()
        except HacException as error:
            raise error
        
        # If sanity check passed then, initialize the board
        self.init_board()
        

    def __str__(self):
        return f"----------------\nBoard name: {self.name}\nBoard size: {self.size}\nBorders: '{self.ui_border_left}','{self.ui_border_right}','{self.ui_border_top}','{self.ui_border_bottom}',\nBoard void cell: '{self.ui_board_void_cell}'\n----------------"
    
    def init_board(self):
        """
        Initialize the board with BoardItem that uses ui_board_void_cell as model.
        I.e:
          BoardItem(model=self.ui_board_void_cell)
        """
        # self._matrix = [[ BoardItem(model=self.ui_board_void_cell) ]*self.size[0]]*self.size[1]
        # [ [ None for i in range(5) ] for j in range(4) ]
        self._matrix = [ [ BoardItem(model=self.ui_board_void_cell) for i in range(0,self.size[0],1) ] for j in range(0,self.size[1],1) ]
    
    def check_sanity(self):
        sanity_check=0
        if type(self.size) is list:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'size' parameter must be a list.")
        if len(self.size) == 2:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'size' parameter must be a list of 2 elements.")
        if type(self.size[0]) is int:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The first element of the 'size' list must be an integer.")
        if type(self.size[1]) is int:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The second element of the 'size' list must be an integer.")
        if type(self.name) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'name' parameter must be a string.")
        if type(self.ui_border_bottom) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'ui_border_bottom' parameter must be a string.")
        if type(self.ui_border_top) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'ui_border_top' parameter must be a string.")
        if type(self.ui_border_left) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'ui_border_left' parameter must be a string.")
        if type(self.ui_border_right) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'ui_border_right' parameter must be a string.")
        if type(self.ui_board_void_cell) is str:
            sanity_check += 1
        else:
            raise HacException('SANITY_CHECK_KO',"The 'ui_board_void_cell' parameter must be a string.")
        
        if self.size[0] > 80:
            warn(f'The first dimension of your board is {self.size[0]}. It is a good practice to keep it at a maximum of 80 for compatibility with older terminals.')
        
        if self.size[1] > 80:
            warn(f'The second dimension of your board is {self.size[1]}. It is a good practice to keep it at a maximum of 80 for compatibility with older terminals.')

        # If all sanity check clears return True else raise a general error.
        # I have no idea how the general error could ever occur but... better safe than sorry!
        if sanity_check == 10:
            return True
        else:
            raise HacException('SANITY_CHECK_KO',"The board data are not valid.")

    def display(self):
        border_top = ''
        border_bottom = ''
        for x in self._matrix[0]:
            border_bottom += self.ui_border_bottom
            border_top += self.ui_border_top
        border_bottom += self.ui_border_bottom*2
        border_top += self.ui_border_top*2
        print(border_top)
        for x in self._matrix:
            print(self.ui_border_left,end='')
            for y in x:
                print(y,end='')
            print(self.ui_border_right)
        print(border_bottom)

    def item(self,x,y):
        """
        Return the item at the x,y position if within board's bounds.
        Else raise an HacOutOfBoardBoundException
        """
        if x < self.size[0] and y < self.size[0]:
            return self._matrix[x][y]
        else:
            raise HacOutOfBoardBoundException(f"There is no item at coordinates [{x},{y}] because it's out of the board boundaries ({self.size[0]}x{self.size[1]}).")
    
    def place_item(self,item,x,y):
        """
        Place an item at coordinates x and y.
        If x or y are our of the board boundaries, an HacOutOfBoardBoundException is raised.
        If the item is not a subclass of BoardItem, an HacInvalidTypeException
        """
        if x < self.size[0] and y < self.size[0]:
            if isinstance(item, BoardItem):
                self._matrix[x][y] = item
            else:
                raise HacInvalidTypeException("The item passed in argument is not a subclass of BoardItem")
        else:
            raise HacOutOfBoardBoundException(f"There is no item at coordinates [{x},{y}] because it's out of the board boundaries ({self.size[0]}x{self.size[1]}).")





