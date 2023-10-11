.. _constants-module:

constants
=========

Accessible constants are the following:

General purpose:

* PYGAMELIB_VERSION

.. autoenum:: pygamelib.constants.SizeConstraint
    :members:

.. autoenum:: pygamelib.constants.Alignment
    :members:

.. autoenum:: pygamelib.constants.Orientation
    :members:

.. autoenum:: pygamelib.constants.InputValidator
    :members:

.. autoenum:: pygamelib.constants.Direction
    :members:

**The following constants are used in versions <= 1.3.0 and have been deprecated starting version 1.4.0.**

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

* ORIENTATION_HORIZONTAL
* ORIENTATION_VERTICAL
* ALIGN_LEFT
* ALIGN_RIGHT
* ALIGN_CENTER

Actions states (for Actuators for example):

* RUNNING
* PAUSED
* STOPPED

Accepted input (mainly used in pygamelib.gfx.ui for input dialogs):
* INTEGER_FILTER
* PRINTABLE_FILTER
  
Path Finding Algorithm Constants:

* ALGO_BFS
* ALGO_ASTAR

Text styling constants:

* BOLD
* UNDERLINE

Special constants:

* NO_PLAYER : That constant is used to tell the Game object not to manage the player.
* MODE_RT : Set the game object to Real Time mode. The game runs independently from the user input.
* MODE_TBT : Set the game object to Turn By Turn mode. The game runs turn by turn and pause between each user input.

.. automodule:: pygamelib.constants

