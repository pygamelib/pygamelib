#!/usr/bin/env python3

import sys
import os
import time
import random

sys.path.append(os.path.abspath(os.path.join("..", "..", "..")))

from gamelib.Game import Game  # noqa: E402
from gamelib.Board import Board  # noqa: E402
from gamelib.Characters import Player  # noqa: E402
from gamelib.Characters import NPC  # noqa: E402
import gamelib.Sprites as Sprites  # noqa: E402
import gamelib.Constants as Constants  # noqa: E402
import gamelib.Utils as Utils  # noqa: E402
from gamelib.Structures import Door  # noqa: E402
from gamelib.Structures import Treasure  # noqa: E402
from gamelib.BoardItem import BoardItemVoid  # noqa: E402

# Here are our global variables (it is usually a bad idea to use global variables but
# it will simplify that tutorial, keep in mind that we don't usually rely on global
# variables)
# The board we want to load for the first level
level_1 = "levels/TutoMap-hac-game-lib.json"

# The help level (a header for our menu, boards can be used for many things)
help_menu = "levels/Help_Menu.json"

# And the game over screen
game_over = "levels/Game_Over.json"

# The notifications are going to be used to give info to the player without entering a
# full dialog mode.
# IMPORTANT: The player movement clears the notifications not the rest of the game. As
# we are going to multithread the game at some point it's important to take the right
# decision from start.
notifications = []

# Now create a variable to hold the current menu.
current_menu = "default"

# We also need to keep track of how much gold was given to the fairy
fairy_gold = 0

# We will need to keep a counter for the number of turns left in level 2
level_2_turns_left = 21

# Create the game object. We are going to use this as a global variable.
g = Game()


def print_animated(message):
    for line in message:
        print(line, end="", flush=True)
        if line == "\n":
            time.sleep(1)
        else:
            time.sleep(0.1)


def introduction_scene():
    intro_dialog = (
        f"{Sprites.MAGE}: Hu... Where am I?\n"
        f"{Sprites.UNICORN_FACE}: Welcome Mighty Wizard!\n"
        f"{Sprites.UNICORN_FACE}: Your help is needed to bring balance to the "
        f"wildlife of this world.\n"
        f"{Sprites.UNICORN_FACE}: Only then will you be able to ask the portal fairy "
        f"to open the portal to continue your journey.\n"
        f"{Sprites.UNICORN_FACE}: Good luck!\n{Sprites.MAGE}: Ok then, let's go!"
    )

    g.clear_screen()
    print_animated(intro_dialog)

    input("\n\n(hit the ENTER key to start the game)")


def refresh_screen():
    global g
    global notifications
    global current_menu
    global level_2_turns_left
    g.clear_screen()
    g.display_player_stats()
    g.display_board()
    if g.current_level == 2:
        print(
            Utils.cyan_bright(
                f"Inventory ({g.player.inventory.size()}/"
                f"{g.player.inventory.max_size})  "
            )
            + Utils.green_bright(f"Turns left: {level_2_turns_left} ")
        )
    else:
        print(
            Utils.cyan_bright(
                (
                    f"Inventory ({g.player.inventory.size()}/"
                    f"{g.player.inventory.max_size})  "
                )
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
    # Then we display the menu
    g.display_menu(current_menu, Constants.ORIENTATION_VERTICAL, 15)
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
        damage_player([damage_value / 2])


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
    elif level == 2:
        g.clear_screen()
        print_animated(
            f"{Sprites.UNICORN_FACE}: Congratulations {g.player.name},"
            f" you found the entrance to a world of riches!\n{Sprites.UNICORN_FACE}:"
            f" However, your time is limited and you will need to grab as much"
            f" treasures as you can in 20 moves only!\n{Sprites.UNICORN_FACE}:"
            f" Good luck!"
        )
        input("\n\n(Hit ENTER when you are ready to enter the world of riches)")
        g.player.inventory.max_size += 1500
        g.change_level(2)


def whale_behavior():
    # This function is really only the minimum viable product. We could do much better,
    # for example:
    # 1) We could implement dialogues so we leave to the player to give or not the
    # octopus.
    # 2) We could implement different dialogues to give hints more gradually to the
    # player.
    # 3) One more thing is that we should use Actuators.pause() and Actuator.run() to
    # prevent the whale from moving away from the player (that part is going to be
    # critical when we multi-thread the program).
    # That list is non exhaustive.
    global g
    global notifications
    whales = []
    # Here we only ask for the movable objects (like the NPCs) that have "whale" in
    # their type.
    # This matches both "left_whale" and "right_whale"
    for item in g.current_board().get_movables(type="whale"):
        if item.type == "right_whale" or item.type == "left_whale":
            whales.append(item)
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
                                    model=Utils.Back.BLUE
                                    + Sprites.OCTOPUS
                                    + Utils.Style.RESET_ALL,
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
                                    model=Utils.Back.BLUE
                                    + Sprites.OCTOPUS
                                    + Utils.Style.RESET_ALL,
                                    name="Swimming Octopus (Right)",
                                    type="swimming_octopus",
                                ),
                                14,
                                37,
                            )
                            row = 25
                            column = 32
                        notifications.append(
                            f"{whale.model}: Thank you! Here, let me extinguish that "
                            f"fire for you!"
                        )
                        notifications.append(f"{whale.model}: {Sprites.WATER_DROP}")
                        g.player.inventory.delete_item(inventory_item_name)
                        g.current_board().item(row, column).model = Sprites.WATER_DROP
                        whale.type = f"happy_{whale.type}"
                        refresh_screen()
                        time.sleep(1.5)
                        g.current_board().clear_cell(row, column)
                        refresh_screen()

                    else:
                        notifications.append(
                            f"{whale.model}: I am so lonely, if only I had an aquatic "
                            f"friend to play with..."
                        )


def update_fairy_dialog():
    # That function is updating the fairy dialog.
    global g
    # If the menu is not empty we delete it.
    if g.get_menu_entry("portal_fairy_dialog", "1") is not None:
        g.delete_menu_category("portal_fairy_dialog")

    g.add_menu_entry(
        "portal_fairy_dialog",
        None,
        f"{Sprites.FAIRY} Welcome, I am the portal fairy, I can open a portal to a"
        f" secret place.",
    )
    g.add_menu_entry(
        "portal_fairy_dialog",
        None,
        f"{Utils.BLACK_SQUARE} At last I could but I am all out of gold. *sigh*",
    )
    g.add_menu_entry(
        "portal_fairy_dialog",
        None,
        f"{Utils.BLACK_SQUARE} If only I had some I would be happy to open a portal"
        f" for you.",
    )
    g.add_menu_entry("portal_fairy_dialog", "1", "Tell the fairy you have no gold.")
    money_bags = g.player.inventory.search("Money")
    if len(money_bags) >= 1:
        g.add_menu_entry(
            "portal_fairy_dialog", "2", "Give 1 bag of gold to the portal fairy."
        )
    if len(money_bags) >= 2:
        g.add_menu_entry(
            "portal_fairy_dialog", "3", "Give 2 bag of gold to the portal fairy."
        )
    if len(money_bags) >= 3:
        g.add_menu_entry(
            "portal_fairy_dialog",
            "4",
            "Give all your bags of gold to the portal fairy.",
        )


def portal_fairy_behavior():
    # That function is our portal fairy controller.
    # It works a bit like the whale controller: look around for a player, offer a
    # dialog and ultimately open the portal.
    global g
    global current_menu
    global fairy_gold
    fairy = g.current_board().get_movables(type="fairy")
    portal = g.current_board().get_immovables(type="portal")
    if g.player in g.neighbors(1, fairy[0]):
        if portal[0].model == g.current_board().ui_board_void_cell:
            # If the player is around the fairy, then we set the menu to the portal
            # fairy dialog
            current_menu = "portal_fairy_dialog"
            # And pause the other NPC to refresh the screen
            g.pause()
            # Before refreshing we update the dialog
            update_fairy_dialog()
            refresh_screen()
            # If the player has gold in his inventory we give the possibility to give it
            #  to the fairy.
            money_bags = g.player.inventory.search("Money")
            # Now we want to get the answer immediately, we don't want that function to
            # return.
            # Note: This is going to be a problem when we multithread this code. But
            # it's going to be a good exercise.
            key = Utils.get_key()
            if key == "1":
                print(f"{Sprites.FAIRY} That is too bad, good bye.")
                current_menu = "default"
                refresh_screen()
            elif key == "2":
                fairy_gold += money_bags[0].value
                g.player.inventory.delete_item(money_bags[0].name)
            elif key == "3":
                fairy_gold += money_bags[0].value
                fairy_gold += money_bags[1].value
                g.player.inventory.delete_item(money_bags[0].name)
                g.player.inventory.delete_item(money_bags[1].name)
            elif key == "4":
                for b in money_bags:
                    fairy_gold += b.value
                    g.player.inventory.delete_item(b.name)
            update_fairy_dialog()
            refresh_screen()
            if fairy_gold >= 300:
                refresh_screen()
                print(f"{Sprites.FAIRY} Great! Thank you!! Now let's do some magic.")
                print(
                    f"{Utils.BLACK_SQUARE}{Sprites.CYCLONE} By my powers, cometh forth"
                    f" dimensional portal {Sprites.CYCLONE}"
                )
                portal[0].model = Sprites.CYCLONE
                portal[0].set_overlappable(False)
                time.sleep(2)
                current_menu = "default"
                refresh_screen()
            elif fairy_gold < 300 and (
                key == "1" or key == "2" or key == "3" or key == "4"
            ):
                print(
                    f"{Sprites.FAIRY} Thank you, that is a good start but I still "
                    f"don't have enough gold to open a portal."
                )
            # When we are finished we un-pause the game
            g.start()
        else:
            print(
                f"{Sprites.FAIRY} I have already opened the only portal I could in "
                f"this world!"
            )


def teleport_player(row, column):
    g.current_board().clear_cell(g.player.pos[0], g.player.pos[1])
    g.current_board().place_item(g.player, row, column)


# Load the board as level 1
b = g.load_board(level_1, 1)
# The game over screen is going to be level 999. There is no reason for that, it is just
# a convention as I don't think that this game is going to have more than 998 levels.
g.load_board(game_over, 999)
# And help 998
g.load_board(help_menu, 998)

# Now let's build a random generated bonus stage!
# First we need a board. Same size 50x30 but the player starting position is random.
player_starting_row = random.randint(0, 29)
player_starting_column = random.randint(0, 49)
bonus_board = Board(
    name="Bonus Stage",
    size=[50, 30],
    player_starting_position=[player_starting_row, player_starting_column],
    ui_borders=Utils.YELLOW_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
)
g.add_board(2, bonus_board)
# To place the treasures we have 30*50 = 1500 cells available on the map, minus the
# player it brings the total to 1499.
# Now let's randomely place 300 money bags. Each bag increase the score by 100.
for k in range(0, 300):
    row = None
    column = None
    retry = 0
    while True:
        if row is None:
            row = random.randint(0, bonus_board.size[1] - 1)
        if column is None:
            column = random.randint(0, bonus_board.size[0] - 1)
        if isinstance(bonus_board.item(row, column), BoardItemVoid):
            break
        elif retry > 20:
            break
        else:
            row = None
            column = None
            retry += 1
    bonus_board.place_item(
        Treasure(model=Sprites.MONEY_BAG, value=100, name=f"gold_bag_{k}"), row, column
    )

# And finally let's put 100 diamonds. Each diamond increase the score by 1000.
for k in range(0, 100):
    row = None
    column = None
    retry = 0
    while True:
        if row is None:
            row = random.randint(0, bonus_board.size[1] - 1)
        if column is None:
            column = random.randint(0, bonus_board.size[0] - 1)
        if isinstance(bonus_board.item(row, column), BoardItemVoid):
            break
        elif retry > 20:
            break
        else:
            row = None
            column = None
            retry += 1
    bonus_board.place_item(
        Treasure(model=Sprites.GEM_STONE, value=1000, name=f"diamond_{k}"), row, column
    )

# And ultimately 25 crown with a super high value of 5000.
for k in range(0, 100):
    row = None
    column = None
    retry = 0
    while True:
        if row is None:
            row = random.randint(0, bonus_board.size[1] - 1)
        if column is None:
            column = random.randint(0, bonus_board.size[0] - 1)
        if isinstance(bonus_board.item(row, column), BoardItemVoid):
            break
        elif retry > 20:
            break
        else:
            row = None
            column = None
            retry += 1
    bonus_board.place_item(
        Treasure(model=Sprites.CROWN, value=5000, name=f"crown_{k}"), row, column
    )


# Create the player object.
g.player = Player(name="Mighty Wizard", model=Sprites.MAGE)
g.change_level(1)

introduction_scene()

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

# Now let's build the menus
# First the default menu with only one entry : the help menu.
g.add_menu_entry("default", "h", 'Type the "h" key to display the help menu')
# Now the actual help menu
g.add_menu_entry("help", "w", "Move the player up")
g.add_menu_entry("help", "s", "Move the player down")
g.add_menu_entry("help", "a", "Move the player left")
g.add_menu_entry("help", "d", "Move the player right")
g.add_menu_entry("help", "q", "Quit the game")
g.add_menu_entry("help", "b", "Go back to the game")
# Let's take care of the portal fairy dialog now
update_fairy_dialog()
# We are going to need to add the options to give gold bags to the fairy only if the
# player collected the gold before going to the fairy.

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
    elif key == "v" and g.current_level == 1:
        teleport_player(
            g.current_board().player_starting_position[0],
            g.current_board().player_starting_position[1],
        )
    elif key == "b" and g.current_level == 1:
        teleport_player(22, 10)
    elif key == "n" and g.current_level == 1:
        teleport_player(2, 42)
    elif key == "m" and g.current_level == 1:
        teleport_player(3, 4)
    elif key == "p" and g.current_level == 1:
        notifications.append(
            f"Player position is [{g.player.pos[0]},{g.player.pos[1]}]"
        )
    elif current_menu == "default":
        # If we are in the default menu we use the normal controls.
        if key == "w":
            g.move_player(Constants.UP, 1)
            # If we are in level 2, we need to decrease the number of turn left for each
            # move
            if g.current_level == 2:
                level_2_turns_left -= 1
        elif key == "s":
            g.move_player(Constants.DOWN, 1)
            # If we are in level 2, we need to decrease the number of turn left for each
            # move
            if g.current_level == 2:
                level_2_turns_left -= 1
        elif key == "a":
            g.move_player(Constants.LEFT, 1)
            # If we are in level 2, we need to decrease the number of turn left for each
            # move
            if g.current_level == 2:
                level_2_turns_left -= 1
        elif key == "d":
            g.move_player(Constants.RIGHT, 1)
            # If we are in level 2, we need to decrease the number of turn left for each
            # move
            if g.current_level == 2:
                level_2_turns_left -= 1
        elif key == "h":
            current_menu = "help"
        # We also have to take care of the navigation here (to change level when
        # required)
    elif current_menu == "help":
        if key == "b":
            current_menu = "default"
    # Now care care of the specific case to adjust the levels accordingly.
    if current_menu == "help" and g.current_level != 998:
        previous_level = g.current_level
        g.pause()
        g.change_level(998)
    elif current_menu == "default" and g.current_level > 2:
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
        # First, does he have a Scroll of Wisdom. If yes we save him and warn him that
        # next time he is dead.
        if len(g.player.inventory.search("Scroll of Wisdom")) > 0:
            # To do so we set the HP back to the maximum
            g.player.hp = g.player.max_hp
            # Warn the player
            print(
                Utils.red_bright(
                    "You have been saved by the Scroll of Wisdom, be careful next time"
                    " you will die!"
                )
            )
            # And consume the scroll in the process
            g.player.inventory.delete_item("Scroll of Wisdom")
        else:
            # If he doesn't, well... Death is the sentence and that's game over.
            g.clear_screen()
            Utils.print_white_on_red(
                f"\n\n\n\t{g.player.name} is dead!\n\t      ** Game over **     \n\n"
            )
            g.change_level(999)
            g.display_board()
            break
    # Finally if the amount of turn left in level 2 is 0 we exit with a message
    if level_2_turns_left == 0:
        g.clear_screen()
        print_animated(
            f"{Sprites.UNICORN_FACE}: Congratulations Mighty Wizard!\n"
            f"{Sprites.UNICORN_FACE}: The whales are happy and the sheep are "
            f"patrolling!\n"
            f"{Sprites.UNICORN_FACE}: You also got "
            f"{Utils.green_bright(str(g.player.inventory.value()+(g.player.hp*100)))}"
            f" points!\n"
            f"{Sprites.UNICORN_FACE}: Try to do even better next time.\n\n"
            f"{Sprites.UNICORN_FACE}: Thank you for playing!\n"
        )
        break
    key = Utils.get_key()
