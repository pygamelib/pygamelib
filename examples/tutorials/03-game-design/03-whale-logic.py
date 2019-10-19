#!/usr/bin/env python3

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join("..", "..", "..")))

from gamelib.Game import Game  # noqa: E402
from gamelib.Characters import Player  # noqa: E402
from gamelib.Characters import NPC  # noqa: E402
import gamelib.Sprites as Sprites  # noqa: E402
import gamelib.Constants as Constants  # noqa: E402
import gamelib.Utils as Utils  # noqa: E402
from gamelib.Structures import Door  # noqa: E402


def refresh_screen():
    global g
    global notifications
    g.clear_screen()
    g.display_player_stats()
    g.display_board()
    print(
        Utils.cyan_bright(
            f"Inventory ({g.player.inventory.size()}/{g.player.inventory.max_size})  "
        )
    )
    if g.player.inventory.size() > 0:
        # If inventory is not empty print it
        items_by_type = {}
        for item_name in g.player.inventory.items_name():
            item = g.player.inventory.get_item(item_name)
            if item.type in items_by_type.keys():
                items_by_type[item.type]["cumulated_size"] += item.size()
            else:
                items_by_type[item.type] = {
                    "cumulated_size": item.size(),
                    "model": item.model,
                    "name": item.name,
                }
        count = 1
        for k in items_by_type.keys():
            print(
                f" {items_by_type[k]['model']} : {items_by_type[k]['cumulated_size']} ",
                end="",
            )
            count += 1
            if count == 5:
                count = 0
                print("\n", end="")
        print("\n", end="")
    for n in notifications:
        print(n)


# Here we define all the callbacks we are going to need
# One to damage the player (to be used with fire walls and explosions)
def damage_player(params):
    global g
    g.player.hp -= params[0]


# One to manage the explosions
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
        item.set_overlappable(True)
        item.set_restorable(True)
        time.sleep(0.5)
        damage_player([damage_value])
    else:
        damage_player([damage_value / 2])


# And one to manage the portals activation
def activate_portal(params):
    global g
    level = params[0]
    if level == 1:
        if g.current_board().item(3, 3).model == Sprites.CYCLONE:
            # That logic is just a placeholder for the moment, ultimately it will lead
            # to the next level
            g.clear_screen()
            print(Utils.green_bright("CONGRATULATIONS\n\nYOU WIN!"))
            exit()


def whale_behavior():
    global g
    global notifications
    whales = []
    # Here we only ask for the movable objects (like the NPCs) that have "whale" in
    # their type. This matches both "left_whale" and "right_whale"
    for item in g.current_board().get_movables(type="whale"):
        if item.type == "right_whale" or item.type == "left_whale":
            whales.append(item)
    # if right_whale != None:
    #     for item in g.neighbors(2,right_whale):
    #         if isinstance(item,Player):
    #             inventory_item_name = None
    #             for item_name in g.player.inventory.items_name():
    #                 if item_name.startswith('Happy Octopus'):
    #                    inventory_item_name = item_name
    #                    break
    #             if inventory_item_name != None:
    #                 g.player.inventory.delete_item(inventory_item_name)
    #                 g.current_board().place_item(BoardItemVoid(model=g.current_board().ui_board_void_cell),25,32)
    if len(whales) > 0:
        for whale in whales:
            # Let's look at the neighborhood of the whales (within a 2 cells radius)
            for item in g.neighbors(2, whale):
                # If there is a Player around, then look into the inventory...
                if isinstance(item, Player):
                    inventory_item_name = None
                    # And reserve that Happy Octopus if present
                    for item_name in g.player.inventory.items_name():
                        if item_name.startswith("Happy Octopus"):
                            inventory_item_name = item_name
                            break
                    if inventory_item_name is not None:
                        row = 0
                        column = 0
                        if whale.type == "left_whale":
                            g.add_npc(
                                1,
                                NPC(
                                    model=Sprites.OCTOPUS,
                                    name="Swimming Octopus (Left)",
                                    type="swimming_octopus",
                                ),
                                8,
                                16,
                            )
                            row = 26
                            column = 32
                        else:
                            g.add_npc(
                                1,
                                NPC(
                                    model=Sprites.OCTOPUS,
                                    name="Swimming Octopus (Right)",
                                    type="swimming_octopus",
                                ),
                                14,
                                37,
                            )
                            row = 25
                            column = 32
                        notifications.append(
                            whale.model
                            + ": Thank you! Here, let me extinguish that fire for you!"
                        )
                        notifications.append(whale.model + ": " + Sprites.WATER_DROP)
                        g.player.inventory.delete_item(inventory_item_name)
                        g.current_board().item(row, column).model = Sprites.WATER_DROP
                        whale.type = "happy_" + whale.type
                        refresh_screen()
                        time.sleep(1.5)
                        g.current_board().clear_cell(row, column)
                        refresh_screen()

                    else:
                        notifications.append(
                            whale.model
                            + ": I am so lonely, if only I had an aquatic friend to"
                            + " play with..."
                        )


# The board we want to load for the first level
level_1 = "levels/TutoMap-hac-game-lib.json"

# And the game over screen
game_over = "levels/Game_Over.json"

# The notifications are going to be used to give info to the player without entering a
# full dialog mode.
# IMPORTANT: The player movement clears the notifications not the rest of the game.
# As we are going to multithread the game at some point it's important to take the
# right decision from start.
notifications = []

# Create the game object. We are going to use this as a global variable.
g = Game()

# Load the board as level 1
b = g.load_board(level_1, 1)
# The game over screen is going to be level 999. There is no reason for that, it is
# just a convention as I don't think that this game is going to have more than 998
# levels.
g.load_board(game_over, 999)

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
        # GenericActionable object. explosion() takes 3 parameters: the calling item,
        # a model to use when it's exploded and a damage value to hurt the player.
        if item.type == "simple_explosion":
            item.action = explosion
            item.action_parameters = [item, Sprites.FIRE, 10]
        else:
            item.action = explosion
            item.action_parameters = [item, Sprites.EXPLOSION, 80]
    elif item.type == "portal":
        item.model = g.current_board().ui_board_void_cell
        item.action = activate_portal
        item.action_parameters = [1]
        # Here is a small trick: we configure the portal to be overlappable so that
        # even if the Player has a hint that something must be there (because of the
        # trees for example), he is not bumping into an invisible wall.
        item.set_overlappable(True)
    # Finally, we set the fire walls to damage the player a bit
    elif item.type == "fire_wall":
        item.action = damage_player
        item.action_parameters = [10]

key = None
# This one is going to be useful later
run = True

while run:
    if key == "w":
        g.move_player(Constants.UP, 1)
    elif key == "s":
        g.move_player(Constants.DOWN, 1)
    elif key == "a":
        g.move_player(Constants.LEFT, 1)
    elif key == "d":
        g.move_player(Constants.RIGHT, 1)
    elif key == "q":
        run = False
        break
    refresh_screen()
    notifications.clear()
    g.actuate_npcs(g.current_level)
    if g.current_level == 1:
        whale_behavior()
    if g.player.hp <= 0:
        g.clear_screen()
        Utils.print_white_on_red(
            f"\n\n\n\t{g.player.name} is dead!\n\t      ** Game over **     \n\n"
        )
        g.change_level(999)
        g.display_board()
        break
    key = Utils.get_key()
