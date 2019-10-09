#!/usr/bin/env python3

from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import time
import sys

board_to_load = 'hac-maps/test-board.json'

if len(sys.argv) > 1:
    board_to_load = sys.argv[1]

max_iter = 10
if len(sys.argv) > 2:
    max_iter = int(sys.argv[2])


g = Game()

b = g.load_board(board_to_load, 1)

print(b)

g.player = Player(model=Sprites.FLYING_SAUCER)
g.change_level(1)


idx = 0
key = None

while idx < max_iter or max_iter == 0:
    if key == 'w':
        g.move_player(Constants.UP, 1)
    elif key == 's':
        g.move_player(Constants.DOWN, 1)
    elif key == 'a':
        g.move_player(Constants.LEFT, 1)
    elif key == 'd':
        g.move_player(Constants.RIGHT, 1)
    elif key == 'q':
        break
    g.clear_screen()
    g.actuate_npcs(1)
    g.display_board()

    if max_iter == 0:
        key = Utils.get_key()
    else:
        time.sleep(0.1)
        idx += 1
