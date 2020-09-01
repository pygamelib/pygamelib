"""
Accessible constants are the following:

General purpose:
 * PYGAMELIB_VERSION

Directions:
 * NO_DIR : This one is used when no direction can be provided by an actuator
    (destination reached for a PathFinder for example)
 * UP
 * DOWN
 * LEFT
 * RIGHT
 * DRUP : Diagonal right up
 * DRDOWN : Diagonal right down
 * DLUP : Diagonal Left up
 * DLDOWN : Diagonal left down

Permissions:
 * PLAYER_AUTHORIZED
 * NPC_AUTHORIZED
 * ALL_PLAYABLE_AUTHORIZED (deprecated in 1.2.0 in favor of ALL_CHARACTERS_AUTHORIZED)
 * ALL_CHARACTERS_AUTHORIZED
 * ALL_MOVABLE_AUTHORIZED
 * NONE_AUTHORIZED

UI positions:
 * POS_TOP
 * POS_BOTTOM
 * ORIENTATION_HORIZONTAL
 * ORIENTATION_VERTICAL

Actions states (for Actuators for example):
 * RUNNING
 * PAUSED
 * STOPPED

Special constants:
 * NO_PLAYER: That constant is used to tell the Game object not to manage the player.
 * MODE_RT: Set the game object to Real Time mode. The game runs independently from the
    user input.
 * MODE_TBT: Set the game object to Turn By Turn mode. The game runs turn by turn and
    pause between each user input.
"""

# Main version
PYGAMELIB_VERSION = "1.2.3"

# Directions
NO_DIR = 10000000
UP = 10000001
DOWN = 10000010
LEFT = 10000011
RIGHT = 10000100
DRUP = 10000101
DRDOWN = 10000110
DLUP = 10000111
DLDOWN = 10001000

# Permissions
PLAYER_AUTHORIZED = 20000001
NPC_AUTHORIZED = 20000010
ALL_CHARACTERS_AUTHORIZED = 20000011
ALL_PLAYABLE_AUTHORIZED = ALL_CHARACTERS_AUTHORIZED
ALL_MOVABLE_AUTHORIZED = 20000100
NONE_AUTHORIZED = 20000101

# UI positions
POS_TOP = 30000001
POS_BOTTOM = 30000010
ORIENTATION_HORIZONTAL = 30000011
ORIENTATION_VERTICAL = 30000100


# Running states
RUNNING = 40000001
PAUSED = 40000010
STOPPED = 40000011

# Special constants
NO_PLAYER = 90000001
MODE_RT = 90000002
MODE_TBT = 90000003
