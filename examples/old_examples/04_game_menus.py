import examples_includes  # noqa: F401

# For this example we need to import Game, Board, Text
from pygamelib.engine import Game
from pygamelib.base import Text

# First of all let's create a Game object
mygame = Game(name="Demo game")

# Set a message variable to display a message on selected menu item
message = None

# Now we want to create some menus to tell the player what to do, or to
# give some information/directions
# IMPORTANT: Menu do absolutely nothing by themselves, they are just a
# structured display of information.
# The syntax is game_object.add_menu_entry(category,shortcut,message, data)
# the data parameter is optional.
option_red = "A cool menu in dim red"
option_magenta = "Another cool menu in bright magenta"
mygame.add_menu_entry("main_menu", None, "=" * 22)
mygame.add_menu_entry("main_menu", "h", "Show the help menu")
mygame.add_menu_entry("main_menu", None, "=" * 22)
mygame.add_menu_entry("main_menu", "1", Text.red_dim(option_red))
mygame.add_menu_entry("main_menu", "2", Text.magenta_bright(option_magenta))
mygame.add_menu_entry("main_menu", "q", "Quit game")

mygame.add_menu_entry("help_menu", None, "---------")
mygame.add_menu_entry("help_menu", None, "Help Menu")
mygame.add_menu_entry("help_menu", None, "---------")
mygame.add_menu_entry("help_menu", "j", "Random help menu")
mygame.add_menu_entry("help_menu", "b", "Back to main menu")

# let's set a variable that hold the current menu category (for navigation)
current_menu = "main_menu"
# Now let's make a loop to dynamically navigate in the menu
key = None
while True:
    # clear screen
    mygame.clear_screen()

    # First print the message if something is in the variable
    if message is not None:
        print(message)
        # We don't want to print the message more than once, so we put
        # the message to None once it's printed.
        message = None

    # Now let's display the main_menu
    mygame.display_menu(current_menu)

    # Take user input, we could also use Game.get_key()
    key = input("> ")

    if key == "1" or key == "2" or key == "j":
        message = Text.green_bright(f"Selected menu is: {current_menu}/{key}")
    elif key == "q":
        print("Quitting...")
        break
    elif key == "h":
        current_menu = "help_menu"
    elif key == "b":
        current_menu = "main_menu"
    else:
        message = Text.red_bright("Invalid menu shortcut.")
