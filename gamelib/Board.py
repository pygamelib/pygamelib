from gamelib.Utils import warn, debug
from gamelib.HacExceptions import HacException, HacOutOfBoardBoundException, HacInvalidTypeException, HacObjectIsNotMovableException
from gamelib.BoardItem import BoardItem, BoardItemVoid
from gamelib.Movable import Movable
from gamelib.Immovable import Immovable,Actionnable
import gamelib.Constants as Constants

class Board():
    """
    A class that represent a game board.
    The board is being represented by a square matrix.
    For the moment a board only support one player.
    Board can have the following parameters:
     - name: str
     - size: array [x,y]
     - player_starting_position: array [x,y]
     - ui_borders : str - to set all the borders to the same value
     - ui_border_left: str
     - ui_border_right: str
     - ui_border_top: str
     - ui_border_bottom: str
     - ui_board_void_cell: str
    """
    
    def __init__(self,**kwargs):
        self.name = "Board"
        self.size = [10,10]
        self.player_starting_position = [0,0]
        self.ui_border_left = '|'
        self.ui_border_right = '|'
        self.ui_border_top = '-'
        self.ui_border_bottom = '-'
        self.ui_board_void_cell = ' '
        # Setting class parameters
        for item in ['name','size','ui_border_bottom','ui_border_top','ui_border_left','ui_border_right','ui_board_void_cell','player_starting_position']:
            if item in kwargs:
                setattr(self,item,kwargs[item])
        # if ui_borders is set then set all borders to that value
        if 'ui_borders' in kwargs.keys():
            for item in ['ui_border_bottom','ui_border_top','ui_border_left','ui_border_right']:
                setattr(self,item,kwargs[item])
        # Now checking for board's data sanity
        try:
            self.check_sanity()
        except HacException as error:
            raise error
        
        # Init the list of movables and immovables objects
        self._movables = []
        self._immovables = []
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

        self._matrix = [ [ BoardItemVoid(model=self.ui_board_void_cell) for i in range(0,self.size[0],1) ] for j in range(0,self.size[1],1) ]
    
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
                item.store_position(x,y)
                if isinstance(item, Movable):
                    self._movables.append(item)
                elif isinstance(item, Immovable):
                    self._immovables.append(item)
            else:
                raise HacInvalidTypeException("The item passed in argument is not a subclass of BoardItem")
        else:
            raise HacOutOfBoardBoundException(f"There is no item at coordinates [{x},{y}] because it's out of the board boundaries ({self.size[0]}x{self.size[1]}).")
    
    def move(self,item,direction,step):
        """
        Move an item in the specified direction for a number of steps.
        Ex: board.move(player,Constants.UP,1)

        Parameters are:
         - item : an item to move (it has to be a subclass of Movable)
         - direction : a direction from Constants
         - step : the number of steps to move the item.

        If the number of steps is greater than the Board, the item will be move to the maximum possible position.

        If the item is not a subclass of Movable, an HacObjectIsNotMovableException exception.

        Important: if the move is successfull, an empty BoardItemVoid will be put at the departure position.
        """
        if isinstance(item, Movable) and item.can_move():
            new_x = None
            new_y = None
            if direction == Constants.UP:
                new_x = item.pos[0] - step
                new_y = item.pos[1]
            elif direction == Constants.DOWN:
                new_x = item.pos[0] + step
                new_y = item.pos[1]
            elif direction == Constants.LEFT:
                new_x = item.pos[0]
                new_y = item.pos[1] - step
            elif direction == Constants.RIGHT:
                new_x = item.pos[0]
                new_y = item.pos[1] + step
            if new_x != None and new_y != None and new_x>=0 and new_y>=0 and new_x < self.size[1] and new_y < self.size[0] and self._matrix[new_x][new_y].overlappable():
                if isinstance(self._matrix[new_x][new_y],Actionnable):
                    self._matrix[new_x][new_y].activate()
                else:
                    self.place_item( BoardItemVoid(model=self.ui_board_void_cell), item.pos[0], item.pos[1] )
                    self.place_item( item, new_x, new_y )
        else:
            raise HacObjectIsNotMovableException(f"Item '{item.name}' at position [{item.pos[0]},{item.pos[1]}] is not a subclass of Movable, therefor it cannot be moved.")
    
    def clear_cell(self,x,y):
        """
        This method clears a cell, meaning it position a void_cell BoardItemVoid at these coordinates.
        Ex: myboard.clear_cell(3,4)
        Parameters:
         - x : int
         - y : int
        
        WARNING: This method does not check the content before, it *will* overwrite the content.
        """
        self.place_item( BoardItemVoid(model=self.ui_board_void_cell, name='void_cell'), x, y )






