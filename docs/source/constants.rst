.. _constants-module:

constants
=========

Accessible constants are the following:

General purpose:

* PYGAMELIB_VERSION

Directions:

* NO_DIR: This one is used when no direction can be provided by an actuator (destination reached for a PathFinder for example)
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
* SCREEN_H_CENTER : when placing elements with Screen.place() automatically calculate the horizontal center (use as the column parameter).
* SCREEN_V_CENTER : when placing elements with Screen.place() automatically calculate the vertical center (use as the row parameter).

Actions states (for Actuators for example):

* RUNNING
* PAUSED
* STOPPED

Accepted input (mainly used in pygamelib.gfx.ui for input dialogs):
* INTEGER_FILTER
* PRINTABLE_FILTER

Special constants:

* NO_PLAYER : That constant is used to tell the Game object not to manage the player.
* MODE_RT : Set the game object to Real Time mode. The game runs independently from the user input.
* MODE_TBT : Set the game object to Turn By Turn mode. The game runs turn by turn and pause between each user input.

.. automodule:: pygamelib.constants

    
