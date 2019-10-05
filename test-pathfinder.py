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
            g.current_board().place_item(Door(model=Utils.RED_SQUARE,type='path_marker'),r,c)

def reset_drawn_path():
    global g
    for i in g.current_board().get_immovables(type='path_marker'):
        g.current_board().place_item(BoardItemVoid(),i.pos[0],i.pos[1])

# Destination (24,24) is the center of the labyrinth
dest_row = 24
dest_col = 24

if len(sys.argv) > 1:
    dest_row = int(sys.argv[1])

if len(sys.argv) > 2:
    dest_col = int(sys.argv[2])

g = Game()
b = g.load_board('hac-maps/Maze.json',1)

g.player = Player(name='The Mighty Wizard',model=Sprites.MAGE)
g.change_level(1)
g.actuate_npcs(1)

pf = PathFinder(game=g,actuated_object=g.player)

pf.add_waypoint(dest_row,dest_col)
pf.add_waypoint(24,24)
pf.add_waypoint(21,40)

pf.circle_waypoints = True

pf.set_destination(dest_row,dest_col)

blocker = NPC(model=Sprites.SKULL)
g.current_board().place_item(blocker, 20,1)

nm = None
(wpr,wpc) = (None,None)
path = []

while nm != Constants.NO_DIR:
    nm = pf.next_move()

    # The following code is only to draw the path calculated by the PathFinder.
    (tmp_wpr,tmp_wpc) = pf.current_waypoint()
    if wpr != tmp_wpr or wpc != tmp_wpc:
        if len(path) != 0:
            reset_drawn_path()
        path = pf.current_path()
        draw_path(path)
        wpr = tmp_wpr
        wpc = tmp_wpc
    if g.player.pos[0] == 15 and g.player.pos[1] == 0:
        g.current_board().move(blocker, Constants.LEFT, 1)
    if g.player.pos[0] == 19 and g.player.pos[1] == 1:
        reset_drawn_path()
        path = pf.current_path()
        draw_path(path)
        g.current_board().place_item(blocker, 20,0)
    
    # Now we use the direction to move the player and display the board.
    g.move_player(nm,1)
    g.clear_screen()
    g.display_board()
    time.sleep(0.05)