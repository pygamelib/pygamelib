class Board():
    """
    A class that represent a game board.
    The board is being represented by a square matrix.
    Board can have the following parameters:
    name: str
    size: array [x,y]
    ui_board_contour: str
    ui_board_void_cell: str
    """
    name = "Board"
    size = [10,10]
    ui_board_contour = '|'
    ui_board_void_cell = ' '
    def __init__(self,**kwargs):
        for item in ['name','size','ui_board_contour','ui_board_void_cell']:
            if item in kwargs:
                setattr(self,item,kwargs[item])
        try:
            self.check_sanity()
        except BoardException as error:
            raise error

    def __str__(self):
        return f"----------------\nBoard name: {self.name}\nBoard size: {self.size}\nBoard contour: '{self.ui_board_contour}'\nBoard void cell: '{self.ui_board_void_cell}'\n----------------"
    
    def init_board(self):
        pass
    
    def check_sanity(self):
        sanity_check=0
        if len(self.size) == 2:
            sanity_check += 1
        if type(self.size[0]) is int:
            sanity_check += 1
        if type(self.size[1]) is int:
            sanity_check += 1
        if type(self.name) is str:
            sanity_check += 1
        if type(self.ui_board_contour) is str:
            sanity_check += 1
        if type(self.ui_board_void_cell) is str:
            sanity_check += 1
        if sanity_check == 6:
            return True
        else:
            raise BoardException('SANITY_CHECK_KO',"The board data are not valid.")

    def display(self):
        pass


class BoardException(Exception):
    """
    Exception raised for errors in Board handling.
    """
    def __init__(self,error,message):
        self.error = error 
        self.message = message