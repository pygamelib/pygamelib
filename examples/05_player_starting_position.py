import examples_includes  # noqa: F401

# For this example we need to import Game, Board, Utils and Player
from gamelib.Game import Game
from gamelib.Board import Board
from gamelib.Characters import Player
import gamelib.Utils as Utils

# import system modules
import time
import sys


# This function is to display a 5 secondes countdown
def countdown():
    print("Changing level in: ")
    for i in range(0, 10):
        time.sleep(1)
        sys.stdout.write("\u001b[1000D")
        # sys.stdout.flush()
        # time.sleep(1)
        sys.stdout.write(str(9 - i) + " secondes")
        sys.stdout.flush()
    print()


# first let's create 3 boards, we are just going to create default boards
# with different border colors.
# We are going to set different starting position for the player on each board.

# On this board the player starts at the top left corner
lvl1 = Board(
    ui_borders=Utils.CYAN_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[0, 0],
)

# On that board the player starts at the center
lvl2 = Board(
    ui_borders=Utils.MAGENTA_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[5, 5],
)

# And on that board the player starts at the bottom right corner
lvl3 = Board(
    ui_borders=Utils.RED_SQUARE,
    ui_board_void_cell=Utils.BLACK_SQUARE,
    player_starting_position=[9, 9],
)

# Now let's create a game object.
mygame = Game(name="demo")

# And a Player
nazbrok = Player(name="Nazbrok", model=Utils.green_bright("¤¤"))

# Now add the boards to the game so the Game object can manage them
# the parameters of add_board() are a level number and a board.
mygame.add_board(1, lvl1)
mygame.add_board(2, lvl2)
mygame.add_board(3, lvl3)

# Now we also want our player to be managed by the game
mygame.player = nazbrok

# Now let's show a clean screen to our player
mygame.clear_screen()

# We haven't place nazbrok on any board, but that's ok because we are going
# to use Game to manage the starting position of our player
# First let's display nazbrok's position
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]}, {nazbrok.pos[0]})"
    f" -- BEFORE changing level"
)
# Now the only thing we need is to change level
mygame.change_level(1)
# and Nazbrok is auto-magically at the starting position for our lvl1 board!
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]}, {nazbrok.pos[0]})"
    f" -- AFTER changing level to level 1"
)

# Now let's display the current board
mygame.current_board().display()

# Let's wait a little
countdown()

# Now do it all again: clear the screen, print Nazbrok's position, change
# level, print the new position and wait a little
mygame.clear_screen()
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]},{nazbrok.pos[0]})"
    f" -- BEFORE changing level"
)
# Now let's go to level 2
mygame.change_level(2)
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]},{nazbrok.pos[0]})"
    f" -- AFTER changing level to level 2"
)
mygame.current_board().display()
countdown()

# And finally do that one last time to go to level 3
mygame.clear_screen()
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]},{nazbrok.pos[0]})"
    f" -- BEFORE changing level"
)
# Now let's go to level 3
mygame.change_level(3)
Utils.debug(
    f"Nazbrok is at position ({nazbrok.pos[0]},{nazbrok.pos[0]})"
    f" -- AFTER changing level to level 3"
)
mygame.current_board().display()

print(
    Utils.white_bright(
        "As you can see even though we never actively"
        " moved the player, the Game() object took care"
        " of it for us while changing level."
        "\nThe Game.change_level() method takes care of:\n -"
        " placing the player at the board's"
        " player_starting_position\n - cleanning the previous"
        " board from the player presence.\n - setting the"
        " Game.current_level instance variable"
    )
)
