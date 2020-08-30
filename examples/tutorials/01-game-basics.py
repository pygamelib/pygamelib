import examples_includes  # noqa: F401
from pygamelib import engine, board_items
from pygamelib.assets import graphics
import time

###############################################################################
#                                                                             #
# IMPORTANT NOTE:                                                             #
#                                                                             #
# The companion article for this tutorial code is at:                         #
# https://astro.hyrul.es/guides/hac-game-lib/tutorial-01-the-game-object.html #
#                                                                             #
###############################################################################

mygame = engine.Game(name="Demo game")
board1 = engine.Board(
    name="Level 1",
    ui_borders=graphics.Models.BRICK,
    ui_board_void_cell=graphics.BLACK_SQUARE,
    player_starting_position=[0, 0],
)
board2 = engine.Board(
    name="Level 2",
    ui_borders=graphics.RED_SQUARE,
    ui_board_void_cell=graphics.BLACK_SQUARE,
    player_starting_position=[4, 4],
)

mygame.player = board_items.Player(name="DaPlay3r", model=graphics.Models.UNICORN)

mygame.add_board(1, board1)
mygame.add_board(2, board2)

count = 0
lvl = 1

while count < 10:
    mygame.clear_screen()
    mygame.change_level(lvl)
    mygame.current_board().display()
    lvl += 1
    if lvl > 2:
        lvl = 1
    time.sleep(2)
    count += 1
