from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Sprites as Sprites
import gamelib.Utils as Utils
import gamelib.Constants as Constants

g = Game()

b = g.load_board("hac-maps/kneighbors.json", 1)


g.player = Player(model=Sprites.FLYING_SAUCER, name="player")
g.change_level(1)

key = None

while True:
    if key == Utils.key.UP:
        g.move_player(Constants.UP, 1)
    elif key == Utils.key.DOWN:
        g.move_player(Constants.DOWN, 1)
    elif key == Utils.key.LEFT:
        g.move_player(Constants.LEFT, 1)
    elif key == Utils.key.RIGHT:
        g.move_player(Constants.RIGHT, 1)
    elif key == "q":
        break
    g.clear_screen()
    g.display_board()
    for i in g.neighbors(1):
        print(f"Player: {i.name} ({i.pos[0]},{i.pos[1]})")

    for i in g.neighbors(1, g.current_board().item(7, 7)):
        print(f"NPC: {i.name} ({i.pos[0]},{i.pos[1]})")

    key = Utils.get_key()
