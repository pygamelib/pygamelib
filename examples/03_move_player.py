import examples_includes  # noqa: F401
import time

# Board is our base object  to display so we need that
from gamelib.Board import Board

# Then we need to get the Player object from Characters.py
from gamelib.Characters import Player

# Also import Utils as it contains a lot of useful things
import gamelib.Utils as Utils

# Finally import Constants as it holds valuable movement constantes
import gamelib.Constants as Constants

# First let's create a Board that uses squares as delimiters
# Borders are going to be white squares
# Cells with nothing inside are going to be black squares
myboard = Board(
    name="A demo board",
    size=[40, 20],
    ui_border_left=Utils.WHITE_SQUARE,
    ui_border_right=Utils.WHITE_SQUARE,
    ui_border_top=Utils.WHITE_SQUARE,
    ui_border_bottom=Utils.WHITE_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[10, 20],
)

# Then create a player
playerone = Player(model=Utils.yellow_bright("××"))

# Place it on the board
myboard.place_item(playerone, 10, 10)

# Now let's display our board
myboard.display()

# And make a short loop that moves the player and display the board
# WARNING: in real life we would use the Game object to manage the game
# and the screen
for k in range(1, 10, 1):
    # Clear screen
    Utils.clear_screen()
    # Print a debug message
    Utils.debug(
        f"Round {k} player position is ({playerone.pos[0]},"
        f"{playerone.pos[1]}) -- BEFORE moving"
    )
    # Ask myboard to move playerone to the right by one cell
    myboard.move(playerone, Constants.RIGHT, 1)
    # print another debug message
    Utils.debug(
        f"Round {k} player position is now ({playerone.pos[0]},"
        f"{playerone.pos[1]}) -- AFTER moving"
    )
    # and display the board
    myboard.display()
    # Wait a second to let you admire the work!
    time.sleep(1)
