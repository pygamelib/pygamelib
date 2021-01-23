from pygamelib import base, engine, constants, board_items
from pygamelib.gfx import core
from pygamelib.assets import graphics
import argparse
import os
import time


menu = ["File", "Edit", "Help"]
menu_idx = 0
boxes = ["menu", "sprite", "info", "sprite_list", "toolbox", "palette"]
boxes_idx = 0
tools = [
    "Select model",
    "Select FG color",
    "Select BG color",
    "(E)raser mode",
    "(A)dd to palette",
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
nav_increments = {
    "KEY_UP": -1,
    "KEY_DOWN": 1,
    "KEY_LEFT": -1,
    "KEY_RIGHT": 1,
}


def draw_box(row, column, height, width, group="", title=""):
    global boxes_idx
    global boxes
    scr = engine.Game.instance().screen
    color = core.Color(255, 255, 255)
    if boxes[boxes_idx % len(boxes)] == group:
        color = core.Color(0, 255, 0)
    vert_sprix = core.Sprixel(graphics.BoxDrawings.LIGHT_VERTICAL, fg_color=color)
    horiz_sprix = core.Sprixel(graphics.BoxDrawings.LIGHT_HORIZONTAL, fg_color=color)
    scr.place(
        core.Sprixel(graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT, fg_color=color),
        row,
        column,
    )
    if title == "":
        for c in range(column + 1, column + width - 1):
            scr.place(horiz_sprix, row, c)
    else:
        for c in range(column + 1, column + 1 + round(width / 2 - len(title) / 2)):
            scr.place(horiz_sprix, row, c)
        scr.place(
            base.Text(title, fg_color=color),
            row,
            column + 1 + int(width / 2 - 1 - len(title) / 2),
        )
        cs = column + 1 + int(width / 2 - 1 - len(title) / 2) + len(title)
        for c in range(cs, cs + int(width / 2 - len(title) / 2)):
            scr.place(horiz_sprix, row, c)
    scr.place(
        core.Sprixel(graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT, fg_color=color),
        row,
        column + width - 1,
    )
    vert_sprix = core.Sprixel(graphics.BoxDrawings.LIGHT_VERTICAL, fg_color=color)
    for r in range(1, height - 1):
        scr.place(vert_sprix, row + r, column)
        scr.place(
            vert_sprix,
            row + r,
            column + width - 1,
        )
    scr.place(
        core.Sprixel(graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT, fg_color=color),
        row + height - 1,
        column,
    )
    for c in range(column + 1, column + width - 1):
        scr.place(horiz_sprix, row + height - 1, c)
    scr.place(
        core.Sprixel(graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT, fg_color=color),
        row + height - 1,
        column + width - 1,
    )


def draw_ui():
    global filename
    global collection
    global screen_dimensions
    global ui_init
    g = engine.Game.instance()
    screen = g.screen
    spr_l_c_idx = sprite_list_idx % len(sprite_list)
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
    for i in range(0, len(palette)):
        screen.place(
            palette[i],
            screen.height - screen_dimensions["palette"] + 1,
            1 + i,
        )
        # g.screen.place(cell, 7, last_col)
        for c in range(1 + i + 1, 1 + i + palette[i].length):
            g.screen.place(
                core.Sprixel(), screen.height - screen_dimensions["palette"] + 1, c
            )
    # not testing and affecting all the time might be faster than testing before
    # affectation
    ui_init = True


def update_sprite_info(g, sprite_name):
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


def update_sprixel_under_cursor(g, v_move):
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
            g.screen.place(
                f"FG: ({cell.fg_color.r},{cell.fg_color.g},{cell.fg_color.b})",
                9,
                first_col,
            )
        else:
            g.screen.place("No foreground", 9, first_col)
        if cell.bg_color is not None:
            g.screen.place(
                f"BG: ({cell.bg_color.r},{cell.bg_color.g},{cell.bg_color.b})",
                10,
                first_col,
            )
        else:
            g.screen.place("No background", 10, first_col)
        # g.screen.place(f"{cell.bg_color}", 9, first_col)


def load_sprite_to_board(g):
    global sprite_list
    global sprite_list_idx
    global ui_init
    spr_c_idx = sprite_list_idx % len(sprite_list)
    spr_name = sprite_list[spr_c_idx]
    if ui_init:
        g.screen.place(
            f"{spr_name} ui_init is True",
            g.screen.height - 3,
            3,
        )
        diag = base.Text(
            f" Please wait, loading {spr_name} ",
            core.Color(0, 0, 0),
            core.Color(0, 128, 128),
        )
        tl = base.Console.instance().length(diag.text)
        dr = int((g.screen.height - 7) / 2)
        dc = int((g.screen.width - 21) / 2) - int(tl / 2)
        g.screen.place(core.Sprite.from_text(diag), dr, dc, 2)
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
    g.get_board(1 + spr_c_idx).place_item(
        board_items.Tile(sprite=collection[spr_name], null_sprixel=core.Sprixel()),
        0,
        0,
    )
    if (
        collection[spr_name].size[0] >= g.screen.height - 12
        or collection[spr_name].size[1] >= g.screen.width - 23
    ):
        g.get_board(1 + spr_c_idx).enable_partial_display = True
        g.get_board(1 + spr_c_idx).partial_display_viewport = [
            int((g.screen.height - 12) / 2),
            int((g.screen.width - 23) / 2),
        ]
        g.get_board(1 + spr_c_idx).partial_display_focus = g.player
    g.change_level(1 + spr_c_idx)
    update_sprite_info(g, spr_name)
    if ui_init:
        g.screen.delete(dr, dc)


def erase_cell(g, row, column):
    g.current_board().place_item(
        board_items.BoardItemVoid(
            sprixel=core.Sprixel(g.current_board().ui_board_void_cell_sprixel.model)
        ),
        row,
        column,
    )


def update_screen(g, inkey, dt):
    global boxes_idx
    global frames
    global boxes
    global sprite_list_idx
    global collection
    global start
    global nav_increments
    global eraser_mode
    global current_sprixel
    redraw_ui = True
    screen = g.screen
    boxes_current_id = boxes_idx % len(boxes)
    if inkey == "Q":
        g.stop()
    elif inkey.name == "KEY_TAB":
        boxes_idx += 1
    elif inkey.name == "KEY_ENTER":
        if boxes[boxes_current_id] != "sprite":
            boxes_idx = boxes.index("sprite")
    elif boxes[boxes_current_id] == "sprite":
        if inkey == engine.key.UP:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.UP, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.UP, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
        elif inkey == engine.key.DOWN:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.DOWN, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.DOWN, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
        elif inkey == engine.key.LEFT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.LEFT, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.LEFT, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
        elif inkey == engine.key.RIGHT:
            update_sprixel_under_cursor(
                g, base.Vector2D.from_direction(constants.RIGHT, 1)
            )
            update_cursor_info(g)
            pos = g.player.pos
            g.move_player(constants.RIGHT, 1)
            if eraser_mode:
                erase_cell(g, pos[0], pos[1])
        elif inkey == "E":
            eraser_mode = not eraser_mode
        elif inkey == "A" and current_sprixel is not None:
            palette.append(current_sprixel)
        else:
            redraw_ui = False
    elif boxes[boxes_current_id] == "sprite_list" and (
        inkey == engine.key.UP or inkey == engine.key.DOWN
    ):
        sprite_list_idx += nav_increments[inkey.name]
        spr_c_idx = sprite_list_idx % len(sprite_list)
        try:
            g.change_level(1 + spr_c_idx)
        except Exception:
            load_sprite_to_board(g)
    else:
        redraw_ui = False
    if redraw_ui or (frames % 60) == 0:
        draw_ui()
        fps = f"FPS: {round(frames / ((time.time() - start)))}"
        screen.place(base.Text(fps), 1, screen.width - len(fps) - 2)
        frames = 0
        start = time.time()
    screen.place(
        f"Box current_id={boxes_idx} current value={boxes[boxes_current_id]}",
        screen.height - 2,
        3,
    )
    screen.update()
    frames += 1


parser = argparse.ArgumentParser(
    description="A tool to create/edit pygamelib's sprites."
)
parser.add_argument("sprite_file", help="An sprite file to load and edit.", default="")
args = parser.parse_args()
collection = None
if args.sprite_file != "" and os.path.exists(args.sprite_file):
    collection = core.SpriteCollection.load_json_file(args.sprite_file)
    sprite_list = list(collection.keys())
    filename = args.sprite_file
else:
    collection = core.SpriteCollection()
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
