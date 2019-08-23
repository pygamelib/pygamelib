#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..','..')))

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

# Here we define all the callbacks we are going to need
# One to damage the player (to be used with fire walls and explosions)
def damage_player(params):
    pass

# One to manage the explosions
def explosion(params):
    pass

# And one to manage the portals activation
def activate_portal(params):
    pass

# The name of board we want to load for the first level
level_1 = 'levels/TutoMap-hac-game-lib.json'

# Create the game object. We are going to use this as a global variable.
g = Game()

# Load the board as level 1
b = g.load_board(level_1,1)

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
    if 'explosion' in item.type:
        print(f"{item.model} : {item.type} {item.name}")
        # First let's set our model to the same as the current level's board void cell model.
        item.model = g.current_board().ui_board_void_cell

        # Then depending on the type of explosion we use the explosion() function.
        # This function will be called when the player interact with the GenericActionable object.
        # explosion() takes 3 parameters: the calling item, a model to use when it's exploded and a damage value to hurt the player.
        if item.type == 'simple_explosion':
            pass
        else:
            pass
    # Now let's hide the portal
    elif item.type == 'portal':
        item.model = g.current_board().ui_board_void_cell
        # Here is a small trick: we configure the portal to be overlappable so that even if the Player has a hint that something must be there (because of the trees for example), he is not bumping into an invisible wall.
        item.set_overlappable(True)
    # Finally, we set the fire walls to damage the player a bit
    elif item.type == 'fire_wall':
        pass

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
    key = Utils.get_key()
