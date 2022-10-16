#!/usr/bin/env python3

from pygamelib import base, engine, constants, board_items
from pygamelib import functions
from pygamelib.gfx import core, ui
from pygamelib.assets import graphics
from pygamelib.functions import clamp
from pathlib import Path
import argparse
import os
import sys
import time
import random
import copy
import webbrowser


class EditorVariables:
    def __init__(self) -> None:
        self.collection = None
        self.menu = None
        self.menu_idx = -1
        self.boxes = ["menu", "sprite", "info", "sprite_list", "toolbox", "brushes"]
        self.boxes_idx = 0
        self.tools = [
            "Create new brush",
            "Select model",
            "Select FG color",
            "Select BG color",
            "Remove BG color",
            "Remove FG color",
            "     ------     ",
            "Fill w/ FG color",
            "Fill w/ BG color",
            "     ------     ",
            "(E)raser mode",
            "(A)dd to brushes",
            "(R)andom brush",
            "     ------     ",
            "Rename sprite",
            "Duplicate sprite",
            "Delete sprite",
            "     ------     ",
            "Play animation",
        ]
        self.tools_idx = 0
        self.sprite_list = []
        self.sprite_list_idx = 0
        self.brushes = []
        self.brushes_idx = 0
        self.filename = ""
        self.start = time.time()
        self.frames = 0
        self.screen_dimensions = {"menu": 3, "central_zone": 15, "brushes": 7}
        self.ui_init = False
        self.eraser_mode = False
        self.current_sprixel = None
        self.previous_cursor_pos = [None, None]
        self.nav_increments = {
            "KEY_UP": -1,
            "KEY_DOWN": 1,
            "KEY_LEFT": -1,
            "KEY_RIGHT": 1,
        }
        self.ui_config = None
        self.ui_config_selected = None
        self.ui_config_popup = None
        self.brush_models = [
            " ",
            "!",
            "¡",
            "?",
            "¿",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "¯",
            "¸",
            "=",
            "+",
            "{",
            "}",
            "[",
            "]",
            ";",
            ":",
            ",",
            "/",
            "\\",
            "|",
            "`",
            "'",
            "´",
            "‘",
            "’",
            "“",
            '"',
            "”",
            "¨",
            "~",
        ]
        self.brush_models.extend(
            [
                str(getattr(graphics.BoxDrawings, elt))
                for elt in dir(graphics.BoxDrawings)
                if not elt.startswith("_")
            ]
        )
        self.brush_models.extend(
            [
                str(getattr(graphics.Blocks, elt))
                for elt in dir(graphics.Blocks)
                if not elt.startswith("_")
            ]
        )
        self.brush_models.extend(
            [
                str(getattr(graphics.GeometricShapes, elt))
                for elt in dir(graphics.GeometricShapes)
                if not elt.startswith("_")
            ]
        )
        # emojis = [
        #     str(getattr(graphics.Models, elt))
        #     for elt in dir(graphics.Models)
        #     if not elt.startswith("_")
        # ]
        # for e in emojis:
        #     sp = core.Sprixel(e)
        #     if sp.length == 1:
        #         self.brush_models.append(f"{e}")
        #     else:
        #         self.brush_models.append(e)

        self.copy_paste_state = "idle"
        self.copy_paste_start = [None, None]
        self.copy_paste_stop = [None, None]
        self.copy_paste_previous_stop = [None, None]
        self.copy_paste_sprite_idx = -1
        self.copy_paste_board_id = -1
        self.modified = False
        self.config_dir = Path.home().joinpath(Path(".pygamelib", "editor"))
        self.config_file = self.config_dir.joinpath("sprite_editor.json")


ev = EditorVariables()


def open_api_doc():
    webbrowser.open_new_tab("https://pygamelib.readthedocs.io")


def flood_fill(
    board: engine.Board,
    sprite: core.Sprite,
    r,
    c,
    replace: core.Sprixel,
    sprixel: core.Sprixel,
):
    if r < 0 or r >= board.height or c < 0 or c >= board.width:
        return
    # if not isinstance(board.item(r, c), board_items.BoardItemVoid):
    if board.item(r, c).sprixel != replace:
        return
    # if isinstance(board.item(r, c), board_items.BoardItemVoid):
    if board.item(r, c).sprixel == replace:
        board.place_item(board_items.Door(sprixel=sprixel.copy()), r, c)
        sprite.set_sprixel(r, c, sprixel.copy())
    flood_fill(board, sprite, r + 1, c, replace, sprixel)
    flood_fill(board, sprite, r - 1, c, replace, sprixel)
    flood_fill(board, sprite, r, c + 1, replace, sprixel)
    flood_fill(board, sprite, r, c - 1, replace, sprixel)


def draw_box(
    row: int, column: int, height: int, width: int, group: str = "", title: str = ""
):
    box = ui.Box(width, height, title, ev.ui_config)
    if ev.boxes[ev.boxes_idx % len(ev.boxes)] == group:
        box.config = ev.ui_config_selected
    engine.Game.instance().screen.place(box, row, column)


def draw_progress_bar(
    row: int,
    column: int,
    length: int,
    value: int,
    total: int,
    progress_marker=graphics.GeometricShapes.BLACK_RECTANGLE,
    empty_marker: str = " ",
    fg_color=core.Color(0, 0, 0),
    bg_color=core.Color(0, 128, 128),
):
    g = engine.Game.instance()
    prog = int((value * length) / total)
    pb = base.Text(
        progress_marker * prog + " " * (length - prog),
        fg_color=fg_color,
        bg_color=bg_color,
    )
    g.screen.place(pb, row, column, 2)
    g.screen.trigger_rendering()
    g.screen.update()


def display_help():
    g = engine.Game.instance()
    screen = g.screen
    ev.menu.current_entry().collapse()
    screen.force_update()
    bgc = ev.ui_config_popup.bg_color
    ev.ui_config_popup.bg_color = None
    msg = ui.MessageDialog(width=screen.width - 6, config=ev.ui_config_popup)
    msg.add_line("")
    msg.add_line(
        base.Text(
            "Help", core.Color(0, 200, 200), style=constants.BOLD + constants.UNDERLINE
        ),
        constants.ALIGN_CENTER,
    )
    msg.add_line("")
    msg.add_line(
        base.Text(
            "General Shortcuts", core.Color(0, 175, 175), style=constants.UNDERLINE
        )
    )
    msg.add_line("Tab: cycle through the panels or fields in dialogs.")
    msg.add_line("Shift + H: Display this help.")
    msg.add_line("Shift + S: Save the current sprite as (i.e: ask for the location).")
    msg.add_line("Shift + O: Open a sprite collection.")
    msg.add_line("Shift + B: Select the Brushes panel.")
    msg.add_line("Shift + L: Select the Sprite List panel.")
    msg.add_line("Shift + T: Select the Tools panel.")
    msg.add_line(
        "Shift + A: Add the current sprixel (see the info pannel) to the Brushes."
    )
    msg.add_line("Shift + R: Create a random brush and add it to the Brushes.")
    msg.add_line(
        f"{graphics.Models.UP_ARROW}/{graphics.Models.DOWN_ARROW}: Navigate up and"
        " down in panels."
    )
    msg.add_line("Esc.: Closes most of the dialog windows (including that one). ")
    msg.add_line("      A dialog does not return anything when closed with escape.")
    msg.add_line(
        "Enter: In most panels execute the action and return to the sprite canvas."
    )
    msg.add_line("       In dialogs (like this one) close and return the selection.")

    msg.add_line("")
    msg.add_line(
        base.Text(
            "Menubar specific shortcuts",
            core.Color(0, 175, 175),
            style=constants.UNDERLINE,
        )
    )
    msg.add_line(
        f"{graphics.Models.LEFT_ARROW}/{graphics.Models.RIGHT_ARROW}: Navigate left and"
        " right. Open and close submenus. "
    )
    msg.add_line(
        f"{graphics.Models.UP_ARROW}/{graphics.Models.DOWN_ARROW}: Navigate up and"
        " down in menus or submenus."
    )
    msg.add_line(
        "Esc.: Close the current menu or submenu. If no menu is open, select"
        " the sprite canvas."
    )
    msg.add_line("Enter: Activate a menu entry or open a menu or submenu.")

    msg.add_line("")
    msg.add_line(
        base.Text(
            "Sprite canvas specific shortcuts",
            core.Color(0, 175, 175),
            style=constants.UNDERLINE,
        )
    )
    msg.add_line("Shift + E: Switch between Edit and Erase mode.")
    msg.add_line("i/j/k/l: Place the selected sprixel on the sprite canvas an ")
    msg.add_line("         move up/left/right/up.")
    msg.add_line("Esc.: Select the menu bar.")
    msg.add_line("")
    msg.add_line(
        base.Text(
            "Sprite list specific shortcuts",
            core.Color(0, 175, 175),
            style=constants.UNDERLINE,
        )
    )
    msg.add_line("Enter: Select the sprite canvas.")
    msg.add_line("")
    msg.add_line(
        base.Text(
            "Tools specific shortcuts",
            core.Color(0, 175, 175),
            style=constants.UNDERLINE,
        )
    )
    msg.add_line("Esc.: Select the sprite canvas.")
    msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    # msg.add_line("")
    screen.place(msg, screen.vcenter - int(msg.height / 2), 3)
    msg.show()
    # screen.delete(screen.vcenter - int(msg.height / 2), 3)
    ev.ui_config_popup.bg_color = bgc


def draw_ui():
    g = engine.Game.instance()
    screen = g.screen
    spr_l_c_idx = ev.sprite_list_idx % len(ev.sprite_list)
    tb_c_idx = ev.tools_idx % len(ev.tools)
    # Draw the menu
    draw_box(0, 0, ev.screen_dimensions["menu"], screen.width, "menu")
    screen.place(ev.menu, 1, 2, 2)
    # +2 because we start at 1 and need +1 to move past the menubar
    col = ev.menu.length() + 2
    screen.place(core.Sprixel(graphics.BoxDrawings.LIGHT_TRIPLE_DASH_VERTICAL), 1, col)
    # Draw the sprite edition area
    title = "Sprite"
    if ev.filename != "":
        title += f": {ev.sprite_list[spr_l_c_idx]} @ {ev.filename}"
    draw_box(3, 0, screen.height - 10, screen.width - 21, "sprite", title)
    screen.place(g.current_board(), 4, 1)
    # Right side bar
    # Positions
    info_row = 3
    spr_lst_row = info_row + 9
    tb_start_row = spr_lst_row + int((screen.height - 10) / 3) + 1
    # Draw the info box
    draw_box(info_row, screen.width - 20, spr_lst_row - info_row, 20, "info", "Infos")
    # Draw the sprite list
    sprite_list_box_height = int((screen.height - 10) / 3) + 1
    # Sprite list is fairly dynamic so we clear it first
    for idx in range(sprite_list_box_height):
        screen.delete(spr_lst_row + 1 + idx, screen.width - 18)
    draw_box(
        spr_lst_row,
        screen.width - 20,
        sprite_list_box_height,
        20,
        "sprite_list",
        "Sprites list",
    )
    idx = rs = 0
    end = len(ev.sprite_list)
    if len(ev.sprite_list) > sprite_list_box_height - 2:
        rs = int(spr_l_c_idx / (sprite_list_box_height - 2)) * (
            sprite_list_box_height - 2
        )
    end = functions.clamp(end, rs, sprite_list_box_height - 2 + rs)
    for k in range(rs, end):
        s = ev.sprite_list[k]
        if idx + rs == spr_l_c_idx:
            screen.place(
                base.Text(s, fg_color=core.Color(0, 255, 0), style=constants.BOLD),
                spr_lst_row + 1 + idx,
                screen.width - 18,
            )
        else:
            screen.place(base.Text(s), spr_lst_row + 1 + idx, screen.width - 18)
        idx += 1
    # Draw the toolbox
    # tb_start_row = int((screen.height - 10) / 3) + 4
    tb_start_col = screen.width - 20
    tb_box_height = screen.height - tb_start_row
    # Sprite list is fairly dynamic so we clear it first
    for idx in range(tb_box_height - 1):
        screen.delete(tb_start_row + 1 + idx, tb_start_col + 2)
    draw_box(
        tb_start_row,
        tb_start_col,
        tb_box_height,
        20,
        "toolbox",
        "Tools",
    )
    idx = rt = 0
    end = len(ev.tools)
    if len(ev.tools) > tb_box_height - 2:
        rt = int(tb_c_idx / (tb_box_height - 2)) * (tb_box_height - 2)
    end = functions.clamp(end, rt, tb_box_height - 2 + rt)
    for i in range(rt, end):
        if idx + rt == tb_c_idx:
            screen.place(
                base.Text(
                    ev.tools[i], fg_color=core.Color(0, 255, 0), style=constants.BOLD
                ),
                tb_start_row + idx + 1,
                tb_start_col + 2,
            )
        else:
            screen.place(ev.tools[i], tb_start_row + idx + 1, tb_start_col + 2)
        idx += 1
    # Draw the brushes box
    draw_box(
        screen.height - ev.screen_dimensions["brushes"],
        0,
        ev.screen_dimensions["brushes"],
        screen.width - 21,
        "brushes",
        "Brushes",
    )
    pal_idx = 2
    nl = 0
    for i in range(0, len(ev.brushes)):
        screen.place(
            ev.brushes[i],
            screen.height - ev.screen_dimensions["brushes"] + 2 + nl,
            pal_idx,
        )
        # TODO: Adjust!!
        # g.log(
        #     'Place sprixel at '
        #     f'{screen.height - ev.screen_dimensions["brushes"] + 2 + nl} '
        #     f", {pal_idx} trying to fill null sprixels between {1 + pal_idx} and "
        #     f"{ 1 + pal_idx + ev.brushes[i].length} i={i}"
        # )
        # for c in range(1 + i + 1, 1 + i + ev.brushes[i].length):
        # for c in range(1 + pal_idx, 1 + pal_idx + ev.brushes[i].length):
        #     screen.place(
        #         core.Sprixel(),
        #         screen.height - ev.screen_dimensions["brushes"] + 2 + nl, c
        #     )
        # Draw the selector
        if ev.brushes_idx == i:
            sel = ui.Box(ev.brushes[i].length + 2, 3, config=ev.ui_config_selected)
            screen.place(
                sel,
                screen.height - ev.screen_dimensions["brushes"] + 1 + nl,
                pal_idx - 1,
            )
            ev.previous_cursor_pos = [
                screen.height - ev.screen_dimensions["brushes"] + 1 + nl,
                pal_idx - 1,
            ]
        pal_idx += 2
        if pal_idx >= screen.width - 23:
            if nl == 2:
                ev.brushes = ev.brushes[0:i]
                break
            else:
                nl += 2
                pal_idx = 2
    # not testing and affecting all the time might be faster than testing before
    # affectation
    ev.ui_init = True


def update_sprite_info(g: engine.Game, sprite_name: str):
    g.screen.place(
        base.Text("Sprite size (WxH):", style=constants.BOLD),
        4,
        g.screen.width - 19,
    )
    g.screen.place(
        f"{ev.collection[sprite_name].width}x{ev.collection[sprite_name].height}",
        5,
        g.screen.width - 17,
    )


def update_cursor_info(g):
    g.screen.place(
        f"Cursor @ {g.player.row},{g.player.column}",
        6,
        g.screen.width - 19,
    )


def update_sprixel_under_cursor(g: engine.Game, v_move: base.Vector2D):
    b = g.current_board()
    r = g.player.row + v_move.row
    c = g.player.column + v_move.column
    if r >= 0 and r < b.height and c >= 0 and c < b.width:
        ev.current_sprixel = cell = b.render_cell(r, c)
        update_sprixel_info(g, cell)


def update_sprixel_info(g: engine.Game, cell: core.Sprixel):
    first_col = g.screen.width - 19
    txt = "Sprixel:"
    g.screen.place(
        base.Text(txt, style=constants.BOLD),
        7,
        first_col,
    )
    last_col = g.screen.width - 10
    g.screen.place(cell, 7, last_col)
    for c in range(last_col + 1, last_col + cell.length):
        g.screen.place(core.Sprixel(), 7, c)
    g.screen.place(f"Model: '{cell.model}'", 8, first_col)
    if cell.fg_color is not None:
        color = base.Text(
            f"({cell.fg_color.r},{cell.fg_color.g},{cell.fg_color.b})",
            fg_color=cell.fg_color,
        )
        g.screen.place(
            "FG:",
            9,
            first_col,
        )
        g.screen.place(
            color,
            9,
            first_col + 4,
        )
    else:
        g.screen.place("No foreground     ", 9, first_col)
    if cell.bg_color is not None:
        color = base.Text(
            f"({cell.bg_color.r},{cell.bg_color.g},{cell.bg_color.b})",
            fg_color=cell.bg_color,
        )
        g.screen.place(
            "BG:",
            10,
            first_col,
        )
        g.screen.place(
            color,
            10,
            first_col + 4,
        )
    else:
        # In case you read this and wonder why the spaces, the answer is what you
        # think: lazy programming.
        g.screen.place("No background     ", 10, first_col)
    # g.screen.place(f"{cell.bg_color}", 9, first_col)


def load_sprite_to_board(g: engine.Game, spr_c_idx: int):
    try:
        # This can fail if we just removed the board. We need to change level but we
        # can't yet. So let it fail silently.
        if g.current_board() is not None:
            try:
                # This call can fail if we just delete the sprite/board. In that case we
                # just have to ignore the error since it just means that we don't have
                # to care about it ;)
                g.current_board().remove_item(g.player)
            except base.PglException:
                pass
    except base.PglInvalidLevelException:
        pass
    spr_c_idx = spr_c_idx % len(ev.sprite_list)
    spr_name = ev.sprite_list[spr_c_idx]
    if ev.ui_init:
        diag = base.Text(
            f" Please wait, loading {spr_name} ",
            core.Color(0, 0, 0),
            core.Color(0, 128, 128),
        )
        tl = base.Console.instance().length(diag.text)
        dr = int((g.screen.height - 7) / 2)
        dc = int((g.screen.width - 21) / 2) - int(tl / 2)
        progress_bar = ui.ProgressDialog(diag, 0, tl, tl, config=ev.ui_config)
        g.screen.place(progress_bar, dr, dc, 2)
        g.screen.trigger_rendering()
        g.screen.update()
    void_sprixel_model = "X"
    # Pick 3 points to determine the sprite's sprixel size
    if (
        ev.collection[spr_name].sprixel(0, 0).length == 2
        and ev.collection[spr_name]
        .sprixel(
            int(ev.collection[spr_name].size[1] / 2),
            int(ev.collection[spr_name].size[0] / 2),
        )
        .length
        == 2
        and ev.collection[spr_name]
        .sprixel(
            ev.collection[spr_name].size[1] - 1, ev.collection[spr_name].size[0] - 1
        )
        .length
        == 2
    ):
        g.player.sprixel = core.Sprixel(
            graphics.BoxDrawings.HEAVY_VERTICAL_AND_LEFT
            + graphics.BoxDrawings.HEAVY_VERTICAL_AND_RIGHT,
            fg_color=core.Color(255, 0, 0),
        )
        void_sprixel_model = "XX"
    g.add_board(
        1 + spr_c_idx,
        engine.Board(
            ui_borders="",
            size=ev.collection[spr_name].size,
            ui_board_void_cell_sprixel=core.Sprixel(void_sprixel_model),
            DISPLAY_SIZE_WARNINGS=False,
            player_starting_position=[0, 0],
        ),
    )

    board = g.get_board(1 + spr_c_idx)
    total = board.width * board.height
    if ev.ui_init:
        progress_bar.value = 1
        g.screen.update()
        progress_bar.maximum = total
    cidx = 0
    null_sprixel = core.Sprixel()
    last_prog = 0
    for r in range(board.height):
        for c in range(board.width):
            if ev.collection[spr_name].sprixel(r, c) == null_sprixel:
                cidx += 1
                continue
            board.place_item(
                board_items.Door(sprixel=ev.collection[spr_name].sprixel(r, c)), r, c
            )
            if ev.ui_init:
                cidx += 1
                prog = int((cidx * tl) / total)
                if prog > last_prog:
                    # draw_progress_bar(dr + 1, dc, tl, cidx, total)
                    progress_bar.value = cidx
                    g.screen.update()
                    last_prog = prog
    if (
        ev.collection[spr_name].size[0] >= g.screen.height - 12
        or ev.collection[spr_name].size[1] >= g.screen.width - 23
    ):
        board.enable_partial_display = True
        board.partial_display_viewport = [
            int((g.screen.height - 12) / 2),
            int((g.screen.width - 23) / 2),
        ]
        board.partial_display_focus = g.player

    # [DIRTY HACK]
    # There is a bug somewhere in the code that place the player on the board and the
    # arrival position's sprixel is lost. By doing that swap, we ensure that the board
    # loads correctly and is correctly displayed.
    player = g.player
    g.player = constants.NO_PLAYER
    g.change_level(1 + spr_c_idx)
    g.player = player
    # Reset the background color so we don have any artifact
    g.player.sprixel.bg_color = None
    g.current_board().place_item(g.player, 0, 0)
    # [/DIRTY HACK]
    update_sprite_info(g, spr_name)
    if ev.ui_init:
        g.screen.delete(dr, dc)
        g.screen.delete(dr + 1, dc)


def erase_cell(g: engine.Game, row: int, column: int):
    g.current_board().clear_cell(row, column)


def toggle_eraser_mode(screen: engine.Screen):
    ev.eraser_mode = not ev.eraser_mode
    if ev.eraser_mode:
        txt = base.Text(
            "ERASER MODE ON",
            fg_color=core.Color(255, 0, 0),
            style=constants.BOLD,
        )
        screen.place(txt, 1, screen.hcenter)
        engine.Game.instance().player.sprixel.fg_color = core.Color(255, 0, 0)
    else:
        engine.Game.instance().player.sprixel.fg_color = core.Color(0, 255, 0)
        screen.delete(1, screen.hcenter)


def delete_current_sprite(g: engine.Game):
    _current_sprite_idx = ev.sprite_list_idx % len(ev.sprite_list)
    del ev.collection[ev.sprite_list[_current_sprite_idx]]
    g.delete_level(_current_sprite_idx + 1)
    last_moved_idx = None
    moved = 0
    try:
        for lvl in range(_current_sprite_idx + 2, len(ev.sprite_list)):
            if g.get_board(lvl) is not None:
                g.add_board(lvl - 1, g.get_board(lvl))
                moved += 1
                last_moved_idx = lvl
    except KeyError:
        pass
    if moved > 1:
        g.delete_level(last_moved_idx)
    # ev.sprite_list = list(ev.collection.keys())
    del ev.sprite_list[_current_sprite_idx]
    ev.sprite_list_idx = _current_sprite_idx
    load_sprite_to_board(g, ev.sprite_list_idx)


def is_blended(item):
    return hasattr(item, "blended") and getattr(item, "blended")


def update_copy_paste(g: engine.Game):
    if ev.copy_paste_state == "selecting":
        ev.copy_paste_previous_stop = ev.copy_paste_stop
        ev.copy_paste_stop = g.player.pos
    if ev.copy_paste_state == "selecting" or ev.copy_paste_state == "selected":
        start_row = min(ev.copy_paste_start[0], ev.copy_paste_stop[0])
        stop_row = max(ev.copy_paste_start[0], ev.copy_paste_stop[0])
        start_col = min(ev.copy_paste_start[1], ev.copy_paste_stop[1])
        stop_col = max(ev.copy_paste_start[1], ev.copy_paste_stop[1])
        dst_to_start = base.Math.distance(
            ev.copy_paste_start[0],
            ev.copy_paste_start[1],
            ev.copy_paste_stop[0],
            ev.copy_paste_stop[1],
        )
        previous_dst_to_start = base.Math.distance(
            ev.copy_paste_start[0],
            ev.copy_paste_start[1],
            ev.copy_paste_previous_stop[0],
            ev.copy_paste_previous_stop[1],
        )
        if dst_to_start < previous_dst_to_start:
            # clear_copy_paste(g)
            # delete previously selected column
            start = ev.copy_paste_start[0]
            stop = ev.copy_paste_previous_stop[0]
            if ev.copy_paste_previous_stop[0] < ev.copy_paste_start[0]:
                stop = ev.copy_paste_start[0]
                start = ev.copy_paste_previous_stop[0]
            for cpr in range(start, stop + 1):
                item = g.get_board(ev.copy_paste_board_id).item(
                    cpr, ev.copy_paste_previous_stop[1]
                )
                if item.sprixel is not None:
                    if hasattr(item, "_original_bg_color"):
                        item.sprixel.bg_color = getattr(item, "_original_bg_color")
                    if hasattr(item, "_original_fg_color"):
                        item.sprixel.fg_color = getattr(item, "_original_fg_color")
                    setattr(item, "blended", False)
            # delete previously selected row
            start = ev.copy_paste_start[1]
            stop = ev.copy_paste_previous_stop[1]
            if ev.copy_paste_previous_stop[1] < ev.copy_paste_start[1]:
                stop = ev.copy_paste_start[1]
                start = ev.copy_paste_previous_stop[1]
            for cpr in range(start, stop + 1):
                item = g.get_board(ev.copy_paste_board_id).item(
                    ev.copy_paste_previous_stop[0], cpr
                )
                if item.sprixel is not None:
                    if hasattr(item, "_original_bg_color"):
                        item.sprixel.bg_color = getattr(item, "_original_bg_color")
                    if hasattr(item, "_original_fg_color"):
                        item.sprixel.fg_color = getattr(item, "_original_fg_color")
                    setattr(item, "blended", False)

        for cpr in range(start_row, stop_row + 1):
            for cpc in range(start_col, stop_col + 1):
                item = g.get_board(ev.copy_paste_board_id).item(cpr, cpc)
                if item.sprixel is not None:
                    if not is_blended(item):
                        setattr(item, "_original_bg_color", item.sprixel.bg_color)
                        setattr(item, "_original_fg_color", item.sprixel.fg_color)
                        if item.sprixel.bg_color is not None:
                            item.sprixel.bg_color = item.sprixel.bg_color.blend(
                                core.Color(0, 255, 200)
                            )
                        else:
                            item.sprixel.bg_color = core.Color(0, 255, 200)
                        if item.sprixel.fg_color is not None:
                            item.sprixel.fg_color = item.sprixel.fg_color.blend(
                                core.Color(0, 255, 200)
                            )
                        else:
                            item.sprixel.fg_color = core.Color(0, 255, 200)
                        setattr(item, "blended", True)


def clear_copy_paste(g):
    start_row = min(ev.copy_paste_start[0], ev.copy_paste_stop[0])
    stop_row = max(ev.copy_paste_start[0], ev.copy_paste_stop[0])
    start_col = min(ev.copy_paste_start[1], ev.copy_paste_stop[1])
    stop_col = max(ev.copy_paste_start[1], ev.copy_paste_stop[1])
    # spr_c_idx = ev.copy_paste_sprite_idx % len(ev.sprite_list)
    # spr_name = ev.sprite_list[spr_c_idx]
    for cpr in range(start_row, stop_row + 1):
        for cpc in range(start_col, stop_col + 1):
            item = g.get_board(ev.copy_paste_board_id).item(cpr, cpc)
            if item.sprixel is not None:
                # item.sprixel = copy.deepcopy(ev.collection[spr_name].sprixel(
                #   cpr,
                #   cpc)
                # )
                if hasattr(item, "_original_bg_color"):
                    item.sprixel.bg_color = getattr(item, "_original_bg_color")
                if hasattr(item, "_original_fg_color"):
                    item.sprixel.fg_color = getattr(item, "_original_fg_color")
                setattr(item, "blended", False)


def paste_clipboard(g: engine.Game):
    clip_spr_c_idx = ev.copy_paste_sprite_idx % len(ev.sprite_list)
    clip_spr_name = ev.sprite_list[clip_spr_c_idx]
    clip_sprite = ev.collection[clip_spr_name]
    _current_sprite = ev.collection[
        ev.sprite_list[ev.sprite_list_idx % len(ev.sprite_list)]
    ]
    sr = g.player.row
    sc = g.player.column
    # Get the curseur out of the way
    b = g.current_board()
    b.remove_item(g.player)
    b.place_item(g.player, sr, sc, 1)
    start_row = min(ev.copy_paste_start[0], ev.copy_paste_stop[0])
    stop_row = max(ev.copy_paste_start[0], ev.copy_paste_stop[0])
    start_col = min(ev.copy_paste_start[1], ev.copy_paste_stop[1])
    stop_col = max(ev.copy_paste_start[1], ev.copy_paste_stop[1])
    clear_copy_paste(g)
    for r in range(start_row, stop_row + 1):
        if sr + r - start_row >= _current_sprite.height:
            break
        for c in range(start_col, stop_col + 1):
            if sc + c - start_col >= _current_sprite.width:
                break
            sprix = clip_sprite.sprixel(r, c)
            if sprix != core.Sprixel():
                b.place_item(
                    board_items.Door(sprixel=copy.copy(sprix)),
                    sr + r - start_row,
                    sc + c - start_col,
                    0,
                )
            else:
                b.place_item(
                    b.generate_void_cell(), sr + r - start_row, sc + c - start_col, 0
                )
            _current_sprite.set_sprixel(sr + r - start_row, sc + c - start_col, sprix)


def open_file(file=None):
    g = engine.Game.instance()
    screen = g.screen
    ev.menu.close()
    if file is None:
        width = int(screen.width / 3)
        default = Path(ev.filename)
        fid = ui.FileDialog(
            default.parent,
            width,
            10,
            "Open a sprite collection",
            filter="*.spr",
            config=ev.ui_config_popup,
        )
        screen.place(fid, screen.vcenter - 5, screen.hcenter - int(width / 2))
        file = fid.show()
    # g.log(f"Got file={file} from FileDialog")
    # screen.delete(screen.vcenter - 5, screen.hcenter - int(width / 2))
    if file is not None and not file.is_dir():
        ev.collection = core.SpriteCollection.load_json_file(file)
        # ev.sprite_list = sorted(list(ev.collection.keys()))
        ev.sprite_list = list(ev.collection.keys())
        ev.filename = str(file)
        g.delete_all_levels()
        if len(ev.collection) > 0:
            load_sprite_to_board(g, 0)
        ma = ui.MenuAction(
            ev.filename, open_file, parameter=file, config=ev.menu.config
        )
        if ev.menu.entries[0].entries[1].entries[0].title.text == "No recent file":
            ev.menu.entries[0].entries[1].entries[0] = ma
        elif ev.filename not in [
            entry.title.text for entry in ev.menu.entries[0].entries[1].entries
        ]:
            ev.menu.entries[0].entries[1].add_entry(ma)
    screen.force_update()


def save_workspace_as() -> None:
    screen = engine.Game.instance().screen
    width = int(screen.width / 3)
    default = Path(ev.filename)
    fid = ui.FileDialog(
        default.parent,
        width,
        10,
        "Save as",
        filter="*.spr",
        config=ev.ui_config_popup,
    )
    screen.place(fid, screen.vcenter - 5, screen.hcenter - int(width / 2))
    file = fid.show()
    # g.log(f"Got file={file} from FileDialog")
    # screen.delete(screen.vcenter - 5, screen.hcenter - int(width / 2))
    if file is not None and not file.is_dir():
        ev.filename = str(file)
        save_workspace()


def save_workspace() -> None:
    screen = engine.Game.instance().screen

    for spr_id in range(0, len(ev.sprite_list)):
        spr_name = ev.sprite_list[spr_id]
        sprite = ev.collection[spr_name]
        try:
            board = g.get_board(1 + spr_id)
        except Exception:
            continue
        sprite_set_sprixel = sprite.set_sprixel
        board_item = board.item
        if ev.ui_init:
            diag = base.Text(
                f" Please wait, saving {spr_name} ",
                core.Color(0, 0, 0),
                core.Color(0, 128, 128),
            )
            tl = diag.length
            dr = int((screen.height - 7) / 2)
            dc = int((screen.width - 21) / 2) - int(tl / 2)
            progress_bar = ui.ProgressDialog(diag, 0, tl, tl, config=ev.ui_config)
            screen.place(progress_bar, dr, dc, 2)
            screen.trigger_rendering()
            screen.update()
            total = board.width * board.height
            screen.update()
            progress_bar.maximum = total
        cidx = 0
        prog = 0
        last_prog = 0
        for r in range(sprite.height):
            for c in range(sprite.width):
                csprix = board_item(r, c).sprixel
                if board_item(r, c) == g.player:
                    cidx += 1
                    csprix = ev.current_sprixel
                if csprix is None or csprix.model == "X" or csprix.model == "XX":
                    sprite_set_sprixel(r, c, core.Sprixel())
                else:
                    sprite_set_sprixel(r, c, csprix)
                if ev.ui_init:
                    cidx += 1
                    prog = int((cidx * tl) / total)
                    if prog > last_prog:
                        # draw_progress_bar(dr + 1, dc, tl, cidx, total)
                        progress_bar.value = cidx
                        g.screen.update()
                        last_prog = prog
        if ev.ui_init:
            screen.delete(dr, dc)
    # TODO: create a wait dialog
    ev.collection.to_json_file(ev.filename)


def edit_paste() -> None:
    ev.copy_paste_state = "pasted"
    paste_clipboard(engine.Game.instance())


def edit_copy() -> None:
    if ev.boxes_idx != ev.boxes.index("sprite"):
        ev.boxes_idx = ev.boxes.index("sprite")
        # Close the menubar just in case
        ev.menu.close()
    g = engine.Game.instance()
    if ev.copy_paste_start != [None, None] and ev.copy_paste_stop != [
        None,
        None,
    ]:
        clear_copy_paste(g)
    ev.copy_paste_start = g.player.pos
    ev.copy_paste_stop = g.player.pos
    ev.copy_paste_sprite_idx = ev.sprite_list_idx
    ev.copy_paste_board_id = g.current_level
    ev.copy_paste_state = "selecting"


def edit_new_sprite() -> None:
    g = engine.Game.instance()
    screen = g.screen
    fields = [
        {
            "label": "Enter the height of the new sprite:",
            "default": "",
            "filter": constants.INTEGER_FILTER,
        },
        {
            "label": "Enter the width of the new sprite:",
            "default": "",
            "filter": constants.INTEGER_FILTER,
        },
        {
            "label": "Enter the name of the new sprite:",
            "default": f"Sprite {len(ev.sprite_list)}",
            "filter": constants.PRINTABLE_FILTER,
        },
    ]
    minp = ui.MultiLineInputDialog(
        title="New sprite", fields=fields, config=ev.ui_config_popup
    )
    screen.place(minp, screen.vcenter - len(fields), screen.hcenter - 18)
    filled_fields = minp.show()
    # screen.delete(screen.vcenter - len(fields), screen.hcenter - 18)
    if (
        filled_fields[0]["user_input"] != ""
        and filled_fields[1]["user_input"] != ""
        and filled_fields[2]["user_input"] != ""
    ):
        nn = filled_fields[2]["user_input"]
        ev.collection[nn] = core.Sprite(
            size=[
                int(filled_fields[1]["user_input"]),
                int(filled_fields[0]["user_input"]),
            ]
        )
        ev.collection[nn].name = nn
        ev.sprite_list.append(nn)
        ev.sprite_list_idx = len(ev.sprite_list) - 1
        load_sprite_to_board(g, ev.sprite_list_idx)
        ev.boxes_idx = ev.boxes.index("sprite")


def edit_new_brush():
    g = engine.Game.instance()
    screen = g.screen
    bgc = ev.ui_config_popup.bg_color
    ev.ui_config_popup.bg_color = None
    msg = ui.MessageDialog(width=screen.width - 6, config=ev.ui_config_popup)
    msg.add_line("")
    msg.add_line(
        base.Text(
            "Create brush",
            core.Color(0, 200, 200),
            style=constants.BOLD + constants.UNDERLINE,
        ),
        constants.ALIGN_CENTER,
    )
    msg.add_line("")
    msg.add_line("This wizard will guide you into creating a new brush.")
    msg.add_line(
        "You will need to select a model, a forground color and a background " "color."
    )
    msg.add_line("")
    msg.add_line(
        "The model is mandatory, however you can hit ESC on any of the color "
        "choice if you don't need a specific color."
    )
    msg.add_line("For example, hit ESC if you don't need a background color.")
    msg.add_line("")
    msg.add_line("Press ENTER to continue or ESC to cancel.")
    screen.place(msg, screen.vcenter - int(msg.height / 2), 3)
    key_pressed = msg.show()
    ev.ui_config_popup.bg_color = bgc
    if key_pressed.name == "KEY_ENTER":
        width = int(screen.width / 2)
        height = 15
        gs = ui.GridSelectorDialog(
            ev.brush_models,
            height,
            width,
            "Select a brush model",
            config=ev.ui_config_popup,
        )
        screen.place(
            gs,
            int(screen.vcenter - (height / 2)),
            int(screen.hcenter - (width / 2)),
            2,
        )
        sprix = gs.show()
        if sprix is not None and sprix.model != "":
            model = sprix.model
            cp = ui.ColorPickerDialog(
                "Pick a FOREGROUND color", config=ev.ui_config_popup
            )
            screen.place(cp, screen.vcenter, screen.hcenter - 13)
            fg_color = cp.show()
            cp.set_color(core.Color(128, 128, 128))
            cp.set_selection(0)
            cp.title = "Pick a BACKGROUND color"
            screen.place(cp, screen.vcenter, screen.hcenter - 13)
            bg_color = cp.show()
            ev.brushes.append(core.Sprixel(model, bg_color, fg_color))


def update_screen(g: engine.Game, inkey, dt: float):
    redraw_ui = True
    screen = g.screen
    boxes_current_id = ev.boxes_idx % len(ev.boxes)
    _current_sprite = ev.collection[
        ev.sprite_list[ev.sprite_list_idx % len(ev.sprite_list)]
    ]
    # if inkey.is_sequence:
    #     g.log("got sequence: {0}.".format((str(inkey), inkey.name, inkey.code)))
    if inkey == "Q":
        g.stop()
    elif inkey == "R" or (
        inkey.name == "KEY_ENTER"
        and ev.boxes[boxes_current_id] == "toolbox"
        and ev.tools[ev.tools_idx % len(ev.tools)] == "(R)andom brush"
    ):
        bg = core.Color()
        bg.randomize()
        fg = core.Color()
        fg.randomize()
        ev.brushes.append(core.Sprixel(random.choice(ev.brush_models), bg, fg))
    elif inkey == "B":
        if ev.boxes[boxes_current_id] != "brushes":
            ev.boxes_idx = ev.boxes.index("brushes")
    elif inkey == "L":
        if ev.boxes[boxes_current_id] != "sprite_list":
            ev.boxes_idx = ev.boxes.index("sprite_list")
    elif inkey == "T":
        if ev.boxes[boxes_current_id] != "toolbox":
            ev.boxes_idx = ev.boxes.index("toolbox")
    elif inkey == "H":
        display_help()
    elif inkey == "O":
        open_file()
    elif inkey == "S":
        save_workspace()
        redraw_ui = False
    elif inkey == "N":
        edit_new_sprite()
    elif inkey == "U":
        edit_new_brush()
    elif inkey.name == "KEY_TAB":
        ev.boxes_idx += 1
        ev.menu.close()
    elif ev.boxes[boxes_current_id] == "menu":
        # if ev.ui_init:
        #     ev.menu.activate()
        #     ev.boxes_idx = ev.boxes.index("sprite")
        if inkey == engine.key.DOWN:
            if ev.menu.current_entry() is not None:
                ev.menu.current_entry().activate()
        elif inkey == engine.key.LEFT:
            ev.menu.select_previous()
        elif inkey == engine.key.RIGHT:
            ev.menu.select_next()
        elif inkey.name == "KEY_ENTER":
            if ev.menu.current_entry() is not None:
                ev.menu.current_entry().activate()
        elif inkey.name == "KEY_ESCAPE":
            ev.boxes_idx = ev.boxes.index("sprite")
            ev.menu.close()
        else:
            redraw_ui = False
    elif ev.boxes[boxes_current_id] == "sprite":
        if inkey == engine.key.UP:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.UP, 1)
            )
            pos = g.player.pos
            g.move_player(constants.UP, 1)
            update_cursor_info(g)
            update_copy_paste(g)
        elif inkey == engine.key.DOWN or inkey.name == "KEY_ENTER":
            if inkey.name == "KEY_ENTER" and ev.copy_paste_state == "selecting":
                ev.copy_paste_state = "selected"
            else:
                update_sprixel_under_cursor(
                    g, base.Vector2D.from_direction(constants.DOWN, 1)
                )
                pos = g.player.pos
                g.move_player(constants.DOWN, 1)
                update_cursor_info(g)
                update_copy_paste(g)
        elif inkey == engine.key.LEFT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.LEFT, 1)
            )
            pos = g.player.pos
            g.move_player(constants.LEFT, 1)
            update_cursor_info(g)
            update_copy_paste(g)
        elif inkey == engine.key.RIGHT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.RIGHT, 1)
            )
            pos = g.player.pos
            g.move_player(constants.RIGHT, 1)
            update_cursor_info(g)
            update_copy_paste(g)
        elif inkey == "j":
            pos = g.player.pos
            if g.player.column - 1 >= 0:
                g.move_player(constants.LEFT)
            else:
                g.move_player(constants.RIGHT)
            update_cursor_info(g)
            if ev.eraser_mode:
                erase_cell(g, pos[0], pos[1])
                _current_sprite.set_sprixel(pos[0], pos[1], core.Sprixel())
            elif len(ev.brushes) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=ev.brushes[ev.brushes_idx].copy()),
                    pos[0],
                    pos[1],
                    0,
                )
                _current_sprite.set_sprixel(pos[0], pos[1], ev.brushes[ev.brushes_idx])
        elif inkey == "l":
            pos = g.player.pos
            if g.player.column + 1 < g.current_board().width:
                g.move_player(constants.RIGHT)
            else:
                g.move_player(constants.LEFT)
            update_cursor_info(g)
            if ev.eraser_mode:
                erase_cell(g, pos[0], pos[1])
                _current_sprite.set_sprixel(pos[0], pos[1], core.Sprixel())
            elif len(ev.brushes) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=ev.brushes[ev.brushes_idx].copy()),
                    pos[0],
                    pos[1],
                )
                _current_sprite.set_sprixel(pos[0], pos[1], ev.brushes[ev.brushes_idx])
        elif inkey == "i":
            pos = g.player.pos
            if g.player.row - 1 >= 0:
                g.move_player(constants.UP)
            else:
                g.move_player(constants.DOWN)
            update_cursor_info(g)
            if ev.eraser_mode:
                erase_cell(g, pos[0], pos[1])
                _current_sprite.set_sprixel(pos[0], pos[1], core.Sprixel())
            elif len(ev.brushes) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=ev.brushes[ev.brushes_idx].copy()),
                    pos[0],
                    pos[1],
                )
                _current_sprite.set_sprixel(pos[0], pos[1], ev.brushes[ev.brushes_idx])
        elif inkey == "k":
            pos = g.player.pos
            if g.player.row + 1 < g.current_board().height:
                g.move_player(constants.DOWN)
            else:
                g.move_player(constants.UP)
            update_cursor_info(g)
            if ev.eraser_mode:
                erase_cell(g, pos[0], pos[1])
                _current_sprite.set_sprixel(pos[0], pos[1], core.Sprixel())
            elif len(ev.brushes) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=ev.brushes[ev.brushes_idx].copy()),
                    pos[0],
                    pos[1],
                )
                _current_sprite.set_sprixel(pos[0], pos[1], ev.brushes[ev.brushes_idx])
        elif inkey == "E":
            toggle_eraser_mode(screen)
        elif inkey == "A" and ev.current_sprixel is not None:
            ev.brushes.append(ev.current_sprixel)
        elif inkey.isdigit() and int(inkey) < len(ev.brushes) + 1:
            screen.delete(ev.previous_cursor_pos[0], ev.previous_cursor_pos[1])
            ev.brushes_idx = int(inkey) - 1
            if ev.brushes_idx < 0:
                ev.brushes_idx = 9
        elif inkey.name == "KEY_BACKSPACE":
            if g.player.column - 1 >= 0:
                g.current_board().clear_cell(g.player.row, g.player.column - 1)
                _current_sprite.set_sprixel(
                    g.player.row, g.player.column - 1, core.Sprixel()
                )
                g.move_player(constants.LEFT)
                update_cursor_info(g)
        # blessed documentation explicitely discourage making a difference between
        # KEY_DELETE and KEY_BACKSPACE but since we are in fullscreen mode, let's hope
        # that it'll work.
        elif inkey.name == "KEY_DELETE":
            pos = g.player.pos
            if g.player.column + 1 < g.current_board().width:
                g.move_player(constants.RIGHT)
            else:
                g.move_player(constants.LEFT)
            g.current_board().clear_cell(pos[0], pos[1])
            _current_sprite.set_sprixel(pos[0], pos[1], core.Sprixel())
            # Trying to move the player so fast makes is impossible in MODE_RT, so we
            # temporarily go to turn by turn and restore RT after.
            g.mode = constants.MODE_TBT
            v = base.Vector2D(0, pos[1] - g.player.column)
            g.current_board().move(g.player, v)
            g.mode = constants.MODE_RT
            update_cursor_info(g)
        elif inkey.name == "KEY_HOME":
            if g.player.column > 0:
                mvt = base.Vector2D(0, -g.player.column)
                g.move_player(mvt)
            else:
                mvt = base.Vector2D(-g.player.row, 0)
                g.move_player(mvt)
        elif inkey.name == "KEY_END":
            if g.player.column < g.current_board().width - 1:
                mvt = base.Vector2D(0, g.current_board().width - 1 - g.player.column)
                g.move_player(mvt)
            else:
                mvt = base.Vector2D(g.current_board().height - 1 - g.player.row, 0)
                g.move_player(mvt)
        elif inkey == "C":
            edit_copy()
            # if ev.copy_paste_start != [None, None] and ev.copy_paste_stop != [
            #     None,
            #     None,
            # ]:
            #     clear_copy_paste(g)
            # ev.copy_paste_start = g.player.pos
            # ev.copy_paste_stop = g.player.pos
            # ev.copy_paste_sprite_idx = ev.sprite_list_idx
            # ev.copy_paste_board_id = g.current_level
            # ev.copy_paste_state = "selecting"
        elif inkey == "V":
            edit_paste()
        elif inkey.name == "KEY_ESCAPE" and (
            ev.copy_paste_state == "selecting" or ev.copy_paste_state == "selected"
        ):
            ev.copy_paste_state = "none"
            clear_copy_paste(g)
        elif inkey.name == "KEY_ESCAPE":
            ev.boxes_idx = ev.boxes.index("menu")
        elif inkey is not None and inkey != "" and inkey.isprintable():
            # If the character is printable we just add it to the canvas
            sprixel = core.Sprixel(str(inkey))
            # look for available position to put the cursor: to the right by default,
            # else to the left
            pos = g.player.pos
            if g.player.column + 1 < g.current_board().width:
                g.move_player(constants.RIGHT)
            else:
                g.move_player(constants.LEFT)
            g.current_board().place_item(
                board_items.Door(sprixel=sprixel), pos[0], pos[1]
            )
            _current_sprite.set_sprixel(pos[0], pos[1], sprixel)
        else:
            redraw_ui = False
    elif ev.boxes[boxes_current_id] == "toolbox":
        if (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Select model"
        ):
            width = int(screen.width / 2)
            height = 15
            gs = ui.GridSelectorDialog(
                ev.brush_models,
                height,
                width,
                "Select a brush model",
                config=ev.ui_config_popup,
            )
            screen.place(
                gs,
                int(screen.vcenter - (height / 2)),
                int(screen.hcenter - (width / 2)),
                2,
            )
            sprix = gs.show()
            if (
                len(ev.brushes) > ev.brushes_idx
                and sprix is not None
                and sprix.model != ""
            ):
                ev.brushes[ev.brushes_idx].model = sprix.model
            # screen.delete(
            #     int(screen.vcenter - (height / 2)), int(screen.hcenter - (width / 2))
            # )
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Rename sprite"
        ):
            old_name = ev.sprite_list[ev.sprite_list_idx % len(ev.sprite_list)]
            edit = ui.LineInputDialog(
                "Rename sprite",
                "Enter the new sprite name:",
                old_name,
                config=ev.ui_config_popup,
            )
            screen.place(edit, screen.vcenter, screen.hcenter - 13)
            new_name = edit.show()
            if new_name != "":
                ev.collection.rename(old_name, new_name)
                ev.sprite_list[ev.sprite_list_idx % len(ev.sprite_list)] = new_name
                # ev.sprite_list = sorted(ev.sprite_list)
                # ev.sprite_list_idx = ev.sprite_list.index(new_name)
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Select FG color"
        ):
            cp = ui.ColorPickerDialog(config=ev.ui_config_popup)
            cp.set_color(ev.brushes[ev.brushes_idx].fg_color)
            screen.place(cp, screen.vcenter - 2, screen.hcenter - 13)
            color = cp.show()
            if len(ev.brushes) > ev.brushes_idx and color is not None:
                ev.brushes[ev.brushes_idx].fg_color = color
            # screen.delete(screen.vcenter - 2, screen.hcenter - 13)
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Select BG color"
        ):
            cp = ui.ColorPickerDialog(config=ev.ui_config_popup)
            cp.set_color(ev.brushes[ev.brushes_idx].bg_color)
            screen.place(cp, screen.vcenter - 2, screen.hcenter - 13)
            color = cp.show()
            if len(ev.brushes) > ev.brushes_idx and color is not None:
                ev.brushes[ev.brushes_idx].bg_color = color
            # screen.delete(screen.vcenter - 2, screen.hcenter - 13)
        elif inkey.name == "KEY_ENTER" and (
            ev.tools[ev.tools_idx % len(ev.tools)] == "Fill w/ FG color"
            or ev.tools[ev.tools_idx % len(ev.tools)] == "Fill w/ BG color"
        ):
            # Get the right color
            color = ev.brushes[ev.brushes_idx].fg_color
            if "BG" in ev.tools[ev.tools_idx % len(ev.tools)]:
                color = ev.brushes[ev.brushes_idx].bg_color
            # Create a sprixel with no model to fill the space with
            sprx = core.Sprixel(" ", color)
            # Clear the cursor so the flood fill algo doesn't stop right away
            g.current_board().clear_cell(g.player.row, g.player.column)
            # Fill
            flood_fill(
                g.current_board(),
                _current_sprite,
                g.player.row,
                g.player.column,
                ev.current_sprixel,
                sprx,
            )
            # Re place the cursor
            g.current_board().place_item(g.player, g.player.row, g.player.column)
            # Update the current sprixel info
            ev.current_sprixel = sprx
            update_sprixel_info(g, ev.current_sprixel)
            # Got to the edition canvas
            ev.boxes_idx = ev.boxes.index("sprite")
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "(E)raser mode"
        ):
            toggle_eraser_mode(screen)
            ev.boxes_idx = ev.boxes.index("sprite")
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Remove BG color"
        ):
            if len(ev.brushes) > ev.brushes_idx:
                ev.brushes[ev.brushes_idx].bg_color = None
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Remove FG color"
        ):
            if len(ev.brushes) > ev.brushes_idx:
                ev.brushes[ev.brushes_idx].fg_color = None
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "(A)dd to brushes"
        ):
            if ev.current_sprixel is not None:
                ev.brushes.append(ev.current_sprixel)
            ev.boxes_idx = ev.boxes.index("sprite")
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Duplicate sprite"
        ):
            spr_c_idx = ev.sprite_list_idx % len(ev.sprite_list)
            initial_sprite = ev.collection[ev.sprite_list[spr_c_idx]]
            new_sprite = initial_sprite.copy()
            new_sprite.name += " copy"
            for sr in range(initial_sprite.height):
                for sc in range(initial_sprite.width):
                    new_sprite.set_sprixel(sr, sc, initial_sprite.sprixel(sr, sc))
            ev.collection.add(new_sprite)
            # rebuild_sprite_list(g)x
            ev.sprite_list.append(new_sprite.name)
            ev.sprite_list_idx = len(ev.sprite_list) - 1
            # ev.sprite_list = list(ev.collection.keys())
            # ev.sprite_list_idx = ev.sprite_list.index(new_sprite.name)
            load_sprite_to_board(g, ev.sprite_list_idx)
            ev.boxes_idx = ev.boxes.index("sprite")
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Delete sprite"
        ):
            delete_current_sprite(g)
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Create new brush"
        ):
            edit_new_brush()
        elif (
            inkey.name == "KEY_ENTER"
            and ev.tools[ev.tools_idx % len(ev.tools)] == "Play animation"
        ):
            # a ui widget could be better here...
            anim = core.Animation(frames=ev.collection)
            loop = True
            # find the largest sprite name (and sprite)
            max_sprite_width = 0
            max_sprite_height = 0
            max_sprite_name_length = 0
            for f in anim.frames:
                if f.width - 2 >= screen.width or f.height - 4 >= screen.height:
                    err = f"The sprite '{f.name}' is too large to be displayed in full."
                    ts = len(err)
                    loop = False
                    bg = ev.ui_config_popup.bg_color
                    ev.ui_config_popup.bg_color = None
                    msg = ui.MessageDialog(
                        [
                            base.Text(err),
                            base.Text("Cancelling animation preview."),
                        ],
                        width=ts + 2,
                        config=ev.ui_config_popup,
                    )
                    screen.place(
                        msg,
                        screen.vcenter - 2,
                        screen.hcenter - int(ts / 2),
                    )
                    msg.show()
                    # screen.delete(screen.vcenter - 2, screen.hcenter - int(ts / 2))
                    ev.ui_config_popup.bg_color = bg
                    break
                if f.width > max_sprite_width:
                    max_sprite_width = f.width
                if f.height > max_sprite_height:
                    max_sprite_height = f.height
                if len(f.name) > max_sprite_name_length:
                    max_sprite_name_length = len(f.name)
            key = None

            if loop:
                box_width = max([max_sprite_name_length + 17, max_sprite_width + 2, 29])
                # -3 to account for the extra lines of info we're adding to the box
                arow = screen.vcenter - int(max_sprite_height / 2) - 3
                acol = screen.hcenter - int(box_width / 2)
                box = ui.Box(
                    width=box_width,
                    height=max_sprite_height + 7,
                    config=ev.ui_config_popup,
                    fill=False,
                    filling_sprixel=core.Sprixel(" "),
                )
                screen.place(box, arow, acol, 2)
            while loop:
                if key is not None:
                    if (
                        key.name == "KEY_ESCAPE"
                        or key == " "
                        or key.name == "KEY_ENTER"
                    ):
                        loop = False
                    elif key == "+":
                        anim.display_time += 0.01
                    elif key == "-":
                        anim.display_time -= 0.01
                        if anim.display_time < 0:
                            anim.display_time = 0
                    elif key.lower() == "r":
                        anim.frames.reverse()
                        # 27,3,15   118,201,214
                    for f in anim.frames:
                        screen.place(f"Current frame: {f.name}", arow + 1, acol + 1, 2)
                        screen.place(
                            f"Frame time: {round(anim.display_time,2)} sec.",
                            arow + 2,
                            acol + 1,
                            2,
                        )
                        screen.place(
                            "+ or -: change frame speed.", arow + 3, acol + 1, 2
                        )
                        screen.place("r to reverse frame order.", arow + 4, acol + 1, 2)
                        # # Clear previous frame
                        for cr in range(arow + 5, arow + 5 + f.height):
                            for cc in range(
                                acol + int(box_width / 2) - int(f.width / 2),
                                acol + int(box_width / 2) - int(f.width / 2) + f.width,
                            ):
                                screen.buffer[cr][cc] = " "
                        screen.place(
                            f, arow + 5, acol + int(box_width / 2) - int(f.width / 2), 2
                        )
                        screen.force_update()
                        time.sleep(anim.display_time)
                key = g.terminal.inkey(timeout=0.1)
            screen.delete(arow, acol)
            screen.delete(arow + 5, acol + int(box_width / 2) - int(f.width / 2))
            for r in range(1, 5):
                screen.delete(arow + r, acol + 1)

        elif inkey.name == "KEY_UP":
            ev.tools_idx -= 1
        elif inkey.name == "KEY_DOWN":
            ev.tools_idx += 1
        elif inkey.name == "KEY_ESCAPE":
            ev.boxes_idx = ev.boxes.index("sprite")
        else:
            redraw_ui = False
    elif ev.boxes[boxes_current_id] == "brushes":
        clean_cursor = True
        if inkey.name == "KEY_RIGHT":
            ev.brushes_idx += 1
        elif inkey.name == "KEY_LEFT":
            ev.brushes_idx -= 1
        elif inkey.name == "KEY_DOWN":
            # TODO : the -1 should probably be "- ev.brushes[ev.brushes_idx].length"
            ev.brushes_idx += int((screen.width - 23) / 2) - 1
        elif inkey.name == "KEY_UP":
            ev.brushes_idx -= int((screen.width - 23) / 2) - 1
        elif inkey.name == "KEY_ENTER":
            # If we hit the enter key, we go back to the sprite canvas
            ev.boxes_idx = ev.boxes.index("sprite")
        else:
            redraw_ui = False
            clean_cursor = False
        if clean_cursor and (
            ev.previous_cursor_pos[0] is not None
            and ev.previous_cursor_pos[1] is not None
        ):
            screen.delete(ev.previous_cursor_pos[0], ev.previous_cursor_pos[1])
        # Clamp the ev.brushes_idx between 0 and len of the list
        ev.brushes_idx = clamp(ev.brushes_idx, 0, len(ev.brushes) - 1)
    elif ev.boxes[boxes_current_id] == "sprite_list" and (
        inkey == engine.key.UP or inkey == engine.key.DOWN
    ):
        ev.sprite_list_idx += ev.nav_increments[inkey.name]
        # spr_c_idx = ev.sprite_list.index(
        #     sorted(ev.sprite_list)[ev.sprite_list_idx % len(ev.sprite_list)]
        # )
        spr_c_idx = ev.sprite_list_idx % len(ev.sprite_list)
        try:
            g.change_level(1 + spr_c_idx)
        except Exception:
            load_sprite_to_board(g, spr_c_idx)
        update_sprite_info(g, ev.sprite_list[spr_c_idx])
    elif (
        screen.height != screen.buffer.shape[0]
        or screen.width != screen.buffer.shape[1]
    ):
        screen.clear_buffers()
    elif inkey.name == "KEY_ENTER":
        if ev.boxes[boxes_current_id] != "sprite":
            ev.boxes_idx = ev.boxes.index("sprite")
    else:
        redraw_ui = False
    if redraw_ui or (ev.frames % 60) == 0:
        draw_ui()
        fps = f"FPS: {round(ev.frames / ((time.time() - ev.start)))}"
        screen.place(base.Text(fps), 1, screen.width - len(fps) - 2)
        ev.frames = 0
        ev.start = time.time()

    screen.update()
    ev.frames += 1


if __name__ == "__main__":
    print(
        base.Text(
            "The sprite editor is under heavy development and is not production ready."
            "If you find bugs or have feature requests please go to "
            "https://github.com/pygamelib/pygamelib/issues",
            core.Color(0, 150, 255),
            style=constants.BOLD,
        )
    )
    g = engine.Game.instance(
        player=board_items.Player(
            sprixel=core.Sprixel(
                graphics.BoxDrawings.HEAVY_VERTICAL_AND_HORIZONTAL,
                fg_color=core.Color(0, 255, 0),
            ),
            movement_speed=0.01,
        ),
        user_update=update_screen,
        mode=constants.MODE_RT,
        input_lag=0.0001,
    )
    g.DEBUG = True
    if ev.config_file.exists():
        g.load_config(ev.config_file, "editor_config")
        for spr_data in g.config("editor_config")["brushes"]:
            ev.brushes.append(core.Sprixel.load(spr_data))
    else:
        g.create_config("editor_config")
        g.config("editor_config")["brushes"] = []
        g.config("editor_config")["recent_files"] = []
    if g.screen.width < 102 or g.screen.height < 42:
        print(
            base.Text(
                "Your terminal window is too small, the sprite editor requires a"
                "console of 42 rows by 102 columns at minimum. Your terminal is "
                f"currently {g.screen.height} rows by {g.screen.width} columns",
                core.Color(255, 0, 0),
                style=constants.BOLD,
            )
        )
        sys.exit()
    parser = argparse.ArgumentParser(
        description="A tool to create/edit pygamelib's sprites."
    )
    parser.add_argument(
        "sprite_file", help="An sprite file to load and edit.", nargs="?", default=""
    )
    args = parser.parse_args()
    ev.collection = None
    if args.sprite_file != "" and os.path.exists(args.sprite_file):
        print(f"Loading sprite collection: {args.sprite_file}...", end="", flush=True)
        ev.collection = core.SpriteCollection.load_json_file(args.sprite_file)
        # ev.sprite_list = sorted(list(ev.collection.keys()))
        ev.sprite_list = list(ev.collection.keys())
        ev.filename = args.sprite_file
        print("done")
    else:
        ev.collection = core.SpriteCollection()
        ev.collection["default"] = core.Sprite(size=[16, 8])
        ev.collection["default"].name = "default"
        # ev.sprite_list = sorted(list(ev.collection.keys()))
        ev.sprite_list = list(ev.collection.keys())
        if args.sprite_file != "":
            ev.filename = args.sprite_file

    # TODO check for minimum size (84x34)
    ev.ui_config = ui.UiConfig(
        game=g, fg_color=core.Color(0, 0, 0), bg_color=core.Color(0, 128, 128)
    )
    ev.ui_config_selected = ui.UiConfig(game=g, border_fg_color=core.Color(0, 255, 0))
    ev.ui_config_popup = ui.UiConfig(
        game=g,
        fg_color=core.Color(0, 0, 0),
        bg_color=core.Color(0, 128, 128),
        borderless_dialog=False,
    )
    # Build menu
    ev.menu = ui.MenuBar(spacing=0, config=ev.ui_config)
    ev.menu.add_entry(
        ui.Menu(
            "File",
            [
                ui.MenuAction("Open", open_file),
                ui.Menu("Open recent >", [ui.MenuAction("No recent file", None)]),
                ui.MenuAction("Save", save_workspace),
                ui.MenuAction("Save As...", save_workspace_as),
                ui.MenuAction("Quit", g.stop),
            ],
        )
    )
    ev.menu.add_entry(
        ui.Menu(
            "Edit",
            [
                ui.MenuAction("Copy (Shift+C)", edit_copy),
                ui.MenuAction("Paste (Shift+V)", edit_paste),
                ui.MenuAction("New sprite", edit_new_sprite),
                ui.MenuAction("New brush", edit_new_brush),
            ],
        )
    )
    ev.menu.add_entry(
        ui.Menu(
            "Help",
            [
                ui.MenuAction("Quick help (Shift+H)", display_help),
                ui.MenuAction("Open documentation", open_api_doc),
            ],
        )
    )
    if (
        "recent_files" in g.config("editor_config")
        and len(g.config("editor_config")["recent_files"]) > 0
    ):
        for file_str in g.config("editor_config")["recent_files"]:
            file = Path(file_str)
            ma = ui.MenuAction(
                file_str, open_file, parameter=file, config=ev.menu.config
            )
            if ev.menu.entries[0].entries[1].entries[0].title.text == "No recent file":
                ev.menu.entries[0].entries[1].entries[0] = ma
            elif file_str not in [
                entry.title.text for entry in ev.menu.entries[0].entries[1].entries
            ]:
                ev.menu.entries[0].entries[1].add_entry(ma)
        file = Path(ev.filename).resolve()
        if str(file) not in [
            entry.title.text for entry in ev.menu.entries[0].entries[1].entries
        ]:
            ma = ui.MenuAction(
                str(file), open_file, parameter=file, config=ev.menu.config
            )
            if ev.menu.entries[0].entries[1].entries[0].title.text == "No recent file":
                ev.menu.entries[0].entries[1].entries[0] = ma
            else:
                ev.menu.entries[0].entries[1].add_entry(ma)
    # Default empty board.
    g.add_board(
        1,
        engine.Board(
            ui_borders="",
            size=[g.screen.width - 23, g.screen.height - 12],
            ui_board_void_cell_sprixel=core.Sprixel(" "),
            DISPLAY_SIZE_WARNINGS=False,
            player_starting_position=[0, 0],
        ),
    )
    g.change_level(1)
    ev.screen_dimensions["central_zone"] = g.screen.height - 10
    if len(ev.collection) > 0:
        load_sprite_to_board(g, 0)
    ev.start = time.time()
    g.run()
    # print(
    #     f"{ev.frames} ev.frames in {round(time.time()-ev.start,2)} secondes or "
    #     f"{round(ev.frames/(time.time()-ev.start))} FPS"
    # )

    # Save config file
    g.config("editor_config")["brushes"] = [spr.serialize() for spr in ev.brushes]
    g.config("editor_config")["recent_files"] = []
    for entry in ev.menu.entries[0].entries[1].entries:
        if entry.title.text == "No recent file":
            break
        else:
            g.config("editor_config")["recent_files"].append(entry.title.text)
    if not ev.config_dir.exists():
        ev.config_dir.mkdir(parents=True, exist_ok=True)
    g.save_config("editor_config", ev.config_file)
    # Display session logs if any
    for log in g.session_logs():
        print(log)
