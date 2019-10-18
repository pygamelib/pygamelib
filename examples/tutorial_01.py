import examples_includes  # noqa: F401
from gamelib.Game import Game
from gamelib.Board import Board
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites
from gamelib.Characters import Player
import time

###############################################################################
#                                                                             #
# IMPORTANT NOTE:                                                             #
#                                                                             #
# The companion article for this tutorial code is at:                         #
# https://astro.hyrul.es/guides/hac-game-lib/tutorial-01-the-game-object.html #
#                                                                             #
###############################################################################

mygame = Game(name="Demo game")
board1 = Board(
    name="Level 1",
    ui_borders=Sprites.WALL,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[0, 0],
)
board2 = Board(
    name="Level 2",
    ui_borders=Utils.RED_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[4, 4],
)

mygame.player = Player(name="DaPlay3r", model=Sprites.UNICORN_FACE)

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
