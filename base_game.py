from gamelib.Board import Board
from gamelib.BoardItem import BoardItem
from gamelib.Characters import Player
from gamelib.Game import Game
from gamelib.Structures import Wall,Treasure, GenericStructure, GenericActionnableStructure
import gamelib.Constants as cst
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites
import time
import sys

sprite_mode = 'nosprite'

sprite_player = None
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
    sprite_player = Sprites.SHEEP
    sprite_portal = Sprites.CYCLONE
    sprite_treasure = Sprites.GEM_STONE
    sprite_treasure2 = Sprites.MONEY_BAG
    sprite_tree = Sprites.TREE_PINE
    sprite_wall = Sprites.WALL
else:
    sprite_player = Utils.RED_BLUE_SQUARE
    sprite_portal = Utils.CYAN_SQUARE
    sprite_treasure = Utils.YELLOW_RECT+Utils.RED_RECT
    sprite_treasure2 = sprite_treasure
    sprite_tree = Utils.GREEN_SQUARE
    sprite_wall = Utils.WHITE_SQUARE


game = Game(name='HAC Game')
p = Player(model=sprite_player,name='Nazbrok')

def refresh_screen(mygame,player):
    mygame.clear_screen()
    print(Utils.magenta_bright(f"\t\t~+~ Welcome to {mygame.name} ~+~"))
    mygame.current_board().display()
    print( Utils.yellow_dim( 'Where should ' )+Utils.cyan_bright(player.name)+Utils.yellow_dim(' go?') )
    mygame.print_menu()
    Utils.debug(f"Player stored position is ({player.pos[0]},{player.pos[1]})")

def goto_lvl2():
    game.change_level(2)

def goto_lvl1():
    game.change_level(1)

lvl1 = Board(name='Level_1',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE,player_starting_position=[10,20])
lvl2 = Board(name='Level_2',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE, player_starting_position=[0,0])
game.add_board(1,lvl1)
game.add_board(2,lvl2)

t = Treasure(model=sprite_treasure,name='Cool treasure')
money_bag = Treasure(model=sprite_treasure2,name='money')

tree = GenericStructure(model=sprite_tree)
tree.set_overlappable(False)
tree.set_pickable(False)

portal2 = GenericActionnableStructure(model=sprite_portal)
portal2.set_overlappable(True)
portal2.action = goto_lvl2

portal1 = GenericActionnableStructure(model=sprite_portal)
portal1.set_overlappable(True)
portal1.action = goto_lvl1

game.player = p

# lvl1.place_item(p,10,20)

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

for i in range(4,40,1):
    lvl1.place_item(tree,6,i)
    if i%4 != 0:
        lvl1.place_item(tree,8,i)
        for j in range(9,15,1):
            lvl1.place_item(tree,j,i)

lvl1.place_item(t,3,2)
lvl1.place_item(portal2,19,39)

lvl2.place_item(money_bag,10,35)
lvl2.place_item(portal1,11,35)
# lvl2.place_item(p,0,0)

game.add_menu_entry('w','Go up')
game.add_menu_entry('s','Go down')
game.add_menu_entry('a','Go left')
game.add_menu_entry('d','Go right')
game.add_menu_entry(None,'-'*17)
game.add_menu_entry('1','Go to level 1')
game.add_menu_entry('2','Go to level 2')
game.add_menu_entry('q','Quit game')

# Once Game, Boards and Player are created we change level
game.change_level(1)

direction = None
while direction != 'q':
    refresh_screen(game,p)
    # direction = str(input("What direction do you want to take: "))
    direction = Utils.get_key()
    if direction == 'w':
        game.current_board().move(p,cst.UP,1)
    elif direction == 's':
        game.current_board().move(p,cst.DOWN,1)
    elif direction == 'a':
        game.current_board().move(p,cst.LEFT,1)
    elif direction == 'd':
        game.current_board().move(p,cst.RIGHT,1)
    elif direction == 'q':
        game.clear_screen()
        print(Utils.yellow_bright('Good bye!'))
        break
    elif direction == '1':
        game.change_level(1)
    elif direction == '2':
        game.change_level(2)
    elif direction == 'c':
        game.current_board().clear_cell(4,3)
    else:
        Utils.fatal("Invalid direction: "+str(ord(direction)))
    time.sleep(0.2)


