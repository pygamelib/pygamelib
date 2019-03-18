import os
from gamelib.HacExceptions import HacInvalidTypeException, HacInvalidLevelException
from gamelib.Board import Board

class Game():
    def __init__(self,name='Game',boards = {}, menu = [], current_level = None):
        self.name = name
        self._boards = boards
        self._menu = menu
        self.current_level = current_level
        self.player = None

    
    def add_menu_entry(self,shortcut,message):
        self._menu.append({'shortcut' : shortcut,'message':message})
    
    def print_menu(self):
        for k in self._menu:
            if k['shortcut'] == None:
                print(k['message'])
            else:
                print( f"{k['shortcut']} - {k['message']}" )
    
    def clear_screen(self):
        os.system('clear')
    
    def add_board(self,level_number,board):
        """
        Add a board for the level number.
        Ex: game.add_board(1,myboard)

         - level_number : the level number of the board. Must be an int.
         - board : a Board object corresponding to the level number.

         If either of these parameters are not of the correct type, a HacInvalidTypeException exception is raised.
        """
        if type(level_number) is int:
            if isinstance(board, Board):
                self._boards[level_number] = board
            else:
                raise HacInvalidTypeException("The board paramater must be a gamelib.Board.Board() object.")
        else:
            raise HacInvalidTypeException("The board number must be an int.")
    
    def current_board(self):
        """
        This method return the board object corresponding to the current_level.
        Ex: game.current_board().display()

        If current_level is set to a value with no corresponding board a HacException excpetion is raised with an invalid_level error.
        """
        if  self.current_level in self._boards.keys():
            return self._boards[self.current_level]
        else:
            raise HacInvalidLevelException("The current level does not correspond to any board.")
    
    def change_level(self,level_number):
        """
        Change the current level, load the board and place the player to the right place.
        Ex: game.change_level(1)

        Parameter:
         - level_number: int
        
        If parameter is not an int, a HacInvalidTypeException is raised.
        """
        if type(level_number) is int:
            if  level_number in self._boards.keys():
                if self.player.pos[0] != None or self.player.pos[1] != None:
                    self._boards[self.current_level].clear_cell(self.player.pos[0],self.player.pos[1]) 
                self.current_level = level_number
                b = self._boards[self.current_level]
                b.place_item(self.player,b.player_starting_position[0],b.player_starting_position[1])
            else:
                raise HacInvalidLevelException(f"Impossible to change level to an unassociated level (level number {level_number} is not associated with any board).\nHave you called:\ngame.add_board({level_number},Board()) ?")
        else:
            raise HacInvalidTypeException('level_number needs to be an int in change_level(level_number).')