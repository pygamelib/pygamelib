import os
from gamelib.HacExceptions import HacInvalidTypeException, HacInvalidLevelException, HacException
from gamelib.Board import Board
from gamelib.BoardItem import BoardItemVoid
from gamelib.Characters import NPC
from gamelib.Actuators.SimpleActuators import RandomActuator
import gamelib.Constants as C
import random

class Game():
    def __init__(self,name='Game',boards = {}, menu = {}, current_level = None):
        self.name = name
        self._boards = boards
        self._menu = menu
        self.current_level = current_level
        self.player = None

    
    def add_menu_entry(self,category,shortcut,message):
        if category in self._menu.keys():
            self._menu[category].append({'shortcut' : shortcut,'message':message})
        else:
            self._menu[category] = [{'shortcut' : shortcut,'message':message}]
    
    def print_menu(self,category):
        if category not in self._menu:
            raise HacException('invalid_menu_category',f"The '{category}' category is not registered in the menu. Did you add any menu entry in that category with Game.add_menu_entry('{category}','some shortcut','some message') ? If yes, then you should check for typos." )
        for k in self._menu[category]:
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
                self._boards[level_number] = {'board':board,'npcs':[]}
            else:
                raise HacInvalidTypeException("The board paramater must be a gamelib.Board.Board() object.")
        else:
            raise HacInvalidTypeException("The level number must be an int.")
    
    def current_board(self):
        """
        This method return the board object corresponding to the current_level.
        Ex: game.current_board().display()

        If current_level is set to a value with no corresponding board a HacException excpetion is raised with an invalid_level error.
        """
        if  self.current_level in self._boards.keys():
            return self._boards[self.current_level]['board']
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
                    self._boards[self.current_level]['board'].clear_cell(self.player.pos[0],self.player.pos[1]) 
                self.current_level = level_number
                b = self._boards[self.current_level]['board']
                b.place_item(self.player,b.player_starting_position[0],b.player_starting_position[1])
            else:
                raise HacInvalidLevelException(f"Impossible to change level to an unassociated level (level number {level_number} is not associated with any board).\nHave you called:\ngame.add_board({level_number},Board()) ?")
        else:
            raise HacInvalidTypeException('level_number needs to be an int in change_level(level_number).')
        
    def add_npc(self,level_number,npc,x=None,y=None):
        """
        Add a NPC to the game. It will be placed on the board corresponding to the level_number.
        If x and y are not None, the NPC is placed at these coordinates. Else, it's randomly placed in an empy cell.
        Ex: game.add_board(1,myboard)

         - level_number : the level number of the board. Must be an int.
         - npc : the NPC to place. Must be a gamelib.Characters.NPC (or a subclass of it)
         - x and y: the coordinates to place the NPC. Must be an int.

         If either of these parameters are not of the correct type, a HacInvalidTypeException exception is raised.

         IMPORTANT: If the NPC does not have an actuator, this method is going to affect a gamelib.Actuators.SimpleActuators.RandomActuator() to npc.actuator.
                    And if npc.step == None, this method sets it to 1
        """
        if type(level_number) is int:
            if isinstance(npc, NPC):
                if x == None or y == None:
                    retry = 0
                    while True :
                        if x == None:
                            x = random.randint(0,self._boards[level_number]['board'].size[1]-1)
                        if y == None:
                            y = random.randint(0,self._boards[level_number]['board'].size[0]-1)
                        # print(f"Game.add_npc() finding a position for NPC {npc.name} trying ({x},{y})")
                        if isinstance(self._boards[level_number]['board'].item(x,y), BoardItemVoid):
                            break
                        else:
                            x = None
                            y = None
                            retry += 1
                if type(x) is int:
                    if type(y) is int:
                        if npc.actuator == None:
                            npc.actuator = RandomActuator(moveset=[C.UP,C.DOWN,C.LEFT,C.RIGHT])
                        if npc.step == None:
                            npc.step = 1
                        self._boards[level_number]['board'].place_item(npc,x,y)
                        self._boards[level_number]['npcs'].append(npc)
                    else:
                        raise HacInvalidTypeException("y must be an int.")
                else:
                    raise HacInvalidTypeException("x must be an int.")
            else:
                raise HacInvalidTypeException("The npc paramater must be a gamelib.Characters.NPC() object.")
        else:
            raise HacInvalidTypeException("The level number must be an int.")
        
    def move_npcs(self,level_number):
        # TODO: Documentation
        # TODO: Check data type and availability
        for npc in self._boards[level_number]['npcs']:
            self._boards[level_number]['board'].move(npc, npc.actuator.next_move(), npc.step)