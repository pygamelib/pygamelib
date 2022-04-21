import examples_includes  # noqa: F401

# First let's import the game module. It holds Board, Game and Inventory.
import pygamelib.engine as engine

# Then some graphics to display nice colored squares.
import pygamelib.assets.graphics as graphics

# And gfx.core to do the same but with sprixels.
from pygamelib.gfx import core

# And finally board_items as it hold everything we can put on a board.
import pygamelib.board_items as board_items

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
    ui_board_void_cell_sprixel=core.Sprixel.black_square(),
    player_starting_position=[10, 20],
)

# Now let's make a couple of walls using colored squares as sprixels
green_wall = board_items.Wall(sprixel=core.Sprixel.green_square())
blue_wall = board_items.Wall(sprixel=core.Sprixel.blue_square())
cyan_wall = board_items.Wall(sprixel=core.Sprixel.cyan_square())
magenta_wall = board_items.Wall(sprixel=core.Sprixel.magenta_square())

# Now let's place these walls on the board
for k in range(1, 6, 1):
    myboard.place_item(green_wall, 1, k)
    myboard.place_item(magenta_wall, k, 6)

for k in range(2, 6, 1):
    myboard.place_item(blue_wall, k, 1)
    myboard.place_item(cyan_wall, 5, k)

# And just for the fun of it, let's place a orange-ish colored wall
# in the middle of that "structure"
myboard.place_item(
    board_items.Wall(sprixel=core.Sprixel("  ", core.Color(255, 123, 28))),
    3,
    3,
)

# Finally let's display the board
myboard.display()
