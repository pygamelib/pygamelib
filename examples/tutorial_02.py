import examples_includes  # noqa: F401
from pygamelib import engine, board_items, constants, base
from pygamelib.assets import graphics
import time

###############################################################################
#                                                                             #
# IMPORTANT NOTE:                                                             #
#                                                                             #
# The companion article for this tutorial code is at:                         #
# https://astro.hyrul.es/guides/hac-game-lib/tutorial-02-player-movements.html#
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

mygame.change_level(1)

key = None
# Main game loop
while True:

    if key == "q":
        print(base.Text.yellow_bright("Good bye and thank you for playing!"))
        break
    elif key == "w" or key == engine.key.UP:
        mygame.move_player(constants.UP, 1)
    elif key == "s" or key == engine.key.DOWN:
        mygame.move_player(constants.DOWN, 1)
    elif key == "a" or key == engine.key.LEFT:
        mygame.move_player(constants.LEFT, 1)
    elif key == "d" or key == engine.key.RIGHT:
        mygame.move_player(constants.RIGHT, 1)
    elif key == "3":
        mygame.move_player(constants.DRDOWN, 1)
    mygame.clear_screen()
    mygame.display_board()
    key = mygame.get_key()
    time.sleep(0.1)
