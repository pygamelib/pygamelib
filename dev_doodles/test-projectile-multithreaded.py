from gamelib.Game import Game
from gamelib.Characters import Player, NPC
from gamelib.BoardItem import BoardItemVoid
from gamelib.Animation import Animation
from gamelib.Board import Board
from gamelib.Actuators.SimpleActuators import RandomActuator
from gamelib.Movable import Projectile
from gamelib.Structures import Wall
import gamelib.Assets.Graphics as Graphics
import gamelib.Constants as Constants
import gamelib.Utils as Utils
import _thread
import time
from blessed import Terminal
from playsound import playsound
from copy import deepcopy

SFX_DIR = "/home/arnaud/Code/Python/hac-n-rogue/sound/sfx/"


def fireball_callback(projectile, objects, *args):
    _thread.start_new_thread(playsound, (SFX_DIR + "fireball-explosion.wav",))
    if len(objects) == 0:
        return None
    if isinstance(objects[0], BoardItemVoid):
        return None
    for o in objects:
        if isinstance(o, NPC):
            o.hp -= 5


def zap_callback(projectile, objects, *args):
    _thread.start_new_thread(playsound, (SFX_DIR + "spell-02.wav",))
    if len(objects) == 0:
        return None
    if isinstance(objects[0], BoardItemVoid):
        return None
    for o in objects:
        if isinstance(o, NPC):
            o.hp -= 6


def redraw_screen():
    global g
    global terminal
    global current_spell_template
    g.clear_screen()
    nb_blocks_mp = int((g.player.mp / g.player.max_mp) * 20)
    nb_blocks_hp = int((g.player.hp / g.player.max_hp) * 20)
    print(
        f"HP |{Graphics.RED_RECT * nb_blocks_hp}"
        f"{Graphics.BLACK_RECT * (20 - nb_blocks_hp)}| "
        f"Mana |{Graphics.BLUE_RECT * nb_blocks_mp}"
        f"{Graphics.BLACK_RECT * (20 - nb_blocks_mp)}|"
    )
    print(f"\rLevel: {g.player.level}")
    print("\r", end="")
    g.display_board()
    print(f"Terminal size: {terminal.width}x{terminal.height}")
    b = g.current_board()
    with terminal.location(b.size[0] * 2 + 5, 3):
        print(terminal.bold_underline_green("Enemies"))
    line = 4
    # for o in g.current_board().get_movables():
    for o in g.neighbors(current_spell_template.range, g.player):
        if isinstance(o, NPC):
            nb_blocks_hp = int((o.hp / o.max_hp) * 20)
            with terminal.location(terminal.width - 20, line):
                print(
                    f"{Graphics.GREEN_RECT * nb_blocks_hp}"
                    f"{Graphics.BLACK_RECT * (20 - nb_blocks_hp)}"
                )
            with terminal.location(terminal.width - 20, line + 1):
                print(f"{o.name}")
            line += 2
    with terminal.location(b.size[0] * 2 + 5, 12):
        print(terminal.bold_underline_blue("Spells"))
    with terminal.location(b.size[0] * 2 + 5, 13):
        print(terminal.bold("9 - Fireball"))
    with terminal.location(b.size[0] * 2 + 5, 14):
        print(terminal.bold("0 - Bolt"))
    with terminal.location(0, b.size[1] + 6):
        color_prefix = ""
        if current_spell_template.name == "fireball":
            color_prefix = Utils.Fore.BLUE
        print(
            color_prefix
            + Graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL * 3
            + Graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT
            + "\n\r"
            + Graphics.BoxDrawings.LIGHT_VERTICAL
            + Utils.red_bright("-")
            + color_prefix
            + Graphics.Sprites.COLLISION
            + Graphics.BoxDrawings.LIGHT_VERTICAL
            + "\n\r"
            + Graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL
            + "9"
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL
            + Graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT
            + Graphics.Style.RESET_ALL
            + "\n\r"
        )
    color_prefix = ""
    if current_spell_template.name == "zap":
        color_prefix = Utils.Fore.BLUE
    with terminal.location(5, b.size[1] + 6):
        print(
            color_prefix
            + Graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL * 3
            + Graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT
        )
    with terminal.location(5, b.size[1] + 7):
        print(
            color_prefix
            + Graphics.BoxDrawings.LIGHT_VERTICAL
            + " "
            + Graphics.Sprites.HIGH_VOLTAGE
            + Graphics.BoxDrawings.LIGHT_VERTICAL
        )
    with terminal.location(5, b.size[1] + 8):
        print(
            color_prefix
            + Graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL
            + "0"
            + Graphics.BoxDrawings.LIGHT_HORIZONTAL
            + Graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT
            + Graphics.Style.RESET_ALL
            + "\n\r"
        )


def ui_threaded():
    global g
    global game_running
    while game_running:
        if g.player.mp < g.player.max_mp:
            g.player.mp += 0.1
        for o in g.current_board().get_movables():
            if isinstance(o, NPC) and o.hp <= 0:
                _thread.start_new_thread(playsound, (SFX_DIR + "goblin-00.wav",))
                g.remove_npc(1, o)
        redraw_screen()
        g.actuate_npcs(1)
        g.actuate_projectiles(1)
        g.animate_items(1)
        time.sleep(0.1)


game_running = True
b = Board(
    ui_borders=Graphics.WHITE_SQUARE,
    ui_board_void_cell=Graphics.BLACK_SQUARE,
    size=[20, 20],
    player_starting_position=[5, 5],
)
wall = Wall(model=Graphics.Sprites.BRICK)
b.place_item(wall, 1, 6)
b.place_item(wall, 5, 10)
g = Game()
g.add_board(1, b)
g.player = Player(model=Graphics.Sprites.MAGE)
g.player.level = 1
g.player.mp = 20
g.player.max_mp = 20

g.add_npc(
    1,
    NPC(
        name="Bob Soontobedead",
        model=Graphics.Sprites.SKULL,
        hp=10,
        actuator=RandomActuator(moveset=[Constants.NO_DIR]),
    ),
    6,
    10,
)
g.add_npc(
    1,
    NPC(
        name="Bob Soontobedead II",
        model=Graphics.Sprites.SKULL,
        hp=10,
        actuator=RandomActuator(moveset=[Constants.NO_DIR]),
    ),
    7,
    11,
)
g.add_npc(
    1,
    NPC(
        name="Bob Soontobedead III",
        model=Graphics.Sprites.SKULL,
        hp=10,
        actuator=RandomActuator(moveset=[Constants.NO_DIR]),
    ),
    8,
    10,
)
g.add_npc(
    1,
    NPC(
        name="Mover",
        model=Graphics.Sprites.ZOMBIE,
        hp=10,
        actuator=RandomActuator(
            moveset=[Constants.UP, Constants.DOWN, Constants.LEFT, Constants.RIGHT]
        ),
    ),
    18,
    18,
)

g.change_level(1)
key = None
last_direction = Constants.RIGHT
is_fullscreen = False

terminal = Terminal()
print(terminal.enter_fullscreen)

black_circle = "\U000025CF"
circle_jot = "\U0000233E"

throw_fireball = False

_thread.start_new_thread(ui_threaded, ())

# Fireball template
fireball_template = Projectile(
    model=Utils.red_bright(f"~{black_circle}"),
    name="fireball",
    range=7,
    hit_model=Graphics.Sprites.COLLISION,
    hit_animation=None,
    hit_callback=fireball_callback,
    step=1,
    is_aoe=True,
    aoe_radius=1,
)
zap_template = Projectile(
    model=Utils.yellow_bright("\U00002301\U00002301"),
    name="zap",
    range=8,
    hit_model=Graphics.Sprites.HIGH_VOLTAGE,
    hit_callback=zap_callback,
)
# Left
fireball_template.add_directional_model(
    Constants.LEFT, Utils.red_bright(f"{black_circle}~")
)
fa = Animation(
    auto_replay=True,
    animated_object=fireball_template,
    refresh_screen=redraw_screen,
    display_time=0.5,
)
fa.add_frame(Utils.red_bright(f"{black_circle}~"))
fa.add_frame(Utils.red_bright(f"{circle_jot}~"))
fireball_template.add_directional_animation(Constants.RIGHT, fa)
# Right
fireball_template.add_directional_model(
    Constants.RIGHT, Utils.red_bright(f"~{black_circle}")
)
fa = Animation(
    auto_replay=True,
    animated_object=fireball_template,
    refresh_screen=redraw_screen,
    display_time=0.5,
)
fa.add_frame(Utils.red_bright(f"~{black_circle}"))
fa.add_frame(Utils.red_bright(f"-{circle_jot}"))
fireball_template.add_directional_animation(Constants.RIGHT, fa)

# Up
fireball_template.add_directional_model(
    Constants.UP, Utils.red_bright(f" {black_circle}")
)
fa = Animation(
    auto_replay=True,
    animated_object=fireball_template,
    refresh_screen=redraw_screen,
    display_time=0.5,
)
fa.add_frame(Utils.red_bright(f" {black_circle}"))
fa.add_frame(Utils.red_bright(f" {circle_jot}"))
fireball_template.add_directional_animation(Constants.UP, fa)

# Down
fireball_template.add_directional_model(
    Constants.DOWN, Utils.red_bright(f" {black_circle}")
)
fa = Animation(
    auto_replay=True,
    animated_object=fireball_template,
    refresh_screen=redraw_screen,
    display_time=0.5,
)
fa.add_frame(Utils.red_bright(f" {black_circle}"))
fa.add_frame(Utils.red_bright(f" {circle_jot}"))
fireball_template.add_directional_animation(Constants.DOWN, fa)

current_spell_template = fireball_template

while True:
    if key == "Q":
        game_running = False
        break
    elif key == "F":
        if is_fullscreen:
            terminal.exit_fullscreen()
        else:
            terminal.enter_fullscreen()
            is_fullscreen = True
    elif key == "1":
        viewport = [10, 10]
        g.partial_display_viewport = viewport
    elif key == "2":
        viewport = [15, 30]
        g.partial_display_viewport = viewport
    elif key == "3":
        viewport = [20, 20]
        g.partial_display_viewport = viewport
    elif key == "9":
        current_spell_template = fireball_template
    elif key == "0":
        current_spell_template = zap_template
    if key == Utils.key.SPACE:
        if g.player.mp >= 4:
            spell = deepcopy(current_spell_template)
            if last_direction == Constants.LEFT:
                spell.set_direction(Constants.LEFT)
                g.add_projectile(1, spell, g.player.pos[0], g.player.pos[1] - 1)
            elif last_direction == Constants.UP:
                spell.set_direction(Constants.UP)
                g.add_projectile(1, spell, g.player.pos[0] - 1, g.player.pos[1])
            elif last_direction == Constants.DOWN:
                spell.set_direction(Constants.DOWN)
                g.add_projectile(1, spell, g.player.pos[0] + 1, g.player.pos[1])
            else:
                spell.set_direction(Constants.RIGHT)
                g.add_projectile(1, spell, g.player.pos[0], g.player.pos[1] + 1)

            if current_spell_template == fireball_template:
                _thread.start_new_thread(playsound, (SFX_DIR + "fireball.wav",))
                g.player.mp -= 4
            elif current_spell_template == zap_template:
                _thread.start_new_thread(playsound, (SFX_DIR + "dizzy-bolt-spell.wav",))
                g.player.mp -= 3
    elif key == Utils.key.UP:
        if last_direction == Constants.UP:
            g.move_player(Constants.UP, 1)
        else:
            last_direction = Constants.UP
    elif key == Utils.key.DOWN:
        # g.move_player(Constants.DOWN, 1)
        if last_direction == Constants.DOWN:
            g.move_player(Constants.DOWN, 1)
        else:
            last_direction = Constants.DOWN
    elif key == Utils.key.LEFT:
        # g.move_player(Constants.LEFT, 1)
        if last_direction == Constants.LEFT:
            g.move_player(Constants.LEFT, 1)
        else:
            last_direction = Constants.LEFT
    elif key == Utils.key.RIGHT:
        # g.move_player(Constants.RIGHT, 1)
        if last_direction == Constants.RIGHT:
            g.move_player(Constants.RIGHT, 1)
        else:
            last_direction = Constants.RIGHT

    key = Utils.get_key()

print(terminal.exit_fullscreen)
