from gamelib.Actuators.AdvancedActuators import PathFinder
from gamelib.Actuators.SimpleActuators import RandomActuator
from gamelib.BoardItem import BoardItemVoid
from gamelib.Structures import Door
from gamelib.Game import Game
from gamelib.Characters import Player
import gamelib.Sprites as Sprites
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import time
import math

DEBUG = False


def redraw():
    global g
    global chasing
    g.clear_screen()
    g.display_player_stats()
    print(f"Position: {g.player.pos[0]},{g.player.pos[1]}")
    # if not DEBUG:
    g.display_board()
    if chasing:
        Utils.print_white_on_red("Guard is chasing!!!")


def reset_drawn_path():
    global g
    for i in g.current_board().get_immovables(type="path_marker"):
        g.current_board().place_item(BoardItemVoid(), i.pos[0], i.pos[1])


def nearest_cell(o1, o2):
    global g
    free_cells = []
    try:
        item = g.current_board().item(o1.pos[0] + 1, o1.pos[1])
        if isinstance(item, BoardItemVoid):
            free_cells.append((o1.pos[0] + 1, o1.pos[1]))
    except IndexError:
        pass

    try:
        item = g.current_board().item(o1.pos[0] - 1, o1.pos[1])
        if isinstance(item, BoardItemVoid):
            free_cells.append((o1.pos[0] - 1, o1.pos[1]))
    except IndexError:
        pass

    try:
        item = g.current_board().item(o1.pos[0], o1.pos[1] + 1)
        if isinstance(item, BoardItemVoid):
            free_cells.append((o1.pos[0], o1.pos[1] + 1))
    except IndexError:
        pass

    try:
        item = g.current_board().item(o1.pos[0], o1.pos[1] - 1)
        if isinstance(item, BoardItemVoid):
            free_cells.append((o1.pos[0], o1.pos[1] - 1))
    except IndexError:
        pass

    dc_r = 99999
    dc_c = 99999
    sum_dc = 9999
    winner = None
    for r, c in free_cells:
        # input(f"BoardItemVoid position: {r},{c}")
        tmp_dc_r = o2.pos[0] - r
        tmp_dc_c = o2.pos[1] - c
        eucli_dist = math.hypot(tmp_dc_c, tmp_dc_r)
        if tmp_dc_r < dc_r and tmp_dc_c < dc_c and eucli_dist < sum_dc:
            winner = (r, c)
            # print(f'dc_r: {o2.pos[0]}-{r} = {tmp_dc_r}')
            dc_r = o2.pos[0] - r
            # print(f'dc_c: {o2.pos[1]}-{c} = {tmp_dc_c}')
            dc_c = o2.pos[1] - c
            sum_dc = eucli_dist
            # print(
            #     f"Updating winner with {winner} and deltas {dc_r},{dc_c} "
            #     f"and sum_dc = {sum_dc}"
            # )
    if DEBUG:
        reset_drawn_path()
        g.current_board().place_item(
            Door(model=Utils.GREEN_SQUARE, type="path_marker"), winner[0], winner[1]
        )
        redraw()
    # input(f'Winner: {winner}')
    return winner


g = Game()
# b = g.load_board('/home/arnaud/Code/Games/hgl-editor/TestChasing.json', 1)
b = g.load_board("hac-maps/The_Castle.json", 1)

g.player = Player(name="The Mighty Wizard", model=Sprites.MAGE)
g.change_level(1)

guards = []

for item in g.current_board().get_movables(type="guard"):
    guards.append(item)

nm = None
key = None
chasing = False

while nm != Constants.NO_DIR:
    if g.player.hp <= 0:
        g.clear_screen()
        Utils.print_white_on_red("GAME OVER")
        break
    r = g.player.pos[0]
    c = g.player.pos[1]
    if key == Utils.key.UP:
        g.move_player(Constants.UP, 1)
    elif key == Utils.key.DOWN:
        g.move_player(Constants.DOWN, 1)
    elif key == Utils.key.RIGHT:
        g.move_player(Constants.RIGHT, 1)
    elif key == Utils.key.LEFT:
        g.move_player(Constants.LEFT, 1)
    elif key == "Q":
        break
    for guard in guards:
        if g.player in g.neighbors(5, guard):
            guard.actuator = PathFinder(game=g, actuated_object=guard)
            chasing = True
            winner = nearest_cell(g.player, guard)
            guard.actuator.set_destination(winner[0], winner[1])
        else:
            guard.actuator = RandomActuator(
                moveset=[Constants.UP, Constants.DOWN, Constants.LEFT, Constants.RIGHT]
            )
            chasing = False
        if chasing and g.player in g.neighbors(1, guard):
            g.player.hp -= 5
        else:
            g.actuate_npcs(1)
    redraw()
    time.sleep(0.1)
    key = Utils.get_key()

print("That's all folks!")
