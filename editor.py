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


def color_picker():
    global game
    game.clear_screen()
    print('Pick a form and color from the list:')
    game.display_menu('graphics_utils',Constants.ORIENTATION_HORIZONTAL,8)
    return str(input('\n(Enter a number)> '))

def sprite_picker():
    global game
    game.clear_screen()
    print('Pick a sprite from the list:')
    game.display_menu('graphics_sprites',Constants.ORIENTATION_HORIZONTAL,8)
    return str(input('\n(Enter a number)> '))

def model_picker():
    global game
    game.clear_screen()
    print("What kind of model do you want (you can edit that later)?\n1 - Colored squares and rectangles\n2 - Sprites\n3 - Set your own string of character(s)")
    choice = str( input('> ') )
    if choice == '1':
        return game.get_menu_entry('graphics_utils',color_picker())['data']
    if choice == '2':
        return game.get_menu_entry('graphics_sprites',sprite_picker())['data']
    if choice == '3':
        return str( input('Enter your string now: ') )

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
        game.add_menu_entry('graphics_utils',str(i), '"'+getattr(Utils,sp)+'"', getattr(Utils,sp))
        i += 1

i = 0
for sp in dir(Sprites):
    if not sp.startswith('__'):
        game.add_menu_entry('graphics_sprites',str(i), getattr(Sprites,sp), getattr(Sprites,sp) )
        i += 1

game.add_menu_entry('main',None,'\n=== Menu ===')
game.add_menu_entry('main','Space','Switch between edit/delete mode')
game.add_menu_entry('main','a/w/s/d','Move cursor Left/Up/Down/Right')
game.add_menu_entry('main','j/i/k/l',Utils.green_bright('Place')+' the current object and then move cursor Left/Up/Down/Right')
game.add_menu_entry('main','c','Create a new object (becomes the current object, previous object is placed in history)')
game.add_menu_entry('main','p','Modify board parameters')
game.add_menu_entry('main','P','Set player starting position')
game.add_menu_entry('main','Q','Quit the editor')

game.add_menu_entry('board',None,'=== Board ===')
game.add_menu_entry('board','1','Change '+Utils.white_bright('width')+' (only sizing up)')
game.add_menu_entry('board','2','Change '+Utils.white_bright('height')+' (only sizing up)')
game.add_menu_entry('board','3','Change '+Utils.white_bright('name'))
game.add_menu_entry('board','4','Change '+Utils.white_bright('top')+' border')
game.add_menu_entry('board','5','Change '+Utils.white_bright('bottom')+' border')
game.add_menu_entry('board','6','Change '+Utils.white_bright('left')+' border')
game.add_menu_entry('board','7','Change '+Utils.white_bright('right')+' border')
game.add_menu_entry('board','8','Change '+Utils.white_bright('void cell'))
game.add_menu_entry('board','0','Go back to the main menu')


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
    elif current_menu == 'main':
        if key == 'w':
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
        elif key in '1234567890' and current_menu == 'main':
            current_object = object_history[int(key)]
        elif key == 'P':
            game.current_board().player_starting_position = game.player.pos
            is_modified = True
            dbg_messages.append(f'New player starting position set at {game.player.pos}')
        elif key == 'p':
            current_menu = 'board'
        elif key == 'c':
            if len(object_history) <= 10 and current_object not in object_history and not isinstance(current_object,BoardItemVoid):
                object_history.append(current_object)
    elif current_menu == 'board':
        if key == "0":
            current_menu = 'main'
        elif key == "1":
            game.clear_screen()
            nw = int(input("Enter the new width: "))
            if nw >= game.current_board().size[0]:
                old_value = game.current_board().size[0]
                game.current_board().size[0] = nw
                for x in range(0,game.current_board().size[1],1):
                    for y in range(old_value,game.current_board().size[0],1):
                        game.current_board()._matrix[x].append( BoardItemVoid( model=game.current_board().ui_board_void_cell ) )
                        is_modified = True


        elif key == "2":
            game.clear_screen()
            nw = int(input("Enter the new height: "))
            if nw >= game.current_board().size[1]:
                old_value = game.current_board().size[1]
                game.current_board().size[1]=nw
                for x in range(old_value,nw,1):
                    new_array = []
                    for y in range(0, game.current_board().size[0], 1 ):
                        new_array.append( BoardItemVoid( model=game.current_board().ui_board_void_cell ) )
                    game.current_board()._matrix.append(new_array)
                    is_modified = True

        elif key == "3":
            game.clear_screen()
            n = str(input('Enter the new name: '))
            game.current_board().name = n
            is_modified = True
        elif key == '4':
            game.current_board().ui_border_top = model_picker()
            is_modified = True
        elif key == '5':
            game.current_board().ui_border_bottom = model_picker()
            is_modified = True
        elif key == '6':
            game.current_board().ui_border_left = model_picker()
            is_modified = True
        elif key == '7':
            game.current_board().ui_border_right = model_picker()
            is_modified = True
        elif key == '8':
            game.current_board().ui_board_void_cell = model_picker()
            is_modified = True

        
     # Print the screen and interface   
    game.clear_screen()
    if current_menu == 'main' or current_menu == 'board':
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
    game.display_menu(current_menu)
    for m in dbg_messages:
        Utils.debug(m)
    key = Utils.get_key()

