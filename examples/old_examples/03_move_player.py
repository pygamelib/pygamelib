import examples_includes  # noqa: F401
import time

# Engine contains Board, and Board is our base object  to display so we need that
from pygamelib import engine

# Then we need to get the Player object from Characters.py
from pygamelib.board_items import Player

# Also import graphics and gfx for the graphical things
from pygamelib.assets import graphics
from pygamelib.gfx import core

from pygamelib import base

# Finally import Constants as it holds valuable movement constants
from pygamelib import constants

# First let's create a Board that uses squares as delimiters
# Borders are going to be white squares
# Cells with nothing inside are going to be black squares
myboard = engine.Board(
    name="A demo board",
    size=[40, 20],
    ui_borders=graphics.WHITE_SQUARE,
    ui_board_void_cell_sprixel=core.Sprixel.black_square(),
    player_starting_position=[10, 10],
)

# Then create a Game object
game = engine.Game.instance()

# Then create a player, and give it to manage to the Game engine
game.player = Player(sprixel=core.Sprixel("××", None, core.Color(255, 255, 0)))

# Associate the board to level number 1
game.add_board(1, myboard)

# Now change the current level to 1. This will automatically place the player at the
# player_starting_position of the board associated with level 1.
game.change_level(1)

# And make a short loop that moves the player and display the board
for k in range(1, 10, 1):
    # Clear screen.
    game.clear_screen()
    # Print a debug message
    base.Text.debug(
        f"Round {k} player position is ({game.player.row},"
        f"{game.player.column}) -- BEFORE moving"
    )
    # Ask the game object to manage the movement of the player to the right by one cell
    game.move_player(constants.RIGHT, 1)
    # print another debug message
    base.Text.debug(
        f"Round {k} player position is now ({game.player.row},"
        f"{game.player.column}) -- AFTER moving"
    )
    # and display the board
    game.display_board()
    # Wait a second to let you admire the work!
    time.sleep(1)
