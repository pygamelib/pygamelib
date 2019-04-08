from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Sprites as Sprites
import time
import sys

board_to_load = 'hac-maps/test-board.json'

if len(sys.argv) > 1:
    board_to_load = sys.argv[1]

max_iter = 10
if len(sys.argv) > 2:
    max_iter = int(sys.argv[2])


g = Game()

b = g.load_board(board_to_load,1)

print(b)

g.player = Player(model=Sprites.FLYING_SAUCER)
g.change_level(1)

# print('Printing the complete list of sprites')
# print([getattr(Sprites,item) for item in dir(Sprites) if not item.startswith("__")])
idx=0
while idx< max_iter: 
    g.clear_screen()
    g.actuate_npcs(1)
    g.display_board()

    time.sleep(0.1)
    idx += 1
