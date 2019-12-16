"""This module regroup different utility functions and constants.
"""

from colorama import Fore, Back, Style, init
import colorama.ansi

# We need to ignore that one as it is used by user to compare keys (i.e Utils.key.UP)
from readchar import readkey, key  # noqa: F401
import subprocess
import sys

WHITE_RECT = Back.WHITE + " " + Style.RESET_ALL
BLUE_RECT = Back.BLUE + " " + Style.RESET_ALL
RED_RECT = Back.RED + " " + Style.RESET_ALL
MAGENTA_RECT = Back.MAGENTA + " " + Style.RESET_ALL
GREEN_RECT = Back.GREEN + " " + Style.RESET_ALL
YELLOW_RECT = Back.YELLOW + " " + Style.RESET_ALL
BLACK_RECT = Back.BLACK + " " + Style.RESET_ALL
CYAN_RECT = Back.CYAN + " " + Style.RESET_ALL

WHITE_SQUARE = Back.WHITE + "  " + Style.RESET_ALL
MAGENTA_SQUARE = Back.MAGENTA + "  " + Style.RESET_ALL
GREEN_SQUARE = Back.GREEN + "  " + Style.RESET_ALL
RED_SQUARE = Back.RED + "  " + Style.RESET_ALL
BLUE_SQUARE = Back.BLUE + "  " + Style.RESET_ALL
YELLOW_SQUARE = Back.YELLOW + "  " + Style.RESET_ALL
BLACK_SQUARE = Back.BLACK + "  " + Style.RESET_ALL
CYAN_SQUARE = Back.CYAN + "  " + Style.RESET_ALL

RED_BLUE_SQUARE = Back.RED + " " + Back.BLUE + " " + Style.RESET_ALL
YELLOW_CYAN_SQUARE = Back.YELLOW + " " + Back.CYAN + " " + Style.RESET_ALL

# get clear sequence for the terminal
# TODO: check OS
_exitcode, clear_sequence = subprocess.getstatusoutput("tput clear")
if _exitcode:
    clear_sequence = colorama.ansi.clear_screen()

"""
Utils define a couple of constants and functions for styling the Board and terminal.

Some colored rectangles:
 * WHITE_RECT
 * BLUE_RECT
 * RED_RECT
 * MAGENTA_RECT
 * GREEN_RECT
 * YELLOW_RECT
 * BLACK_RECT
 * CYAN_RECT

Then some colored squares:
 * WHITE_SQUARE
 * MAGENTA_SQUARE
 * GREEN_SQUARE
 * RED_SQUARE
 * BLUE_SQUARE
 * YELLOW_SQUARE
 * BLACK_SQUARE
 * CYAN_SQUARE

And finally an example of composition of rectangles to make different colored squares:
 * RED_BLUE_SQUARE = RED_RECT+BLUE_RECT
 * YELLOW_CYAN_SQUARE = YELLOW_RECT+CYAN_RECT

"""


def get_key():
    """Reads the next key-stroke returning it as a string.

    Example::

        key = Utils.get_key()
        if key == Utils.key.UP:
            print("Up")
        elif key == "q"
            exit()

    .. note:: See `readkey` documentation in `readchar` package.
    """
    return readkey()


# the warn() function print a message prefixed by a yellow WARNING.
def warn(message):
    """Print a warning message.

    The warning is a regular message prefixed by WARNING in black on a yellow
    background.

    :param message: The message to print.
    :type message: str

    Example::

        Utils.warn("This is a warning.")
    """
    print(Fore.BLACK + Back.YELLOW + "WARNING" + Style.RESET_ALL + ": " + message)


def fatal(message):
    """Print a fatal message.

    The fatal message is a regular message prefixed by FATAL in white on a red
    background.

    :param message: The message to print.
    :type message: str

    Example::

        Utils.fatal("|x_x|")
    """
    print(
        Fore.WHITE
        + Back.RED
        + Style.BRIGHT
        + "FATAL"
        + Style.RESET_ALL
        + ": "
        + message
    )


def info(message):
    """Print an informative message.

    The info is a regular message prefixed by INFO in white on a blue background.

    :param message: The message to print.
    :type message: str

    Example::

        Utils.info("This is a very informative message.")
    """
    print(Fore.WHITE + Back.BLUE + "INFO" + Style.RESET_ALL + ": " + message)


def debug(message):
    """Print a debug message.

    The debug message is a regular message prefixed by INFO in blue on a green
    background.

    :param message: The message to print.
    :type message: str

    Example::

        Utils.debug("This is probably going to success, eventually...")
    """
    print(
        Fore.BLUE
        + Back.GREEN
        + Style.BRIGHT
        + "DEBUG"
        + Style.RESET_ALL
        + ": "
        + message
    )


def print_white_on_red(message):
    """Print a white message over a red background.

    :param message: The message to print.
    :type message: str

    Example::

        Utils.print_white_on_red("This is bright!")
    """
    print(Fore.WHITE + Back.RED + message + Style.RESET_ALL)


# Colored bright functions
def green_bright(message):
    """
    Return a string formatted to be bright green

    :param message: The message to format.
    :type message: str
    :return: The formatted string
    :rtype: str

    Example::

        print( Utils.green_bright("This is a formatted message") )

    """
    return Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL


def blue_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLUE + Style.BRIGHT + message + Style.RESET_ALL


def red_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.RED + Style.BRIGHT + message + Style.RESET_ALL


def yellow_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.YELLOW + Style.BRIGHT + message + Style.RESET_ALL


def magenta_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.MAGENTA + Style.BRIGHT + message + Style.RESET_ALL


def cyan_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.CYAN + Style.BRIGHT + message + Style.RESET_ALL


def white_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.WHITE + Style.BRIGHT + message + Style.RESET_ALL


def black_bright(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLACK + Style.BRIGHT + message + Style.RESET_ALL


# Colored normal functions
def green(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.GREEN + message + Style.RESET_ALL


def blue(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLUE + message + Style.RESET_ALL


def red(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.RED + message + Style.RESET_ALL


def yellow(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.YELLOW + message + Style.RESET_ALL


def magenta(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.MAGENTA + message + Style.RESET_ALL


def cyan(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.CYAN + message + Style.RESET_ALL


def white(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.WHITE + message + Style.RESET_ALL


def black(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLACK + message + Style.RESET_ALL


# Colored dim function
def green_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.GREEN + Style.DIM + message + Style.RESET_ALL


def blue_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLUE + Style.DIM + message + Style.RESET_ALL


def red_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.RED + Style.DIM + message + Style.RESET_ALL


def yellow_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.YELLOW + Style.DIM + message + Style.RESET_ALL


def magenta_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.MAGENTA + Style.DIM + message + Style.RESET_ALL


def cyan_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.CYAN + Style.DIM + message + Style.RESET_ALL


def white_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.WHITE + Style.DIM + message + Style.RESET_ALL


def black_dim(message):
    """
    This method works exactly the way green_bright() work with different color.
    """
    return Fore.BLACK + Style.DIM + message + Style.RESET_ALL


def clear_screen():
    """
    This methods clear the screen
    """
    sys.stdout.write(clear_sequence)


def init_term_colors():
    """
    This function is a forward to colorama.init()
    """
    init()
