import os
from gamelib.HacExceptions import HacInvalidTypeException, HacInvalidLevelException, HacException
from gamelib.Board import Board
from gamelib.BoardItem import BoardItemVoid
from gamelib.Characters import NPC
from gamelib.Actuators.SimpleActuators import RandomActuator
import gamelib.Constants as C
import gamelib.Utils as U
import random
from configparser import ConfigParser

class Game():
    """A class that serve as a game engine.

    This object is the central system that allow the management of a game. It holds boards (see :class:`gamelib.Board.Board`), associate it to level, takes care of level changing, etc.

    :param name: The Game name.
    :type name: str
    :param boards: A dictionnary of boards with the level number as key and a board reference as value.
    :type boards: dict
    :param menu: A dictionnary of menus with a category (str) as key and another dictionnary (key: a shortcut, value: a description) as value.
    :type menu: dict
    :param current_level: The current level.
    :type current_level: int
    """
    def __init__(self,name='Game',boards = {}, menu = {}, current_level = None):
        self.name = name
        self._boards = boards
        self._menu = menu
        self.current_level = current_level
        self.player = None
        self._config_parsers = None
        self._configuration = None

    
    def add_menu_entry(self,category,shortcut,message):
        """Add a new entry to the menu.

        Add another shortcut and message to the specified category.

        Categories help organize the different sections of a menu or dialogues.
        
        :param category: The category to wich the entry should be added.
        :type category: str
        :param shortcut: A shortcut (usually one key) to display.
        :type shortcut: str
        :param message: a message that explains what the shortcut does.
        :type message: str

        The shortcut is optional.

        Example:
            game.add_menu_entry('main_menu','d','Go right')
            game.add_menu_entry('main_menu',None,'-'\*17)
            game.add_menu_entry('main_menu','v','Change game speed')

        """
        if category in self._menu.keys():
            self._menu[category].append({'shortcut' : shortcut,'message':message})
        else:
            self._menu[category] = [{'shortcut' : shortcut,'message':message}]
    
    def print_menu(self,category):
        """
        .. TODO:: Documentation
        """
        if category not in self._menu:
            raise HacException('invalid_menu_category',f"The '{category}' category is not registered in the menu. Did you add any menu entry in that category with Game.add_menu_entry('{category}','some shortcut','some message') ? If yes, then you should check for typos." )
        for k in self._menu[category]:
            if k['shortcut'] == None:
                print(k['message'])
            else:
                print( f"{k['shortcut']} - {k['message']}" )
    
    def clear_screen(self):
        """
        Clear the whole screen (i.e: remove everything written in terminal)
        """
        os.system('clear')
    
    def load_config(self,filename,section='main',defaults={}):
        """
        Load a configuration file from the disk.
        The configuration file must respect the INI syntax.
        
        :param filename: The filename to load. does not check for existence.
        :type filename: str
        :param section: The section to put the read config file into. This allow for multiple files for multiple purpose.
        :type section: str
        :param defaults: The default value for each variable in the config file (or not). If your config file uses sections, your defaults needs to represent that.
        :type defaults: dict
        
        See https://docs.python.org/3/library/configparser.html for more information on that.
        
        Example:
            mygame.load_config('game_controls.ini','game_control')
        
        """
        if self._config_parsers == None:
            self._config_parsers = {}
        if section not in self._config_parsers.keys():
            self._config_parsers[section] = ConfigParser()
        self._config_parsers[section].read(filename)
    
    def add_board(self,level_number,board):
        """Add a board for the level number.

        This method associate a Board (:class:`gamelib.Board.Board`) to a level number.

        Example:
            game.add_board(1,myboard)

        :param level_number: the level number to associate the board to.
        :type level_number: int
        :param board: a Board object corresponding to the level number.
        :type board: gamelib.Board.Board

        :raises HacInvalidTypeException: If either of these parameters are not of the correct type.
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
        
        Example: 
            game.current_board().display()

        If current_level is set to a value with no corresponding board a HacException excepetion is raised with an invalid_level error.
        """
        if  self.current_level in self._boards.keys():
            return self._boards[self.current_level]['board']
        else:
            raise HacInvalidLevelException("The current level does not correspond to any board.")
    
    def change_level(self,level_number):
        """
        Change the current level, load the board and place the player to the right place.

        Example: 
            game.change_level(1)

        :param level_number: the level number to change to.
        :type level_number: int

        :raises HacInvalidTypeException: If parameter is not an int.
        """
        if type(level_number) is int:
            if self.player == None:
                raise HacException('undefined_player','Game.player is undefined. We cannot change level without a player. Please set player in your Game object: mygame.player = Player()')
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

        Example: 
            game.add_board(1,myboard)

        :param level_number: the level number of the board.
        :type level_number: int
        :param npc: the NPC to place.
        :type npc: gamelib.Characters.NPC
        :param x: the x coordinate to place the NPC at.
        :type x: int
        :param y: the y coordinate to place the NPC at.
        :type y: int

        If either of these parameters are not of the correct type, a HacInvalidTypeException exception is raised.

        .. Important:: If the NPC does not have an actuator, this method is going to affect a gamelib.Actuators.SimpleActuators.RandomActuator() to npc.actuator. And if npc.step == None, this method sets it to 1
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
        
    def actuate_npcs(self,level_number):
        """Actuate all NPCs on a given level

        This method actuate all NPCs on a board associated with a level. At the moment it means moving the NPCs but as the Actuators become more capable this method will evolve to allow mpre choice (like attack use objects, etc.)

        :param level_number: The number of the level to actuate NPCs in.
        :type int:

        Example:
            mygame.actuate_npcs(1)
        """
        if type(level_number) is int:
            if  level_number in self._boards.keys():
                for npc in self._boards[level_number]['npcs']:
                    self._boards[level_number]['board'].move(npc, npc.actuator.next_move(), npc.step)
            else:
                raise HacInvalidLevelException(f"Impossible to actuate NPCs for this level (level number {level_number} is not associated with any board).")
        else:
            raise HacInvalidTypeException('In actuate_npcs(level_number) the level_number must be an int.')

    def display_player_stats(self,life_model=U.RED_RECT, void_model=U.BLACK_RECT):
        """Display the player name and health.
        
        This method print the Player name, a health bar (20 blocks of life_model). When life is missing the complement (20-life missing) is printed using void_model.
        It also display the inventory value as "Score".

        :param life_model: The character(s) that should be used to represent the *remaining* life.
        :type life_model: str
        :param void_model: The character(s) that should be used to represent the *lost* life.
        :type void_model: str

        .. note:: This method might change in the futur. Particularly it could take a template of what to display.

        """
        if self.player == None:
            return ''
        info = ''
        info += f' {self.player.name}'
        nb_blocks = int( (self.player.hp / self.player.max_hp) * 20 )
        info += ' [' + life_model * nb_blocks + void_model * (20-nb_blocks) +']'
        info += '     Score: '+str(self.player.inventory.value())
        print(info)

    def move_player(self, direction, step):
        """
        Easy wrapper for Board.move().

        Example:
            mygame.move_player(Constants.RIGHT,1)
        """
        self._boards[self.current_level]['board'].move(self.player,direction,step)
    
    def display_board(self):
        """Display the current board.

        This is an alias for Board.current_board().display()
        """
        self.current_board().display()