#!/usr/bin/env python3

from gamelib.Board import Board
from gamelib.Characters import Player, NPC
from gamelib.Game import Game
from gamelib.Structures import (
    Wall, Treasure, GenericStructure, GenericActionableStructure,
)
import gamelib.Constants as cst
from gamelib.Actuators.SimpleActuators import PathActuator
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites
import time
import sys
import random

sprite_mode = 'nosprite'

sprite_player = {
    'left': Utils.red_bright('-|'),
    'right': Utils.red_bright('|-'),
}
sprite_npc = None
sprite_npc2 = None
sprite_portal = None
sprite_treasure = None
sprite_treasure2 = None
sprite_tree = None
sprite_wall = None
sprite_heart = None
sprite_heart_minor = None

# The following code is used to switch rendering between
# emojis enabled terminal and the others.
# Use 'nosprite' if you see unicode codes displayed in your terminal.
if 'nosprite' in sys.argv:
    sprite_mode = 'nosprite'
elif 'sprite' in sys.argv:
    sprite_mode = 'sprite'
else:
    print('How do you want the game to be rendered?\n 1 - \
         with icons and sprites (might not render correctly \
         in your terminal)\n 2 - with color blocks\n')
    answer = input('Answer (1 or 2): ')
    if answer == '1':
        sprite_mode = 'sprite'
    else:
        sprite_mode = 'nosprite'

if sprite_mode == 'sprite':
    # sprite_player = Sprites.SHEEP
    sprite_portal = Sprites.CYCLONE
    sprite_treasure = Sprites.GEM_STONE
    sprite_treasure2 = Sprites.MONEY_BAG
    sprite_tree = Sprites.TREE_PINE
    sprite_wall = Sprites.WALL
    sprite_npc = Sprites.SKULL
    sprite_npc2 = Sprites.POO
    sprite_heart = Sprites.HEART_SPARKLING
    sprite_heart_minor = Sprites.HEART_BLUE
else:
    # sprite_player = Utils.RED_BLUE_SQUARE
    sprite_portal = Utils.CYAN_SQUARE
    sprite_treasure = Utils.YELLOW_RECT+Utils.RED_RECT
    sprite_treasure2 = Utils.yellow_bright('$$')
    sprite_tree = Utils.GREEN_SQUARE
    sprite_wall = Utils.WHITE_SQUARE
    sprite_npc = Utils.magenta_bright("oO")
    sprite_npc2 = Utils.magenta_bright("'&")
    sprite_heart = Utils.red_bright('<3')
    sprite_heart_minor = Utils.blue_bright('<3')


# Here are some functions to manage the game
# This one clear the screen, print the game title, print the player stats,
# display the current board, print the inventory and print the menu.
def refresh_screen(mygame, player, menu):
    mygame.clear_screen()
    # print(Utils.magenta_bright(f"\t\t~+~ Welcome to {mygame.name} ~+~"))
    mygame.display_player_stats()
    mygame.display_board()
    if player.inventory.size() > 0:
        # If inventory is not empty print it
        items_by_type = {}
        for item_name in player.inventory.items_name():
            item = player.inventory.get_item(item_name)
            if item.type in items_by_type.keys():
                items_by_type[item.type]['cumulated_size'] += item.size()
            else:
                items_by_type[item.type] = {
                    'cumulated_size': item.size(),
                    'model': item.model,
                    'name': item.name,
                }
        count = 1
        for k in items_by_type.keys():
            print(f" {items_by_type[k]['model']} : \
                {items_by_type[k]['cumulated_size']} ", end='')
            count += 1
            if count == 5:
                count = 0
                print("\n", end='')
        print("\n", end='')
    print(
        Utils.yellow_dim('\nWhere should ')
        + Utils.cyan_bright(player.name)
        + Utils.yellow_dim(' go?'))
    mygame.display_menu(menu)
    Utils.debug(f"Player stored position is ({player.pos[0]},{player.pos[1]})")


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


lvl1 = Board(
    name='Level_1',
    size=[40, 20],
    ui_border_left=Utils.WHITE_SQUARE,
    ui_border_right=Utils.WHITE_SQUARE,
    ui_border_top=Utils.WHITE_SQUARE,
    ui_border_bottom=Utils.WHITE_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[10, 20],
)
lvl2 = Board(
    name='Level_2',
    size=[40, 20],
    ui_border_left=Utils.WHITE_SQUARE,
    ui_border_right=Utils.WHITE_SQUARE,
    ui_border_top=Utils.WHITE_SQUARE,
    ui_border_bottom=Utils.WHITE_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[0, 0],
)

game = Game(name='HAC Game')
p = Player(model=sprite_player['right'], name='Nazbrok')
npc1 = NPC(model=sprite_npc, name='Bad guy 1', step=1)
# Test of the PathActuator
npc1.actuator = PathActuator(
    path=[
        cst.UP, cst.UP, cst.UP, cst.UP, cst.UP, cst.UP, cst.UP, cst.UP,
        cst.RIGHT, cst.RIGHT, cst.RIGHT, cst.RIGHT, cst.DOWN, cst.DOWN,
        cst.DOWN, cst.DOWN, cst.DOWN, cst.DOWN, cst.DOWN, cst.DOWN,
        cst.LEFT, cst.LEFT, cst.LEFT, cst.LEFT])

game.add_board(1, lvl1)
game.add_board(2, lvl2)

t = Treasure(model=sprite_treasure, name='Cool treasure', type='gem')
money_bag = Treasure(model=sprite_treasure2, name='money', value=20)

tree = GenericStructure(model=sprite_tree)
tree.set_overlappable(False)
tree.set_pickable(False)

portal2 = GenericActionableStructure(model=sprite_portal)
portal2.set_overlappable(False)
portal2.action = change_current_level
portal2.action_parameters = [game, 2]

portal1 = GenericActionableStructure(model=sprite_portal)
portal1.set_overlappable(False)
portal1.action = change_current_level
portal1.action_parameters = [game, 1]

life_heart = GenericActionableStructure(model=sprite_heart)
life_heart.set_overlappable(True)
life_heart.action = add_hp
life_heart.action_parameters = [game, 100]

life_heart_minor = GenericActionableStructure(model=sprite_heart_minor)
life_heart_minor.set_overlappable(True)
life_heart_minor.action = add_hp
life_heart_minor.action_parameters = [game, 25]

game.player = p

# Adding walls to level 1
lvl1.place_item(Wall(model=sprite_wall), 2, 3)
lvl1.place_item(Wall(model=sprite_wall), 2, 2)
lvl1.place_item(Wall(model=sprite_wall), 2, 1)
lvl1.place_item(Wall(model=sprite_wall), 2, 0)
lvl1.place_item(Wall(model=sprite_wall), 3, 3)
lvl1.place_item(Wall(model=sprite_wall), 4, 3)
lvl1.place_item(Wall(model=sprite_wall), 5, 3)
lvl1.place_item(Wall(model=sprite_wall), 6, 3)
lvl1.place_item(Wall(model=sprite_wall), 6, 2)
lvl1.place_item(Wall(model=sprite_wall), 6, 1)
lvl1.place_item(Wall(model=sprite_wall), 7, 1)
lvl1.place_item(Wall(model=sprite_wall), 8, 1)
lvl1.place_item(Wall(model=sprite_wall), 8, 3)
lvl1.place_item(Wall(model=sprite_wall), 9, 3)
lvl1.place_item(Wall(model=sprite_wall), 10, 3)
lvl1.place_item(Wall(model=sprite_wall), 10, 2)
lvl1.place_item(Wall(model=sprite_wall), 10, 1)
lvl1.place_item(Wall(model=sprite_wall), 10, 0)

# Now adding trees
for i in range(4, 40, 1):
    lvl1.place_item(tree, 6, i)
    if i % 4 != 0:
        lvl1.place_item(tree, 8, i)
        for j in range(9, 15, 1):
            lvl1.place_item(tree, j, i)

lvl1.place_item(t, 3, 2)
lvl1.place_item(
    Treasure(model=sprite_treasure, name='Cool treasure', type='gem'), 9, 0,
)
lvl1.place_item(portal2, 19, 39)
lvl1.place_item(life_heart, 15, 10)
lvl1.place_item(life_heart_minor, 15, 22)
# Now we add NPCs
game.add_npc(1, npc1, 15, 4)
# Now creating the movement path of the second NPC of lvl 1 (named Bad Guy 2)
bg2_actuator = PathActuator(path=[cst.RIGHT for k in range(0, 30, 1)])
for k in range(0, 30, 1):
    bg2_actuator.path.append(cst.LEFT)
game.add_npc(
    1,
    NPC(
        model=sprite_npc,
        name='Bad guy 2',
        actuator=bg2_actuator,
        step=1,
    ),
    7, 9)

lvl2.place_item(money_bag, 10, 35)
lvl2.place_item(portal1, 11, 35)

for k in range(0, 20, 1):
    game.add_npc(2, NPC(model=sprite_npc2, name=f'poopy_{k}', step=1))


# Now let's add a nice NPC, one we can talk to!
nice_npc = NPC(
    name='Unipici',
    model=Sprites.UNICORN_FACE,
    step=0)  # because of step=0 this NPC is static
game.add_npc(1, nice_npc, 18, 1)
# Now let's use the menu system to have the basis for a dialog
game.add_menu_entry(
    'unipici_dialog', None,
    'Hello! I am Unipici. Nice to meet you! What can I do for you?')
game.add_menu_entry(
    'unipici_dialog', '1', 'Restore my life '+Sprites.HEART_SPARKLING)
game.add_menu_entry('unipici_dialog', '2', 'Nearly kill me '+Sprites.SKULL)
game.add_menu_entry('unipici_dialog', '3', 'Solve the Uni-riddle')
game.add_menu_entry('unipici_dialog', '4', 'Stop talking')

game.add_menu_entry('main_menu', 'w', 'Go up')
game.add_menu_entry('main_menu', 's', 'Go down')
game.add_menu_entry('main_menu', 'a', 'Go left')
game.add_menu_entry('main_menu', 'd', 'Go right')
game.add_menu_entry('main_menu', None, '-'*17)
game.add_menu_entry('main_menu', 'v', 'Change game speed')
game.add_menu_entry('main_menu', 'k', 'Damage player (5 HP)')
game.add_menu_entry('main_menu', 'q', 'Quit game')

game.add_menu_entry('speed_menu', '1', 'Slow')
game.add_menu_entry('speed_menu', '2', 'Medium slow')
game.add_menu_entry('speed_menu', '3', 'Normal')
game.add_menu_entry('speed_menu', '4', 'Fast')
game.add_menu_entry('speed_menu', '5', 'Super Duper Fast!!!!')
game.add_menu_entry('speed_menu', 'b', 'Back to main menu')

# Once Game, Boards and Player are created we change level
game.change_level(1)

key = None
game_speed = 0.1
current_menu = 'main_menu'
npc_movements = [cst.UP, cst.DOWN, cst.LEFT, cst.RIGHT]

uniriddles = [
    {
        'q': 'Who is never hungry during Christmas?',
        'a': 'The turkey because he is always stuffed.',
        'k': ['turkey', 'stuff'],
    },
    {
        'q': 'The more you take away, the more I become.\nWhat am I?',
        'a': 'A hole.',
        'k': ['hole'],
    },
    {
        'q': 'I have no feet, no hands, no wings, but I \
            climb to the sky.\nWhat am I?',
        'a': 'Smoke.',
        'k': ['smoke'],
    },
    {
        'q': 'Why do mummies like Christmas so much?',
        'a': 'Because of all the wrapping.',
        'k': ['wrap'],
    }
]

while key != 'q':
    refresh_screen(game, p, current_menu)
    Utils.debug(f"Current game speed: {game_speed}")
    Utils.debug(f"Current menu: {current_menu}")
    key = Utils.get_key()

    if current_menu == 'main_menu':
        if key == 'w' or key == '8':
            game.move_player(cst.UP, 1)
        elif key == 's' or key == '2':
            game.move_player(cst.DOWN, 1)
        elif key == 'a' or key == '4':
            p.model = sprite_player['left']
            game.move_player(cst.LEFT, 1)
        elif key == 'd' or key == '6':
            p.model = sprite_player['right']
            game.move_player(cst.RIGHT, 1)
        elif key == '9':
            p.model = sprite_player['right']
            game.move_player(cst.DRUP, 1)
        elif key == '7':
            p.model = sprite_player['left']
            game.move_player(cst.DLUP, 1)
        elif key == '1':
            p.model = sprite_player['left']
            game.move_player(cst.DLDOWN, 1)
        elif key == '3':
            p.model = sprite_player['right']
            game.move_player(cst.DRDOWN, 1)
        elif key == 'q':
            game.clear_screen()
            print(Utils.cyan_bright(f'Thanks for playing {game.name}'))
            print(Utils.yellow_bright('Good bye!'))
            break
        elif key == 'v':
            current_menu = 'speed_menu'
        elif key == 'k':
            game.player.hp -= 5

        # Once we've moved we check if we are in the neighborhood of Unipici
        if game.player in game.neighbors(1, nice_npc):
            current_menu = 'unipici_dialog'
    # Here we change the speed of the game and then go back to main menu.
    elif current_menu == 'speed_menu':
        if key == '1':
            game_speed = 0.5
            current_menu = 'main_menu'
        elif key == '2':
            game_speed = 0.25
            current_menu = 'main_menu'
        elif key == '3':
            game_speed = 0.1
            current_menu = 'main_menu'
        elif key == '4':
            game_speed = 0.05
            current_menu = 'main_menu'
        elif key == '5':
            game_speed = 0.01
            current_menu = 'main_menu'
        elif key == 'b':
            current_menu = 'main_menu'
    # Here is the interaction menu with Unipici
    elif current_menu == 'unipici_dialog':
        if key == '4':
            current_menu = 'main_menu'
        elif key == '2':
            game.player.hp -= (game.player.max_hp-5)
        elif key == '1':
            game.player.hp = game.player.max_hp
        elif key == '3':
            # The riddle game
            game.clear_screen()
            print(
                nice_npc.model
                + Utils.cyan_bright(
                    ' YEAAAH RIDDLE TIME!! Answer my riddle and you \
                        will be awarded an awesome treasure!'))
            riddle = random.choice(uniriddles)
            print(nice_npc.model + Utils.magenta_bright(riddle['q']))
            answer = input('And your answer is? ')
            match_count = 0
            for k in riddle['k']:
                if k.lower() in answer.lower():
                    match_count += 1
            if len(riddle['k']) == match_count:
                print(
                    nice_npc.model
                    + Utils.green_bright(
                        'You got it!! Congratulations! Here is your prize: '
                        + Sprites.RAINBOW + ' Rainbow Prize!',
                    ),
                )
                game.player.inventory.add_item(
                    Treasure(
                        model=Sprites.RAINBOW,
                        value=1000,
                        name='Rainbow Prize',
                        type='good_prize'),
                    )
            else:
                print(
                    nice_npc.model
                    + Utils.red_bright(
                        'WRONG! You still get a prize... '
                        + sprite_npc2
                        + ' a nice looser poop!'))
                print(
                    nice_npc.model
                    + Utils.cyan_bright(
                        f" by the way, the answer is: {riddle['a']}"))
                game.player.inventory.add_item(
                    Treasure(
                        model=sprite_npc2,
                        value=-1000,
                        name='Looser poop',
                        type='loose_prize'))
            print(
                nice_npc.model +
                Utils.cyan_bright(
                    'Come again for more fun!\n \
                    (press any key to exit this dialog)'))
            Utils.get_key()
    else:
        Utils.fatal("Invalid direction: "+str(ord(key)))

    # Now let's take care of our NPC movement.
    # NPC move whatever our input, even when we navigates in menus.
    # Finally, we only move the NPCs of the current level.
    # Nothing moves in the other levels.
    game.actuate_npcs(game.current_level)
    time.sleep(game_speed)
