![Tested OS: Linux](https://img.shields.io/badge/Tested%20OS-Linux-green.svg "Tested OS: Linux")
![Untested OS: Windows, Mac OS](https://img.shields.io/badge/Untested%20OS-Windows,Mac%20OS-important.svg "Untested OS: Windows, Mac OS")
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Documentation Status](https://readthedocs.org/projects/hac-game-lib/badge/?version=latest)](http://hac-game-lib.readthedocs.io/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2849/badge)](https://bestpractices.coreinfrastructure.org/projects/2849)
[![CircleCI](https://circleci.com/gh/arnauddupuis/hac-game-lib.svg?style=svg)](https://circleci.com/gh/arnauddupuis/hac-game-lib)

# hac-game-lib
Hyrule Astronomy Club - base library for a game development

## Introduction

This library is used as a base to teach coding to kids from 6 to 12.
It aims at giving an environment to new and learning developers (including kids) that let them focus on the algorithm instead of the lousy display or precise management.

This is **obviously** extremely simple and does not aim at being anything serious for game developers (although it can probably be used as a nice base now).

There is a [Youtube channel](https://www.youtube.com/channel/UCT_SxIlKaD6MM7JlQKelpgw) that contains tutorials.

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
We use [pipenv](https://github.com/pypa/pipenv) to manage dependencies.

Run Pipenv to install the requirements (only colorama):

```bash
pip3 install pipenv
pipenv install
```

If you want the developmnent dependencies you need to run:
```bash
pip3 install pipenv
pipenv install --dev
```

### Runing tests 

To run the unit tests use the following command:

```bash
python -m unittest discover -s tests
```

### Terminal color and emojis

It is not really a hard requirement but colored emojis are really bringing the games created to life.  
We then recommend to have a color emojis font installed like Noto Color Emojis (on most Linux distributions you can install it from the package manager, search for "noto-color-emoji").

If your terminal application is not displaying color emojis, please have a look at this [file](https://gist.github.com/IgnoredAmbience/7c99b6cf9a8b73c9312a71d1209d9bbb) and follow the instructions.

### Running examples

To run the examples using [pipenv](https://github.com/pypa/pipenv):

```bash
pipenv shell
(hac-game-lib) cd examples
(hac-game-lib) python3 01_board_and_wall.py
```

## Limitations

There is tons of limitations but for the most important ones: 
* Only one player is supported.
* There is little protections against messing up with the internal. This is *on purpose*, I want the kids to learn to use the API not mess up with the internals of every single class.
