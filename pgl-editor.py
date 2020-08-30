#!/usr/bin/env python3

import os
import uuid
from copy import deepcopy
from pygamelib import constants
from pygamelib import actuators
from pygamelib import engine
from pygamelib import board_items
from pygamelib.assets import graphics
from pygamelib import base
import pygamelib.gfx.core as gfx_core

# Global variables
is_modified = False
edit_mode = True
dbg_messages = []
info_messages = []
warn_messages = []
# TODO: migrate the settings to .pygamelib
base_config_dir = os.path.join(os.path.expanduser("~"), ".hac-game-lib")
config_dir = os.path.join(base_config_dir, "config")
editor_config_dir = os.path.join(config_dir, "editor")
default_map_dir = os.path.join(base_config_dir, "editor", "maps")
viewport_height = 10
viewport_width = 30


# Functions definition
def place_and_go(obj, x, y, direction):
    global is_modified
    global game
    global current_menu
    initial_position = game.player.pos
    game.move_player(direction, 1)
    if initial_position != game.player.pos:
        game.current_board().place_item(deepcopy(obj), x, y)
        is_modified = True
        if isinstance(obj, board_items.NPC) and isinstance(
            obj.actuator, actuators.PathFinder
        ):
            current_menu = "waypoint_edition"
        return game.current_board().item(x, y)


def clear_and_go(direction):
    global is_modified
    global game
    new_x = game.player.pos[0]
    new_y = game.player.pos[1]
    if direction == constants.DOWN:
        new_x += 1
    elif direction == constants.UP:
        new_x -= 1
    elif direction == constants.LEFT:
        new_y -= 1
    elif direction == constants.RIGHT:
        new_y += 1

    if (
        new_x < 0
        or new_y < 0
        or new_x > (game.current_board().size[1] - 1)
        or new_y > (game.current_board().size[0] - 1)
    ):
        base.Text.warn(
            f"Cannot remove anything at [{new_x},{new_y}] " "as it is out of bound."
        )
    else:
        game.current_board().clear_cell(new_x, new_y)
        game.move_player(direction, 1)
        is_modified = True


def switch_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    if edit_mode:
        game.update_menu_entry(
            "main",
            base.Text.white_bright("j/i/k/l"),
            base.Text.green_bright("Place")
            + " the current object and then move cursor Left/Up/Down/Right",
        )
        game.update_menu_entry(
            "main",
            base.Text.white_bright("0 to 9"),
            base.Text.green_bright("Select")
            + " an item in history to be the current item",
        )
    else:
        game.update_menu_entry(
            "main",
            base.Text.white_bright("j/i/k/l"),
            "Move cursor Left/Up/Down/Right and "
            + base.Text.red_bright("Delete")
            + " anything that was at destination.",
        )
        game.update_menu_entry(
            "main",
            base.Text.white_bright("0 to 9"),
            base.Text.red_bright("Remove") + " an item from history",
        )


def color_picker():
    global game
    game.clear_screen()
    print("Pick a form and color from the list:")
    game.display_menu("graphics_utils", constants.ORIENTATION_HORIZONTAL, 8)
    return str(input_digit("\n(Enter a number)> "))


def utf8_picker(category):
    global game
    nb_elts = int(game.terminal.width / 12)
    if len(game._menu[category]) / nb_elts > game.screen.height:
        idx_line = 0
        idx_col = 0
        offset = 0
        while True:
            game.clear_screen()
            print("Pick a glyph from the list:")
            while idx_line < game.screen.height - 5:
                idx_col = nb_elts * idx_line + offset
                if idx_col < 0:
                    idx_col = 0
                elif idx_col >= len(game._menu[category]):
                    break
                for k in range(idx_col, idx_col + nb_elts, 1):
                    if k >= len(game._menu[category]):
                        break
                    elt = game._menu[category][k]
                    print(
                        f"{' '*(4-len(elt['shortcut']))}{elt['shortcut']} - "
                        f"{elt['message']}",
                        end=" | ",
                    )
                print("")
                idx_line += 1
            key = input("(Enter a number or n/p for next/previous page)> ")
            if key == "n" and (idx_col + nb_elts) <= len(game._menu[category]):
                idx_line = 0
                offset = idx_col + nb_elts
            elif key == "p":
                offset -= nb_elts * idx_line
                if offset < 0:
                    offset = 0
                idx_line = 0
            elif key.isdigit() or key == "":
                return key
            else:
                idx_line = 0
    else:
        game.display_menu(category, constants.ORIENTATION_HORIZONTAL, nb_elts)
        return str(input_digit("\n(Enter a number)> "))


def model_picker():
    global game
    while True:
        game.clear_screen()
        print(
            "What kind of model do you want (you can edit that later)?\n"
            "1 - Colored squares and rectangles\n"
            "2 - Models (emojis)\n"
            "3 - Blocks\n"
            "4 - Box drawings\n"
            "5 - Geometric shapes\n"
            "6 - Set your own string of character(s)"
        )
        choice = str(engine.Game.get_key())
        if choice == "1":
            picked = game.get_menu_entry("graphics_utils", color_picker())
            if picked is not None:
                return picked["data"]
        elif choice == "2":
            picked = game.get_menu_entry(
                "graphics_models", utf8_picker("graphics_models")
            )
            if picked is not None:
                return picked["data"]
        elif choice == "3":
            picked = game.get_menu_entry(
                "graphics_blocks", utf8_picker("graphics_blocks")
            )
            if picked is not None:
                return picked["data"]
        elif choice == "4":
            picked = game.get_menu_entry(
                "graphics_box_drawings", utf8_picker("graphics_box_drawings")
            )
            if picked is not None:
                return picked["data"]
        elif choice == "5":
            picked = game.get_menu_entry(
                "graphics_geometric_shapes", utf8_picker("graphics_geometric_shapes")
            )
            if picked is not None:
                return picked["data"]
        elif choice == "6":
            return str(input("Enter your string now: "))


def to_history(object):
    global object_history
    if (
        len(object_history) <= 10
        and object not in object_history
        and not isinstance(object, board_items.BoardItemVoid)
    ):
        object_history.append(object)
    elif (
        len(object_history) > 10
        and object not in object_history
        and not isinstance(object, board_items.BoardItemVoid)
    ):
        del object_history[0]
        object_history.append(object)


def input_digit(msg):
    while True:
        result = input(msg)
        if result.isdigit() or result == "":
            return result


def create_wizard():
    global game
    key = ""
    while True:
        game.clear_screen()
        print(base.Text.green_bright("\t\tObject creation wizard"))
        print("What do you want to create: a NPC or a structure?")
        print("1 - NPC (Non Playable Character)")
        print("2 - Structure (Wall, Door, Treasure, Portal, Trees, etc.)")
        key = engine.Game.get_key()
        if key == "1" or key == "2":
            break
    if key == "1":
        game.clear_screen()
        print(
            base.Text.green_bright("\t\tObject creation wizard: ")
            + base.Text.cyan_bright("NPC")
        )
        new_object = board_items.NPC()
        print("First give a name to your NPC. Default value: " + new_object.name)
        r = str(input("(Enter name)> "))
        if len(r) > 0:
            new_object.name = r
        print(
            "Then give it a type. A type is important as it allows grouping.\n"
            "Type is a string. Default value: " + new_object.type
        )
        r = str(input("(Enter type)> "))
        if len(r) > 0:
            new_object.type = r
        print("Now we need a model. Default value: " + new_object.model)
        input('Hit "Enter" when you are ready to choose a model.')
        new_object.model = model_picker()
        game.clear_screen()
        print(
            base.Text.green_bright("\t\tObject creation wizard: ")
            + base.Text.cyan_bright("NPC")
            + f" - {new_object.model}"
        )
        print(
            "We now needs to go through some basic statistics. "
            "You can decide to go with default by simply hitting "
            'the "Enter" key.'
        )
        r = input_digit(
            f"Number of cell crossed in one turn. "
            f"Default: {new_object.step}(type: int) > "
        )
        if len(r) > 0:
            new_object.step = int(r)
        else:
            # If it's 0 it means it's going to be a static NPC so to prevent
            # python to pass some random pre-initialized default, we explicitly
            # set the Actuator to a static one
            new_object.actuator = actuators.RandomActuator(moveset=[])

        r = input_digit(
            f"Max HP (Health Points). " f"Default: {new_object.max_hp}(type: int) > "
        )
        if len(r) > 0:
            new_object.max_hp = int(r)
        new_object.hp = new_object.max_hp

        r = input_digit(
            f"Max MP (Mana Points). " f"Default: {new_object.max_mp}(type: int) > "
        )
        if len(r) > 0:
            new_object.max_mp = int(r)
        new_object.mp = new_object.max_mp

        r = input_digit(
            f"Remaining lives (it is advised to set that to 1 for a "
            f"standard NPC). "
            f"Default: {new_object.remaining_lives}(type: int) > "
        )
        if len(r) > 0:
            new_object.remaining_lives = int(r)

        r = input_digit(
            f"AP (Attack Power). " f"Default: {new_object.attack_power}(type: int) > "
        )
        if len(r) > 0:
            new_object.attack_power = int(r)

        r = input_digit(
            f"DP (Defense Power). " f"Default: {new_object.defense_power}(type: int) > "
        )
        if len(r) > 0:
            new_object.defense_power = int(r)

        r = input_digit(f"Strength. Default: {new_object.strength}(type: int) > ")
        if len(r) > 0:
            new_object.strength = int(r)

        r = input_digit(
            f"Intelligence. Default: {new_object.intelligence}(type: int) > "
        )
        if len(r) > 0:
            new_object.intelligence = int(r)

        r = input_digit(f"Agility. Default: {new_object.agility}(type: int) > ")
        if len(r) > 0:
            new_object.agility = int(r)

        game.clear_screen()
        print(
            "We now need to give some life to that NPC. "
            "What kind of movement should it have:"
        )
        print("1 - Randomly chosen from a preset of directions")
        print("2 - Following a predetermined path")
        print("3 - Following a predetermined path back and forth")
        print(
            "4 - Automatically finding it's way from one point to another (no"
            " pre-determined path, you will set the points on the map)."
        )
        r = engine.Game.get_key()
        if r == "1":
            new_object.actuator = actuators.RandomActuator(moveset=[])
            print(
                "Random it is! Now choose from which preset "
                "of movements should we give it:"
            )
            print("1 - UP,DOWN,LEFT, RIGHT")
            print("2 - UP,DOWN")
            print("3 - LEFT, RIGHT")
            print("4 - UP,DOWN,LEFT, RIGHT + all DIAGONALES")
            print(
                "5 - DIAGONALES (DIAG UP LEFT, DIAG UP RIGHT, etc.) "
                "but NO straight UP, DOWN, LEFT and RIGHT"
            )
            print("6 - No movement")
            r = engine.Game.get_key()
            if r == "1":
                new_object.actuator.moveset = [
                    constants.UP,
                    constants.DOWN,
                    constants.LEFT,
                    constants.RIGHT,
                ]
            elif r == "2":
                new_object.actuator.moveset = [constants.UP, constants.DOWN]
            elif r == "3":
                new_object.actuator.moveset = [constants.RIGHT, constants.LEFT]
            elif r == "4":
                new_object.actuator.moveset = [
                    constants.UP,
                    constants.DOWN,
                    constants.LEFT,
                    constants.RIGHT,
                    constants.DLDOWN,
                    constants.DLUP,
                    constants.DRDOWN,
                    constants.DRUP,
                ]
            elif r == "5":
                new_object.actuator.moveset = [
                    constants.DLDOWN,
                    constants.DLUP,
                    constants.DRDOWN,
                    constants.DRUP,
                ]
            elif r == "6":
                new_object.actuator.moveset = []
            else:
                base.Text.warn(
                    f'"{r}" is not a valid choice. Movement set is now empty.'
                )
                new_object.actuator.moveset = []
        elif r == "2" or r == "3":
            if r == "2":
                new_object.actuator = actuators.PathActuator(path=[])
            elif r == "3":
                new_object.actuator = actuators.PatrolActuator(path=[])
            print("Great, so what path this NPC should take:")
            print("1 - UP/DOWN patrol")
            print("2 - DOWN/UP patrol")
            print("3 - LEFT/RIGHT patrol")
            print("4 - RIGHT/LEFT patrol")
            print("5 - Circle patrol: LEFT, DOWN, RIGHT, UP")
            print("6 - Circle patrol: LEFT, UP, RIGHT, DOWN")
            print("7 - Circle patrol: RIGHT, DOWN, LEFT, UP")
            print("8 - Circle patrol: RIGHT, UP, LEFT, DOWN")
            print("9 - Write your own path")
            r = engine.Game.get_key()
            if r == "1":
                print(
                    "How many steps should the NPC go in one direction "
                    "before turning back ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += ([constants.UP for i in range(0, r, 1)],)
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
            elif r == "2":
                print(
                    "How many steps should the NPC go in one "
                    "direction before turning back ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
            elif r == "3":
                print(
                    "How many steps should the NPC go in one "
                    "direction before turning back ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
            elif r == "3":
                print(
                    "How many steps should the NPC go in one direction "
                    "before turning back ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
            elif r == "4":
                print(
                    "How many steps should the NPC go in one "
                    "direction before turning back ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
            elif r == "5":
                print(
                    "How many steps should the NPC go in EACH "
                    "direction before changing ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
            elif r == "6":
                print(
                    "How many steps should the NPC go in EACH "
                    "direction before changing ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
            elif r == "7":
                print(
                    "How many steps should the NPC go in EACH "
                    "direction before changing ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
            elif r == "8":
                print(
                    "How many steps should the NPC go in EACH direction "
                    "before changing ?"
                )
                r = int(input_digit("(please enter an integer)> "))
                new_object.actuator.path += [constants.RIGHT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
                new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
            elif r == "9":
                print(
                    "Write your own path using only words from this list: "
                    "UP, DOWN, LEFT, RIGHT, DLDOWN, DLUP, DRDOWN, DRUP."
                )
                print("Each direction has to be separated by a coma.")
                r = str(input("Write your path: ")).upper()
                new_object.actuator.path = r.split(",")
            else:
                base.Text.warn(f'"{r}" is not a valid choice. Path is now empty.')
                new_object.actuator.path = []
        elif r == "4":
            new_object.actuator = actuators.PathFinder(
                parent=new_object, circle_waypoints=True
            )
            print(
                "Do you want the NPC to go through your way points once and stop or"
                " to cycle through all of them infinitely ?"
            )
            print("1 - Cycle once")
            print("2 - Cycle infinitely (default value)")
            r = engine.Game.get_key()
            if r == "1":
                new_object.actuator.circle_waypoints = False
        return new_object
    elif key == "2":
        while True:
            game.clear_screen()
            print(
                base.Text.green_bright("\t\tObject creation wizard: ")
                + base.Text.magenta_bright("Structure")
            )
            print("What kind of structure do you want to create:")
            print(
                "1 - A wall like structure (an object that cannot be picked-up "
                "and is not overlappable). Ex: walls, trees, non moving "
                "elephant (try to go through an elephant or to pick it up "
                "in your backpack...)"
            )
            print("2 - A door (player and/or NPC can go through)")
            print(
                "3 - A treasure (can be picked up, take space in the "
                "inventory, give points to the player)"
            )
            print(
                "4 - A generic object (you can set the properties to "
                "make it pickable or overlappable)"
            )
            print(
                "5 - A generic actionable object (to make portals, heart "
                "to replenish life, etc.)"
            )
            key = engine.Game.get_key()
            new_object = None
            if key == "1":
                new_object = board_items.Wall()
                new_object.name = str(uuid.uuid1())
                new_object.model = model_picker()
                break
            elif key == "2":
                new_object = board_items.Door()
                new_object.name = str(uuid.uuid1())
                new_object.model = model_picker()
                break
            elif key == "3":
                new_object = board_items.Treasure()
                print(
                    "First give a name to your Treasure. Default value: "
                    + new_object.name
                )
                r = str(input("(Enter name)> "))
                if len(r) > 0:
                    new_object.name = r
                print(
                    "Then give it a type. A type is important as it allows "
                    "grouping (in this case probably in the inventory).\n"
                    "Type is a string. Default value: " + new_object.type
                )
                r = str(input("(Enter type)> "))
                if len(r) > 0:
                    new_object.type = r
                print("Now we need a model. Default value: " + new_object.model)
                input('Hit "Enter" when you are ready to choose a model.')
                new_object.model = model_picker()
                break
            elif key == "4" or key == "5":
                if key == "4":
                    new_object = board_items.GenericStructure()
                else:
                    new_object = board_items.GenericActionableStructure()
                new_object.set_overlappable(False)
                new_object.set_pickable(False)
                print(
                    "First give a name to your structure. Default value: "
                    + new_object.name
                )
                r = str(input("(Enter name)> "))
                if len(r) > 0:
                    new_object.name = r
                print(
                    "Then give it a type. \nType is a string. Default value: "
                    + new_object.type
                )
                r = str(input("(Enter type)> "))
                if len(r) > 0:
                    new_object.type = r
                print("Now we need a model. Default value: " + new_object.model)
                input('Hit "Enter" when you are ready to choose a model.')
                new_object.model = model_picker()
                print(
                    "Is this object pickable? (can it be picked up " "by the player)?"
                )
                print("0 - No")
                print("1 - Yes")
                r = engine.Game.get_key()
                if r == "1":
                    new_object.set_pickable(True)
                print(
                    "Is this object overlappable? (can it be walked " "over by player?"
                )
                print("0 - No")
                print("1 - Yes")
                r = engine.Game.get_key()
                if r == "1":
                    new_object.set_overlappable(True)
                break

        return new_object

    # Placeholder
    return board_items.BoardItemVoid()


def save_current_board():
    global game
    global object_history
    global is_modified
    game.object_library = object_history
    game.save_board(1, current_file)
    is_modified = False


def create_board_wizard():
    global game
    global is_modified
    global current_file
    global default_map_dir
    game.clear_screen()
    print(base.Text.blue_bright("\t\tNew board"))
    print("First we need some information on your new board:")
    name, width, height = None, None, None
    if game.config("settings")["last_used_board_parameters"]["name"] is not None:
        name = game.config("settings")["last_used_board_parameters"]["name"]
    else:
        name = "New Board"
    name = str(input(f"Name (default: {name}): ")) or name
    if game.config("settings")["last_used_board_parameters"]["width"] is not None:
        width = game.config("settings")["last_used_board_parameters"]["width"]
    else:
        width = 20
    width = int(
        input_digit(f"Width (in number of cells) (default: {width}): ") or width
    )
    if game.config("settings")["last_used_board_parameters"]["height"] is not None:
        height = game.config("settings")["last_used_board_parameters"]["height"]
    else:
        height = 20
    height = int(
        input_digit(f"Height (in number of cells) (default: {height}): ") or height
    )
    print(
        "\nFinally, we need to know how to configure your new board regarding the "
        "items that you are going to put inside. Do you plan to use a mix of emojis "
        "(that displays on 2 characters in the terminal) and regular single characters?"
        "Or do you plan to use only squared items (emojis and colored squares)?"
    )
    use_square = input_digit(
        "0 - Mixed: emojis, rectangles and any other characters\n"
        "1 - Squares only: emojis and colored square (or any double characters)\n"
        "Your choice: "
    )
    ui_borders = graphics.WHITE_SQUARE
    ui_board_void_cell = graphics.BLACK_SQUARE
    use_complex_item = False
    if use_square == "0":
        ui_borders = graphics.WHITE_RECT
        ui_board_void_cell = graphics.BLACK_RECT
        base.Text.warn(
            "You have to pay attention to the items movements, you probably"
            " want to make sure the items move faster horizontally than vertically."
        )
        cursor = gfx_core.Sprite(
            sprixels=[[gfx_core.Sprixel("["), gfx_core.Sprixel("]")]]
        )
        game.player = board_items.ComplexPlayer(sprite=cursor)
        use_complex_item = True
        input("\n\nPress ENTER to continue.")
    game.add_board(
        1,
        engine.Board(
            name=name,
            size=[width, height],
            ui_borders=ui_borders,
            ui_board_void_cell=ui_board_void_cell,
        ),
    )
    game.get_board(1).use_complex_item = use_complex_item
    is_modified = True
    current_file = os.path.join(default_map_dir, name.replace(" ", "_") + ".json")
    game.config("settings")["last_used_board_parameters"] = {
        "name": name,
        "width": width,
        "height": height,
    }
    if game.get_board(1).size[0] > 20 or game.get_board(1).size[1] > 20:
        game.enable_partial_display = True
        game.partial_display_viewport = [10, 10]


def first_use():
    global config_dir
    global editor_config_dir
    global base_config_dir
    global default_map_dir
    global game
    print(base.Text.yellow_bright("Configuration wizard (fresh install or update)"))
    print(
        "You may see that wizard because hgl-editor was updated with new settings.\n"
        "Please check that everything is fine (your previous values are showned as "
        "default values)\n"
    )
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(os.path.join(base_config_dir, "editor", "maps")):
        os.makedirs(os.path.join(base_config_dir, "editor", "maps"))
    if not os.path.exists(editor_config_dir):
        os.makedirs(editor_config_dir)
    print(
        "We need to set up the default directory where we are going to save maps.",
        f"Default is {default_map_dir}",
    )
    new_default = str(input("Default maps directory: "))
    while (
        not os.path.exists(new_default)
        or not os.path.isdir(new_default)
        or not os.path.isabs(new_default)
    ) and new_default != "":
        print(base.Text.red("The path to directory needs to exists and be absolute."))
        new_default = str(input("Default maps directory: "))
    if new_default != "":
        default_map_dir = new_default
    if not os.path.exists(os.path.join(config_dir, "directories.json")):
        with open(os.path.join(config_dir, "directories.json"), "w") as fp:
            fp.write(f'["{default_map_dir}","pgl-maps","hac-maps","maps"]')
    if not os.path.exists(os.path.join(editor_config_dir, "settings.json")):
        game.create_config("settings")
        game.config("settings")["directories"] = [
            default_map_dir,
            "pgl-maps",
            "hac-maps",
            "maps",
        ]
        game.config("settings")["config_file_version"] = 10100
        game.config("settings")["enable_partial_display"] = True
        game.config("settings")["partial_display_viewport"] = [10, 30]
        game.config("settings")["menu_mode"] = "full"
        game.config("settings")["last_used_board_parameters"] = {
            "name": None,
            "width": None,
            "height": None,
        }
        game.config("settings")["object_library"] = []


# Main program
game = engine.Game()
current_file = ""
game.player = board_items.Player(model="[]")

key = "None"
current_object = board_items.BoardItemVoid(model="None")
current_object_instance = board_items.BoardItemVoid(model="None")
object_history = []
viewport_board = engine.Board(
    name="Viewport testing board",
    size=[viewport_width * 2, viewport_height * 2],
    ui_borders=graphics.GREEN_SQUARE,
    ui_board_void_cell=graphics.RED_SQUARE,
)
game.add_board(2, viewport_board)
current_menu = "main"
while True:
    game.clear_screen()
    print(base.Text.cyan_bright("PYGAMELIB - EDITOR v" + constants.PYGAMELIB_VERSION))
    # Create config_dir if not exist and populate it with a directories.json file.
    if (
        not os.path.exists(config_dir)
        or not os.path.isdir(config_dir)
        or not os.path.exists(base_config_dir)
        or not os.path.isdir(base_config_dir)
        or not os.path.isdir(editor_config_dir)
        or not os.path.exists(os.path.join(editor_config_dir, "settings.json"))
    ):
        first_use()
    else:
        game.load_config(os.path.join(editor_config_dir, "settings.json"), "settings")
        viewport_height = game.config("settings")["partial_display_viewport"][0]
        viewport_width = game.config("settings")["partial_display_viewport"][1]
        viewport_board.size = [viewport_width * 2, viewport_height * 2]
        viewport_board.init_board()
        # The objects library is stored as a list of references. We need to convert that
        # before using the objects.
        objlib = []
        for ref in game.config("settings")["object_library"]:
            objlib.append(engine.Game._ref2obj(ref))
        game.config("settings")["object_library"] = objlib
    print("Looking for existing maps in selected directories...", end="")
    default_map_dir = None
    hmaps = []
    for directory in game.config("settings")["directories"]:
        # files = [f'{directory}/{f}' for f in os.listdir(directory)]
        # hmaps += files
        test_dir = os.path.join(base_config_dir, directory)
        if os.path.exists(test_dir):
            directory = test_dir
            # Utils.debug(f"Setting directory to: {directory}")
        if os.path.exists(directory):
            if default_map_dir is None:
                default_map_dir = directory
            for f in os.listdir(directory):
                if os.path.isabs(f):
                    hmaps.append(f)
                else:
                    if os.path.exists(f):
                        hmaps.append(f)
                    elif os.path.exists(os.path.join(directory, f)):
                        hmaps.append(os.path.join(directory, f))
    if len(hmaps) > 0:
        print(base.Text.green("OK"))
    else:
        print(base.Text.red_bright("KO"))

    if len(hmaps) > 0:
        map_num = 0
        game.add_menu_entry("boards_list", None, "Choose a map to edit")
        for m in hmaps:
            print(f"{map_num} - edit {m}")
            game.add_menu_entry("boards_list", str(map_num), f"edit {m}", f"{m}")
            map_num += 1
        game.add_menu_entry("boards_list", "B", "Go Back to main menu")
    else:
        print("No pre-existing map found.")
    print("n - create a new map")
    print("q - Quit the editor")
    choice = input("Enter your choice (and hit ENTER): ")
    if choice == "q":
        print("Good Bye!")
        exit()
    elif choice == "n":
        create_board_wizard()
        break
    elif choice.isdigit() and int(choice) < len(hmaps):
        current_file = hmaps[int(choice)]
        board = game.load_board(hmaps[int(choice)], 1)
        if board.size[0] >= viewport_height or board.size[1] >= viewport_width:
            game.enable_partial_display = True
            game.partial_display_viewport = [viewport_height, viewport_width]
        else:
            game.enable_partial_display = False
        break

game.change_level(1)

if len(game.object_library) > 0:
    object_history += game.object_library
    for i in game.object_library:
        if i not in game.config("settings")["object_library"]:
            game.config("settings")["object_library"].append(i)

# Build the menus
i = 0
# WARNING: This might break!!!!
for sp in dir(graphics):
    if sp.endswith("_SQUARE") or sp.endswith("_RECT"):
        game.add_menu_entry(
            "graphics_utils",
            str(i),
            '"' + getattr(graphics, sp) + '"',
            getattr(graphics, sp),
        )
        i += 1

# WARNING: This might/will break!!!!
i = 0
for sp in dir(graphics.Models):
    if not sp.startswith("__"):
        game.add_menu_entry(
            "graphics_models",
            str(i),
            getattr(graphics.Models, sp),
            getattr(graphics.Models, sp),
        )
        i += 1
i = 0
for sp in dir(graphics.Blocks):
    if not sp.startswith("__"):
        game.add_menu_entry(
            "graphics_blocks",
            str(i),
            getattr(graphics.Blocks, sp),
            getattr(graphics.Blocks, sp),
        )
        i += 1
i = 0
for sp in dir(graphics.BoxDrawings):
    if not sp.startswith("__"):
        game.add_menu_entry(
            "graphics_box_drawings",
            str(i),
            getattr(graphics.BoxDrawings, sp),
            getattr(graphics.BoxDrawings, sp),
        )
        i += 1
i = 0
for sp in dir(graphics.GeometricShapes):
    if not sp.startswith("__"):
        game.add_menu_entry(
            "graphics_geometric_shapes",
            str(i),
            getattr(graphics.GeometricShapes, sp),
            getattr(graphics.GeometricShapes, sp),
        )
        i += 1
game.add_menu_entry(
    "main", None, "\n=== Menu (" + game.config("settings")["menu_mode"] + ") ==="
)
game.add_menu_entry(
    "main", base.Text.white_bright("Space"), "Switch between edit/delete mode"
)
game.add_menu_entry(
    "main",
    base.Text.white_bright("0 to 9"),
    base.Text.green_bright("Select") + " an item in history to be the current item",
)
game.add_menu_entry(
    "main",
    base.Text.white_bright("\u2190/\u2191/\u2193/\u2192"),
    "Move cursor Left/Up/Down/Right",
)
game.add_menu_entry(
    "main",
    base.Text.white_bright("j/i/k/l"),
    base.Text.green_bright("Place")
    + " the current item and then move cursor Left/Up/Down/Right",
)
game.add_menu_entry(
    "main",
    base.Text.white_bright("c"),
    "Create a new board item (becomes the current item,"
    + " previous one is placed in history)",
)
game.add_menu_entry("main", base.Text.white_bright("p"), "Modify board parameters")
game.add_menu_entry("main", base.Text.white_bright("P"), "Set player starting position")
game.add_menu_entry(
    "main", base.Text.white_bright("V"), "Modify partial display viewport (resolution)"
)
game.add_menu_entry(
    "main", base.Text.white_bright("S"), f"Save the current Board to {current_file}"
)
game.add_menu_entry(
    "main", base.Text.white_bright("+"), "Save this Board and create a new one"
)
game.add_menu_entry(
    "main", base.Text.white_bright("L"), "Save this Board and load a new one"
)
game.add_menu_entry(
    "main",
    base.Text.white_bright("m"),
    "Switch menu display mode between full or hidden",
)
game.add_menu_entry("main", base.Text.white_bright("Q"), "Quit the editor")

game.add_menu_entry("board", None, "=== Board ===")
game.add_menu_entry(
    "board", "1", "Change " + base.Text.white_bright("width") + " (only sizing up)"
)
game.add_menu_entry(
    "board", "2", "Change " + base.Text.white_bright("height") + " (only sizing up)"
)
game.add_menu_entry("board", "3", "Change " + base.Text.white_bright("name"))
game.add_menu_entry("board", "4", "Change " + base.Text.white_bright("top") + " border")
game.add_menu_entry(
    "board", "5", "Change " + base.Text.white_bright("bottom") + " border"
)
game.add_menu_entry(
    "board", "6", "Change " + base.Text.white_bright("left") + " border"
)
game.add_menu_entry(
    "board", "7", "Change " + base.Text.white_bright("right") + " border"
)
game.add_menu_entry("board", "8", "Change " + base.Text.white_bright("void cell"))
game.add_menu_entry("board", "0", "Go back to the main menu")
game.add_menu_entry(
    "viewport",
    base.Text.white_bright("\u2191"),
    "Increase the number of rows displayed",
)
game.add_menu_entry(
    "viewport",
    base.Text.white_bright("\u2193"),
    "Decrease the number of rows displayed",
)
game.add_menu_entry(
    "viewport",
    base.Text.white_bright("\u2192"),
    "Increase the number of columns displayed",
)
game.add_menu_entry(
    "viewport",
    base.Text.white_bright("\u2190"),
    "Decrease the number of columns displayed",
)
game.add_menu_entry("viewport", "B", "Go back to the main menu")
game.add_menu_entry("waypoint_edition", "j/i/k/l", "Place a waypoint")
game.add_menu_entry("waypoint_edition", "d", "Delete a waypoint")
game.add_menu_entry("waypoint_edition", "B", "Finish waypoints edition")
while True:
    # Empty the messages
    dbg_messages = []
    info_messages = []
    warn_messages = []

    if key == "Q":
        if is_modified:
            print(
                "Board has been modified, do you want to save it",
                "to avoid loosing your changes? (y/n)",
            )
            answer = str(input("> "))
            if answer.startswith("y"):
                if not os.path.exists("pgl-maps") or not os.path.isdir("pgl-maps"):
                    os.makedirs("pgl-maps")
                game.object_library = object_history
                for o in object_history:
                    if o not in game.config("settings")["object_library"]:
                        game.config("settings")["object_library"].append(o)
                game.save_board(1, current_file)
        break
    elif key == "S":
        save_current_board()
        info_messages.append("Board saved")
    elif key == "m":
        if game.config("settings")["menu_mode"] == "full":
            game.config("settings")["menu_mode"] = "hidden"
        else:
            game.config("settings")["menu_mode"] = "full"
        game.update_menu_entry(
            "main",
            None,
            "\n=== Menu (" + game.config("settings")["menu_mode"] + ") ===",
        )
    elif current_menu == "main":
        if key == engine.key.UP:
            game.move_player(constants.UP, 1)
        elif key == engine.key.DOWN:
            game.move_player(constants.DOWN, 1)
        elif key == engine.key.LEFT:
            game.move_player(constants.LEFT, 1)
        elif key == engine.key.RIGHT:
            game.move_player(constants.RIGHT, 1)
        elif key == "k" and edit_mode:
            current_object_instance = place_and_go(
                current_object, game.player.pos[0], game.player.pos[1], constants.DOWN
            )
        elif key == "i" and edit_mode:
            current_object_instance = place_and_go(
                current_object, game.player.pos[0], game.player.pos[1], constants.UP
            )
        elif key == "j" and edit_mode:
            current_object_instance = place_and_go(
                current_object, game.player.pos[0], game.player.pos[1], constants.LEFT
            )
        elif key == "l" and edit_mode:
            current_object_instance = place_and_go(
                current_object, game.player.pos[0], game.player.pos[1], constants.RIGHT
            )
        elif key == "k" and not edit_mode:
            clear_and_go(constants.DOWN)
        elif key == "i" and not edit_mode:
            clear_and_go(constants.UP)
        elif key == "j" and not edit_mode:
            clear_and_go(constants.LEFT)
        elif key == "l" and not edit_mode:
            clear_and_go(constants.RIGHT)
        elif key == " ":
            switch_edit_mode()
        elif key in "1234567890" and current_menu == "main":
            if edit_mode:
                if len(object_history) > int(key):
                    o = object_history[int(key)]
                    to_history(current_object)
                    current_object = o
            else:
                if len(object_history) > int(key):
                    del object_history[int(key)]
                    is_modified = True
        elif key == "P":
            game.current_board().player_starting_position = game.player.pos
            is_modified = True
            info_messages.append(
                f"New player starting position set at {game.player.pos}"
            )
        elif key == "p":
            current_menu = "board"
        elif key == "V":
            current_menu = "viewport"
            game.change_level(2)
            game.player.model = graphics.RED_SQUARE
        elif key == "c":
            to_history(current_object)
            current_object = create_wizard()
            to_history(current_object)
        elif key == "+":
            save_current_board()
            create_board_wizard()
        elif key == "L":
            save_current_board()
            current_menu = "boards_list"
    elif current_menu == "board":
        if key == "0":
            current_menu = "main"
        elif key == "1":
            game.clear_screen()
            nw = int(input_digit("Enter the new width: "))
            if nw >= game.current_board().size[0]:
                old_value = game.current_board().size[0]
                game.current_board().size[0] = nw
                for x in range(0, game.current_board().size[1], 1):
                    for y in range(old_value, game.current_board().size[0], 1):
                        game.current_board()._matrix[x].append(
                            board_items.BoardItemVoid(
                                model=game.current_board().ui_board_void_cell
                            )
                        )
                        is_modified = True

        elif key == "2":
            game.clear_screen()
            nw = int(input_digit("Enter the new height: "))
            if nw >= game.current_board().size[1]:
                old_value = game.current_board().size[1]
                game.current_board().size[1] = nw
                for x in range(old_value, nw, 1):
                    new_array = []
                    for y in range(0, game.current_board().size[0], 1):
                        new_array.append(
                            board_items.BoardItemVoid(
                                model=game.current_board().ui_board_void_cell
                            )
                        )
                    game.current_board()._matrix.append(new_array)
                    is_modified = True

        elif key == "3":
            game.clear_screen()
            n = str(input("Enter the new name: "))
            game.current_board().name = n
            is_modified = True
        elif key == "4":
            game.current_board().ui_border_top = model_picker()
            is_modified = True
        elif key == "5":
            game.current_board().ui_border_bottom = model_picker()
            is_modified = True
        elif key == "6":
            game.current_board().ui_border_left = model_picker()
            is_modified = True
        elif key == "7":
            game.current_board().ui_border_right = model_picker()
            is_modified = True
        elif key == "8":
            game.current_board().ui_board_void_cell = model_picker()
            is_modified = True
    elif current_menu == "boards_list":
        if key in "1234567890":
            e = game.get_menu_entry("boards_list", key)
            if e is not None:
                board = game.load_board(e["data"], 1)
                if board.size[0] >= 50 or board.size[1] >= 50:
                    game.enable_partial_display = True
                    game.partial_display_viewport = [viewport_height, viewport_width]
                else:
                    game.enable_partial_display = False
                board.place_item(
                    game.player,
                    board.player_starting_position[0],
                    board.player_starting_position[1],
                )
                current_file = e["data"]
                game.update_menu_entry(
                    "main",
                    base.Text.white_bright("S"),
                    f"Save the current Board to {current_file}",
                )
                current_menu = "main"
        elif key == "B":
            current_menu = "main"
    elif current_menu == "viewport":
        if game.current_level != 2:
            game.change_level(2)
        if key == "B":
            game.change_level(1)
            game.player.model = "[]"
            current_menu = "main"
        elif key == engine.key.UP:
            viewport_height += 1
        elif key == engine.key.DOWN:
            viewport_height -= 1
        elif key == engine.key.LEFT:
            viewport_width -= 1
        elif key == engine.key.RIGHT:
            viewport_width += 1
        viewport_board.size = [viewport_width * 2, viewport_height * 2]
        viewport_board.init_board()
        game.partial_display_viewport = [viewport_height, viewport_width]
        game.config("settings")["partial_display_viewport"][0] = viewport_height
        game.config("settings")["partial_display_viewport"][1] = viewport_width
    elif current_menu == "waypoint_edition":
        game.player.model = base.Text.green_bright("[]")
        initial_position = game.player.pos
        # I'm lazy so I just go for the bazooka option
        for o in game.current_board().get_immovables(type="waypoint_marker"):
            game.current_board().clear_cell(o.pos[0], o.pos[1])
        for wp in current_object_instance.actuator.waypoints:
            game.current_board().place_item(
                board_items.Door(model=graphics.GREEN_SQUARE, type="waypoint_marker"),
                wp[0],
                wp[1],
            )
        if key == "B":
            current_menu = "main"
            game.player.model = "[]"
            for o in game.current_board().get_immovables(type="waypoint_marker"):
                game.current_board().clear_cell(o.pos[0], o.pos[1])
        elif key == engine.key.UP:
            game.move_player(constants.UP, 1)
        elif key == engine.key.DOWN:
            game.move_player(constants.DOWN, 1)
        elif key == engine.key.LEFT:
            game.move_player(constants.LEFT, 1)
        elif key == engine.key.RIGHT:
            game.move_player(constants.RIGHT, 1)
        elif key == "k" and edit_mode:
            place_and_go(
                board_items.Door(model=graphics.GREEN_SQUARE, type="waypoint_marker"),
                game.player.pos[0],
                game.player.pos[1],
                constants.DOWN,
            )
            if initial_position != game.player.pos:
                current_object_instance.actuator.add_waypoint(
                    initial_position[0], initial_position[1]
                )
        elif key == "i" and edit_mode:
            place_and_go(
                board_items.Door(model=graphics.GREEN_SQUARE, type="waypoint_marker"),
                game.player.pos[0],
                game.player.pos[1],
                constants.UP,
            )
            if initial_position != game.player.pos:
                current_object_instance.actuator.add_waypoint(
                    initial_position[0], initial_position[1]
                )
        elif key == "j" and edit_mode:
            place_and_go(
                board_items.Door(model=graphics.GREEN_SQUARE, type="waypoint_marker"),
                game.player.pos[0],
                game.player.pos[1],
                constants.LEFT,
            )
            if initial_position != game.player.pos:
                current_object_instance.actuator.add_waypoint(
                    initial_position[0], initial_position[1]
                )
        elif key == "l" and edit_mode:
            place_and_go(
                board_items.Door(model=graphics.GREEN_SQUARE, type="waypoint_marker"),
                game.player.pos[0],
                game.player.pos[1],
                constants.RIGHT,
            )
            if initial_position != game.player.pos:
                current_object_instance.actuator.add_waypoint(
                    initial_position[0], initial_position[1]
                )
        elif key == "d":
            try:
                current_object_instance.actuator.remove_waypoint(
                    game.player.pos[0], game.player.pos[1]
                )
            except ValueError:
                print("There is no waypoint here.")

    # Print the screen and interface
    game.clear_screen()
    if current_menu == "main" or current_menu == "board":
        print(base.Text.white_bright("Current mode: "), end="")
        if edit_mode:
            print(base.Text.green_bright("EDIT"), end="")
        else:
            print(base.Text.red_bright("DELETE"), end="")
        print(
            f" | Board: {game.current_board().name} -",
            f"{game.current_board().size} | Cursor @ {game.player.pos}",
        )
    game.display_board()
    if len(object_history) > 10:
        del object_history[0]
    if current_menu == "main":
        print("Item history:")
        cnt = 0
        for o in object_history:
            print(f"{cnt}: {o.model}", end="  ")
            cnt += 1
        print("")
        print(f"Current item: {current_object.model}")
    if not (
        current_menu == "main" and game.config("settings")["menu_mode"] == "hidden"
    ):
        game.display_menu(current_menu, constants.ORIENTATION_VERTICAL, 15)
    for m in dbg_messages:
        base.Text.debug(m)
    for m in info_messages:
        base.Text.info(m)
    for m in warn_messages:
        base.Text.warn(m)
    if current_menu == "boards_list":
        key = input("Enter your choice (and hit ENTER): ")
    else:
        key = engine.Game.get_key()

# Before saving we need to transform the object library into reference that json can
# understand
reflib = []
for o in game.config("settings")["object_library"]:
    reflib.append(engine.Game._obj2ref(o))
game.config("settings")["object_library"] = reflib
# Let's also save the partial display viewport
game.config("settings")["partial_display_viewport"][0] = viewport_height
game.config("settings")["partial_display_viewport"][1] = viewport_width
game.save_config("settings", os.path.join(editor_config_dir, "settings.json"))
