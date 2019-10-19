import examples_includes  # noqa: F401
from gamelib.Game import Game
from gamelib.Board import Board
import gamelib.Utils as Utils
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
from gamelib.Characters import Player
import time

###############################################################################
#                                                                             #
# IMPORTANT NOTE:                                                             #
#                                                                             #
# The companion article for this tutorial code is at:                         #
# https://astro.hyrul.es/guides/hac-game-lib/tutorial-02-player-movements.html#
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

mygame.change_level(1)

key = None
# Main game loop
while True:

    if key == "q":
        print(Utils.yellow_bright("Good bye and thank you for playing!"))
        break
    elif key == "w":
        mygame.move_player(Constants.UP, 1)
    elif key == "s":
        mygame.move_player(Constants.DOWN, 1)
    elif key == "a":
        mygame.move_player(Constants.LEFT, 1)
    elif key == "d":
        mygame.move_player(Constants.RIGHT, 1)
    elif key == "3":
        mygame.move_player(Constants.DRDOWN, 1)
    mygame.clear_screen()
    mygame.display_board()
    key = Utils.get_key()
    time.sleep(0.1)
