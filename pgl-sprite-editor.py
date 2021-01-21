from pygamelib import base, engine, constants, board_items
from pygamelib.gfx import core
from pygamelib.assets import graphics
import argparse
import os

boxes = ["menu", "sprite", "sprite_list", "toolbox", "history"]
boxes_idx = 0
cursor = board_items.Camera(
    sprixel=core.Sprixel("+", fg_color=core.Color(255, 0, 0), is_bg_transparent=True)
)
filename = ""


def draw_box(row, column, height, width, group="", title=""):
    global boxes_idx
    global boxes
    scr = engine.Game.instance().screen
    color = core.Color(255, 255, 255)
    if boxes[boxes_idx % len(boxes)] == group:
        color = core.Color(0, 255, 0)
    scr.place(
        base.Text(graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT, fg_color=color),
        row,
        column,
    )
    scr.place(
        base.Text(
            graphics.BoxDrawings.LIGHT_HORIZONTAL * int(width / 2 - 1 - len(title) / 2),
            fg_color=color,
        ),
        row,
        column + 1,
    )
    scr.place(
        base.Text(title, fg_color=color),
        row,
        column + 1 + int(width / 2 - 1 - len(title) / 2),
    )
    scr.place(
        base.Text(
            graphics.BoxDrawings.LIGHT_HORIZONTAL
            * round(width / 2 - 1 - len(title) / 2),
            fg_color=color,
        ),
        row,
        column + 1 + int(width / 2 - 1 - len(title) / 2) + len(title),
    )
    scr.place(
        base.Text(graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT, fg_color=color),
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
            base.Text(graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT, fg_color=color),
            row + height - 1,
            column,
        )
        scr.place(
            base.Text(
                graphics.BoxDrawings.LIGHT_HORIZONTAL * (width - 2), fg_color=color
            ),
            row + height - 1,
            column + 1,
        )
        scr.place(
            base.Text(graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT, fg_color=color),
            row + height - 1,
            column + width - 1,
        )


def draw_ui():
    g = engine.Game.instance()
    screen = g.screen
    draw_box(0, 0, 3, screen.width - 2, "menu")
    draw_box(10, 0, 3, screen.width - 1, "sprite", "Sprite")
    col = 2
    screen.place("File", 1, col)
    col += len("File") + 2
    screen.place("Edit", 1, col)
    col += len("Edit") + 2
    screen.place("Help", 1, col)


def update_screen(g, inkey, dt):
    global boxes_idx
    screen = g.screen
    if inkey == "X":
        g.stop()
    elif inkey.name == "KEY_TAB":
        boxes_idx += 1
    draw_ui()
    screen.update()


parser = argparse.ArgumentParser(
    description="A tool to create/edit pygamelib's sprites."
)
parser.add_argument(
    "sprite_file", help="An sprite file to load and edit.", default="", required=False
)
args = parser.parse_args()
collection = None
if args.sprite_file != "" and os.path.exists(args.sprite_file):
    collection = core.SpriteCollection.load_json_file(args.sprite_file)
    filename = args.sprite_file
else:
    collection = core.SpriteCollection()
    if args.sprite_file != "":
        filename = args.sprite_file
g = engine.Game.instance(
    player=constants.NO_PLAYER, user_update=update_screen, mode=constants.MODE_RT
)
# We need a board to benefit from the run() mechanic.
g.add_board(1, engine.Board(ui_borders="", size=[0, 0]))
g.change_level(1)
g.run()
