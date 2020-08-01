#!/usr/bin/env python3

import pygamelib.engine as engine
import pygamelib.board_items as board_items
import pygamelib.assets.graphics as graphics
import pygamelib.constants as constants
import time
import sys

board_to_load = "hac-maps/test-board.json"

if len(sys.argv) > 1:
    board_to_load = sys.argv[1]

max_iter = 10
if len(sys.argv) > 2:
    max_iter = int(sys.argv[2])


g = engine.Game()

b = g.load_board(board_to_load, 1)

if b.width >= g.screen.width or b.height >= g.screen.height:
    g.enable_partial_display = True
    g.partial_display_viewport = [
        int((g.screen.height - 2) / 2),
        int((g.screen.width - 2) / 4),
    ]

g.player = board_items.Player(model=graphics.Models.FLYING_SAUCER)
g.player.inventory.max_size = 99999
g.change_level(1)


idx = 0
key = None

while idx < max_iter or max_iter == 0:
    if key == "w":
        g.move_player(constants.UP, 1)
    elif key == "s":
        g.move_player(constants.DOWN, 1)
    elif key == "a":
        g.move_player(constants.LEFT, 1)
    elif key == "d":
        g.move_player(constants.RIGHT, 1)
    elif key == "q":
        break
    g.clear_screen()
    g.actuate_npcs(1)
    g.display_board()

    if max_iter == 0:
        key = engine.Game.get_key()
    else:
        time.sleep(0.1)
        idx += 1
