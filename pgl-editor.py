#!/usr/bin/env python3

import os
import uuid
import numpy as np
from copy import deepcopy

from pygamelib import constants
from pygamelib import actuators
from pygamelib import engine
from pygamelib import board_items
from pygamelib.assets import graphics
from pygamelib import base
import pygamelib.gfx.core as gfx_core


class PglEditor:
    def __init__(self):
        self.is_modified = False
        self.edit_mode = True
        self.dbg_messages = []
        self.info_messages = []
        self.warn_messages = []
        # TODO: migrate the settings to .pygamelib
        self.base_config_dir = os.path.join(os.path.expanduser("~"), ".hac-game-lib")
        self.config_dir = os.path.join(self.base_config_dir, "config")
        self.editor_config_dir = os.path.join(self.config_dir, "editor")
        self.default_map_dir = os.path.join(self.base_config_dir, "editor", "maps")
        self.game = engine.Game()
        self.viewport_height = int(self.game.screen.height / 2) - 11
        self.viewport_width = int(self.game.screen.width / 4) - 2
        self.game.player = board_items.Player(model="[]")
        self.current_menu = "main"
        self.object_history = []
        self.current_file = ""
        self.use_complex_item = False
        self.complex_item_null_sprixel = gfx_core.Sprixel("PGL_EDITOR_NULL_SPRIXEL")

    # Functions definition
    def place_and_go(self, obj, x, y, direction):
        game = self.game
        initial_position = game.player.pos
        if direction == constants.LEFT or direction == constants.RIGHT:
            game.move_player(direction, obj.width)
        elif direction == constants.UP or direction == constants.DOWN:
            game.move_player(direction, obj.height)
        if initial_position != game.player.pos:
            new_obj = deepcopy(obj)
            if isinstance(new_obj, board_items.BoardComplexItem):
                for ir in range(new_obj.sprite.height):
                    for ic in range(new_obj.width):
                        if new_obj.sprite.sprixel(ir, ic).bg_color is None:
                            new_obj.sprite.sprixel(
                                ir, ic
                            ).bg_color = (
                                game.current_board().ui_board_void_cell_sprixel.bg_color
                            )
            else:
                if new_obj.sprixel.bg_color is None:
                    new_obj.sprixel.bg_color = (
                        game.current_board().ui_board_void_cell_sprixel.bg_color
                    )
            game.current_board().place_item(new_obj, x, y)
            self.is_modified = True
            if isinstance(obj, board_items.NPC) and isinstance(
                obj.actuator, actuators.PathFinder
            ):
                self.current_menu = "waypoint_edition"
            return new_obj
        return None

    def clear_and_go(self, direction):
        game = self.game
        new_x = game.player.pos[0]
        new_y = game.player.pos[1]
        if direction == constants.DOWN:
            new_x += game.player.height
        elif direction == constants.UP:
            new_x -= game.player.height
        elif direction == constants.LEFT:
            new_y -= game.player.width
        elif direction == constants.RIGHT:
            new_y += game.player.width

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
            self.is_modified = True

    def switch_edit_mode(self):
        game = self.game
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
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

    def color_picker(self):
        game = self.game
        game.clear_screen()
        print("Pick a form and color from the list:")
        game.display_menu("graphics_utils", constants.ORIENTATION_HORIZONTAL, 8)
        return str(input_digit("\n(Enter a number)> "))

    def custom_color_picker(self):
        # Custom color chooser.
        game = self.game
        step = 1
        base_char = ""
        print("What type of color block do you want:\n1 - Rectangle\n2 - Square")
        c_ch = input_digit("\n(Enter a number)> ")
        if c_ch == "1":
            base_char = " "
        else:
            base_char = "  "
        bg_color = gfx_core.Color(128, 128, 128)
        spr = gfx_core.Sprixel(base_char, bg_color)
        key = None
        while key != engine.key.ENTER:
            game.clear_screen()
            print(game.terminal.center("Build your color\n"))
            print(
                f"{base.Text.red('Red')}: {spr.bg_color.r} "
                f"{base.Text.green_bright('Green')}: {spr.bg_color.g} "
                f"{base.Text.blue_bright('Blue')}: {spr.bg_color.b}\n\n"
                f"Your color: {spr}\n"
            )
            print("4/1 - Increase/decrease the red value")
            print("5/2 - Increase/decrease the green value")
            print("6/3 - Increase/decrease the blue value")
            print(f"+/- - Increase/decrease the increment step (current: {step})")
            print("r - Randomize values")
            key = game.get_key()
            if key == "1" and bg_color.r >= step:
                bg_color.r -= step
            elif key == "4" and bg_color.r + step <= 255:
                bg_color.r += step
            if key == "2" and bg_color.g >= step:
                bg_color.g -= step
            elif key == "5" and bg_color.g + step <= 255:
                bg_color.g += step
            if key == "3" and bg_color.b >= step:
                bg_color.b -= step
            elif key == "6" and bg_color.b + step <= 255:
                bg_color.b += step
            if key == "-":
                step -= 1
            elif key == "+":
                step += 1
            elif key == "r":
                bg_color.randomize()
            # Since 1.3.0, this is required to force the rebuilt of the color cache.
            spr.bg_color = bg_color
        return spr

    def utf8_picker(self, category):
        game = self.game
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

    def model_picker(self):
        game = self.game
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
            ret_val = None
            if choice == "1":
                choice = self.color_picker()
                if int(choice) > 0:
                    picked = game.get_menu_entry("graphics_utils", choice)
                    if picked is not None:
                        ret_val = picked["data"]
                else:
                    ret_val = self.custom_color_picker()
            elif choice == "2":
                picked = game.get_menu_entry(
                    "graphics_models", self.utf8_picker("graphics_models")
                )
                if picked is not None:
                    ret_val = picked["data"]
            elif choice == "3":
                picked = game.get_menu_entry(
                    "graphics_blocks", self.utf8_picker("graphics_blocks")
                )
                if picked is not None:
                    ret_val = picked["data"]
            elif choice == "4":
                picked = game.get_menu_entry(
                    "graphics_box_drawings", self.utf8_picker("graphics_box_drawings")
                )
                if picked is not None:
                    ret_val = picked["data"]
            elif choice == "5":
                picked = game.get_menu_entry(
                    "graphics_geometric_shapes",
                    self.utf8_picker("graphics_geometric_shapes"),
                )
                if picked is not None:
                    ret_val = picked["data"]
            elif choice == "6":
                ret_val = str(input("Enter your string now: "))
            # Process ret_val before returning it.
            if self.use_complex_item:
                if type(ret_val) is str:
                    # If it's a string we take each character and convert it to a
                    # sprixel of the final sprite.
                    sprixs = []
                    for letter in ret_val:
                        spx = gfx_core.Sprixel(letter)
                        sprixs.append(spx)
                        # In case it's an emoji or other character longer than 1
                        for _ in range(spx.length - 1):
                            sprixs.append(gfx_core.Sprixel(""))
                    # Sprite.sprixels is a 2D array.
                    return gfx_core.Sprite(sprixels=[sprixs])
                elif isinstance(ret_val, gfx_core.Sprixel):
                    sprixs = [ret_val]
                    # Most likely an emoji so we pad the extra character length with
                    # empty space
                    for _ in range(ret_val.length - 1):
                        sprixs.append(gfx_core.Sprixel(""))
                    return gfx_core.Sprite(sprixels=[sprixs])
                # If not in the previous cases we just return the return value.
                return ret_val
            else:
                if type(ret_val) is str:
                    return gfx_core.Sprixel(ret_val)
                return ret_val

    def to_history(self, obj):
        object_history = self.object_history
        if (
            len(object_history) <= 10
            and obj not in object_history
            and not isinstance(obj, board_items.BoardItemVoid)
        ):
            object_history.append(obj)
        elif (
            len(object_history) > 10
            and obj not in object_history
            and not isinstance(obj, board_items.BoardItemVoid)
        ):
            del object_history[0]
            object_history.append(obj)

    def create_wizard(self):
        # TODO This should be split up into multiple methods
        game = self.game
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
            new_object = None
            if self.use_complex_item:
                new_object = board_items.ComplexNPC(
                    null_sprixel=self.complex_item_null_sprixel
                )
            else:
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
            chosen_model = self.model_picker()
            if isinstance(chosen_model, gfx_core.Sprixel):
                new_object.sprixel = chosen_model
                # also sets new_objects model, for backward compatibility
                # new_object.model = str(chosen_model)
            elif isinstance(chosen_model, gfx_core.Sprite):
                new_object.sprite = chosen_model
            else:
                # new_object.model = chosen_model
                new_object.sprixel = gfx_core.Sprixel(chosen_model)

            game.clear_screen()
            print(
                base.Text.green_bright("\t\tObject creation wizard: ")
                + base.Text.cyan_bright("NPC")
                + f" - {new_object.sprixel}"
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
                f"Max HP (Health Points). "
                f"Default: {new_object.max_hp}(type: int) > "
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
                f"AP (Attack Power). "
                f"Default: {new_object.attack_power}(type: int) > "
            )
            if len(r) > 0:
                new_object.attack_power = int(r)

            r = input_digit(
                f"DP (Defense Power). "
                f"Default: {new_object.defense_power}(type: int) > "
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
                    new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
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
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
                elif r == "3":
                    print(
                        "How many steps should the NPC go in one direction "
                        "before turning back ?"
                    )
                    r = int(input_digit("(please enter an integer)> "))
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
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
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
                    new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
                elif r == "6":
                    print(
                        "How many steps should the NPC go in EACH "
                        "direction before changing ?"
                    )
                    r = int(input_digit("(please enter an integer)> "))
                    new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                    new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
                    new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                elif r == "7":
                    print(
                        "How many steps should the NPC go in EACH "
                        "direction before changing ?"
                    )
                    r = int(input_digit("(please enter an integer)> "))
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
                    new_object.actuator.path += [constants.DOWN for i in range(0, r, 1)]
                    new_object.actuator.path += [constants.LEFT for i in range(0, r, 1)]
                    new_object.actuator.path += [constants.UP for i in range(0, r, 1)]
                elif r == "8":
                    print(
                        "How many steps should the NPC go in EACH direction "
                        "before changing ?"
                    )
                    r = int(input_digit("(please enter an integer)> "))
                    new_object.actuator.path += [
                        constants.RIGHT for i in range(0, r, 1)
                    ]
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
                    if self.use_complex_item:
                        new_object = board_items.ComplexWall(
                            null_sprixel=self.complex_item_null_sprixel
                        )
                    else:
                        new_object = board_items.Wall()
                    new_object.name = str(uuid.uuid1())
                    chosen_model = self.model_picker()
                    if isinstance(chosen_model, gfx_core.Sprixel):
                        new_object.sprixel = chosen_model
                        # also sets new_objects model, for backward compatibility
                        new_object.model = str(chosen_model)
                    elif isinstance(chosen_model, gfx_core.Sprite):
                        new_object.sprite = chosen_model
                    else:
                        new_object.sprixel = gfx_core.Sprixel(chosen_model)
                        new_object.model = chosen_model
                    break
                elif key == "2":
                    if self.use_complex_item:
                        new_object = board_items.ComplexDoor(
                            null_sprixel=self.complex_item_null_sprixel
                        )
                    else:
                        new_object = board_items.Door()
                    new_object.name = str(uuid.uuid1())
                    chosen_model = self.model_picker()
                    if isinstance(chosen_model, gfx_core.Sprixel):
                        new_object.sprixel = chosen_model
                        # also sets new_objects model, for backward compatibility
                        new_object.model = str(chosen_model)
                    elif isinstance(chosen_model, gfx_core.Sprite):
                        new_object.sprite = chosen_model
                    else:
                        new_object.sprixel = gfx_core.Sprixel(chosen_model)
                        new_object.model = chosen_model
                    break
                elif key == "3":
                    if self.use_complex_item:
                        new_object = board_items.ComplexTreasure(
                            null_sprixel=self.complex_item_null_sprixel
                        )
                    else:
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
                    chosen_model = self.model_picker()
                    if isinstance(chosen_model, gfx_core.Sprixel):
                        new_object.sprixel = chosen_model
                        # also sets new_objects model, for backward compatibility
                        new_object.model = str(chosen_model)
                    elif isinstance(chosen_model, gfx_core.Sprite):
                        new_object.sprite = chosen_model
                    else:
                        new_object.sprixel = gfx_core.Sprixel(chosen_model)
                        new_object.model = chosen_model
                    break
                elif key == "4" or key == "5":
                    if key == "4":
                        if self.use_complex_item:
                            new_object = board_items.Tile(
                                null_sprixel=self.complex_item_null_sprixel
                            )
                        else:
                            new_object = board_items.GenericStructure()
                    else:
                        if self.use_complex_item:
                            new_object = board_items.ActionableTile(
                                null_sprixel=self.complex_item_null_sprixel
                            )
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
                    chosen_model = self.model_picker()
                    self.dbg_messages.append(
                        f"ActionableTile: received type {type(chosen_model)}"
                    )
                    if isinstance(chosen_model, gfx_core.Sprixel):
                        new_object.sprixel = chosen_model
                        # also sets new_objects model, for backward compatibility
                        new_object.model = str(chosen_model)
                    elif isinstance(chosen_model, gfx_core.Sprite):
                        new_object.sprite = chosen_model
                    else:
                        new_object.sprixel = gfx_core.Sprixel(chosen_model)
                        new_object.model = chosen_model
                    print(
                        "Is this object pickable? (can it be picked up by the player)?"
                    )
                    print("0 - No")
                    print("1 - Yes")
                    r = engine.Game.get_key()
                    if r == "1":
                        new_object.set_pickable(True)
                    print(
                        "Is this object overlappable? (can it be walked over by player?"
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

    def save_current_board(self):
        self.game.object_library = self.object_history
        self.game.save_board(1, self.current_file)
        self.is_modified = False

    def create_board_wizard(self):
        game = self.game
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
            "items that you are going to put inside. "
            "Do you plan to use a mix of emojis (that displays on 2 characters "
            "in the terminal) and regular single characters? "
            "Or do you plan to use only squared items (emojis and colored squares)?"
        )
        use_square = input_digit(
            "0 - Mixed: emojis, rectangles and any other characters\n"
            "1 - Squares only: emojis and colored square (or any double characters)\n"
            "Your choice: "
        )
        ui_borders = graphics.WHITE_SQUARE
        ui_board_void_cell = gfx_core.Sprixel.black_square()
        self.use_complex_item = False
        width_divider = 4
        if use_square == "0":
            ui_borders = graphics.WHITE_RECT
            ui_board_void_cell = gfx_core.Sprixel.black_rect()
            base.Text.warn(
                "You have to pay attention to the items movements, you probably"
                " want to make sure the items move faster horizontally than vertically."
            )
            # cursor = gfx_core.Sprite(
            #     sprixels=[[gfx_core.Sprixel("["), gfx_core.Sprixel("]")]]
            # )
            # game.player = board_items.ComplexPlayer(sprite=cursor)
            self.use_complex_item = True
            game.player.sprixel = gfx_core.Sprixel(
                graphics.BoxDrawings.HEAVY_VERTICAL_AND_HORIZONTAL,
            )
            width_divider = 2
            input("\n\nPress ENTER to continue.")
        game.add_board(
            1,
            engine.Board(
                name=name,
                size=[width, height],
                ui_borders=ui_borders,
                ui_board_void_cell_sprixel=ui_board_void_cell,
            ),
        )
        self.is_modified = True
        self.current_file = os.path.join(
            self.default_map_dir, name.replace(" ", "_") + ".json"
        )
        game.config("settings")["last_used_board_parameters"] = {
            "name": name,
            "width": width,
            "height": height,
        }
        if (
            game.get_board(1).width >= game.screen.width - 4
            or game.get_board(1).height >= game.screen.height - 19
        ):
            game.enable_partial_display = True
            game.partial_display_viewport = [
                int(game.screen.height / 2) - 11,
                int(game.screen.width / width_divider) - 2,
            ]
            self.viewport_height = game.partial_display_viewport[0]
            self.viewport_width = game.partial_display_viewport[1]

    def first_use(self):
        game = self.game
        print(base.Text.yellow_bright("Configuration wizard (fresh install or update)"))
        print(
            "You may see that wizard because pgl-editor was updated with new settings."
            "\n"
            "Please check that everything is fine (your previous values are shown as"
            "default values)\n"
        )
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.exists(os.path.join(self.base_config_dir, "editor", "maps")):
            os.makedirs(os.path.join(self.base_config_dir, "editor", "maps"))
        if not os.path.exists(self.editor_config_dir):
            os.makedirs(self.editor_config_dir)
        print(
            "We need to set up the default directory where we are going to save maps.",
            f"Default is {self.default_map_dir}",
        )
        new_default = str(input("Default maps directory: "))
        while (
            not os.path.exists(new_default)
            or not os.path.isdir(new_default)
            or not os.path.isabs(new_default)
        ) and new_default != "":
            print(
                base.Text.red("The path to directory needs to exist and be absolute.")
            )
            new_default = str(input("Default maps directory: "))
        if new_default != "":
            self.default_map_dir = new_default
        if not os.path.exists(os.path.join(self.config_dir, "directories.json")):
            with open(os.path.join(self.config_dir, "directories.json"), "w") as fp:
                fp.write(f'["{self.default_map_dir}","pgl-maps","hac-maps","maps"]')
        if not os.path.exists(os.path.join(self.editor_config_dir, "settings.json")):
            game.create_config("settings")
            game.config("settings")["directories"] = [
                self.default_map_dir,
                "pgl-maps",
                "hac-maps",
                "maps",
            ]
            game.config("settings")["config_file_version"] = 10100
            game.config("settings")["enable_partial_display"] = True
            game.config("settings")["partial_display_viewport"] = [
                int(game.screen.height / 2) - 11,
                int(game.screen.width / 4) - 2,
            ]
            game.config("settings")["menu_mode"] = "full"
            game.config("settings")["last_used_board_parameters"] = {
                "name": None,
                "width": None,
                "height": None,
            }
            game.config("settings")["object_library"] = []

    def main(self):
        # TODO This should be split up into multiple methods
        game = self.game
        key = "None"
        current_object = board_items.BoardItemVoid(model="None")
        current_object_instance = board_items.BoardItemVoid(model="None")
        viewport_board = engine.Board(
            name="Viewport testing board",
            size=[self.viewport_width * 2, self.viewport_height * 2],
            ui_borders=graphics.GREEN_SQUARE,
            ui_board_void_cell=graphics.RED_SQUARE,
        )
        game.add_board(2, viewport_board)
        while True:
            game.clear_screen()
            print(
                base.Text.cyan_bright(
                    "PYGAMELIB - EDITOR v" + constants.PYGAMELIB_VERSION
                )
            )
            # Create config_dir if not exist and populate it with a directories.json
            # file.
            settings_file = os.path.join(self.editor_config_dir, "settings.json")
            if (
                not os.path.exists(self.config_dir)
                or not os.path.isdir(self.config_dir)
                or not os.path.exists(self.base_config_dir)
                or not os.path.isdir(self.base_config_dir)
                or not os.path.isdir(self.editor_config_dir)
                or not os.path.exists(settings_file)
            ):
                self.first_use()
            else:
                game.load_config(settings_file, "settings")
                self.viewport_height, self.viewport_width = game.config("settings")[
                    "partial_display_viewport"
                ]
                viewport_board.size = [
                    self.viewport_width * 2,
                    self.viewport_height * 2,
                ]
                viewport_board.init_board()
                # The objects library is stored as a list of references.
                # We need to convert that before using the objects.
                objlib = []
                for ref in game.config("settings")["object_library"]:
                    objlib.append(engine.Game._ref2obj(ref))
                game.config("settings")["object_library"] = objlib
            print(
                "Looking for existing maps in selected directories...",
                end="",
                flush=True,
            )
            self.default_map_dir = None
            hmaps = []
            for directory in game.config("settings")["directories"]:
                # files = [f'{directory}/{f}' for f in os.listdir(directory)]
                # hmaps += files
                test_dir = os.path.join(self.base_config_dir, directory)
                if os.path.exists(test_dir):
                    directory = test_dir
                    # Utils.debug(f"Setting directory to: {directory}")
                if os.path.exists(directory):
                    if self.default_map_dir is None:
                        self.default_map_dir = directory
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
                    game.add_menu_entry(
                        "boards_list", str(map_num), f"edit {m}", f"{m}"
                    )
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
                self.create_board_wizard()
                break
            elif choice.isdigit() and int(choice) < len(hmaps):
                self.current_file = hmaps[int(choice)]
                board = game.load_board(hmaps[int(choice)], 1)
                ###
                self.use_complex_item = False
                if (
                    board.ui_board_void_cell_sprixel is not None
                    and board.ui_board_void_cell_sprixel.length == 1
                ):
                    self.use_complex_item = True
                    game.player.sprixel = gfx_core.Sprixel(
                        graphics.BoxDrawings.HEAVY_VERTICAL_AND_HORIZONTAL,
                    )
                ###
                is_board_bigger_than_viewport = (
                    board.size[0] >= self.viewport_height
                    or board.size[1] >= self.viewport_width
                )
                if is_board_bigger_than_viewport:
                    game.enable_partial_display = True
                    game.partial_display_viewport = [
                        self.viewport_height,
                        self.viewport_width,
                    ]
                else:
                    game.enable_partial_display = False
                break

        game.change_level(1)

        if len(game.object_library) > 0:
            self.object_history += game.object_library
            for i in game.object_library:
                if i not in game.config("settings")["object_library"]:
                    game.config("settings")["object_library"].append(i)

        # Build the menus
        i = 1
        # WARNING: This might break!!!!
        # for sp in dir(graphics):
        #     if sp.endswith("_SQUARE") or sp.endswith("_RECT"):
        #         game.add_menu_entry(
        #             "graphics_utils",
        #             str(i),
        #             '"' + getattr(graphics, sp) + '"',
        #             getattr(graphics, sp),
        #         )
        #         i += 1

        # First element is for custom color
        game.add_menu_entry("graphics_utils", "0", "Custom color")
        # I don't know if I should be proud or ashamed of that...
        for sp in dir(graphics):
            if sp.endswith("_SQUARE") or sp.endswith("_RECT"):
                f_name = sp.lower()
                if hasattr(gfx_core.Sprixel, f_name) and callable(
                    getattr(gfx_core.Sprixel, f_name)
                ):
                    fct = getattr(gfx_core.Sprixel, f_name)
                    game.add_menu_entry(
                        "graphics_utils",
                        str(i),
                        f'"{fct()}"',
                        fct(),
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
            "main",
            None,
            "\n=== Menu (" + game.config("settings")["menu_mode"] + ") ===",
        )
        game.add_menu_entry(
            "main", base.Text.white_bright("Space"), "Switch between edit/delete mode"
        )
        game.add_menu_entry(
            "main",
            base.Text.white_bright("0 to 9"),
            base.Text.green_bright("Select")
            + " an item in history to be the current item",
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
        game.add_menu_entry(
            "main", base.Text.white_bright("p"), "Modify board parameters"
        )
        game.add_menu_entry(
            "main", base.Text.white_bright("P"), "Set player starting position"
        )
        game.add_menu_entry(
            "main",
            base.Text.white_bright("V"),
            "Modify partial display viewport (resolution)",
        )
        game.add_menu_entry(
            "main",
            base.Text.white_bright("S"),
            f"Save the current Board to {self.current_file}",
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
            "board",
            "1",
            "Change " + base.Text.white_bright("width") + " (only sizing up)",
        )
        game.add_menu_entry(
            "board",
            "2",
            "Change " + base.Text.white_bright("height") + " (only sizing up)",
        )
        game.add_menu_entry("board", "3", "Change " + base.Text.white_bright("name"))
        game.add_menu_entry(
            "board", "4", "Change " + base.Text.white_bright("top") + " border"
        )
        game.add_menu_entry(
            "board", "5", "Change " + base.Text.white_bright("bottom") + " border"
        )
        game.add_menu_entry(
            "board", "6", "Change " + base.Text.white_bright("left") + " border"
        )
        game.add_menu_entry(
            "board", "7", "Change " + base.Text.white_bright("right") + " border"
        )
        game.add_menu_entry(
            "board", "8", "Change " + base.Text.white_bright("void cell")
        )
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
            self.dbg_messages.clear()
            self.info_messages.clear()
            self.warn_messages.clear()

            if key == "Q":
                if self.is_modified:
                    print(
                        "Board has been modified, do you want to save it",
                        "to avoid loosing your changes? (y/n)",
                    )
                    answer = str(input("> "))
                    if answer.startswith("y"):
                        need_pgl_maps_dir = not os.path.exists(
                            "pgl-maps"
                        ) or not os.path.isdir("pgl-maps")
                        if need_pgl_maps_dir:
                            os.makedirs("pgl-maps")
                        game.object_library = self.object_history
                        for o in self.object_history:
                            if o not in game.config("settings")["object_library"]:
                                game.config("settings")["object_library"].append(o)
                        game.save_board(1, self.current_file)
                break
            elif key == "S":
                self.save_current_board()
                self.info_messages.append("Board saved")
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
            elif self.current_menu == "main":
                if key == engine.key.UP:
                    game.move_player(constants.UP, 1)
                elif key == engine.key.DOWN:
                    game.move_player(constants.DOWN, 1)
                elif key == engine.key.LEFT:
                    game.move_player(constants.LEFT, 1)
                elif key == engine.key.RIGHT:
                    game.move_player(constants.RIGHT, 1)
                elif key == "k" and self.edit_mode:
                    current_object_instance = self.place_and_go(
                        current_object,
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.DOWN,
                    )
                elif key == "i" and self.edit_mode:
                    current_object_instance = self.place_and_go(
                        current_object,
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.UP,
                    )
                elif key == "j" and self.edit_mode:
                    current_object_instance = self.place_and_go(
                        current_object,
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.LEFT,
                    )
                elif key == "l" and self.edit_mode:
                    current_object_instance = self.place_and_go(
                        current_object,
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.RIGHT,
                    )
                elif key == "k" and not self.edit_mode:
                    self.clear_and_go(constants.DOWN)
                elif key == "i" and not self.edit_mode:
                    self.clear_and_go(constants.UP)
                elif key == "j" and not self.edit_mode:
                    self.clear_and_go(constants.LEFT)
                elif key == "l" and not self.edit_mode:
                    self.clear_and_go(constants.RIGHT)
                elif key == " ":
                    self.switch_edit_mode()
                elif key in "1234567890" and self.current_menu == "main":
                    if self.edit_mode:
                        if len(self.object_history) > int(key):
                            o = self.object_history[int(key)]
                            self.to_history(current_object)
                            current_object = o
                    else:
                        if len(self.object_history) > int(key):
                            del self.object_history[int(key)]
                            self.is_modified = True
                elif key == "P":
                    game.current_board().player_starting_position = game.player.pos
                    self.is_modified = True
                    self.info_messages.append(
                        f"New player starting position set at {game.player.pos}"
                    )
                elif key == "p":
                    self.current_menu = "board"
                elif key == "V":
                    self.current_menu = "viewport"
                    game.change_level(2)
                    game.player.model = graphics.RED_SQUARE
                elif key == "c":
                    self.to_history(current_object)
                    current_object = self.create_wizard()
                    self.to_history(current_object)
                elif key == "+":
                    self.save_current_board()
                    self.create_board_wizard()
                elif key == "L":
                    self.save_current_board()
                    self.current_menu = "boards_list"
            elif self.current_menu == "board":
                if key == "0":
                    self.current_menu = "main"
                elif key == "1":
                    game.clear_screen()
                    nw = int(input_digit("Enter the new width: "))
                    if nw >= game.current_board().size[0]:
                        current_board = game.current_board()
                        old_value = current_board.size[0]
                        current_board.size[0] = nw
                        ext = np.full(
                            (
                                current_board.size[1],
                                current_board.size[0] - old_value,
                            ),
                            None,
                        )
                        for r in range(current_board.size[1]):
                            for c in range(current_board.size[0] - old_value):
                                ext[r][c] = [
                                    board_items.BoardItemVoid(
                                        pos=[r, c, 0],
                                        sprixel=deepcopy(
                                            current_board.ui_board_void_cell_sprixel
                                        ),
                                        parent=current_board,
                                    )
                                ]
                        current_board._matrix = np.append(current_board._matrix, ext, 1)
                        self.is_modified = True

                elif key == "2":
                    game.clear_screen()
                    nw = int(input_digit("Enter the new height: "))
                    if nw >= game.current_board().size[1]:
                        current_board = game.current_board()
                        old_value = current_board.size[1]
                        current_board.size[1] = nw
                        # TODO: We should use list completion here
                        ext = np.full(
                            (
                                current_board.size[1] - old_value,
                                current_board.size[0],
                            ),
                            None,
                        )
                        for r in range(current_board.size[1] - old_value):
                            for c in range(current_board.size[0]):
                                ext[r][c] = [
                                    board_items.BoardItemVoid(
                                        pos=[r, c, 0],
                                        sprixel=deepcopy(
                                            current_board.ui_board_void_cell_sprixel
                                        ),
                                        parent=current_board,
                                    )
                                ]
                        current_board._matrix = np.append(current_board._matrix, ext, 0)
                        self.is_modified = True

                elif key == "3":
                    game.clear_screen()
                    n = str(input("Enter the new name: "))
                    game.current_board().name = n
                    self.is_modified = True
                elif key == "4":
                    game.current_board().ui_border_top = self.model_picker()
                    self.is_modified = True
                elif key == "5":
                    game.current_board().ui_border_bottom = self.model_picker()
                    self.is_modified = True
                elif key == "6":
                    game.current_board().ui_border_left = self.model_picker()
                    self.is_modified = True
                elif key == "7":
                    game.current_board().ui_border_right = self.model_picker()
                    self.is_modified = True
                elif key == "8":
                    b = game.current_board()
                    spr = self.model_picker()
                    b.ui_board_void_cell_sprixel = spr
                    b.ui_board_void_cell = str(spr)
                    for r in range(b.height):
                        for c in range(b.width):
                            itm = b.item(r, c)
                            if isinstance(itm, board_items.BoardItemVoid):
                                itm.sprixel = b.ui_board_void_cell_sprixel
                    self.is_modified = True
            elif self.current_menu == "boards_list":
                if key in "1234567890":
                    e = game.get_menu_entry("boards_list", key)
                    if e is not None:
                        board = game.load_board(e["data"], 1)
                        if board.size[0] >= 50 or board.size[1] >= 50:
                            game.enable_partial_display = True
                            game.partial_display_viewport = [
                                self.viewport_height,
                                self.viewport_width,
                            ]
                        else:
                            game.enable_partial_display = False
                        board.place_item(
                            game.player,
                            board.player_starting_position[0],
                            board.player_starting_position[1],
                        )
                        self.current_file = e["data"]
                        game.update_menu_entry(
                            "main",
                            base.Text.white_bright("S"),
                            f"Save the current Board to {self.current_file}",
                        )
                        self.current_menu = "main"
                elif key == "B":
                    self.current_menu = "main"
            elif self.current_menu == "viewport":
                if game.current_level != 2:
                    game.change_level(2)
                if key == "B":
                    game.change_level(1)
                    game.player.model = "[]"
                    self.current_menu = "main"
                elif key == engine.key.UP:
                    self.viewport_height += 1
                elif key == engine.key.DOWN:
                    self.viewport_height -= 1
                elif key == engine.key.LEFT:
                    self.viewport_width -= 1
                elif key == engine.key.RIGHT:
                    self.viewport_width += 1
                viewport_board.size = [
                    self.viewport_width * 2,
                    self.viewport_height * 2,
                ]
                viewport_board.init_board()
                (
                    game.config("settings")["partial_display_viewport"][0],
                    game.config("settings")["partial_display_viewport"][1],
                ) = game.partial_display_viewport = [
                    self.viewport_height,
                    self.viewport_width,
                ]
            elif self.current_menu == "waypoint_edition":
                game.player.model = base.Text.green_bright("[]")
                initial_position = game.player.pos
                # I'm lazy so I just go for the bazooka option
                for o in game.current_board().get_immovables(type="waypoint_marker"):
                    game.current_board().clear_cell(o.pos[0], o.pos[1])
                for wp in current_object_instance.actuator.waypoints:
                    game.current_board().place_item(
                        board_items.Door(
                            model=graphics.GREEN_SQUARE, type="waypoint_marker"
                        ),
                        wp[0],
                        wp[1],
                    )
                if key == "B":
                    self.current_menu = "main"
                    game.player.model = "[]"
                    current_board = game.current_board()
                    for o in current_board.get_immovables(type="waypoint_marker"):
                        current_board.clear_cell(o.pos[0], o.pos[1])
                elif key == engine.key.UP:
                    game.move_player(constants.UP, 1)
                elif key == engine.key.DOWN:
                    game.move_player(constants.DOWN, 1)
                elif key == engine.key.LEFT:
                    game.move_player(constants.LEFT, 1)
                elif key == engine.key.RIGHT:
                    game.move_player(constants.RIGHT, 1)
                elif key == "k" and self.edit_mode:
                    self.place_and_go(
                        board_items.Door(
                            model=graphics.GREEN_SQUARE, type="waypoint_marker"
                        ),
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.DOWN,
                    )
                    if initial_position != game.player.pos:
                        current_object_instance.actuator.add_waypoint(
                            initial_position[0], initial_position[1]
                        )
                elif key == "i" and self.edit_mode:
                    self.place_and_go(
                        board_items.Door(
                            model=graphics.GREEN_SQUARE, type="waypoint_marker"
                        ),
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.UP,
                    )
                    if initial_position != game.player.pos:
                        current_object_instance.actuator.add_waypoint(
                            initial_position[0], initial_position[1]
                        )
                elif key == "j" and self.edit_mode:
                    self.place_and_go(
                        board_items.Door(
                            model=graphics.GREEN_SQUARE, type="waypoint_marker"
                        ),
                        game.player.pos[0],
                        game.player.pos[1],
                        constants.LEFT,
                    )
                    if initial_position != game.player.pos:
                        current_object_instance.actuator.add_waypoint(
                            initial_position[0], initial_position[1]
                        )
                elif key == "l" and self.edit_mode:
                    self.place_and_go(
                        board_items.Door(
                            model=graphics.GREEN_SQUARE, type="waypoint_marker"
                        ),
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
            if self.current_menu == "main" or self.current_menu == "board":
                print(base.Text.white_bright("Current mode: "), end="")
                if self.edit_mode:
                    print(base.Text.green_bright("EDIT"), end="")
                else:
                    print(base.Text.red_bright("DELETE"), end="")
                print(
                    f" | Board: {game.current_board().name} -",
                    f"{game.current_board().size} | Cursor @ {game.player.pos}",
                )
            game.display_board()
            if len(self.object_history) > 10:
                del self.object_history[0]
            if self.current_menu == "main":
                print("Item history:")
                cnt = 0
                for o in self.object_history:
                    print(f"{cnt}: {o}", end="  ")
                    cnt += 1
                print("")
                print(f"Current item: {current_object.model}")
            if not (
                self.current_menu == "main"
                and game.config("settings")["menu_mode"] == "hidden"
            ):
                game.display_menu(self.current_menu, constants.ORIENTATION_VERTICAL, 15)
            for m in self.dbg_messages:
                base.Text.debug(m)
            for m in self.info_messages:
                base.Text.info(m)
            for m in self.warn_messages:
                base.Text.warn(m)
            if self.current_menu == "boards_list":
                key = input("Enter your choice (and hit ENTER): ")
            else:
                key = engine.Game.get_key()

        # Before saving we need to transform the object library into a reference
        # that json can understand. We keep only 10 objects for performance
        # and practicality reasons.
        reflib = []
        count = 0
        for o in game.config("settings")["object_library"]:
            # reflib.append(engine.Game._obj2ref(o))
            reflib.append(o.serialize())
            count += 1
            if count > 10:
                break
        game.config("settings")["object_library"] = reflib
        # Let's also save the partial display viewport
        game.config("settings")["partial_display_viewport"][0] = self.viewport_height
        game.config("settings")["partial_display_viewport"][1] = self.viewport_width
        game.save_config(
            "settings", os.path.join(self.editor_config_dir, "settings.json")
        )


def input_digit(msg):
    while True:
        result = input(msg)
        if result.isdigit() or result == "":
            return result


if __name__ == "__main__":
    PglEditor().main()
