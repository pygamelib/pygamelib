from gamelib.Board import Board
from gamelib.BoardItem import BoardItem
from gamelib.Characters import Player, NPC
from gamelib.Game import Game
from gamelib.Structures import Wall,Treasure, GenericStructure, GenericActionnableStructure
import gamelib.Constants as cst
from gamelib.Actuators.SimpleActuators import PathActuator
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites
import time
import sys
import random

sprite_mode = 'nosprite'

sprite_player = {'left':Utils.red_bright('-|'),'right':Utils.red_bright('|-')}
sprite_npc = None
sprite_npc2 = None
sprite_portal = None
sprite_treasure = None
sprite_treasure2 = None
sprite_tree = None
sprite_wall = None

if 'nosprite' in sys.argv:
    sprite_mode = 'nosprite'
elif 'sprite' in sys.argv:
    sprite_mode = 'sprite'
else:
    print('How do you want the game to be rendered?\n 1 - with icons and sprites (might not render correctly in your terminal)\n 2 - with color blocks\n')
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
else:
    # sprite_player = Utils.RED_BLUE_SQUARE
    sprite_portal = Utils.CYAN_SQUARE
    sprite_treasure = Utils.YELLOW_RECT+Utils.RED_RECT
    sprite_treasure2 = sprite_treasure
    sprite_tree = Utils.GREEN_SQUARE
    sprite_wall = Utils.WHITE_SQUARE
    sprite_npc = Utils.magenta_bright("oO")
    sprite_npc2 = Utils.magenta_bright("'&")


# Here are some functions to manage the game
# This one clear the screen, print the game title, display the current board and print the menu.
def refresh_screen(mygame,player,menu):
    mygame.clear_screen()
    print(Utils.magenta_bright(f"\t\t~+~ Welcome to {mygame.name} ~+~"))
    mygame.print_player_stats()
    mygame.current_board().display()
    print( Utils.yellow_dim( 'Where should ' )+Utils.cyan_bright(player.name)+Utils.yellow_dim(' go?') )
    mygame.print_menu(menu)
    Utils.debug(f"Player stored position is ({player.pos[0]},{player.pos[1]})")

# This one is called a "callback", it's automatically called by the game engine when the player tries to go through a portal.
def change_current_level(params):
    params[0].change_level(params[1])

lvl1 = Board(name='Level_1',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE,player_starting_position=[10,20])
lvl2 = Board(name='Level_2',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE, player_starting_position=[0,0])

game = Game(name='HAC Game')
p = Player(model=sprite_player['right'],name='Nazbrok')
npc1 = NPC(model=sprite_npc,name='Bad guy 1')
# Test of the PathActuator
npc1.actuator = PathActuator(path=[cst.UP,cst.UP,cst.UP,cst.UP,cst.UP,cst.UP,cst.UP,cst.UP,cst.RIGHT,cst.RIGHT,cst.RIGHT,cst.RIGHT,cst.DOWN,cst.DOWN,cst.DOWN,cst.DOWN,cst.DOWN,cst.DOWN,cst.DOWN,cst.DOWN,cst.LEFT,cst.LEFT,cst.LEFT,cst.LEFT])

game.add_board(1,lvl1)
game.add_board(2,lvl2)

t = Treasure(model=sprite_treasure,name='Cool treasure',type='gem')
money_bag = Treasure(model=sprite_treasure2,name='money',value=20)

tree = GenericStructure(model=sprite_tree)
tree.set_overlappable(False)
tree.set_pickable(False)

portal2 = GenericActionnableStructure(model=sprite_portal)
portal2.set_overlappable(True)
portal2.action = change_current_level
portal2.action_parameters = [game,2]

portal1 = GenericActionnableStructure(model=sprite_portal)
portal1.set_overlappable(True)
portal1.action = change_current_level
portal1.action_parameters = [game,1]

game.player = p

# Adding walls to level 1
lvl1.place_item(Wall(model=sprite_wall),2,3)
lvl1.place_item(Wall(model=sprite_wall),2,2)
lvl1.place_item(Wall(model=sprite_wall),2,1)
lvl1.place_item(Wall(model=sprite_wall),2,0)
lvl1.place_item(Wall(model=sprite_wall),3,3)
lvl1.place_item(Wall(model=sprite_wall),4,3)
lvl1.place_item(Wall(model=sprite_wall),5,3)
lvl1.place_item(Wall(model=sprite_wall),6,3)
lvl1.place_item(Wall(model=sprite_wall),6,2)
lvl1.place_item(Wall(model=sprite_wall),6,1)
lvl1.place_item(Wall(model=sprite_wall),7,1)
lvl1.place_item(Wall(model=sprite_wall),8,1)
lvl1.place_item(Wall(model=sprite_wall),8,3)
lvl1.place_item(Wall(model=sprite_wall),9,3)
lvl1.place_item(Wall(model=sprite_wall),10,3)
lvl1.place_item(Wall(model=sprite_wall),10,2)
lvl1.place_item(Wall(model=sprite_wall),10,1)
lvl1.place_item(Wall(model=sprite_wall),10,0)

# Now adding trees
for i in range(4,40,1):
    lvl1.place_item(tree,6,i)
    if i%4 != 0:
        lvl1.place_item(tree,8,i)
        for j in range(9,15,1):
            lvl1.place_item(tree,j,i)

lvl1.place_item(t,3,2)
lvl1.place_item(Treasure(model=sprite_treasure,name='Cool treasure',type='gem'),9,0)
lvl1.place_item(portal2,19,39)
# Now we add NPCs
game.add_npc(1,npc1,15,4)
# Now creating the movement path of the second NPC of lvl 1 (named Bad Guy 2)
bg2_actuator = PathActuator( path=[cst.RIGHT for k in range(0,30,1)])
for k in range(0,30,1):
    bg2_actuator.path.append(cst.LEFT)
game.add_npc(1,NPC(model=sprite_npc,name='Bad guy 2',actuator=bg2_actuator),7,9)

lvl2.place_item(money_bag,10,35)
lvl2.place_item(portal1,11,35)

for k in range(0,20,1):
    game.add_npc(2, NPC( model=sprite_npc2 , name=f'poopy_{k}' ) )

game.add_menu_entry('main_menu','w','Go up')
game.add_menu_entry('main_menu','s','Go down')
game.add_menu_entry('main_menu','a','Go left')
game.add_menu_entry('main_menu','d','Go right')
game.add_menu_entry('main_menu',None,'-'*17)
game.add_menu_entry('main_menu','1','Go to level 1')
game.add_menu_entry('main_menu','2','Go to level 2')
game.add_menu_entry('main_menu',None,'-'*17)
game.add_menu_entry('main_menu','v','Change game speed')
game.add_menu_entry('main_menu','q','Quit game')

game.add_menu_entry('speed_menu','1','Slow')
game.add_menu_entry('speed_menu','2','Medium slow')
game.add_menu_entry('speed_menu','3','Normal')
game.add_menu_entry('speed_menu','4','Fast')
game.add_menu_entry('speed_menu','5','Super Duper Fast!!!!')
game.add_menu_entry('speed_menu','b','Back to main menu')

# Once Game, Boards and Player are created we change level
game.change_level(1)

key = None
game_speed = 0.1
current_menu = 'main_menu'
npc_movements = [cst.UP,cst.DOWN,cst.LEFT,cst.RIGHT]
while key != 'q':
    refresh_screen(game,p,current_menu)
    Utils.debug(f"Current game speed: {game_speed}")
    print(p.inventory)
    # direction = str(input("What direction do you want to take: "))
    key = Utils.get_key()
    if key == 'w':
        game.current_board().move(p,cst.UP,1)
    elif key == 's':
        game.current_board().move(p,cst.DOWN,1)
    elif key == 'a':
        p.model = sprite_player['left']
        game.current_board().move(p,cst.LEFT,1)
    elif key == 'd':
        p.model = sprite_player['right']
        game.current_board().move(p,cst.RIGHT,1)
    elif key == 'q':
        game.clear_screen()
        print( Utils.cyan_bright(f'Thanks for playing {game.name}') )
        print(Utils.yellow_bright('Good bye!'))
        break
    elif current_menu == 'main_menu' and (key == '1' or key == '2'):
        game.change_level(int(key))
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
    elif key == 'v':
        current_menu = 'speed_menu'
    elif key == 'c':
        game.current_board().clear_cell(4,3)
    else:
        Utils.fatal("Invalid direction: "+str(ord(key)))
    
    # Now let's take care of our NPC movement.
    # We are going to make it move one cell in a random direction (this is the default actuator)
    # This is not really an efficient strategy...
    # Also the NPC move whatever our input, even when we navigates in menus.
    # Finally, we only move the NPCs of the current level. Nothing moves in the other levels.
    game.actuate_npcs(game.current_level)
    time.sleep(game_speed)


