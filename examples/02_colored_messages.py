import examples_includes  # noqa: F401

# First import the Text object from the base module
from pygamelib.base import Text

# Then get creative!

# you directly print colored messages:
print(Text.magenta_bright("This is a rather flashy magenta..."))

# Each color function has 3 variations : regular, dim and bright
print(Text.yellow_dim("This is dim."))
print(Text.yellow("This is regular."))
print(Text.yellow_bright("This is bright."))

# Now, the color functions are just that: functions. So you can store the
# results in a variable and use them:
blue = Text.blue_bright("blue")
white = Text.white_bright("white")
red = Text.red_bright("red")
print(f"France's flag is {blue} {white} {red}!")
