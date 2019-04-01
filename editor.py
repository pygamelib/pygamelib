#!/usr/bin/env python3

import gamelib.Utils as Utils
import gamelib.Constants as Constants
import gamelib.Structures as Structures
import gamelib.Sprites as Sprites
from gamelib.Game import Game
from gamelib.Characters import Player
from gamelib.Board import Board
from gamelib.BoardItem import BoardItemVoid
import os
from copy import deepcopy

# Global variables
is_modified = False
edit_mode = True

# Functions definition
def place_and_go(object,x,y,direction):
    global is_modified
    global game
    game.move_player(direction,1)
    game.current_board().place_item( deepcopy(object),x,y)
    is_modified = True

def clear_and_go(direction):
    global is_modified
    global game
    new_x = game.player.pos[0]
    new_y = game.player.pos[1]
    if direction == Constants.DOWN:
        new_x += 1
    elif direction == Constants.UP:
        new_x -= 1
    elif direction == Constants.LEFT:
        new_y -= 1
    elif direction == Constants.RIGHT:
        new_y += 1

    if new_x < 0 or new_y < 0 or new_x > (game.current_board().size[1]-1) or new_y > (game.current_board().size[0]-1):
        Utils.warn(f"Cannot remove anything at [{new_x},{new_y}] as it is out of bound.")
    else:
        game.current_board().clear_cell(new_x,new_y)
        game.move_player(direction,1)
        is_modified = True

def switch_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    if edit_mode:
        game.update_menu_entry('main','j/i/k/l',Utils.green_bright('Place')+' the current object and then move cursor Left/Up/Down/Right')
    else:
        game.update_menu_entry('main','j/i/k/l','Move cursor Left/Up/Down/Right and '+Utils.red_bright('Delete')+' anything that was at destination.')

# Main program
game = Game()
game.player = Player(model='[]')
key = 'None'
current_object = BoardItemVoid(model='None')
object_history = []
current_menu = 'main'

game.clear_screen()
print( Utils.cyan_bright("HAC-GAME-LIB - EDITOR v"+Constants.HAC_GAME_LIB_VERSION) )

print('Looking for existing maps in hac-maps/ directory...',end='')
hmaps = []
try:
    hmaps = os.listdir('hac-maps/')
    print(Utils.green('OK'))
except FileNotFoundError as e:
    print(Utils.red('KO'))

if len(hmaps) > 0:
    map_num = 0
    for m in hmaps:
        print(f"{map_num} - edit hac-maps/{m}")
        map_num += 1
else:
    print("No pre-existing map found.")
print("n - create a new map")
print("q - Quit the editor")
choice = str(input("> "))
if choice == "q":
    print("Good Bye!")
    exit()
elif choice == "n":
    print("First we need some informations on your new board:")
    name = str( input('Name: ') )
    width = int( input('Width (in number of cells): ') )
    height = int( input('Height (in number of cells): ') )
    game.add_board(1, Board(name=name,size=[width,height], ui_borders=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE) )
    is_modified=True
elif int(choice) < len(hmaps):
    game.load_board('hac-maps/'+hmaps[int(choice)],1)

game.change_level(1)

# Build the menus
i = 0
for sp in dir(Utils):
    if sp.endswith('_SQUARE') or sp.endswith('_RECT'):
        game.add_menu_entry('graphics_utils',i, '"'+getattr(Utils,sp)+'"' )
        i += 1

i = 0
for sp in dir(Sprites):
    if not sp.startswith('__'):
        game.add_menu_entry('graphics_sprites',i, getattr(Sprites,sp) )
        i += 1

game.add_menu_entry('main',None,'\n=== Menu ===')
game.add_menu_entry('main','Space','Switch between edit/delete mode')
game.add_menu_entry('main','a/w/s/d','Move cursor Left/Up/Down/Right')
game.add_menu_entry('main','j/i/k/l',Utils.green_bright('Place')+' the current object and then move cursor Left/Up/Down/Right')
game.add_menu_entry('main','c','Create a new object (becomes the current object, previous object is placed in history)')
game.add_menu_entry('main','p','Modify board parameters')
game.add_menu_entry('main','P','Set player starting position')
game.add_menu_entry('main','Q','Quit the editor')

# TEST DATA
object_history.append(Structures.Wall(model=Sprites.WALL))
object_history.append( Structures.Treasure(model=Sprites.CROWN) )

while True:
    dbg_messages = []    

    if key == 'Q':
        if is_modified:
            print("Board has been modified, do you want to save it to avoid loosing your changes? (y/n)")
            answer = str(input('> '))
            if answer.startswith('y'):
                if not os.path.exists('hac-maps') or not os.path.isdir('hac-maps'):
                    os.makedirs('hac-maps')
                game.save_board(1,'hac-maps/'+game.current_board().name.replace(' ','_')+'.json')
        break
    elif key == 'w':
        game.move_player(Constants.UP,1)
    elif key == 's':
        game.move_player(Constants.DOWN,1)
    elif key == 'a':
        game.move_player(Constants.LEFT,1)
    elif key == 'd':
        game.move_player(Constants.RIGHT,1)
    elif key == "k" and edit_mode:
        place_and_go( current_object, game.player.pos[0], game.player.pos[1], Constants.DOWN )
    elif key == "i" and edit_mode:
        place_and_go( current_object, game.player.pos[0], game.player.pos[1], Constants.UP )
    elif key == "j" and edit_mode:
        place_and_go( current_object, game.player.pos[0], game.player.pos[1], Constants.LEFT )
    elif key == "l" and edit_mode:
        place_and_go( current_object, game.player.pos[0], game.player.pos[1], Constants.RIGHT )
    elif key == "k" and not edit_mode:
        clear_and_go(Constants.DOWN)
    elif key == "i" and not edit_mode:
        clear_and_go(Constants.UP)
    elif key == "j" and not edit_mode:
        clear_and_go(Constants.LEFT)
    elif key == "l" and not edit_mode:
        clear_and_go(Constants.RIGHT)
    elif key == ' ':
        switch_edit_mode()
    elif key in '1234567890':
        current_object = object_history[int(key)]
    elif key == 'P':
        game.current_board().player_starting_position = game.player.pos
        is_modified = True
        dbg_messages.append(f'New player starting position set at {game.player.pos}')
        
        
     # Print the screen and interface   
    game.clear_screen()
    if current_menu == 'main':
        print(Utils.white_bright('Current mode: '),end='')
        if edit_mode:
            print(Utils.green_bright("EDIT"),end='')
        else:
            print(Utils.red_bright('DELETE'),end='')
        print(f' | Board: {game.current_board().name} - {game.current_board().size} | Cursor @ {game.player.pos}')
    game.display_board()
    if len(object_history) > 10:
        del(object_history[0])
    if current_menu == 'main':
        print('History:')
        cnt = 0
        for o in object_history:
            print(f"{cnt}: {o.model}", end='  ')
            cnt += 1
        print('')
        print(f'Current object: {current_object.model}')
    game.display_menu('main')
    for m in dbg_messages:
        Utils.debug(m)
    key = Utils.get_key()

