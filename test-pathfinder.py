from gamelib.Actuators.AdvancedActuators import PathFinder
from gamelib.Game import Game
from gamelib.Board import Board
from gamelib.Characters import Player, NPC
from gamelib.Structures import Door
from gamelib.BoardItem import BoardItemVoid
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import time
import sys

def draw_path(p):
    global g
    for (r,c) in p:
        if r != g.player.pos[0] or c != g.player.pos[1]:
            g.current_board().place_item(Door(model=Utils.RED_SQUARE),r,c)

def reset_drawn_path(p):
    for i in p:
        g.current_board().place_item(BoardItemVoid(),i[0],i[1])

# Destination 17,12
dest_row = 24
dest_col = 24

if len(sys.argv) > 1:
    dest_row = int(sys.argv[1])

if len(sys.argv) > 2:
    dest_col = int(sys.argv[2])
print(f'dest_row={dest_row} dest_col={dest_col}')
g = Game()
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
    g.clear_screen()
    g.display_board()
    time.sleep(0.1)

pf.add_waypoint(g.player.pos[0],g.player.pos[1])
pf.add_waypoint(24,24)
pf.add_waypoint(21,40)

while True:
    (cwr,cwc) = pf.current_waypoint()
    if g.player.pos[0] == cwr and g.player.pos[1] == cwc:
        (r,c) = pf.next_waypoint()
        pf.set_destination(r,c)
        reset_drawn_path(path)
        path = pf.find_path()
        draw_path(path)
    g.move_player(pf.next_move(),1)
    g.clear_screen()
    g.display_board()
    time.sleep(0.1)