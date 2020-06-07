from gamelib.Game import Game
from gamelib.BoardItem import BoardItemVoid
from gamelib.Characters import Player
from gamelib.Structures import Door
from gamelib.Assets import Graphics
from gamelib.Animation import Animation
import gamelib.Constants as Constants
import time
import random

# Let's create a table of "frames" (i.e colored blocks)
frames = [
    "\033[48;5;44m" + "  " + "\033[0m",
    "\033[48;5;45m" + "  " + "\033[0m",
    "\033[48;5;43m" + " " + "\033[48;5;44m" + " " + "\033[0m",
    "\033[48;5;44m" + " " + "\033[48;5;43m" + " " + "\033[0m",
    "\033[48;5;44m" + " " + "\033[48;5;45m" + " " + "\033[0m",
    "\033[48;5;45m" + " " + "\033[48;5;44m" + " " + "\033[0m",
    "\033[48;5;45m" + " " + "\033[48;5;80m" + " " + "\033[0m",
    "\033[48;5;80m" + " " + "\033[48;5;45m" + " " + "\033[0m",
    "\033[48;5;43m" + "  " + "\033[0m",
    "\033[48;5;80m" + "  " + "\033[0m",
]


# That function simply clear and display the board as well as the
# concatenated frames in one continuous strip.
def redraw_screen(g):
    g.clear_screen()
    # print("".join(frames))
    g.display_board()


# this function implement the flood fill algorithm to fill any area delimited
# by Wall objects (carefull if the area is not closed!)
def flood_filler(g, b, r, c):
    # If we hit anything but a void cell (BoardItemVoid) we have no business here.
    if not isinstance(b.item(r, c), BoardItemVoid):
        return
    # If we do hit a void cell, then we fill it with animated water
    if isinstance(b.item(r, c), BoardItemVoid):
        # First we pick a random integer number between 0 and the max index of the
        # frames array
        fi = random.randint(0, len(frames) - 1)
        # Then create a door object (overlappable and restorable) with that frame as
        # initial model
        d = Door(model=frames[fi])
        # Then create an animation that animate the Door object, with the frames
        # defined earlier and the random index we just picked.
        a = Animation(animated_object=d, frames=frames, initial_index=fi)
        # Set the Door animation to the animation we just built
        d.animation = a
        # Finally place the water on the board
        b.place_item(d, r, c)
    # Redraw the screen and wait to see the nice animation of the algorithm working.
    # Otherwise it's instantanous.
    redraw_screen(g)
    time.sleep(0.1)
    # Now make recursive calls to fill the cells around this one.
    flood_filler(g, b, r + 1, c)
    flood_filler(g, b, r - 1, c)
    flood_filler(g, b, r, c + 1)
    flood_filler(g, b, r, c - 1)


# Using the Game object just to load the board easily
g = Game()
b = g.load_board("/home/arnaud/Code/Games/hgl-editor/Filler.json", 1)
g.player = Player(model=Graphics.Sprites.MAGE)
g.change_level(1)
# We need the player out of our way
g.move_player(Constants.LEFT, 5)

# Now let's flood the floor!!
flood_filler(g, b, 5, 6)

# Show the animated lake for 200 turns (~40 secondes)
i = 0
while i < 200:
    i += 1
    redraw_screen(g)
    g.animate_items(1)
    time.sleep(0.2)
