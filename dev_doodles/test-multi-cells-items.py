from gamelib.Board import Board
from gamelib.Characters import Player, Vehicle
from gamelib.Game import Game
import gamelib.Utils as Utils
import gamelib.Constants as Constants

g = Game()
g.player = Player(model="\u232C")

b = Board(size=[80, 50])
mod_right = [["\u25E3", " "], ["\u25A2", "\u25D7"], ["\u25E4", " "]]
mod_left = [["\u25E2"], ["\u25D6", "\u25A2"], ["\u25E2"]]
mi = Vehicle(model=mod_right)

g.add_board(1, b)
g.change_level(1)
g.current_board().place_item(mi, 20, 20)

key = None

while True:
    if key == Utils.key.UP:
        g.current_board().move(mi, Constants.UP, 1)
    elif key == Utils.key.DOWN:
        g.current_board().move(mi, Constants.DOWN, 1)
    elif key == Utils.key.LEFT:
        # mi.update_model(mod_left)
        g.current_board().move(mi, Constants.LEFT, 1)
    elif key == Utils.key.RIGHT:
        # mi.update_model(mod_right)
        g.current_board().move(mi, Constants.RIGHT, 1)
    elif key == "q":
        break
    g.clear_screen()
    g.display_board()
    print(f"Multi item width={mi.width()} height={mi.height()}")

    key = Utils.get_key()
