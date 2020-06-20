from gamelib.Rendering import Sprite, Tile, MovableTile
from gamelib.Board import Board
from gamelib.Game import Game
from gamelib.Assets import Graphics
from gamelib import Constants
from gamelib.Characters import NPC
import time


rv = Sprite()
rv.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/road-vertical.ans")
print(rv)

rbl = Sprite()
rbl.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/road-bottom-left.ans")

rtl = Sprite()
rtl.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/road-top-left.ans")

rh = Sprite()
rh.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/road-horizontal.ans")

grass = Sprite()
grass.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/grass.ans")

house = Sprite()
house.load_from_file("/home/arnaud/Code/Python/hac-n-rogue/graphics/house-red.ans")

ig = Tile(name="grass", sprite=grass)
irv = Tile(name="road_vertical", sprite=rv)
irh = Tile(name="road_horizontal", sprite=rh)
irbl = Tile(name="road_bottom_left", sprite=rbl)
irtl = Tile(name="road_top_left", sprite=rtl)
ih = Tile(name="red_house", sprite=house)

print()

# 17*8 x 4*10 (sprites are 8x4)
b = Board(size=[136, 40], ui_borders="#", ui_board_void_cell=Graphics.BLUE_RECT)
g = Game()
c = 0
while c < 136:
    b.place_item(ig, 0, c)
    c += 8

b.place_item(irtl, 4, 0)
c = 8
while c < 136:
    b.place_item(irh, 4, c)
    b.place_item(irh, b.size[1] - irbl.dimension[1], c)
    c += 8
r = 8
while r < b.size[1] - irbl.dimension[1]:
    b.place_item(irv, r, 0)
    r += 4
b.place_item(irbl, b.size[1] - irbl.dimension[1], 0)
b.place_item(ih, 8, 8)
r = c = 8
while r < b.size[1] - irbl.dimension[1] - ig.dimension[1]:
    c = 8
    while c < b.size[0] - ig.dimension[0]:
        b.place_item(ih, r, c)
        b.place_item(ig, r, c + ih.dimension[0])
        b.place_item(ig, r + ig.dimension[1], c + ih.dimension[0])
        c += ih.dimension[0] + ig.dimension[0]
    b.place_item(ig, r, c)
    b.place_item(ig, r + ig.dimension[1], c)
    r += ih.dimension[1]
c = 8
while c < b.size[0]:
    b.place_item(ig, r, c)
    c += ig.dimension[0]
g.clear_screen()
b.display()
void = " "
panda_sprite = Sprite(
    sprixels=[
        [void, void, void, void, void, void, void, void],
        [
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
            void,
            void,
            void,
            void,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
        ],
        [
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
        ],
        [
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
        ],
        [
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.RED_RECT,
            Graphics.RED_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
        ],
        [
            void,
            void,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
            void,
            void,
        ],
        [
            void,
            void,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.WHITE_RECT,
            Graphics.BLACK_RECT,
            Graphics.BLACK_RECT,
        ],
        [void, void, Graphics.BLACK_RECT, Graphics.BLACK_RECT, void, void, void, void],
    ],
    size=[8, 8],
)


# panda_sprite = Sprite(sprixels=[["o"]], size=[1, 1])

pf = NPC(model=Graphics.Sprites.PANDA)

print(panda_sprite)
panda = MovableTile(name="panda", sprite=panda_sprite, void_char=" ", parent=b)
b.place_item(panda, 0, 0)
# b.place_item(pf, 1, 0)
input("Next?")
g.clear_screen()
b.display()
count = 0
while count < 10:
    time.sleep(0.2)
    panda.move(Constants.RIGHT, 1)
    # print("Moving panda")
    # b.move(pf, Constants.RIGHT, 1)
    # g.clear_screen()
    b.display()
    count += 1
