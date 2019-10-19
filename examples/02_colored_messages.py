import examples_includes  # noqa: F401

# First import the Utils module
import gamelib.Utils as Utils

# Then get creative!

# you directly print colored messages:
print(Utils.magenta_bright("This is a rather flashy magenta..."))

# Each color function has 3 variations : regular, dim and bright
print(Utils.yellow_dim("This is dim."))
print(Utils.yellow("This is regular."))
print(Utils.yellow_bright("This is bright."))

# Now, the color functions are just that: functions. So you can store the
# results in a variable and use them:
blue = Utils.blue_bright("blue")
white = Utils.white_bright("white")
red = Utils.red_bright("red")
print(f"France's flag is {blue} {white} {red}!")
