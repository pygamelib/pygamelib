from gamelib.Actuators.AdvancedActuators import PathFinder
from gamelib.Game import Game
from gamelib.Board import Board
from gamelib.Characters import Player, NPC
from gamelib.Structures import Door
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import time
import sys


# Destination 17,12
dest_row = 24
dest_col = 24

if len(sys.argv) > 1:
    dest_row = int(sys.argv[1])

if len(sys.argv) > 2:
    dest_col = int(sys.argv[2])
print(f'dest_row={dest_row} dest_col={dest_col}')
g = Game()
# b = g.load_board('hac-maps/Debug_board.json',1)
# b = g.load_board('hac-maps/PathFinding.json',1)
b = g.load_board('hac-maps/Maze.json',1)

g.player = Player(name='The Mighty Wizard',model=Sprites.MAGE)
g.change_level(1)
g.actuate_npcs(1)

pf = PathFinder(game=g,actuated_object=g.player)
pf.set_destination(dest_row,dest_col)
path = pf.find_path()
print("Path found:")
print(path)

for (r,c) in path:
    if r != g.player.pos[0] or c != g.player.pos[1]:
        b.place_item(Door(model=Utils.RED_SQUARE),r,c)

g.display_board()
nm = None
while nm != Constants.NO_DIR:
    nm = pf.next_move()
    g.move_player(nm,1)
    # g.clear_screen()
    g.display_board()
    time.sleep(0.1)