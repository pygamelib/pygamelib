import examples_includes  # noqa: F401
import time

# Engine contains Board, and Board is our base object  to display so we need that
from pygamelib import engine

# Then we need to get the Player object from Characters.py
from pygamelib.board_items import Player

# Also import graphics for the graphical things
from pygamelib.assets import graphics

from pygamelib import base

# Finally import Constants as it holds valuable movement constants
from pygamelib import constants

# First let's create a Board that uses squares as delimiters
# Borders are going to be white squares
# Cells with nothing inside are going to be black squares
myboard = engine.Board(
    name="A demo board",
    size=[40, 20],
    ui_border_left=graphics.WHITE_SQUARE,
    ui_border_right=graphics.WHITE_SQUARE,
    ui_border_top=graphics.WHITE_SQUARE,
    ui_border_bottom=graphics.WHITE_SQUARE,
    ui_board_void_cell=graphics.BLACK_SQUARE,
    player_starting_position=[10, 10],
)

# Then create a Game object
game = engine.Game()

# Then create a player, and give it to manage to the Game engine
game.player = Player(model=base.Text.yellow_bright("××"))

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
        f"Round {k} player position is ({game.player.pos[0]},"
        f"{game.player.pos[1]}) -- BEFORE moving"
    )
    # Ask the game object to manage the movement of the player to the right by one cell
    game.move_player(constants.RIGHT, 1)
    # print another debug message
    base.Text.debug(
        f"Round {k} player position is now ({game.player.pos[0]},"
        f"{game.player.pos[1]}) -- AFTER moving"
    )
    # and display the board
    game.display_board()
    # Wait a second to let you admire the work!
    time.sleep(1)
