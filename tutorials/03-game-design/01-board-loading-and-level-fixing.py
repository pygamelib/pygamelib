#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..')))

from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
from gamelib.Structures import Door
import time
import sys

def refresh_screen():
    global g
    g.clear_screen()
    g.display_player_stats()
    g.display_board()
    if g.player.inventory.size() > 0:
        # If inventory is not empty print it
        items_by_type = {}
        for item_name in g.player.inventory.items_name():
            item = g.player.inventory.get_item(item_name)
            if item.type in items_by_type.keys():
                items_by_type[item.type]['cumulated_size'] += item.size()
            else:
                items_by_type[item.type] = {'cumulated_size':item.size(),'model':item.model,'name':item.name}
        count = 1
        for k in items_by_type.keys():
            print(f" {items_by_type[k]['model']} : {items_by_type[k]['cumulated_size']} ",end='')
            count += 1
            if count == 5:
                count = 0
                print("\n",end='')
        print("\n",end='')

def damage_player(params):
    global g
    g.player.hp -= params[0]

def explosion(params):
    global g
    item = params[0]
    exploded_model = params[1]
    damage_value = params[2]
    if item.model != exploded_model:
        item.model = Sprites.BOMB
        refresh_screen()
        time.sleep(0.5)
        item.model = exploded_model
        refresh_screen()
        item.set_overlapable(True)
        item.set_restorable(True)
    damage_player([damage_value])

def activate_portal(params):
    global g
    level = params[0]
    if level == 1:
        if g.current_board().item(3,3).model == Sprites.CYCLONE:
            # That logic is just a placeholder for the moment, ultimately it will lead to the next level
            g.clear_screen()
            print( Utils.green_bright("CONGRATULATIONS\n\nYOU WIN!") )
            exit()

# The board we want to load for the first level
level_1 = 'levels/TutoMap-hac-game-lib.json'

# And the game over screen
game_over = 'levels/Game_Over.json'

# Create the game object. We are going to use this as a global variable.
g = Game()

# Load the board as level 1
b = g.load_board(level_1,1)
# The game over screen is going to be level 999. There is no reason for that, it is just a convention as I don't think that this game is going to have more than 998 levels.
g.load_board(game_over,999)

# Create the player object.
g.player = Player(name='The Mighty Wizard',model=Sprites.MAGE)
g.change_level(1)

# Now we need to fix the river (it's missing 2 tiles of water)
# First let's move the NPCs so the whales are not replaced by our new tiles.
g.actuate_npcs(1)
# Now let's place the 2 river tiles (we use the Door object as a shortcut to get a overlapable, restorable item)
g.current_board().place_item(Door(model=Utils.BLUE_SQUARE),0,26)
g.current_board().place_item(Door(model=Utils.BLUE_SQUARE),11,0)

# Now we need to take care of the explosions. Hide them and set the callback functions.
for item in g.current_board().get_immovables():
    # Here we need to set the functions that are going to be called when the player touches our hidden traps.
    if item.type == 'simple_explosion' or item.type == 'mega_explosion':
        # First let's set our model to the same as the current level's board void cell model.
        item.model = g.current_board().ui_board_void_cell

        # Then depending on the type of explosion we use the explosion() function.
        # This function will be called when the player interact with the GenericActionable object.
        # explosion() takes 3 parameters: the calling item, a model to use when it's exploded and a damage value to hurt the player.
        if item.type == 'simple_explosion':
            item.action = explosion
            item.action_parameters = [item,Sprites.FIRE,20]
        else:
            item.action = explosion
            item.action_parameters = [item,Sprites.EXPLOSION,100]
    # Now let's hide the portal
    elif item.type == 'portal':
        item.model = g.current_board().ui_board_void_cell
        item.action = activate_portal
        item.action_parameters = [1]
    # Finally, we set the fire walls to damage the player a bit
    elif item.type == 'fire_wall':
        item.action = damage_player
        item.action_parameters = [10]

key = None
# This one is going to be useful later
run = True

while run:
    if key == 'w':
        g.move_player(Constants.UP,1)
    elif key == 's':
        g.move_player(Constants.DOWN,1)
    elif key == 'a':
        g.move_player(Constants.LEFT,1)
    elif key == 'd':
        g.move_player(Constants.RIGHT,1)
    elif key == 'q':
        run = False
        break
    refresh_screen()
    g.actuate_npcs(g.current_level)
    if g.player.hp <= 0:
        g.clear_screen()
        Utils.print_white_on_red(f"\n\n\n\t{g.player.name} is dead!\n\t      ** Game over **     \n\n")
        g.change_level(999)
        g.display_board()
        break
    key = Utils.get_key()
