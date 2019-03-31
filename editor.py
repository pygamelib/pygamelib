#!/usr/bin/env python3

import gamelib.Utils as Utils
import gamelib.Constants as Constants
from gamelib.Game import Game
from gamelib.Characters import Player
import os

game = Game()
game.player = Player(model='[]')


print( Utils.cyan_bright("HAC-GAME-LIB - EDITOR v"+Constants.HAC_GAME_LIB_VERSION) )

print('Looking for existing maps in hac-maps/ directory...',end='')
hmaps = []
try:
    hmaps = os.listdir('hac-maps/')
    print(Utils.green('OK'))
except FileNotFoundError as e:
    print(Utils.red('KO'))

if len(hmaps) > 0:
    map_num = 0
    for m in hmaps:
        print(f"{map_num} - edit hac-maps/{m}")
        map_num += 1
else:
    print("No pre-existing map found.")
print("n - create a new map")
print("q - Quit the editor")
choice = str(input("> "))
if choice == "q":
    print("Good Bye!")
    exit()
elif choice == "n":
    pass
elif int(choice) < len(hmaps):
    game.load_board('hac-maps/'+hmaps[int(choice)],1)
    game.change_level(1)
    game.display_board()