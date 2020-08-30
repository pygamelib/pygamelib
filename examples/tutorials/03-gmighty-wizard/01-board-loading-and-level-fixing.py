#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.abspath(os.path.join("..", "..", "..")))

from gamelib.Game import Game  # noqa: E402
from gamelib.Characters import Player  # noqa: E402
from gamelib.Structures import Door  # noqa: E402
import gamelib.Sprites as Sprites  # noqa: E402
import gamelib.Constants as Constants  # noqa: E402
import gamelib.Utils as Utils  # noqa: E402

# Here are our global variables (it is usually a bad idea to use global variables but
# it will simplify that tutorial, keep in mind that we don't usually rely on global
# variables)

# Create the game object. We are going to use this as a global variable.
g = Game()
# Load the board as level 1
b = g.load_board("levels/TutoMap-hac-game-lib.json", 1)


def refresh_screen():
    global g

    g.clear_screen()
    g.display_player_stats()
    g.display_board()


def damage_player(params):
    pass


def explosion(params):
    pass


def activate_portal(params):
    pass


# Create the player object.
g.player = Player(name="The Mighty Wizard", model=Sprites.MAGE)
g.change_level(1)

# Now we need to fix the river (it's missing 2 tiles of water)
# First let's move the NPCs so the whales are not replaced by our new tiles.
g.actuate_npcs(1)
# Now let's place the 2 river tiles (we use the Door object as a shortcut to get a
# overlapable, restorable item)
g.current_board().place_item(Door(model=Utils.BLUE_SQUARE), 0, 26)
g.current_board().place_item(Door(model=Utils.BLUE_SQUARE), 11, 0)

# Now we need to take care of the explosions. Hide them and set the callback functions.
for item in g.current_board().get_immovables():
    # Here we need to set the functions that are going to be called when the player
    # touches our hidden traps.
    if item.type == "simple_explosion" or item.type == "mega_explosion":
        # First let's set our model to the same as the current level's board void cell
        # model.
        item.model = g.current_board().ui_board_void_cell

        # Then depending on the type of explosion we use the explosion() function.
        # This function will be called when the player interact with the
        # GenericActionable object.
        # explosion() takes 3 parameters: the calling item, a model to use when it's
        # exploded and a damage value to hurt the player.
        if item.type == "simple_explosion":
            item.action = explosion
            item.action_parameters = [item, Sprites.FIRE, 10]
        else:
            item.action = explosion
            item.action_parameters = [item, Sprites.EXPLOSION, 80]
    elif item.type == "portal":
        item.model = g.current_board().ui_board_void_cell
        item.action = activate_portal
        item.action_parameters = [2]
        item.set_overlappable(True)
    # Set a higher score value to the money bags
    elif item.type == "money":
        item.value = 100
    # Same thing with the Scroll of Wisdom.
    elif item.type == "scroll":
        item.value = 1000
    # Finally, we set the fire walls to damage the player a bit
    elif item.type == "fire_wall":
        item.action = damage_player
        item.action_parameters = [10]

# This variable is the input buffer.
key = None
# This one is going to be useful later
run = True
# This one will hold our level history (only the previous)
previous_level = None

while run:
    if key == "q":
        run = False
        break
    elif key == "w":
        g.move_player(Constants.UP, 1)
    elif key == "s":
        g.move_player(Constants.DOWN, 1)
    elif key == "a":
        g.move_player(Constants.LEFT, 1)
    elif key == "d":
        g.move_player(Constants.RIGHT, 1)
    refresh_screen()
    g.actuate_npcs(g.current_level)
    key = Utils.get_key()
