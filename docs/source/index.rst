Hyrule Astronomy Club - hac-game-lib - documentation
====================================================

.. toctree::
   :caption: Contents:

   board
   boarditem
   characters
   constants
   game
   exceptions
   immovable
   inventory
   movable
   graphics
   sprites
   structures
   utils
   actuators
   animation
   authors
   history

Forewords
^^^^^^^^^

This python3 module is a base
for the programming lessons
of the Hyrule Astronomy Club.
It is not meant to be a
comprehensive game building
library.

It is however meant (and used)
to teach core programming concept
to kids from age 6 to 13.

Introduction
^^^^^^^^^^^^

First of all, his module is
exclusively compatible with python 3.

The core concept is that it revolve
around the :ref:`game-module` object,
the :ref:`board-module` object and the
derivatives of :ref:`boarditem-module`.

Here is an example of what the current version allow to build:

.. image:: https://raw.githubusercontent.com/arnauddupuis/hac-game-lib/master/images/base_game.gif

The base game makes use of:
    * The main "game engine" (gamelib.Game.Game)
    * Many different types of structures (from gamelib.Structures), like:
        * Wall (well the walls...),
        * Treasure (gems and money bag),
        * GenericStructure (trees),
        * GenericActionnableStructure (hearts and portals).
    * Game()'s menu capabilities.
    * Player and NPC (from gamelib.Characters)
    * Inventory (from gamelib.Inventory)
    * Player and Inventory stats
    * Simple actuators (gamelib.SimpleActuators) like:
        * RandomActuator (NPCs in level 2),
        * PathActuator (NPCs in level 1).

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
