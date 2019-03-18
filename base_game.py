from gamelib.Board import Board
from gamelib.BoardItem import BoardItem
from gamelib.Characters import Player
from gamelib.Game import Game
import gamelib.Constants as cst
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites

from gamelib.Structures import Wall,Treasure, GenericStructure

def refresh_screen(mygame,player):
    mygame.clear_screen()
    print(Utils.magenta_bright(f"\t\t~+~ Welcome to {mygame.name} ~+~"))
    mygame.current_board().display()
    print( Utils.yellow_dim( 'Where should ' )+Utils.cyan_bright(player.name)+Utils.yellow_dim(' go?') )
    mygame.print_menu()
    Utils.debug(f"Player stored position is ({player.pos[0]},{player.pos[1]})")

game = Game(name='HAC Game')

lvl1 = Board(name='Level_1',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE,player_starting_position=[10,20])
lvl2 = Board(name='Level_2',size=[40,20],ui_border_left=Utils.WHITE_SQUARE,ui_border_right=Utils.WHITE_SQUARE,ui_border_top=Utils.WHITE_SQUARE,ui_border_bottom=Utils.WHITE_SQUARE,ui_board_void_cell=Utils.BLACK_SQUARE, player_starting_position=[0,0])
game.add_board(1,lvl1)
game.add_board(2,lvl2)

w = Wall(model=Utils.GREEN_SQUARE)
portal = Wall(model=Sprites.CYCLONE)
t = Treasure(model=Sprites.GEM_STONE,name='Cool treasure')
p = Player(model=Sprites.SHEEP,name='Nazbrok')
tree = GenericStructure(model=Sprites.TREE_PINE)
tree.set_overlappable(False)
tree.set_pickable(False)

game.player = p

# lvl1.place_item(p,10,20)

lvl1.place_item(Wall(model=Sprites.WALL),2,3)
lvl1.place_item(Wall(model=Sprites.WALL),2,2)
lvl1.place_item(Wall(model=Sprites.WALL),2,1)
lvl1.place_item(Wall(model=Sprites.WALL),2,0)
lvl1.place_item(Wall(model=Sprites.WALL),3,3)
lvl1.place_item(Wall(model=Sprites.WALL),4,3)
lvl1.place_item(Wall(model=Sprites.WALL),5,3)
lvl1.place_item(Wall(model=Sprites.WALL),6,3)
lvl1.place_item(Wall(model=Sprites.WALL),6,2)
lvl1.place_item(Wall(model=Sprites.WALL),6,1)
lvl1.place_item(Wall(model=Sprites.WALL),7,1)
lvl1.place_item(Wall(model=Sprites.WALL),8,1)
lvl1.place_item(Wall(model=Sprites.WALL),8,3)
lvl1.place_item(Wall(model=Sprites.WALL),9,3)
lvl1.place_item(Wall(model=Sprites.WALL),10,3)
lvl1.place_item(Wall(model=Sprites.WALL),10,2)
lvl1.place_item(Wall(model=Sprites.WALL),10,1)
lvl1.place_item(Wall(model=Sprites.WALL),10,0)

for i in range(4,40,1):
    lvl1.place_item(tree,6,i)
    if i%4 != 0:
        lvl1.place_item(tree,8,i)
        for j in range(9,15,1):
            lvl1.place_item(tree,j,i)

lvl1.place_item(t,3,2)
lvl1.place_item(portal,19,39)

lvl2.place_item(t,10,35)
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
    direction = str(input("What direction do you want to take: "))
    if direction == 'w':
        game.current_board().move(p,cst.UP,1)
    elif direction == 's':
        game.current_board().move(p,cst.DOWN,1)
    elif direction == 'a':
        game.current_board().move(p,cst.LEFT,1)
    elif direction == 'd':
        game.current_board().move(p,cst.RIGHT,1)
    elif direction == 'q':
        break
    elif direction == '1':
        game.change_level(1)
    elif direction == '2':
        game.change_level(2)
    elif direction == 'c':
        game.current_board().clear_cell(4,3)
    else:
        Utils.fatal("Invalid direction")


