#!/usr/bin/env python3

from pygamelib import base, engine, constants, board_items
from pygamelib.gfx import core, ui
from pygamelib.assets import graphics
from pygamelib.functions import clamp
from pathlib import Path
import argparse
import os
import time
import random
import copy


menu = ["File", "Edit", "Help"]
menu_idx = 0
boxes = ["menu", "sprite", "info", "sprite_list", "toolbox", "palette"]
boxes_idx = 0
tools = [
    "Create new brush",
    "Select model",
    "Select FG color",
    "Select BG color",
    "(E)raser mode",
    "(A)dd to palette",
    "(R)andom brush",
    "Rename sprite",
    "Duplicate sprite",
]
tools_idx = 0
sprite_list = []
sprite_list_idx = 0
palette = []
palette_idx = 0
filename = ""
start = time.time()
frames = 0
screen_dimensions = {"menu": 3, "central_zone": 15, "palette": 7}
ui_init = False
eraser_mode = False
current_sprixel = None
previous_cursor_pos = [None, None]
nav_increments = {
    "KEY_UP": -1,
    "KEY_DOWN": 1,
    "KEY_LEFT": -1,
    "KEY_RIGHT": 1,
}
ui_config = None
ui_config_selected = None
ui_config_popup = None
brush_models = [
    " ",
    "!",
    "?",
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
    "=",
    "+",
    "{",
    "}",
    "[",
    "]",
    ";",
    ":",
    ",",
    "'",
    '"',
    "/",
    "\\",
    "|",
    "`",
    "~",
]
brush_models.extend(
    [
        str(getattr(graphics.BoxDrawings, elt))
        for elt in dir(graphics.BoxDrawings)
        if not elt.startswith("_")
    ]
)
brush_models.extend(
    [
        str(getattr(graphics.Blocks, elt))
        for elt in dir(graphics.Blocks)
        if not elt.startswith("_")
    ]
)
brush_models.extend(
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
#         brush_models.append(f"{e} ")
#     else:
#         brush_models.append(e)

test = 0


def draw_box(
    row: int, column: int, height: int, width: int, group: str = "", title: str = ""
):
    global boxes_idx, boxes, ui_config, ui_config_selected
    box = ui.Box(width, height, title, ui_config)
    if boxes[boxes_idx % len(boxes)] == group:
        box.config = ui_config_selected
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
    g.screen.place(core.Sprite.from_text(pb), row, column, 2)
    g.screen.trigger_rendering()
    g.screen.update()


def draw_ui():
    global filename, collection, screen_dimensions, ui_init, palette
    global previous_cursor_pos
    g = engine.Game.instance()
    screen = g.screen
    spr_l_c_idx = sprite_list_idx % len(sprite_list)
    tb_c_idx = tools_idx % len(tools)
    # Draw the menu
    draw_box(0, 0, screen_dimensions["menu"], screen.width, "menu")
    col = 0
    for msg in menu:
        col += 2
        screen.place(msg, 1, col)
        col += len(msg)
    col += 1
    screen.place(core.Sprixel(graphics.BoxDrawings.LIGHT_TRIPLE_DASH_VERTICAL), 1, col)
    # Draw the sprite edition area
    title = "Sprite"
    if filename != "":
        title += f": {sprite_list[spr_l_c_idx]} @ {filename}"
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
    draw_box(
        spr_lst_row,
        screen.width - 20,
        int((screen.height - 10) / 3) + 1,
        20,
        "sprite_list",
        "Sprites list",
    )
    idx = 0
    for s in sprite_list:
        if idx == spr_l_c_idx:
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
    draw_box(
        tb_start_row,
        tb_start_col,
        screen.height - tb_start_row,
        20,
        "toolbox",
        "Tools",
    )
    for i in range(0, len(tools)):
        if i == tb_c_idx:
            screen.place(
                base.Text(
                    tools[i], fg_color=core.Color(0, 255, 0), style=constants.BOLD
                ),
                tb_start_row + i + 1,
                tb_start_col + 2,
            )
        else:
            screen.place(tools[i], tb_start_row + i + 1, tb_start_col + 2)
    # Draw the palette box
    draw_box(
        screen.height - screen_dimensions["palette"],
        0,
        screen_dimensions["palette"],
        screen.width - 21,
        "palette",
        "Palette",
    )
    pal_idx = 2
    nl = 0
    for i in range(0, len(palette)):
        screen.place(
            palette[i],
            screen.height - screen_dimensions["palette"] + 2 + nl,
            pal_idx,
        )
        # TODO: Adjust!!
        # g.log(
        #     f'Place sprixel at {screen.height - screen_dimensions["palette"] + 2 + nl} '
        #     f", {pal_idx} trying to fill null sprixels between {1 + pal_idx} and { 1 + pal_idx + palette[i].length} i={i}"
        # )
        # for c in range(1 + i + 1, 1 + i + palette[i].length):
        # for c in range(1 + pal_idx, 1 + pal_idx + palette[i].length):
        #     screen.place(
        #         core.Sprixel(), screen.height - screen_dimensions["palette"] + 2 + nl, c
        #     )
        # Draw the selector
        if palette_idx == i:
            sel = ui.Box(palette[i].length + 2, 3, config=ui_config_selected)
            screen.place(
                sel,
                screen.height - screen_dimensions["palette"] + 1 + nl,
                pal_idx - 1,
            )
            previous_cursor_pos = [
                screen.height - screen_dimensions["palette"] + 1 + nl,
                pal_idx - 1,
            ]
        pal_idx += 2
        if pal_idx >= screen.width - 23:
            if nl == 2:
                palette = palette[0:i]
                break
            else:
                nl += 2
                pal_idx = 2
    # not testing and affecting all the time might be faster than testing before
    # affectation
    ui_init = True


def update_sprite_info(g: engine.Game, sprite_name: str):
    global collection
    g.screen.place(
        base.Text("Sprite size (WxH):", style=constants.BOLD),
        4,
        g.screen.width - 19,
    )
    g.screen.place(
        f"{collection[sprite_name].width}x{collection[sprite_name].height}",
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
    global current_sprixel
    b = g.current_board()
    r = g.player.row + v_move.row
    c = g.player.column + v_move.column
    if r >= 0 and r < b.height and c >= 0 and c < b.width:
        first_col = g.screen.width - 19
        current_sprixel = cell = b.render_cell(r, c)
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


def load_sprite_to_board(g: engine.Game):
    global sprite_list, sprite_list_idx, ui_init, ui_config
    if g.current_board() is not None:
        g.current_board().remove_item(g.player)
    spr_c_idx = sprite_list_idx % len(sprite_list)
    spr_name = sprite_list[spr_c_idx]
    if ui_init:
        diag = base.Text(
            f" Please wait, loading {spr_name} ",
            core.Color(0, 0, 0),
            core.Color(0, 128, 128),
        )
        tl = base.Console.instance().length(diag.text)
        dr = int((g.screen.height - 7) / 2)
        dc = int((g.screen.width - 21) / 2) - int(tl / 2)
        progress_bar = ui.ProgressDialog(diag, 0, tl, tl, config=ui_config)
        g.screen.place(progress_bar, dr, dc, 2)
        g.screen.trigger_rendering()
        g.screen.update()
    void_sprixel_model = "X"
    # Pick 3 points to determine the sprite's sprixel size
    if (
        collection[spr_name].sprixel(0, 0).length == 2
        and collection[spr_name]
        .sprixel(
            int(collection[spr_name].size[1] / 2), int(collection[spr_name].size[0] / 2)
        )
        .length
        == 2
        and collection[spr_name]
        .sprixel(collection[spr_name].size[1] - 1, collection[spr_name].size[0] - 1)
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
            size=collection[spr_name].size,
            ui_board_void_cell_sprixel=core.Sprixel(void_sprixel_model),
            DISPLAY_SIZE_WARNINGS=False,
            player_starting_position=[0, 0],
        ),
    )

    board = g.get_board(1 + spr_c_idx)
    total = board.width * board.height
    if ui_init:
        progress_bar.value = 1
        g.screen.update()
        progress_bar.maximum = total
    cidx = 0
    null_sprixel = core.Sprixel()
    last_prog = 0
    for r in range(board.height):
        for c in range(board.width):
            if collection[spr_name].sprixel(r, c) == null_sprixel:
                cidx += 1
                continue
            board.place_item(
                board_items.Door(sprixel=collection[spr_name].sprixel(r, c)), r, c
            )
            if ui_init:
                cidx += 1
                prog = int((cidx * tl) / total)
                if prog > last_prog:
                    # draw_progress_bar(dr + 1, dc, tl, cidx, total)
                    progress_bar.value = cidx
                    g.screen.update()
                    last_prog = prog
    if (
        collection[spr_name].size[0] >= g.screen.height - 12
        or collection[spr_name].size[1] >= g.screen.width - 23
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
    if ui_init:
        g.screen.delete(dr, dc)
        g.screen.delete(dr + 1, dc)


def erase_cell(g: engine.Game, row: int, column: int):
    g.current_board().clear_cell(row, column)


def update_screen(g: engine.Game, inkey, dt: float):
    global boxes_idx, frames, boxes, sprite_list_idx, collection, start, nav_increments
    global eraser_mode, current_sprixel, filename, sprite_list, ui_config_popup
    global palette_idx, brush_models, tools_idx
    redraw_ui = True
    screen = g.screen
    boxes_current_id = boxes_idx % len(boxes)
    if inkey == "Q":
        g.stop()
    elif inkey == "R" or (
        inkey.name == "KEY_ENTER"
        and boxes[boxes_current_id] == "toolbox"
        and tools[tools_idx % len(tools)] == "(R)andom brush"
    ):
        bg = core.Color()
        bg.randomize()
        fg = core.Color()
        fg.randomize()
        palette.append(core.Sprixel(random.choice(brush_models), bg, fg))
    elif inkey == "P":
        if boxes[boxes_current_id] != "palette":
            boxes_idx = boxes.index("palette")
    elif inkey == "L":
        if boxes[boxes_current_id] != "sprite_list":
            boxes_idx = boxes.index("sprite_list")
    elif inkey == "T":
        if boxes[boxes_current_id] != "toolbox":
            boxes_idx = boxes.index("toolbox")
    elif inkey == "S":
        # FIXME: It looks like there is a bug, I have instances were the file is not saved
        width = int(screen.width / 3)
        default = Path()
        fid = ui.FileDialog(
            default, width, 10, "Save as", filter="*.spr", config=ui_config_popup
        )
        screen.place(fid, screen.vcenter - 5, screen.hcenter - int(width / 2))
        file = fid.show()
        # g.log(f"Got file={file} from FileDialog")
        screen.delete(screen.vcenter - 5, screen.hcenter - int(width / 2))
        if file != default and not file.is_dir():
            filename = str(file)
            # screen.place(
            #     f"Saving current sprite into {filename}",
            #     screen.height - 4,
            #     3,
            # )
            for spr_id in range(0, len(sprite_list)):
                spr_name = sprite_list[spr_id]
                sprite = collection[spr_name]
                try:
                    board = g.get_board(1 + spr_id)
                except Exception:
                    continue
                sprite_set_sprixel = sprite.set_sprixel
                board_item = board.item
                if ui_init:
                    diag = base.Text(
                        f" Please wait, saving {spr_name} ",
                        core.Color(0, 0, 0),
                        core.Color(0, 128, 128),
                    )
                    tl = diag.length
                    dr = int((screen.height - 7) / 2)
                    dc = int((screen.width - 21) / 2) - int(tl / 2)
                    progress_bar = ui.ProgressDialog(diag, 0, tl, tl, config=ui_config)
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
                            csprix = current_sprixel
                        if (
                            csprix is None
                            or csprix.model == "X"
                            or csprix.model == "XX"
                        ):
                            sprite_set_sprixel(r, c, core.Sprixel())
                        else:
                            sprite_set_sprixel(r, c, csprix)
                        if ui_init:
                            cidx += 1
                            prog = int((cidx * tl) / total)
                            if prog > last_prog:
                                # draw_progress_bar(dr + 1, dc, tl, cidx, total)
                                progress_bar.value = cidx
                                g.screen.update()
                                last_prog = prog
                if ui_init:
                    screen.delete(dr, dc)
            # TODO: create a wait dialog
            collection.to_json_file(filename)
        redraw_ui = False
    elif inkey == "N":
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
                "default": f"Sprite {len(sprite_list)}",
                "filter": constants.PRINTABLE_FILTER,
            },
        ]
        minp = ui.MultiLineInputDialog(fields=fields, config=ui_config_popup)
        screen.place(minp, screen.vcenter - len(fields), screen.hcenter - 18)
        filled_fields = minp.show()
        screen.delete(screen.vcenter - len(fields), screen.hcenter - 18)
        if (
            filled_fields[0]["user_input"] != ""
            and filled_fields[1]["user_input"] != ""
            and filled_fields[2]["user_input"] != ""
        ):
            nn = filled_fields[2]["user_input"]
            collection[nn] = core.Sprite(
                size=[
                    int(filled_fields[1]["user_input"]),
                    int(filled_fields[0]["user_input"]),
                ]
            )
            collection[nn].name = nn
            sprite_list = list(collection.keys())
            sprite_list_idx = sprite_list.index(nn)
            load_sprite_to_board(g)
            boxes_idx = boxes.index("sprite")
    elif inkey.name == "KEY_TAB":
        boxes_idx += 1
    elif boxes[boxes_current_id] == "sprite":
        if inkey == engine.key.UP:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.UP, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.UP, 1)
        elif inkey == engine.key.DOWN:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.DOWN, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.DOWN, 1)
        elif inkey == engine.key.LEFT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.LEFT, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.LEFT, 1)
        elif inkey == engine.key.RIGHT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.RIGHT, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.RIGHT, 1)
        elif inkey == "j":
            pos = g.player.pos
            g.move_player(constants.LEFT, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
            elif len(palette) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=palette[palette_idx]), pos[0], pos[1]
                )
        elif inkey == "l":
            pos = g.player.pos
            g.move_player(constants.RIGHT, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
            elif len(palette) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=palette[palette_idx]), pos[0], pos[1]
                )
        elif inkey == "i":
            pos = g.player.pos
            g.move_player(constants.UP, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
            elif len(palette) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=palette[palette_idx]), pos[0], pos[1]
                )
        elif inkey == "k":
            pos = g.player.pos
            g.move_player(constants.DOWN, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
            elif len(palette) > 0:
                g.current_board().place_item(
                    board_items.Door(sprixel=palette[palette_idx]), pos[0], pos[1]
                )
        elif inkey == "E":
            eraser_mode = not eraser_mode
            if eraser_mode:
                txt = base.Text(
                    "ERASER MODE ON",
                    fg_color=core.Color(255, 0, 0),
                    style=constants.BOLD,
                )
                screen.place(txt, 1, screen.hcenter)
            else:
                screen.delete(1, screen.hcenter)
        elif inkey == "A" and current_sprixel is not None:
            palette.append(current_sprixel)
        else:
            redraw_ui = False
    elif boxes[boxes_current_id] == "toolbox":
        if (
            inkey.name == "KEY_ENTER"
            and tools[tools_idx % len(tools)] == "Select model"
        ):
            width = int(screen.width / 2)
            height = 15
            gs = ui.GridSelectorDialog(
                brush_models,
                height,
                width,
                "Select a brush model",
                config=ui_config_popup,
            )
            screen.place(
                gs,
                int(screen.vcenter - (height / 2)),
                int(screen.hcenter - (width / 2)),
                2,
            )
            sprix = gs.show()
            if (
                len(palette) > palette_idx
                and sprix.model is not None
                and sprix.model != ""
            ):
                palette[palette_idx].model = sprix.model
            screen.delete(
                int(screen.vcenter - (height / 2)), int(screen.hcenter - (width / 2))
            )
        elif (
            inkey.name == "KEY_ENTER"
            and tools[tools_idx % len(tools)] == "Rename sprite"
        ):
            old_name = sprite_list[sprite_list_idx % len(sprite_list)]
            edit = ui.LineInputDialog(
                "Enter the new sprite name:",
                old_name,
                config=ui_config_popup,
            )
            screen.place(edit, screen.vcenter, screen.hcenter - 13)
            new_name = edit.show()
            screen.delete(screen.vcenter, screen.hcenter - 13)
            collection.rename(old_name, new_name)
            sprite_list[sprite_list_idx % len(sprite_list)] = new_name
        elif (
            inkey.name == "KEY_ENTER"
            and tools[tools_idx % len(tools)] == "Select FG color"
        ):
            cp = ui.ColorPickerDialog(config=ui_config_popup)
            screen.place(cp, screen.vcenter - 2, screen.hcenter - 13)
            color = cp.show()
            if (
                len(palette) > palette_idx
                and color is not None
                and color != core.Color()
            ):
                palette[palette_idx].fg_color = color
            screen.delete(screen.vcenter - 2, screen.hcenter - 13)
        elif (
            inkey.name == "KEY_ENTER"
            and tools[tools_idx % len(tools)] == "Select BG color"
        ):
            cp = ui.ColorPickerDialog(config=ui_config_popup)
            screen.place(cp, screen.vcenter - 2, screen.hcenter - 13)
            color = cp.show()
            if (
                len(palette) > palette_idx
                and color is not None
                and color != core.Color()
            ):
                palette[palette_idx].bg_color = color
            screen.delete(screen.vcenter - 2, screen.hcenter - 13)
        elif (
            inkey.name == "KEY_ENTER"
            and tools[tools_idx % len(tools)] == "Duplicate sprite"
        ):
            spr_c_idx = sprite_list_idx % len(sprite_list)
            new_sprite = copy.deepcopy(collection[sprite_list[spr_c_idx]])
            new_sprite.name += " copy"
            collection.add(new_sprite)
            sprite_list = list(collection.keys())
            sprite_list_idx = sprite_list.index(new_sprite.name)
            load_sprite_to_board(g)
            boxes_idx = boxes.index("sprite")
        elif inkey.name == "KEY_UP":
            tools_idx -= 1
        elif inkey.name == "KEY_DOWN":
            tools_idx += 1
    elif boxes[boxes_current_id] == "palette":
        clean_cursor = True
        if inkey.name == "KEY_RIGHT":
            palette_idx += 1
        elif inkey.name == "KEY_LEFT":
            palette_idx -= 1
        elif inkey.name == "KEY_DOWN":
            # TODO : the -1 should probably be "- palette[palette_idx].length"
            palette_idx += int((screen.width - 23) / 2) - 1
        elif inkey.name == "KEY_UP":
            palette_idx -= int((screen.width - 23) / 2) - 1
        elif inkey.name == "KEY_ENTER":
            # If we hit the enter key, we go back to the sprite canvas
            boxes_idx = boxes.index("sprite")
        else:
            redraw_ui = False
            clean_cursor = False
        if clean_cursor and (
            previous_cursor_pos[0] is not None and previous_cursor_pos[1] is not None
        ):
            screen.delete(previous_cursor_pos[0], previous_cursor_pos[1])
        # Clamp the palette_idx between 0 and len of the list
        palette_idx = clamp(palette_idx, 0, len(palette) - 1)
    elif boxes[boxes_current_id] == "sprite_list" and (
        inkey == engine.key.UP or inkey == engine.key.DOWN
    ):
        sprite_list_idx += nav_increments[inkey.name]
        spr_c_idx = sprite_list_idx % len(sprite_list)
        try:
            g.change_level(1 + spr_c_idx)
        except Exception:
            load_sprite_to_board(g)
        update_sprite_info(g, sprite_list[spr_c_idx])
    elif (
        screen.height != screen.buffer.shape[0]
        or screen.width != screen.buffer.shape[1]
    ):
        screen.clear_buffers()
    elif inkey.name == "KEY_ENTER":
        if boxes[boxes_current_id] != "sprite":
            boxes_idx = boxes.index("sprite")
    else:
        redraw_ui = False
    if redraw_ui or (frames % 60) == 0:
        draw_ui()
        fps = f"FPS: {round(frames / ((time.time() - start)))}"
        screen.place(base.Text(fps), 1, screen.width - len(fps) - 2)
        frames = 0
        start = time.time()
    screen.update()
    frames += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool to create/edit pygamelib's sprites."
    )
    parser.add_argument(
        "sprite_file", help="An sprite file to load and edit.", nargs="?", default=""
    )
    args = parser.parse_args()
    collection = None
    if args.sprite_file != "" and os.path.exists(args.sprite_file):
        print(f"Loading sprite collection: {args.sprite_file}...", end="", flush=True)
        collection = core.SpriteCollection.load_json_file(args.sprite_file)
        sprite_list = list(collection.keys())
        filename = args.sprite_file
        print("done")
    else:
        collection = core.SpriteCollection()
        collection["default"] = core.Sprite(size=[16, 8])
        collection["default"].name = "default"
        sprite_list = list(collection.keys())
        if args.sprite_file != "":
            filename = args.sprite_file
    g = engine.Game.instance(
        player=board_items.Player(
            sprixel=core.Sprixel(
                graphics.BoxDrawings.HEAVY_VERTICAL_AND_HORIZONTAL,
                fg_color=core.Color(255, 0, 0),
            ),
            movement_speed=0.01,
        ),
        user_update=update_screen,
        mode=constants.MODE_RT,
        input_lag=0.0001,
    )
    ui_config = ui.UiConfig(
        game=g, fg_color=core.Color(0, 0, 0), bg_color=core.Color(0, 128, 128)
    )
    ui_config_selected = ui.UiConfig(game=g, border_fg_color=core.Color(0, 255, 0))
    ui_config_popup = ui.UiConfig(
        game=g,
        fg_color=core.Color(0, 0, 0),
        bg_color=core.Color(0, 128, 128),
        borderless_dialog=False,
    )
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
    screen_dimensions["central_zone"] = g.screen.height - 10
    if len(collection) > 0:
        load_sprite_to_board(g)
    start = time.time()
    g.run()
    # print(
    #     f"{frames} frames in {round(time.time()-start,2)} secondes or "
    #     f"{round(frames/(time.time()-start))} FPS"
    # )
    for log in g.logs():
        print(log)
