from gamelib.Actuators.AdvancedActuators import PathFinder
from gamelib.Game import Game
from gamelib.Characters import Player, NPC
from gamelib.Structures import Door, Wall
from gamelib.BoardItem import BoardItemVoid
from gamelib.Animation import Animation
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import time
import sys


def draw_path(p):
    global g
    for (r, c) in p:
        if r != g.player.pos[0] or c != g.player.pos[1]:
            g.current_board().place_item(
                Door(model=Utils.RED_SQUARE, type="path_marker"), r, c
            )


def reset_drawn_path():
    global g
    for i in g.current_board().get_immovables(type="path_marker"):
        g.current_board().place_item(BoardItemVoid(), i.pos[0], i.pos[1])


def redraw():
    global g
    g.clear_screen()
    g.display_board()


# Destination (24,24) is the center of the labyrinth
dest_row = 24
dest_col = 26

if len(sys.argv) > 1:
    dest_row = int(sys.argv[1])

if len(sys.argv) > 2:
    dest_col = int(sys.argv[2])

g = Game()
b = g.load_board("hac-maps/Maze.json", 1)

g.player = Player(name="The Mighty Wizard", model=Sprites.MAGE)
g.change_level(1)
g.actuate_npcs(1)

pf = PathFinder(game=g, actuated_object=g.player)

pf.add_waypoint(dest_row, dest_col)
pf.add_waypoint(24, 24)
pf.add_waypoint(21, 40)

pf.circle_waypoints = True

pf.set_destination(dest_row, dest_col)

blocker = NPC(model=Sprites.SKULL)
g.current_board().place_item(blocker, 20, 1)

wall = Wall(model=Sprites.WALL)
wall.animation = Animation(animated_object=wall)
wall.animation.add_frame(Sprites.BANKNOTE_DOLLARS)
wall.animation.add_frame(Sprites.BANKNOTE_EUROS)
wall.animation.add_frame(Sprites.BANKNOTE_WINGS)
g.current_board().place_item(wall, 5, 25)

# 43,28 43,34 39,34 39,40 44,40 44,28
patroller = NPC(model=Sprites.ALIEN, name="patroller")
patroller.actuator = PathFinder(
    game=g, actuated_object=patroller, circle_waypoints=True
)
g.add_npc(1, patroller, 43, 29)
patroller.actuator.set_destination(43, 29)
patroller.actuator.add_waypoint(43, 29)
patroller.actuator.add_waypoint(43, 34)
patroller.actuator.add_waypoint(39, 34)
patroller.actuator.add_waypoint(39, 40)
patroller.actuator.add_waypoint(44, 40)
patroller.actuator.add_waypoint(44, 28)
patroller.animation = Animation(
    animated_object=patroller, refresh_screen=redraw, display_time=0.5
)
# patroller.animation.add_frame('--')
# patroller.animation.add_frame(' |')

patroller.animation.add_frame(Sprites.ALIEN)
patroller.animation.add_frame(Sprites.ALIEN_MONSTER)
patroller.animation.add_frame(Sprites.EXPLOSION)
patroller.animation.add_frame(Sprites.SKULL)

patroller.animation.play_all()

nm = None
(wpr, wpc) = (None, None)
path = []

while nm != Constants.NO_DIR:
    nm = pf.next_move()

    # The following code is only to draw the path calculated by the PathFinder.
    (tmp_wpr, tmp_wpc) = pf.current_waypoint()
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
        g.current_board().place_item(blocker, 20, 0)

    # Now we use the direction to move the player and display the board.
    g.move_player(nm, 1)
    g.actuate_npcs(1)
    g.animate_items(1)
    redraw()
    time.sleep(0.1)

print("That's all folks!")
