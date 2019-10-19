import examples_includes  # noqa: F401

# Board is our base object  to display so we need that
from gamelib.Board import Board

# Then we need to get the Wall object from Structures.py
from gamelib.Structures import Wall

# Finally we import Utils as it contains a lot of useful things
import gamelib.Utils as Utils

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

# Now let's make a couple of walls using colored squares as models
green_wall = Wall(model=Utils.GREEN_SQUARE)
blue_wall = Wall(model=Utils.BLUE_SQUARE)
cyan_wall = Wall(model=Utils.CYAN_SQUARE)
magenta_wall = Wall(model=Utils.MAGENTA_SQUARE)

# Now let's place these walls on the board
for k in range(1, 6, 1):
    myboard.place_item(green_wall, 1, k)
    myboard.place_item(magenta_wall, k, 6)

for k in range(2, 6, 1):
    myboard.place_item(blue_wall, k, 1)
    myboard.place_item(cyan_wall, 5, k)

# And just for the fun of it, let's place a yellow and cyan wall
# in the middle of that "structure"
myboard.place_item(Wall(model=Utils.YELLOW_CYAN_SQUARE), 3, 3)

# Finally let's display the board
myboard.display()
