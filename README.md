![Tested OS: Linux](https://img.shields.io/badge/Tested%20OS-Linux-green.svg "Tested OS: Linux")
![Untested OS: Windows, Mac OS](https://img.shields.io/badge/Untested%20OS-Windows,Mac%20OS-important.svg "Untested OS: Windows, Mac OS")
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Documentation Status](https://readthedocs.org/projects/hac-game-lib/badge/?version=latest)](http://hac-game-lib.readthedocs.io/?badge=latest)


# hac-game-lib
Hyrule Astronomy Club - Kids coding class - base library for a game development

## Introduction

This library is used as a base to teach coding to kids from 6 to 12.
It aims at giving an environment to kids that let them focus on the algorithm instead of the lousy display or precise management.

This is **obviously** extremely simple and does not aim at being anythting serious for game developpers.

If this library is useful for other teachers, I'll make tutorials.

![base_game.py screenshot](https://raw.githubusercontent.com/arnauddupuis/hac-game-lib/master/images/base_game_lvl1.png "base_game.py")

Here is a quick view of what can currently be achieved with that library:

![base_game.py animation](https://raw.githubusercontent.com/arnauddupuis/hac-game-lib/master/images/base_game.gif "base_game.py")

The base game makes use of:
* The main "game engine" (gamelib.Game.Game)
* Many different types of structures (from gamelib.Structures): Wall (well the walls...), Treasure (gems and money bag), GenericStructure (trees) and GenericActionnableStructure (hearts and portals)
* Game()'s menu capabilities.
* Player and NPC (from gamelib.Characters)
* Inventory (from gamelib.Inventory)
* Player and Inventory stats
* RandomActuator (NPCs in level 2) and PathActuator (NPCs in level 1) (from gamelib.Actuators.SimpleActuators)

## Requirements

### Python

The hac-game-lib only supports Python 3+. It will **not** run with Python 2.

Run PIP to install the requirements (only colorama):

```bash
pip3 install -r requirements.txt
```

### Terminal color and emojis

It is not really a hard requirement but colored emojis are really bringing the games created to life.  
We then recommend to have a color emojis font installed like Noto Color Emojis (on most Linux distributions you can install it from the package manager, search for "noto-color-emoji").

If your terminal application is not displaying color emojis, please have a look at this [file](https://gist.github.com/IgnoredAmbience/7c99b6cf9a8b73c9312a71d1209d9bbb) and follow the instructions.

## Limitations

There is tons of limitations but for the most important ones: 
* Only one player is supported.
* There is little protections against messing up with the internal. This is *on purpose*, I want the kids to learn to use the API not mess up with the internals of every single class.
