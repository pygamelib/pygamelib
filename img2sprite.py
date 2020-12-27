import climage
import sys
import os
from pygamelib import base
from pygamelib.gfx import core

file = None
tmp_file = None
width = 48

if len(sys.argv) <= 1:
    print("No image file provided.")
    print(
        f"Usage: \n\t{sys.argv[0]} <image to convert> <width in characters "
        f"(default: {width})>"
    )
    exit()

if len(sys.argv) > 1:
    file = sys.argv[1]

if len(sys.argv) > 2:
    width = int(sys.argv[2])

tmp_file = os.path.splitext(file)[0] + ".ans"
output = climage.to_file(
    file,
    tmp_file,
    is_unicode=True,
    is_truecolor=True,
    is_256color=False,
    is_16color=False,
    is_8color=False,
    width=width,
    palette="default",
)

sc = core.SpriteCollection()
spr = core.Sprite.load_from_ansi_file(tmp_file)
final = os.path.splitext(file)[0] + ".spr"
spr_id = os.path.basename(final)
spr_id = os.path.splitext(spr_id)[0]
sc[spr_id] = spr
sc.to_json_file(final)
print(f"Converted {file} in a pygamelib usable sprite and saved it in: {final}")
print(
    "Use pygamelib.gfx.core.SpriteCollection to import and use it in your code.\n"
    "Here's some code example:\n"
)
print(
    base.Text.cyan_bright(
        "from pygamelib.gfx import core\n"
        f"sprite_collection = core.SpriteCollection.load_json_file('{final}')\n"
        f"sprite = sprite_collection['{spr_id}']\n"
    )
)
