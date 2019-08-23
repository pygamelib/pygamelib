#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '..','..')))

from gamelib.Game import Game
from gamelib.Characters import Player, NPC
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
from gamelib.Structures import Door
from gamelib.BoardItem import BoardItemVoid
import time
import sys

def refresh_screen():
    global g
    global notifications
    global current_menu
    g.clear_screen()
    g.display_player_stats()
    g.display_board()
    print( Utils.cyan_bright(f"Inventory ({g.player.inventory.size()}/{g.player.inventory.max_size})  ") )
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
    # Then we display the menu
    g.display_menu(current_menu,Constants.ORIENTATION_VERTICAL,15)
    # And finally the notifications
    for n in notifications:
        print(n)

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
        item.set_overlappable(True)
        item.set_restorable(True)
        time.sleep(0.5)
        damage_player([damage_value])
    else:
        damage_player([damage_value/2])

def activate_portal(params):
    global g
    level = params[0]
    if level == 1:
        if g.current_board().item(3,3).model == Sprites.CYCLONE:
            # That logic is just a placeholder for the moment, ultimately it will lead to the next level
            g.clear_screen()
            print( Utils.green_bright("CONGRATULATIONS\n\nYOU WIN!") )
            exit()

def whale_behavior():
    # This function is really only the minimum viable product. We could do much better, for example:
    # 1) We could implement dialogues so we leave to the player to give or not the octopus.
    # 2) We could implement different dialogues to give hints more gradually to the player.
    # 3) One more thing is that we should use Actuators.pause() and Actuator.run() to prevent the whale from moving away from the player (that part is going to be critical when we multi-thread the program).
    # That list is non exhaustive.
    global g
    global notifications
    whales = []
    # Here we only ask for the movable objects (like the NPCs) that have "whale" in their type. 
    # This matches both "left_whale" and "right_whale"
    for item in g.current_board().get_movables(type="whale"):
        if item.type == 'right_whale' or item.type == 'left_whale':
            whales.append(item)
    if len(whales) > 0:
        for whale in whales:
            # Let's look at the neighborhood of the whales (within a 2 cells radius)
            for item in g.neighbors(2,whale):
                # If there is a Player around, then look into the inventory...
                if isinstance(item,Player):
                    inventory_item_name = None
                    # And reserve that Happy Octopus if present
                    for item_name in g.player.inventory.items_name():
                        if item_name.startswith('Happy Octopus'):
                            inventory_item_name = item_name
                            break
                    if inventory_item_name != None:
                        row = 0
                        column = 0
                        if whale.type == 'left_whale':
                            g.add_npc(1,NPC(model=Sprites.OCTOPUS,name="Swimming Octopus (Left)",type="swimming_octopus"),8,16)
                            row = 26
                            column = 32
                        else:
                            g.add_npc(1,NPC(model=Sprites.OCTOPUS,name="Swimming Octopus (Right)",type="swimming_octopus"),14,37)
                            row = 25
                            column = 32
                        notifications.append(whale.model+": Thank you! Here, let me extinguish that fire for you!")
                        notifications.append(whale.model+": "+Sprites.WATER_DROP)
                        g.player.inventory.delete_item(inventory_item_name)
                        g.current_board().item(row,column).model = Sprites.WATER_DROP
                        whale.type = 'happy_' + whale.type
                        refresh_screen()
                        time.sleep(1.5)
                        g.current_board().clear_cell(row,column)
                        refresh_screen()
                        
                    else:
                        notifications.append(whale.model+": I am so lonely, if only I had an aquatic friend to play with...") 

def portal_fairy_behavior():
    # That function is our portal fairy controller.
    # It works a bit like the whale controller: look around for a player, offer a dialog and 
    pass

# The board we want to load for the first level
level_1 = 'levels/TutoMap-hac-game-lib.json'

# The help level (a header for our menu, boards can be used for many things)
help_menu = 'levels/Help_Menu.json'

# And the game over screen
game_over = 'levels/Game_Over.json'

# The notifications are going to be used to give info to the player without entering a full dialog mode.
# IMPORTANT: The player movement clears the notifications not the rest of the game. As we are going to multithread the game at some point it's important to take the right decision from start.
notifications = []

# Now create a variable to hold the current menu.
current_menu = 'default'

# Create the game object. We are going to use this as a global variable.
g = Game()

# Load the board as level 1
b = g.load_board(level_1,1)
# The game over screen is going to be level 999. There is no reason for that, it is just a convention as I don't think that this game is going to have more than 998 levels.
g.load_board(game_over,999)
# And help 998
g.load_board(help_menu,998)

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
            item.action_parameters = [item,Sprites.FIRE,10]
        else:
            item.action = explosion
            item.action_parameters = [item,Sprites.EXPLOSION,80]
    elif item.type == 'portal':
        item.model = g.current_board().ui_board_void_cell
        item.action = activate_portal
        item.action_parameters = [1]
        item.set_overlappable(True)
    # Set a higher score value to the money bags
    elif item.type == 'money':
        item.value = 100
    # Same thing with the Scroll of Wisdom.
    elif type == 'scroll':
        item.value = 1000
    # Finally, we set the fire walls to damage the player a bit
    elif item.type == 'fire_wall':
        item.action = damage_player
        item.action_parameters = [10]

# Now let's build the menus
# First the default menu with only one entry : the help menu.
g.add_menu_entry('default','h','Type the "h" key to display the help menu')
# Now the actual help menu
g.add_menu_entry('help','w','Move the player up')
g.add_menu_entry('help','s','Move the player down')
g.add_menu_entry('help','a','Move the player left')
g.add_menu_entry('help','d','Move the player right')
g.add_menu_entry('help','q','Quit the game')
g.add_menu_entry('help','b','Go back to the game')

# This variable is the input buffer.
key = None
# This one is going to be useful later
run = True
# This one will hold our level history (only the previous)
previous_level = None

while run:
    if key == 'w':
        g.move_player(Constants.UP,1)
    elif key == 's':
        g.move_player(Constants.DOWN,1)
    elif key == 'a':
        g.move_player(Constants.LEFT,1)
    elif key == 'd':
        g.move_player(Constants.RIGHT,1)
    elif key == 'h':
        current_menu = 'help'
    elif key == 'b':
        current_menu = 'default'
    elif key == 'q':
        run = False
        break
    if current_menu == 'help' and g.current_level != 998:
        previous_level = g.current_level
        g.pause()
        g.change_level(998)
    elif current_menu == 'default' and g.current_level > 2:
        g.change_level(previous_level)
        g.start()
        previous_level = None
    refresh_screen()
    notifications.clear()
    g.actuate_npcs(g.current_level)
    # Here we do everything related to the first level.
    if g.current_level == 1:
        whale_behavior()
        portal_fairy_behavior()
    # Now, let's take care of the case where player's life is down to zero or worst.
    if g.player.hp <= 0:
        # First, does he have a Scroll of Wisdom. If yes we save him and warn him that next time he is dead.
        if len(g.player.inventory.search("Scroll of Wisdom")) > 0:
            # To do so we set the HP back to the maximum
            g.player.hp = g.player.max_hp
            # Warn the player
            print( Utils.red_bright('You have been saved by the Scroll of Wisdom, be careful next time you will die!') )
            # And consume the scroll in the process
            g.player.inventory.delete_item("Scroll of Wisdom")
        else:
            # If he doesn't, well... Death is the sentence and that's game over.
            g.clear_screen()
            Utils.print_white_on_red(f"\n\n\n\t{g.player.name} is dead!\n\t      ** Game over **     \n\n")
            g.change_level(999)
            g.display_board()
            break
    Utils.debug(f"Game state is: {g.state}")
    key = Utils.get_key()
