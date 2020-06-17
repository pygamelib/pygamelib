#!/bin/env python3
import os
import examples_includes  # noqa F401
from gamelib.Game import Game
from gamelib.Characters import Player
from gamelib.Assets import Graphics
from gamelib.Structures import Wall, Door
from gamelib.Board import Board
from gamelib.BoardItem import BoardItemVoid
from gamelib.Structures import GenericActionableStructure, Treasure
from gamelib import Constants
from gamelib import Utils
from gamelib.Movable import Projectile
from time import sleep
from blessed import Terminal
import _thread
import random
import math
import simpleaudio as sa

gravity_speed = 1
gravity_friction = 1.5
enable_rebound = False
term_res = 80
states = ["title", "hiscores", "game", "settings"]
title_screen_menu = [
    "How to play",
    "Start game",
    "Hall of fame",
    "Switch resolution",
    "Change your name",
    "Quit",
]
current_state = "title"
logo = []
term = Terminal()
menu_indicator_left = "> "
menu_indicator_right = " <"
bg_color = "\033[48;5;26m"
traps_color = "\033[38;5;226m"
brick_colors = [
    "\033[48;5;130m",
    "\033[48;5;166m",
    "\033[48;5;214m",
    "\033[48;5;94m",
    "\033[48;5;136m",
]

# Sound effects
jump_wave_obj = sa.WaveObject.from_wave_file(os.path.join("sfx", "panda-jump.wav"))
hit_wave_obj = sa.WaveObject.from_wave_file(os.path.join("sfx", "hit.wav"))
boom_wave_obj = sa.WaveObject.from_wave_file(os.path.join("sfx", "boom.wav"))
zap_wave_obj = sa.WaveObject.from_wave_file(os.path.join("sfx", "zap.wav"))
trap_shoot_wave_obj = sa.WaveObject.from_wave_file(
    os.path.join("sfx", "trap-shoot.wav")
)
pickup_wave_obj = sa.WaveObject.from_wave_file(os.path.join("sfx", "pickup.wav"))


def block_color():
    return random.choice(brick_colors)


def title_screen(g):
    global logo, current_state, term_res
    menu_index = 0
    key = None
    while current_state == "title":
        g.clear_screen()
        for logo_line in logo:
            print(logo_line, end="\r")
        print("\r")
        print(Utils.blue(f"{' '*int(term_res/2-10)}Welcome {g.player.name}!\r"))
        for i in range(0, len(title_screen_menu)):
            if i == menu_index:
                print(
                    Utils.green_bright(
                        f"{' '*int(term_res/2-10)}{menu_indicator_left}"
                        f"{title_screen_menu[i]}{menu_indicator_right}\r"
                    )
                )
            else:
                print(f"  {' '*int(term_res/2-10)}{title_screen_menu[i]}\r")
        key = Utils.get_key()
        if key == Utils.key.DOWN:
            menu_index += 1
            if menu_index >= len(title_screen_menu):
                menu_index = 0
        elif key == Utils.key.UP:
            menu_index -= 1
            if menu_index < 0:
                menu_index = len(title_screen_menu) - 1
        elif key == Utils.key.ENTER:
            if menu_index == 0:
                g.clear_screen()
                print(term.bold_underline_green("How to play"))
                print(
                    "\nThe arrow "
                    + term.bold_underline("(\u2190/\u2191/\u2193/\u2192)")
                    + " keys move the panda.\n\n"
                    + "The "
                    + term.bold_underline("p")
                    + " key, pause the game.\n\n"
                    "The "
                    + term.bold_underline("space")
                    + " key is for jump. You can move while jumping.\n\n"
                    + term.bold_underline("w(z)/a(q)/s/d")
                    + " keys are for shooting seeds that sprouts trees.\n"
                    "              Sprouted trees can be used as platforms but:\n"
                    "               - You can only have 2 trees at the same time.\n"
                    "               - Shooting a seed cost you 3 secondes of time!\n"
                    "\nRunning forward earn you some time (depending on difficulty).\n"
                    "\nYour goal is to reach the end of a level as quickly as "
                    "possible without falling into radioactive wastes.\n"
                    "If you do fall into the radioactive wastes, the game will revive "
                    "you up the nearest safe platform. You can move during that time.\n"
                    "It is up to you to try your luck and trick the game or respawn "
                    "safely. You have 3 lives to complete your run.\n"
                    "\nAt the end of a level look for the portal to the next level. "
                    "It looks like a cyclone: " + Graphics.Sprites.CYCLONE + "\n"
                    "\nTo increase your score, just move forward! The higher the level"
                    " the higher the score. Difficulty also inscrease as you earn less"
                    " time.\n"
                    "\nOh... there's also treasures that gives you time and/or points "
                    "and traps that takes times or score (or your life...)\n"
                    "\n\nGOOD LUCK PANDA!!\n\n"
                    + Graphics.Sprites.WARNING
                    + " This game relies on emojis for its "
                    "user interface. If you don't see a panda face between the "
                    "parenthesis ("
                    + Graphics.Sprites.PANDA
                    + "), it means that your terminal fonts do NOT support "
                    "emojis. This game won't display correctly. Try other fonts.\n\n"
                )
                input("Press ENTER when done reading.")
            elif menu_index == 1:
                current_state = "game"
                # We need to start over so back to level 1
                g.current_level = 0
                # Let's make sure the player is correctly placed by the engine
                g.player.pos = [None, None]
                # And lives, score and timer are reset
                g.timer = 60
                g.score = 0
                g.player.remaining_lives = 3
                # Then reset the player model in case he died
                g.player.model = (
                    bg_color + Graphics.Sprites.PANDA + Graphics.Style.RESET_ALL
                )
                g.clear_screen()
                change_level([g])
            elif menu_index == 2:
                g.clear_screen()
                print(
                    Utils.blue(
                        f"{' '*int(term_res/2-10)}"
                        + term.bold_underline("Hall of fame")
                        + "\r"
                    )
                )
                ranking = 1
                for el in sorted(
                    g.config("settings")["hiscores"], reverse=True, key=lambda x: x[1]
                ):
                    extra = ""
                    if ranking == 1:
                        extra = Graphics.Sprites.FIRST_PLACE_MEDAL
                    elif ranking == 2:
                        extra = Graphics.Sprites.SECOND_PLACE_MEDAL
                    elif ranking == 3:
                        extra = Graphics.Sprites.THIRD_PLACE_MEDAL
                    print(f"{' '*int(term_res/2-10)}{el[0]} : {el[1]} {extra}")
                    ranking += 1
                input("\n\nHit the ENTER key to return to the main menu.\n")
            elif menu_index == 3:
                # Switch resolution
                if term_res == 80:
                    term_res = 140
                else:
                    term_res = 80
                load_logo()
                g.partial_display_viewport = [10, int(term_res / 4)]
            elif menu_index == 4:
                g.player.name = input(
                    "\n\nPlease enter your name (it will be used for high scores)> "
                )
                g.config("settings")["player_name"] = g.player.name
            elif menu_index == (len(title_screen_menu) - 1):
                # Quit
                current_state = "eop"


def load_logo():
    global logo
    with open(f"suparex-{term_res}.utf.ans", "r") as f:
        logo = f.readlines()


def refresh_screen(g):
    # g.clear_screen()
    print(term.home)
    # print(
    #     f"Player: {g.player.pos} size[1]: {g.current_board().size[1]} player max_y: "
    #     f"{int(g.player.max_y)} player dy: {g.player.dy} "
    #     f"gravity friction: {gravity_friction}"
    # )
    # print("\r")
    print(
        f"Score: {Utils.blue_bright(str(g.score))}{' '*12}"
        f"{g.player.remaining_lives*Graphics.Sprites.PANDA}\r"
    )
    # print("\r")
    status = ""
    if g.state == Constants.PAUSED:
        status = (
            " " * 5
            + Graphics.Sprites.PAUSE_BUTTON
            + " GAME PAUSED"
            + Graphics.Sprites.PAUSE_BUTTON
        )
    if g.timer >= 10:
        print(
            f"Time left: {Utils.green_bright(str(round(g.timer,1)))}{' '*5}"
            f"Level: {g.current_level}{status}"
        )
    else:
        print(
            f"Time left: {Utils.red_bright(str(round(g.timer,1)))}{' '*5}"
            f"Level: {g.current_level}{status}"
        )
    print("\r")
    # print(
    #     f"Remaining traps: {g.current_board().available_traps} Scorers: "
    #     f"{g.current_board().treasures['scorers']['count']}/"
    #     f"{g.current_board().treasures['scorers']['placed']} "
    #     f"Timers: {g.current_board().treasures['timers']['count']}/"
    #     f"{g.current_board().treasures['timers']['placed']} 1UP: "
    #     f"{g.current_board().treasures['1UP']['count']}/"
    #     f"{g.current_board().treasures['1UP']['placed']}  Diamond: "
    #     f"{g.current_board().treasures['diamond']['count']}/"
    #     f"{g.current_board().treasures['diamond']['placed']}\r"
    # )
    g.display_board()


def gravity(g):
    # if g.player.pos[0] == g.current_board().size[1] - 1 or g.player.pos[0] == int(
    #     g.player.max_y
    # ):
    if (
        g.player.pos[0] == g.current_board().size[1] - 1
        or g.player.pos[0] == int(g.player.max_y)
    ) and g.player.dy != 0:
        g.player.dy = -g.player.dy
        if g.player.dy > 0:
            g.player.max_y += gravity_friction
    if (
        int(g.player.max_y) == g.current_board().size[1] - 1
        or g.player.pos[0] == g.player.max_y
    ):
        g.player.dy = 0

    if (
        g.player.last_y == g.player.pos[0]
        and g.player.dy < 0
        and g.player.pos[0] < g.current_board().size[1] - 1
        and not g.current_board()
        .item(g.player.pos[0] + 1, g.player.pos[1])
        .overlappable()
    ):
        g.player.dy = 0
        # g.player.max_y = g.player.pos[0]
    elif (
        g.player.last_y == g.player.pos[0]
        and g.player.dy == 0
        and g.player.pos[0] < g.current_board().size[1] - 1
        and g.current_board().item(g.player.pos[0] + 1, g.player.pos[1]).overlappable()
    ):
        g.player.dy = -1
    elif g.player.last_y == g.player.pos[0] and g.player.pos[0] == 0:
        g.player.dy = 0
    elif (
        g.player.last_y == g.player.pos[0]
        and g.player.dy > 0
        and not g.current_board()
        .item(g.player.pos[0] - 1, g.player.pos[1])
        .overlappable()
    ):
        # and g.player.pos[0] < g.current_board().size[1] - 1
        g.player.dy = -1
    g.player.last_y = g.player.pos[0]
    g.move_player(Constants.UP, g.player.dy)


def ui_threaded(g):
    while g.state != Constants.STOPPED:
        gravity(g)
        refresh_screen(g)
        g.actuate_projectiles(g.current_level)
        sleep(0.1)
        if g.state == Constants.RUNNING:
            g.timer -= 0.1
            for trap in g.current_board().get_immovables(type="trap."):
                # Only actually fire for traps that are on screen or close
                if (
                    trap.pos[1] > g.player.pos[1] + g.partial_display_viewport[1] + 5
                    or trap.pos[1] < g.player.pos[1] - g.partial_display_viewport[1] - 5
                ):
                    continue
                if trap.type == "trap.hfire":
                    trap.fire_timer -= 0.1
                    if trap.fire_timer <= 0.0:
                        proj = Projectile(
                            model=bg_color
                            + Utils.yellow_bright("\U00002301\U00002301")
                            + Graphics.Style.RESET_ALL,
                            name="zap",
                            range=5,
                            hit_model=bg_color
                            + Graphics.Sprites.HIGH_VOLTAGE
                            + Graphics.Style.RESET_ALL,
                            hit_callback=zap_callback,
                        )
                        proj.set_direction(trap.fdir)
                        trap_shoot_wave_obj.play()
                        if trap.fdir == Constants.RIGHT:
                            g.add_projectile(
                                g.current_level, proj, trap.pos[0], trap.pos[1] + 1
                            )
                        else:
                            g.add_projectile(
                                g.current_level, proj, trap.pos[0], trap.pos[1] - 1
                            )
                        trap.fire_timer = 1.5
                elif trap.type == "trap.vfire":
                    trap.fire_timer -= 0.1
                    if trap.fire_timer <= 0.0:
                        proj = Projectile(
                            model=bg_color
                            + Graphics.Sprites.BOMB
                            + Graphics.Style.RESET_ALL,
                            name="boom",
                            range=2,
                            hit_model=bg_color
                            + Graphics.Sprites.COLLISION
                            + Graphics.Style.RESET_ALL,
                            hit_callback=boom_callback,
                            is_aoe=True,
                            aoe_radius=1,
                        )
                        proj.set_direction(trap.fdir)
                        trap_shoot_wave_obj.play()
                        # Right now if the player sits on it, it does nothing.
                        g.add_projectile(
                            g.current_level, proj, trap.pos[0] - 1, trap.pos[1]
                        )
                        trap.fire_timer = 2.5
        if g.player.pos[0] == g.current_board().size[1] - 1:
            g.timer = 0.0
        if round(g.timer, 1) <= 0.0:
            g.player.model = bg_color + Graphics.Sprites.SKULL + Utils.Style.RESET_ALL
            g.player.remaining_lives -= 1
            refresh_screen(g)
        if (
            g.player.pos[0] == g.current_board().size[1] - 1 and g.player.dy == 0
        ) or round(g.timer, 1) <= 0.0:
            if g.player.remaining_lives == 0:
                g.stop()
                g.config("settings")["hiscores"].append([g.player.name, g.score])
                if len(g.config("settings")["hiscores"]) > 10:
                    g.config("settings")["hiscores"] = sorted(
                        g.config("settings")["hiscores"],
                        reverse=True,
                        key=lambda x: x[1],
                    )[0:10]
                raise SystemExit()
            else:
                g.current_board().clear_cell(g.player.pos[0], g.player.pos[1])
                potential_respawns = g.neighbors(2, g.player)
                g.player.model = (
                    bg_color + Graphics.Sprites.PANDA + Graphics.Style.RESET_ALL
                )
                for o in potential_respawns:
                    if o.type == "platform":
                        g.current_board().place_item(
                            g.player, g.current_board().size[1] - 10, o.pos[1]
                        )
                        g.player.max_y = g.current_board().size[1] - 11
                        g.player.dy = 0
                        g.timer = 30 + 10 * g.player.remaining_lives
                        break
        if len(g.obj_stack) > 0:
            new_stack = []
            for o in g.obj_stack:
                if isinstance(
                    g.current_board().item(o.pos[0], o.pos[1]), BoardItemVoid
                ):
                    g.current_board().place_item(o, o.pos[0], o.pos[1])
                    sprouted_trees = g.current_board().get_immovables(
                        type="sprouted_tree"
                    )
                    # Some times the game hangs and I wonder if it's not coming from
                    # here. I'm trying to put a hard stop here.
                    hard_stop = 0
                    while (
                        len(g.current_board().get_immovables(type="sprouted_tree")) > 2
                        and hard_stop < 20
                    ):
                        goner = sprouted_trees[0]
                        for i in sprouted_trees:
                            if i.age < goner.age:
                                goner = i
                        g.current_board().clear_cell(goner.pos[0], goner.pos[1])
                        hard_stop += 1
                else:
                    new_stack.append(o)
            g.obj_stack = new_stack
        if g.player.inventory.size() > 0:
            for iname in g.player.inventory.items_name():
                item = g.player.inventory.get_item(iname)
                if item.type == "treasure.scorers":
                    g.score += int(item.value)
                elif item.type == "treasure.timers":
                    g.timer += int(item.value)
                elif item.type == "treasure.diamond":
                    g.timer += item.value
                    g.score += int(item.value)
                elif item.type == "treasure.1UP":
                    g.player.remaining_lives += 1
            g.player.inventory.empty()


def change_level(params):
    game = params[0]
    board = Board(
        size=[250, 30],
        ui_borders="",
        ui_board_void_cell=bg_color + "  " + Graphics.Style.RESET_ALL,
        player_starting_position=[25, 0],
        DISPLAY_SIZE_WARNINGS=False,
    )
    board.ui_border_bottom = Graphics.Sprites.RADIOACTIVE + " "
    board.sprouted_count = 0
    # Let's use a nice curve to increase the trap number.
    board.available_traps = int(10 + 10 * g.current_level * 0.2)
    board.max_traps_number = board.available_traps
    for i in range(0, board.size[0]):
        board.place_item(
            Wall(model=block_color() + "  " + Utils.Style.RESET_ALL, type="platform"),
            board.size[1] - 1,
            i,
        )
    generate_level(game, board)
    game.score += 50 * game.current_level
    new_level = game.current_level + 1
    game.add_board(new_level, board)
    game.change_level(new_level)
    game.move_player(Constants.RIGHT, 3)
    game.player.last_y = game.player.pos[0]
    game.player.last_x = game.player.pos[1]
    g.player.max_y = g.player.pos[0]
    g.player.dy = gravity_speed
    g.obj_stack = []


def make_platform(b, row, column):
    psize = random.randint(2, 10)
    plateform = []
    tmp_game = Game()
    # Only because Game needs it, we don't care.
    tmp_game.player = Player()
    tmp_game.add_board(0, b)
    tmp_game.change_level(0)
    # print(
    #     f"[d] make_platform at {row}, {column}, psize is {psize} column will be "
    #     f"between {column} and {column + psize + 1}"
    # )
    get_up = 0
    # for i in range(column, column + psize + 1):
    for i in range(column - psize - 1, column):
        if i >= b.size[0]:
            break
        if not isinstance(b.item(row, i), BoardItemVoid):
            break
        if i in b.visited_columns:
            break
        # Check if we have other platforms around.
        # If yes moving the platform up.
        if get_up < 3:
            for e in tmp_game.neighbors(2, Door(pos=[row, i])):
                if e.type == "ground":
                    get_up = 3
                    break
        if get_up < 4:
            for e in tmp_game.neighbors(1, Door(pos=[row, i])):
                if e.type == "ground":
                    get_up = 4
                    break
        m = block_color() + "  " + Utils.Style.RESET_ALL
        plateform.append([Wall(model=m, type="platform"), row, i])
    for i in plateform:
        b.place_item(i[0], i[1] - get_up, i[2])
        if random.choice([True, False]):
            generate_treasure(b, i[1] - get_up - 1, i[2])
        else:
            generate_trap(b, i[1] - get_up - 1, i[2])
        b.visited_columns.append(i[2])
    # # And because we love platforms, let's add a layer of them
    # if len(plateform) > 0 and random.randint(0, 100) >= 80:
    #     rel = random.choice(plateform)
    #     make_platform(b, rel[1] - get_up - random.randint(2, 4), rel[2])


def generate_treasure(b, row, column):
    t = random.choice(list(b.treasures.keys()))
    if (
        random.randint(0, 100) >= 100 - b.treasures[t]["rate"]
        and b.treasures[t]["count"] > 0
    ):
        # The value of each treasure object is used differently.
        if t == "scorers":
            b.place_item(
                Treasure(
                    model=bg_color
                    + Graphics.Sprites.TANABATA_TREE
                    + Graphics.Style.RESET_ALL,
                    value=25,
                    type="treasure.scorers",
                ),
                row,
                column,
            )
        elif t == "timers":
            b.place_item(
                Treasure(
                    model=bg_color
                    + Graphics.Sprites.HOURGLASS_NOT_DONE
                    + Graphics.Style.RESET_ALL,
                    value=15,
                    type="treasure.timers",
                ),
                row,
                column,
            )
        elif t == "diamond":
            b.place_item(
                Treasure(
                    model=bg_color
                    + Graphics.Sprites.GEM_STONE
                    + Graphics.Style.RESET_ALL,
                    value=30,
                    type="treasure.diamond",
                ),
                row,
                column,
            )
        elif t == "1UP":
            b.place_item(
                Treasure(
                    model=bg_color
                    + Graphics.Sprites.HEART_WITH_RIBBON
                    + Graphics.Style.RESET_ALL,
                    value=30,
                    type="treasure.1UP",
                ),
                row,
                column,
            )
        b.treasures[t]["count"] -= 1
        b.treasures[t]["placed"] += 1


def generate_trap(b, row, column):
    # Here we just take a chance and put a trap here.
    # but we should actually explore the rest of the column for other suitable place
    if b.available_traps > 0:
        chance = int(b.max_traps_number / b.size[0] * 100)
        if random.randint(0, 100) >= 100 - chance:
            if random.choice([True, False]):
                trap = Wall(
                    model=bg_color
                    + traps_color
                    + Graphics.Blocks.QUADRANT_UPPER_LEFT_AND_LOWER_RIGHT
                    + Graphics.Blocks.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT
                    + Graphics.Style.RESET_ALL,
                    type="trap.hfire",
                )
                trap.fire_timer = random.uniform(1.0, 4.0)
                b.place_item(trap, row, column)
                if isinstance(b.item(row, column - 1), BoardItemVoid):
                    trap.fdir = Constants.LEFT
                else:
                    trap.fdir = Constants.RIGHT
            else:
                trap = Wall(
                    model=bg_color
                    + Utils.red_bright(
                        Graphics.Blocks.QUADRANT_UPPER_RIGHT_AND_LOWER_LEFT_AND_LOWER_RIGHT  # noqa E501
                        + Graphics.Blocks.QUADRANT_UPPER_LEFT_AND_LOWER_LEFT_AND_LOWER_RIGHT  # noqa E501
                    )
                    + Graphics.Style.RESET_ALL,
                    type="trap.vfire",
                )
                trap.fire_timer = random.uniform(2.0, 6.0)
                b.place_item(trap, row, column)
                trap.fdir = Constants.UP
            b.available_traps -= 1


def generate_level(g, b):
    # When we get the map, the last row is full of blocks
    last_alt = b.size[1] - 1
    gap = 0
    gap_threshold = 2
    b.visited_columns = []
    # We keep a count of the treasures we can put on the map as well as the rate we
    # can put them on (in percent). There is no possibility that we will end up with
    # more items, but there is a small possibility that we end up with less
    b.treasures = {
        "timers": {
            "count": int(math.log(g.current_level + 1)),
            "rate": 10,
            "placed": 0,
        },
        "scorers": {
            "count": 1 + int(math.log(g.current_level + 1)),
            "rate": 10,
            "placed": 0,
        },
        "1UP": {"count": 1, "rate": int(math.log(g.current_level + 1)), "placed": 0},
        "diamond": {"count": 1, "rate": 2, "placed": 0},
    }
    # We go through all the column of the map.
    for x in range(5, b.size[0]):
        # print(f"[d] generate level x={x}")
        # We have 50% chance of putting an obstacle.
        if random.choice([True, False]):
            if gap > gap_threshold:
                for k in range(x - gap, x):
                    b.clear_cell(b.size[1] - 1, k)
            alt = random.randint(last_alt - 2, b.size[1] - 1)
            last_alt = alt
            y = 0
            for y in range(alt + 1, b.size[1] - 1):
                # print(f"[d] generate level y={y}")
                b.place_item(
                    Wall(
                        model=block_color() + "  " + Utils.Style.RESET_ALL,
                        type="ground",
                    ),
                    y,
                    x,
                )
                # generate_treasure(b, y - 1, x)
                # For the fun of it and also to break monotony we have 20% of chance
                # of placing a platform here (of random size). We'll put treasures on
                # them later.
                if random.randint(0, 100) >= 80:
                    make_platform(b, last_alt - random.randint(2, 3), x)

            # if y < b.size[1] - 1:
            #     generate_trap(b, alt, x)
            # Just to break monotony, we have 33% chance of putting a cloud
            # in the background
            if random.randint(0, 100) >= 66:
                b.place_item(
                    Door(model=bg_color + "\U00002601 " + Utils.Style.RESET_ALL),
                    alt - 8 + random.randint(-2, 2),
                    x,
                )
            gap = 0
        else:
            # If we didn't put an obstacle, we keep track of the gap we're leaving.
            # When the gap is spreading over a threshold, we have 50% chance of
            # emptying it (we make a pit)
            gap += 1
    b.place_item(
        GenericActionableStructure(
            model=bg_color + Graphics.Sprites.CYCLONE + Utils.Style.RESET_ALL,
            type="exit",
            action=change_level,
            action_parameters=[g],
        ),
        last_alt - 1,
        b.size[0] - 1,
    )
    # The map is done, let's add treasures and traps.
    # we travel the map once again and look for openings
    idx = 0
    while b.available_traps > 0 or idx < 10:
        for col in range(5, b.size[0]):
            if random.choice([True, False]):
                candidates = []
                for row in range(0, b.size[1]):
                    item = b.item(row, col)
                    # We only put treasures and traps on the ground
                    if not isinstance(item, BoardItemVoid) and item.type == "ground":
                        # We want at least 2 free cells in all directions (except down)
                        free_cells = [
                            (row - 1, col),
                            (row - 2, col),
                            (row - 1, col - 1),
                            (row - 1, col - 2),
                            (row - 2, col - 1),
                            (row - 2, col - 2),
                            (row - 1, col + 1),
                            (row - 1, col + 2),
                            (row - 2, col + 1),
                            (row - 2, col + 2),
                        ]
                        good_candidate = True
                        for coord in free_cells:
                            if coord[0] >= b.size[1] or coord[1] >= b.size[0]:
                                continue
                            cell = b.item(coord[0], coord[1])
                            if not isinstance(cell, BoardItemVoid):
                                good_candidate = False
                                break
                        if good_candidate:
                            candidates.append(item)
                for c in candidates:
                    generate_trap(b, c.pos[0], c.pos[1])
        idx += 1
    idx = 0
    while True:
        for col in range(5, b.size[0]):
            if random.choice([True, False]):
                candidates = []
                for row in range(0, b.size[1]):
                    item = b.item(row, col)
                    # We only put treasures and traps on the ground
                    if not isinstance(item, BoardItemVoid) and item.type == "ground":
                        # We want at least 2 free cells in all directions (except down)
                        free_cells = [
                            (row - 1, col),
                            (row - 2, col),
                            (row - 1, col - 1),
                            (row - 1, col - 2),
                            (row - 2, col - 1),
                            (row - 2, col - 2),
                            (row - 1, col + 1),
                            (row - 1, col + 2),
                            (row - 2, col + 1),
                            (row - 2, col + 2),
                        ]
                        good_candidate = True
                        for coord in free_cells:
                            if coord[0] >= b.size[1] or coord[1] >= b.size[0]:
                                continue
                            cell = b.item(coord[0], coord[1])
                            if not isinstance(cell, BoardItemVoid):
                                good_candidate = False
                                break
                        if good_candidate:
                            candidates.append(item)
                for c in candidates:
                    generate_trap(b, c.pos[0], c.pos[1])
        idx += 1
        if b.treasures["scorers"]["count"] <= 0 and b.treasures["timers"]["count"] <= 0:
            break
        if idx == 10:
            break


def sprout(p, *args):
    # if p.parent is None:
    #     return None
    if p is not None:
        o = Wall(
            model=bg_color + Graphics.Sprites.DECIDUOUS_TREE + Utils.Style.RESET_ALL,
            type="sprouted_trees",
        )
        o.pos = p.pos
        # Projectile is own by the Board by default.
        # Board is owned by the Game object.
        if p.parent is not None and p.parent.parent is not None:
            p.parent.sprouted_count += 1
            o.age = p.parent.sprouted_count
            p.parent.parent.obj_stack.append(o)


def zap_callback(p, collidings, *args):
    zap_wave_obj.play()
    if len(collidings) > 0:
        if g.player in collidings:
            g.timer -= 5.0


def boom_callback(p, collidings, *args):
    boom_wave_obj.play()
    if len(collidings) > 0:
        if g.player in collidings:
            g.timer -= 5.0


def adapt_resolution(g):
    global term, term_res
    if term.width >= 140:
        term_res = 140
    else:
        term_res = 80
    g.partial_display_viewport = [10, int(term_res / 4)]


# We need the hac-game-lib v1.1+
if Constants.HAC_GAME_LIB_VERSION < "1.1.0":
    Utils.print_white_on_red(
        "Super Panda Run EX require the hac-game-lib version 1.1.0 or greater."
        f" Version installed is {Constants.HAC_GAME_LIB_VERSION}"
    )
    raise SystemExit()

g = Game()
g.enable_partial_display = True
g.partial_display_viewport = [10, int(term_res / 4)]
g.current_level = 0
g.player = Player(model=bg_color + Graphics.Sprites.PANDA + Graphics.Style.RESET_ALL)
g.player.name = "Zigomar"
g.player.max_y = g.player.pos[0]
g.player.dy = gravity_speed
g.player.last_y = g.player.pos[0]
g.player.last_x = g.player.pos[1]
g.timer = 60
g.score = 0
g.obj_stack = []
g.pause()

if os.path.exists("settings-suparex.json"):
    g.load_config("settings-suparex.json", "settings")
    if g.config("settings")["player_name"] is not None:
        g.player.name = g.config("settings")["player_name"]
else:
    g.create_config("settings")
    g.config("settings")["player_name"] = g.player.name
    g.config("settings")["hiscores"] = []
    names = [
        "Marie Curie",
        "Jane Goodall",
        "Ada Lovelace",
        "Rosalind Franklin",
        "Dorothy Hodgkin",
        "Jocelyn Bell Burnell",
        "Chien-Shiung Wu",
        "Irène Joliot-Curie",
        "Vera Rubin",
        "Grace Hopper",
        "Katherine Johnson",
        "Emmy Noether",
        "Sally Ride",
        "Sophie Germain",
    ]
    # fill the scoreboard with some names that I would have love to meet.
    # Let's use random numbers to insult no one's memory ;)
    i = 0
    while i < 10:
        g.config("settings")["hiscores"].append(
            [random.choice(names), random.randint(10, 600)]
        )
        i += 1

while current_state != "eop":
    if current_state == "title":
        adapt_resolution(g)
        load_logo()
        title_screen(g)
    elif current_state == "game":
        key = "None"
        g.start()
        _thread.start_new_thread(ui_threaded, (g,))
        while g.state != Constants.STOPPED:
            g.score += g.player.pos[1] - g.player.last_x
            if g.player.pos[1] - g.player.last_x > 0:
                # That is clearly where the difficulty should be:
                # the smaller the recuperation time, the bigger the score should be
                # awarded
                # 0.2 is hard
                # The timer automatically refill but with less and less time the further
                # the player goes.
                g.timer += 1 / g.current_level
                # On the other end, the player gains more points the further he goes
                g.score += int(
                    (g.player.pos[1] - g.player.last_x)
                    - 1 / (g.player.pos[1] - g.player.last_x)
                )
            g.player.last_x = g.player.pos[1]
            if key == Utils.key.LEFT:
                g.move_player(Constants.LEFT, 1)
            elif key == Utils.key.RIGHT:
                g.move_player(Constants.RIGHT, 1)
            # elif key == Utils.key.DOWN:
            #     gravity_friction -= 0.1
            # elif key == Utils.key.UP:
            #     gravity_friction += 0.1
            elif key == Utils.key.SPACE:
                if g.player.dy == 0 and len(g.neighbors(1, g.player)) > 0:
                    # Jump
                    # Start with sound
                    jump_wave_obj.play()
                    g.player.max_y = g.player.pos[0] - 3
                    g.player.dy = 1
            elif key == "X":
                g.stop()
                break
            elif key in "awsdzq":
                projectile = Projectile(
                    name="treeball",
                    direction=Constants.RIGHT,
                    range=2,
                    model=Utils.green_bright(bg_color + " *" + Utils.Style.RESET_ALL),
                    hit_model=bg_color
                    + Graphics.Sprites.DECIDUOUS_TREE
                    + Utils.Style.RESET_ALL,
                    hit_callback=sprout,
                )
                row = g.player.pos[0]
                column = g.player.pos[1] + 1
                if key == "w" or key == "z":
                    projectile.set_direction(Constants.UP)
                    row = g.player.pos[0] - 1
                    column = g.player.pos[1]
                elif key == "s":
                    projectile.set_direction(Constants.DOWN)
                    row = g.player.pos[0] + 1
                    column = g.player.pos[1]
                elif key == "a" or key == "q":
                    projectile.set_direction(Constants.LEFT)
                    row = g.player.pos[0]
                    column = g.player.pos[1] - 1
                hit_wave_obj.play()
                g.add_projectile(g.current_level, projectile, row, column)
                g.timer -= projectile.range
            elif key == "p":
                if g.state == Constants.RUNNING:
                    g.pause()
                else:
                    g.start()
            key = Utils.get_key()
        current_state = "title"

g.save_config("settings", "settings-suparex.json")
