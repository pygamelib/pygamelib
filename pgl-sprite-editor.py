#!/usr/bin/env python3

from pygamelib.base import Text
from pygamelib import constants
from pygamelib.gfx.core import Color


print(
    Text(
        "All pygamelib editors are have been consolidated into one: pygamelib-editor. "
        "It is now distributed as a separate package.\nPlease install it with:",
        Color(255, 0, 0),
        style=constants.BOLD,
    )
)
print(Text("pip install pygamelib-editor", Color(0, 255, 0), style=constants.BOLD))
print(
    Text(
        "\nOr visit https://github.com/pygamelib/pygamelib-editor", style=constants.BOLD
    )
)
