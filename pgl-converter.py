import climage
import os
import argparse
from pygamelib import base, engine, board_items
from pygamelib.gfx import core

file = None
tmp_file = None
width = 48

# TODO: use argparse to add more command line flexibility:
#         - --width=<width:int>
#         - --collection=<existing spr file:path> -> add the transformed sprite to a
#                                                    given collection. If non existing
#                                                    it's created
#         - --out=<path to a dir or file> -> if a dir write the file here, if a file
#                                            overwrite it.
#         - --no-code to not show the code example
#         - --show to show the generated sprite
#         - --silent to run the script with no output at all (imply --no-code)
#         - --unicode=<bool> to enable/disable unicode (passed down to climage)
#         - --color=<true|256|16|8> for the color precision (passed down to climage)
#         - --board / --no-board to generate a Board out of the sprite (default: false)
#         - --sprite / --no-sprite to generate or not a sprite out of the image
#                                  (default: true)
parser = argparse.ArgumentParser(
    description="A tool to convert an image to a pygamelib usable Sprite and/or Board."
)
parser.add_argument(
    "--board",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Generate and save a Board out of the image.",
)
parser.add_argument(
    "--sprite",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate and save a Sprite out of the image.",
)
parser.add_argument(
    "--code",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate and display a code example to use the freshly generated material.",
)
parser.add_argument(
    "--show",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Show the generated sprite at the end of the process.",
)
parser.add_argument(
    "--width",
    "-w",
    type=int,
    default=80,
    help="The width (in number of columns) of the generated sprite.",
)
# TODO: Colors other than Truecolor are not supported by the Sprite.load_from_ansi
# TODO: no unicode generates string that are not parsed correctly either.
parser.add_argument(
    "--unicode",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Enable/disable utilization of unicode characters, resulting in a more "
    "detailed image. Warning 1: this is not supported by all terminals. WARNING 2: "
    "use at your own risk, the pygamelib *requires* unicode support.",
)
# parser.add_argument(
#     "--colors",
#     "-c",
#     type=str,
#     action="store",
#     required=False,
#     choices=["true", "256", "16", "8"],
#     default="true",
#   help="Number of colors used to encode the image. 'true' stands for truecolors or 16"
#     " million colors.",
# )
parser.add_argument(
    "--collection",
    type=str,
    action="store",
    required=False,
    default="",
    help="Specify the collection file to save the converted image to. By default it is "
    "saved in <image filename>.spr. If used with --out, collection takes precedence and"
    " --out is ignored.",
)
parser.add_argument(
    "--out",
    type=str,
    action="store",
    required=False,
    default="",
    help="Specify the output directory. If set, all files generated will be store in "
    "that directory. If not, files are going to be stored along the source image.",
)
parser.add_argument(
    "--silent",
    action="store_true",
    default=False,
    required=False,
    help="Turn off all display, implies --no-code --no-show.",
)
parser.add_argument(
    "image", help="An image file to convert to a pygamelib sprite and/or board."
)
args = parser.parse_args()

config = {
    "is_unicode": args.unicode,
    "is_truecolor": True,
    "is_256color": False,
    "is_16color": False,
    "is_8color": False,
}
# if args.colors == "256":
#     config["is_truecolor"] = False
#     config["is_256color"] = True
# elif args.colors == "16":
#     config["is_truecolor"] = False
#     config["is_16color"] = True
# elif args.colors == "8":
#     config["is_truecolor"] = False
#     config["is_8color"] = True

file = args.image
width = args.width

spr_id = os.path.basename(file)
spr_id = os.path.splitext(spr_id)[0]

output_dir = args.out

if output_dir == "":
    output_dir = os.path.dirname(file)

tmp_file = os.path.join(output_dir, spr_id + ".ans")

not args.silent and print(
    f"Converting {base.Text.blue(file)} to ANSI escape sequence...",
    end="",
    flush=True,
)
output = climage.to_file(
    file,
    tmp_file,
    is_unicode=config["is_unicode"],
    is_truecolor=config["is_truecolor"],
    is_256color=config["is_256color"],
    is_16color=config["is_16color"],
    is_8color=config["is_8color"],
    width=width,
    palette="default",
)

not args.silent and print(base.Text.blue("done"), flush=True)

sc = core.SpriteCollection()
final = os.path.join(output_dir, spr_id + ".spr")
if args.collection != "":
    if os.path.exists(args.collection):
        not args.silent and print(
            f"Loading collection: {base.Text.blue(args.collection)}...",
            end="",
            flush=True,
        )
        sc = sc.load_json_file(args.collection)
        not args.silent and print(base.Text.blue("done"), flush=True)
    final = args.collection
not args.silent and print("Converting ANSI sequence to Sprite...", end="", flush=True)
spr = core.Sprite.load_from_ansi_file(tmp_file)
not args.silent and print(base.Text.blue("done"), flush=True)
spr.name = spr_id
sprite_valid = True
if spr_id in sc.keys():
    ans = input(
        f"Sprite {spr_id} is already existing in the collection, do want "
        "to replace it? (y/n): "
    )
    if not ans.startswith("y"):
        sprite_valid = False
        print(f"{spr_id} is {base.Text.red_bright('ignored')}.")
if sprite_valid:
    sc.add(spr)
    sc.to_json_file(final)
os.remove(tmp_file)

board_file = os.path.join(output_dir, spr_id + ".json")

if args.board:
    not args.silent and print(
        "Generating a Board out of the image...", end="", flush=True
    )
    # tile = board_items.Tile(sprite=spr)
    b = engine.Board(
        size=spr.size, ui_borders="", name=spr_id, DISPLAY_SIZE_WARNINGS=False
    )
    # b.place_item(tile, 0, 0)
    # Here we should just place a Tile but unfortunately the previous version of the
    # pygamelib do not actually save and load complex items but their components.
    # So for the moment we will convert each sprixel into a Door object.
    # TODO: add a --compatibility flag : when on we do that, when off we don't (i.e: we
    # place a Tile on the board)
    for sr in range(0, spr.height):
        for sc in range(0, spr.width):
            b.place_item(board_items.Door(sprixel=spr.sprixel(sr, sc)), sr, sc)
    # The game object is required to save boards... not a terribly good design...
    g = engine.Game()
    g.add_board(1, b)
    g.save_board(1, board_file)
    if not args.silent:
        print("done", flush=True)
if args.show and not args.silent and sprite_valid:
    if spr.width <= base.Console.instance().width:
        print(spr)
    else:
        print(
            base.Text.yellow_bright(
                "The generated sprite is to large to display all at once correctly in "
                f"this terminal (sprite size is {spr.width}x{spr.height} and your "
                f"terminal is {base.Console.instance().width}x"
                f"{base.Console.instance().height})."
            )
        )
if not args.silent and sprite_valid:
    print(
        f"Converted {base.Text.green(file)} in a pygamelib usable "
        f"{base.Text.magenta_bright('sprite')} and saved it in: {base.Text.cyan(final)}"
    )
if args.code and not args.silent and sprite_valid:
    print(
        "\nUse pygamelib.gfx.core.SpriteCollection to import and use it in your code.\n"
        "Here's some code example:\n"
    )
    print(
        base.Text.cyan_bright(
            "from pygamelib.gfx import core\n"
            f"sprite_collection = core.SpriteCollection.load_json_file('{final}')\n"
            f"sprite = sprite_collection['{spr_id}']\n"
        )
    )

if args.board and not args.silent:
    print(
        f"Converted {base.Text.green(file)} in a pygamelib usable "
        f"{base.Text.magenta_bright('board')} and saved it in: "
        f"{base.Text.cyan(board_file)}"
    )
if args.board and args.code and not args.silent:
    print(
        "\nUse pygamelib.engine.Game to import and use the board in your code.\n"
        "Here's some code example:\n"
    )
    print(
        base.Text.cyan_bright(
            "from pygamelib import engine, constants\n"
            "# Game needs to be properly configured.\n"
            "my_game = engine.Game(player=constants.NO_PLAYER)\n"
            f"my_game.load_board('{board_file}', 1)\n"
            "my_game.change_level(1)\n"
            "# This is just an example with width but height needs to be managed too.\n"
            "if my_game.current_board().width > my_game.screen.width:\n"
            "    my_game.enable_partial_display = True\n"
            "    my_game.partial_display_viewport = [\n"
            "        int(my_game.screen.height/2),\n"
            "        int(my_game.screen.width/2),\n"
            "    ]\n\n"
            "my_game.display_board()"
        )
    )
