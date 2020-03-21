"""
Accessible constants are the following:

General purpose:
 * HAC_GAME_LIB_VERSION

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
 * ALL_PLAYABLE_AUTHORIZED
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

"""

# Main version
HAC_GAME_LIB_VERSION = "1.0.0"

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
PLAYER_AUTHORIZED = 10001001
NPC_AUTHORIZED = 10001010
ALL_PLAYABLE_AUTHORIZED = 10001011
NONE_AUTHORIZED = 10001100

# UI positions
POS_TOP = 10001101
POS_BOTTOM = 10001110
ORIENTATION_HORIZONTAL = 10001111
ORIENTATION_VERTICAL = 10010000


# Running states
RUNNING = 10010001
PAUSED = 10010010
STOPPED = 10010011
