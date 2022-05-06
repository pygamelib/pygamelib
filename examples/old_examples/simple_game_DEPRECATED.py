#!/usr/bin/env python3

import examples_includes  # noqa: F401
from pygamelib import engine, board_items, base, constants, actuators
from pygamelib.gfx import core
from pygamelib.assets import graphics
import time
import sys
import random

# ====================================++ WARNING ++====================================#
# This game is a very old example dating back to the first release of the library.     #
# It is not very good and certainly does not represent how you should do a game with   #
# the pygamelib library, nor is it deserving to be an example.                         #
# It is not even a good example of a Python application.                               #
# There are some good ideas though (like the orientation of the player's model or the  #
# pure text or text+emoji rendering). Like all code: not everything is bad.            #
# =====================================================================================#


sprixel_mode = "nosprite"

sprixel_player = {
    "left": core.Sprixel("-|", fg_color=core.Color(0, 255, 255)),
    "right": core.Sprixel("|-", fg_color=core.Color(0, 255, 255)),
}
sprixel_npc = None
sprixel_npc2 = None
sprixel_portal = None
sprixel_treasure = None
sprixel_treasure2 = None
sprixel_tree = None
sprixel_wall = None
sprixel_heart = None
sprixel_heart_minor = None

# The following code is used to switch rendering between
# emojis enabled terminal and the others.
# Use 'nosprite' if you see unicode codes displayed in your terminal.
if "nosprite" in sys.argv:
    sprixel_mode = "nosprite"
elif "sprite" in sys.argv:
    sprixel_mode = "sprite"
else:
    print(
        "How do you want the game to be rendered?\n 1 - "
        "with icons and sprites (might not render correctly "
        "in your terminal)\n 2 - with color blocks\n"
    )
    answer = input("Answer (1 or 2): ")
    if answer == "1":
        sprixel_mode = "sprite"
    else:
        sprixel_mode = "nosprite"

if sprixel_mode == "sprite":
    sprixel_portal = core.Sprixel(graphics.Models.CYCLONE)
    sprixel_treasure = core.Sprixel(graphics.Models.GEM_STONE)
    sprixel_treasure2 = core.Sprixel(graphics.Models.MONEY_BAG)
    sprixel_tree = core.Sprixel(graphics.Models.EVERGREEN_TREE)
    sprixel_wall = core.Sprixel(graphics.Models.BRICK)
    sprixel_npc = core.Sprixel(graphics.Models.SKULL)
    sprixel_npc2 = core.Sprixel(graphics.Models.PILE_OF_POO)
    sprixel_heart = core.Sprixel(graphics.Models.SPARKLING_HEART)
    sprixel_heart_minor = core.Sprixel(graphics.Models.BLUE_HEART)
    sprixel_unipici = core.Sprixel(graphics.Models.UNICORN)
else:
    sprixel_portal = core.Sprixel("()", fg_color=core.Color(0, 255, 255))
    sprixel_treasure = core.Sprixel("[]", fg_color=core.Color(255, 255, 0))
    sprixel_treasure2 = core.Sprixel("$$", fg_color=core.Color(255, 255, 0))
    sprixel_tree = core.Sprixel("/\\", fg_color=core.Color(0, 170, 0))
    sprixel_wall = core.Sprixel.white_square()
    sprixel_npc = core.Sprixel("oO", fg_color=core.Color(97, 157, 83))
    sprixel_npc2 = core.Sprixel("'&", fg_color=core.Color(97, 157, 83))
    sprixel_heart = core.Sprixel("<3", fg_color=core.Color(255, 0, 0))
    sprixel_heart_minor = core.Sprixel("<3", fg_color=core.Color(0, 0, 255))
    sprixel_unipici = core.Sprixel("`o", fg_color=core.Color(255, 0, 255))


# Here are some functions to manage the game
# This one clear the screen, print the game title, print the player stats,
# display the current board, print the inventory and print the menu.
def refresh_screen(mygame, player, menu):
    mygame.clear_screen()
    # print(base.Text.magenta_bright(f"\t\t~+~ Welcome to {mygame.name} ~+~"))
    mygame.display_player_stats()
    mygame.display_board()
    if player.inventory.size() > 0:
        # If inventory is not empty print it
        items_by_type = {}
        for item_name in player.inventory.items_name():
            item = player.inventory.get_item(item_name)
            if item.type in items_by_type.keys():
                items_by_type[item.type]["cumulated_size"] += item.inventory_space
            else:
                items_by_type[item.type] = {
                    "cumulated_size": item.inventory_space,
                    "sprixel": item.sprixel,
                    "name": item.name,
                }
        count = 1
        for k in items_by_type.keys():
            print(
                f" {items_by_type[k]['sprixel']} : "
                f"{items_by_type[k]['cumulated_size']} ",
                end="",
            )
            count += 1
            if count == 5:
                count = 0
                print("\n", end="")
        print("\n", end="")
    print(
        base.Text.yellow_dim("\nWhere should ")
        + base.Text.cyan_bright(player.name)
        + base.Text.yellow_dim(" go?")
    )
    mygame.display_menu(menu)
    base.Text.debug(f"Player stored position is ({player.pos[0]},{player.pos[1]})")


# This one is called a "callback", it's automatically called by the game
# engine when the player tries to go through a portal.
def change_current_level(params):
    params[0].change_level(params[1])


def add_hp(params):
    game = params[0]
    nb_hp = params[1]
    if game.player is not None:
        if (game.player.hp + nb_hp) >= game.player.max_hp:
            game.player.hp = game.player.max_hp
        else:
            game.player.hp += nb_hp


lvl1 = engine.Board(
    name="Level_1",
    size=[40, 20],
    ui_border_left=graphics.WHITE_SQUARE,
    ui_border_right=graphics.WHITE_SQUARE,
    ui_border_top=graphics.WHITE_SQUARE,
    ui_border_bottom=graphics.WHITE_SQUARE,
    ui_board_void_cell_sprixel=core.Sprixel.black_square(),
    player_starting_position=[10, 20],
)
lvl2 = engine.Board(
    name="Level_2",
    size=[40, 20],
    ui_border_left=graphics.WHITE_SQUARE,
    ui_border_right=graphics.WHITE_SQUARE,
    ui_border_top=graphics.WHITE_SQUARE,
    ui_border_bottom=graphics.WHITE_SQUARE,
    ui_board_void_cell_sprixel=core.Sprixel.black_square(),
    player_starting_position=[0, 0],
)

game = engine.Game(name="Simple Game (Deprecated)")
p = board_items.Player(sprixel=sprixel_player["right"], name="Nazbrok")
npc1 = board_items.NPC(sprixel=sprixel_npc, name="Bad guy 1", step=1)
# Test of the PathActuator
npc1.actuator = actuators.PathActuator(
    path=[
        constants.UP,
        constants.UP,
        constants.UP,
        constants.UP,
        constants.UP,
        constants.UP,
        constants.UP,
        constants.UP,
        constants.RIGHT,
        constants.RIGHT,
        constants.RIGHT,
        constants.RIGHT,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.DOWN,
        constants.LEFT,
        constants.LEFT,
        constants.LEFT,
        constants.LEFT,
    ]
)

game.add_board(1, lvl1)
game.add_board(2, lvl2)

t = board_items.Treasure(
    sprixel=sprixel_treasure, name="Cool treasure", item_type="gem"
)
money_bag = board_items.Treasure(sprixel=sprixel_treasure2, name="money", value=20)

tree = board_items.GenericStructure(sprixel=sprixel_tree)
tree.set_overlappable(False)
tree.set_pickable(False)

portal2 = board_items.GenericActionableStructure(sprixel=sprixel_portal)
portal2.set_overlappable(False)
portal2.action = change_current_level
portal2.action_parameters = [game, 2]

portal1 = board_items.GenericActionableStructure(sprixel=sprixel_portal)
portal1.set_overlappable(False)
portal1.action = change_current_level
portal1.action_parameters = [game, 1]

life_heart = board_items.GenericActionableStructure(
    sprixel=sprixel_heart, name="life_100"
)
life_heart.set_overlappable(True)
life_heart.action = add_hp
life_heart.action_parameters = [game, 100]

life_heart_minor = board_items.GenericActionableStructure(
    sprixel=sprixel_heart_minor, name="life_25"
)
life_heart_minor.set_overlappable(True)
life_heart_minor.action = add_hp
life_heart_minor.action_parameters = [game, 25]

game.player = p

# Adding walls to level 1
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 2, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 2, 2)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 2, 1)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 2, 0)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 3, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 4, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 5, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 6, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 6, 2)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 6, 1)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 7, 1)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 8, 1)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 8, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 9, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 10, 3)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 10, 2)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 10, 1)
lvl1.place_item(board_items.Wall(sprixel=sprixel_wall), 10, 0)

# Now adding trees
for i in range(4, 40, 1):
    lvl1.place_item(tree, 6, i)
    if i % 4 != 0:
        lvl1.place_item(tree, 8, i)
        for j in range(9, 15, 1):
            lvl1.place_item(tree, j, i)

lvl1.place_item(t, 3, 2)
lvl1.place_item(
    board_items.Treasure(
        sprixel=sprixel_treasure, name="Cool treasure", item_type="gem"
    ),
    9,
    0,
)
lvl1.place_item(portal2, 19, 39)
lvl1.place_item(life_heart, 15, 10)
lvl1.place_item(life_heart_minor, 15, 22)
# Now we add NPCs
game.add_npc(1, npc1, 15, 4)
# Now creating the movement path of the second NPC of lvl 1 (named Bad Guy 2)
bg2_actuator = actuators.PathActuator(path=[constants.RIGHT for k in range(0, 30, 1)])
for k in range(0, 30, 1):
    bg2_actuator.path.append(constants.LEFT)
game.add_npc(
    1,
    board_items.NPC(
        sprixel=sprixel_npc,
        name="Bad guy 2",
        actuator=bg2_actuator,
        step=1,
    ),
    7,
    9,
)

lvl2.place_item(money_bag, 10, 35)
lvl2.place_item(portal1, 11, 35)

for k in range(0, 20, 1):
    game.add_npc(2, board_items.NPC(sprixel=sprixel_npc2, name=f"poopy_{k}", step=1))


# Now let's add a nice NPC, one we can talk to!
nice_npc = board_items.NPC(
    name="Unipici", sprixel=sprixel_unipici, step=0
)  # because of step=0 this NPC is static
game.add_npc(1, nice_npc, 18, 1)
# Now let's use the menu system to have the basis for a dialog
game.add_menu_entry(
    "unipici_dialog",
    None,
    "Hello! I am Unipici. Nice to meet you! What can I do for you?",
)
game.add_menu_entry(
    "unipici_dialog", "1", "Restore my life " + graphics.Models.SPARKLING_HEART
)
game.add_menu_entry("unipici_dialog", "2", "Nearly kill me " + graphics.Models.SKULL)
game.add_menu_entry("unipici_dialog", "3", "Solve the Uni-riddle")
game.add_menu_entry("unipici_dialog", "4", "Stop talking")

game.add_menu_entry("main_menu", "w", "Go up")
game.add_menu_entry("main_menu", "s", "Go down")
game.add_menu_entry("main_menu", "a", "Go left")
game.add_menu_entry("main_menu", "d", "Go right")
game.add_menu_entry("main_menu", None, "-" * 17)
game.add_menu_entry("main_menu", "v", "Change game speed")
game.add_menu_entry("main_menu", "k", "Damage player (5 HP)")
game.add_menu_entry("main_menu", "q", "Quit game")

game.add_menu_entry("speed_menu", "1", "Slow")
game.add_menu_entry("speed_menu", "2", "Medium slow")
game.add_menu_entry("speed_menu", "3", "Normal")
game.add_menu_entry("speed_menu", "4", "Fast")
game.add_menu_entry("speed_menu", "5", "Super Duper Fast!!!!")
game.add_menu_entry("speed_menu", "b", "Back to main menu")

# Once Game, Boards and Player are created we change level
game.change_level(1)

key = None
game_speed = 0.1
current_menu = "main_menu"
npc_movements = [constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT]

uniriddles = [
    {
        "q": "Who is never hungry during Christmas?",
        "a": "The turkey because he is always stuffed.",
        "k": ["turkey", "stuff"],
    },
    {
        "q": "The more you take away, the more I become.\nWhat am I?",
        "a": "A hole.",
        "k": ["hole"],
    },
    {
        "q": "I have no feet, no hands, no wings, but I climb to the sky.\nWhat am I?",
        "a": "Smoke.",
        "k": ["smoke"],
    },
    {
        "q": "Why do mummies like Christmas so much?",
        "a": "Because of all the wrapping.",
        "k": ["wrap"],
    },
]

while key != "q":
    refresh_screen(game, p, current_menu)
    base.Text.debug(f"Current game speed: {game_speed}")
    base.Text.debug(f"Current menu: {current_menu}")
    key = game.get_key()

    if current_menu == "main_menu":
        if key == "w" or key == "8":
            game.move_player(constants.UP, 1)
        elif key == "s" or key == "2":
            game.move_player(constants.DOWN, 1)
        elif key == "a" or key == "4":
            p.sprixel = sprixel_player["left"]
            game.move_player(constants.LEFT, 1)
        elif key == "d" or key == "6":
            p.sprixel = sprixel_player["right"]
            game.move_player(constants.RIGHT, 1)
        elif key == "9":
            p.sprixel = sprixel_player["right"]
            game.move_player(constants.DRUP, 1)
        elif key == "7":
            p.sprixel = sprixel_player["left"]
            game.move_player(constants.DLUP, 1)
        elif key == "1":
            p.sprixel = sprixel_player["left"]
            game.move_player(constants.DLDOWN, 1)
        elif key == "3":
            p.sprixel = sprixel_player["right"]
            game.move_player(constants.DRDOWN, 1)
        elif key == "q":
            game.clear_screen()
            print(base.Text.cyan_bright(f"Thanks for playing {game.name}"))
            print(base.Text.yellow_bright("Good bye!"))
            break
        elif key == "v":
            current_menu = "speed_menu"
        elif key == "k":
            game.player.hp -= 5

        # Once we've moved we check if we are in the neighborhood of Unipici
        if game.player in game.neighbors(1, nice_npc):
            current_menu = "unipici_dialog"
    # Here we change the speed of the game and then go back to main menu.
    elif current_menu == "speed_menu":
        if key == "1":
            game_speed = 0.5
            current_menu = "main_menu"
        elif key == "2":
            game_speed = 0.25
            current_menu = "main_menu"
        elif key == "3":
            game_speed = 0.1
            current_menu = "main_menu"
        elif key == "4":
            game_speed = 0.05
            current_menu = "main_menu"
        elif key == "5":
            game_speed = 0.01
            current_menu = "main_menu"
        elif key == "b":
            current_menu = "main_menu"
    # Here is the interaction menu with Unipici
    elif current_menu == "unipici_dialog":
        if key == "4":
            current_menu = "main_menu"
            game.move_player(constants.RIGHT, 1)
        elif key == "2":
            game.player.hp -= game.player.max_hp - 5
        elif key == "1":
            game.player.hp = game.player.max_hp
        elif key == "3":
            # The riddle game
            game.clear_screen()
            print(
                f"{nice_npc.sprixel}: "
                f'{base.Text.cyan_bright("YEAAAH RIDDLE TIME!! Answer my riddle and ")}'
                f'{base.Text.cyan_bright("you will be awarded an awesome treasure!")}'
            )
            riddle = random.choice(uniriddles)
            print(f"{nice_npc.sprixel}: {base.Text.magenta_bright(riddle['q'])}")
            answer = input("And your answer is? ")
            match_count = 0
            for k in riddle["k"]:
                if k.lower() in answer.lower():
                    match_count += 1
            if len(riddle["k"]) == match_count:
                print(
                    f"{nice_npc.sprixel}: "
                    f'{base.Text.green_bright("You got it!! Congratulations! Here ")}'
                    f'{base.Text.green_bright("is your prize: ")}'
                    f"{graphics.Models.RAINBOW} Rainbow Prize!",
                )
                game.player.inventory.add_item(
                    board_items.Treasure(
                        sprixel=core.Sprixel(graphics.Models.RAINBOW),
                        value=1000,
                        name="Rainbow Prize",
                        item_type="good_prize",
                    ),
                )
            else:
                print(
                    f"{nice_npc.sprixel}: "
                    f'{base.Text.red_bright("WRONG! You still get a prize... ")}'
                    f'{sprixel_npc2} {base.Text.red_bright(" a nice looser poop!")}'
                )
                answer = riddle["a"]
                print(
                    f"{nice_npc.sprixel}: "
                    f'{base.Text.cyan_bright(f" by the way, the answer is: {answer}")}'
                )
                game.player.inventory.add_item(
                    board_items.Treasure(
                        sprixel=sprixel_npc2,
                        value=-1000,
                        name="Looser poop",
                        item_type="loose_prize",
                    )
                )
            print(
                f"{nice_npc.sprixel}: "
                f'{base.Text.cyan_bright("Come again for more fun!")}'
            )
            print(f'{base.Text.cyan_bright("(press any key to exit this dialog)")}')
            game.get_key()
    else:
        base.Text.fatal("Invalid direction: " + str(ord(key)))

    # Now let's take care of our NPC movement.
    # NPC move whatever our input, even when we navigates in menus.
    # Finally, we only move the NPCs of the current level.
    # Nothing moves in the other levels.
    game.actuate_npcs(game.current_level)
    time.sleep(game_speed)
