from colorama import Fore, Back, Style
import sys
import termios
import tty

WHITE_RECT = Back.WHITE+' '+Style.RESET_ALL
BLUE_RECT = Back.BLUE+' '+Style.RESET_ALL
RED_RECT = Back.RED+' '+Style.RESET_ALL
MAGENTA_RECT = Back.MAGENTA+' '+Style.RESET_ALL
GREEN_RECT = Back.GREEN+' '+Style.RESET_ALL
YELLOW_RECT = Back.YELLOW+' '+Style.RESET_ALL
BLACK_RECT = Back.BLACK+' '+Style.RESET_ALL
CYAN_RECT = Back.CYAN+' '+Style.RESET_ALL

WHITE_SQUARE = Back.WHITE+'  '+Style.RESET_ALL
MAGENTA_SQUARE = Back.MAGENTA+'  '+Style.RESET_ALL
GREEN_SQUARE = Back.GREEN+'  '+Style.RESET_ALL
RED_SQUARE = Back.RED+'  '+Style.RESET_ALL
BLUE_SQUARE = Back.BLUE+'  '+Style.RESET_ALL
YELLOW_SQUARE = Back.YELLOW+'  '+Style.RESET_ALL
BLACK_SQUARE = Back.BLACK+'  '+Style.RESET_ALL
CYAN_SQUARE = Back.CYAN+'  '+Style.RESET_ALL

RED_BLUE_SQUARE = Back.RED+' '+Back.BLUE+' '+Style.RESET_ALL
YELLOW_CYAN_SQUARE = Back.YELLOW+' '+Back.CYAN+' '+Style.RESET_ALL

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

# This function comes from: http://code.activestate.com/recipes/577728-simpletron3xpy-game-to-demo-xy-drawing-using-the-k/?in=user-4177147 
# it is named inkey() in this game.
def get_key():
    """Get a key from the keyboard.

    This function capture one unique key from the keyboard **without** waiting for a carriage return.

    Example::

        key = Utils.get_key()
        if key == "q"
            exit()
    
    .. note:: Anything that return more than one key code is not going to be correctly captured (like the arrow keys)

    .. todo:: Make it possible to use the arrow keys.
    """
    fd=sys.stdin.fileno()
    remember_attributes=termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character=sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, remember_attributes)
    return character

## the warn() function print a message prefixed by a yellow WARNING.
def warn(message):
    print(Fore.BLACK + Back.YELLOW + 'WARNING' + Style.RESET_ALL + ': '+message)

def fatal(message):
    print(Fore.WHITE + Back.RED + Style.BRIGHT + 'FATAL' + Style.RESET_ALL + ': '+message)

def info(message):
    print(Fore.WHITE + Back.BLUE + 'INFO' + Style.RESET_ALL + ': '+message)

def debug(message):
    print(Fore.BLUE + Back.GREEN + Style.BRIGHT + 'DEBUG' + Style.RESET_ALL + ': '+message)

def print_white_on_red(message):
    print(Fore.WHITE + Back.RED + message + Style.RESET_ALL)

# Colored bright functions
def green_bright(message):
    return Fore.GREEN+Style.BRIGHT+message+Style.RESET_ALL

def blue_bright(message):
    return Fore.BLUE+Style.BRIGHT+message+Style.RESET_ALL

def red_bright(message):
    return Fore.RED+Style.BRIGHT+message+Style.RESET_ALL

def yellow_bright(message):
    return Fore.YELLOW+Style.BRIGHT+message+Style.RESET_ALL

def magenta_bright(message):
    return Fore.MAGENTA+Style.BRIGHT+message+Style.RESET_ALL

def cyan_bright(message):
    return Fore.CYAN+Style.BRIGHT+message+Style.RESET_ALL

def white_bright(message):
    return Fore.WHITE+Style.BRIGHT+message+Style.RESET_ALL

def black_bright(message):
    return Fore.BLACK+Style.BRIGHT+message+Style.RESET_ALL

# Colored normal functions
def green(message):
    return Fore.GREEN+message+Style.RESET_ALL

def blue(message):
    return Fore.BLUE+message+Style.RESET_ALL

def red(message):
    return Fore.RED+message+Style.RESET_ALL

def yellow(message):
    return Fore.YELLOW+message+Style.RESET_ALL

def magenta(message):
    return Fore.MAGENTA+message+Style.RESET_ALL

def cyan(message):
    return Fore.CYAN+message+Style.RESET_ALL

def white(message):
    return Fore.WHITE+message+Style.RESET_ALL

def black(message):
    return Fore.BLACK+message+Style.RESET_ALL

# Colored dim function
def green_dim(message):
    return Fore.GREEN+Style.DIM+message+Style.RESET_ALL

def blue_dim(message):
    return Fore.BLUE+Style.DIM+message+Style.RESET_ALL

def red_dim(message):
    return Fore.RED+Style.DIM+message+Style.RESET_ALL

def yellow_dim(message):
    return Fore.YELLOW+Style.DIM+message+Style.RESET_ALL

def magenta_dim(message):
    return Fore.MAGENTA+Style.DIM+message+Style.RESET_ALL

def cyan_dim(message):
    return Fore.CYAN+Style.DIM+message+Style.RESET_ALL

def white_dim(message):
    return Fore.WHITE+Style.DIM+message+Style.RESET_ALL

def black_dim(message):
    return Fore.BLACK+Style.DIM+message+Style.RESET_ALL