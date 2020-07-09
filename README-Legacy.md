![Linux: Ok](https://img.shields.io/badge/Linux-Ok-green.svg "Linux: Ok")
![Windows: Ok](https://img.shields.io/badge/Windows-Ok-green.svg "Windows: Ok")
![Mac OS: Ok](https://img.shields.io/badge/Mac%20OS-Ok-green.svg "Mac OS: Ok")
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Documentation Status](https://readthedocs.org/projects/hac-game-lib/badge/?version=latest)](https://hac-game-lib.readthedocs.io/en/latest/?badge=latest)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2849/badge)](https://bestpractices.coreinfrastructure.org/projects/2849)
[![CircleCI](https://circleci.com/gh/arnauddupuis/hac-game-lib.svg?style=svg)](https://circleci.com/gh/arnauddupuis/hac-game-lib)

# hac-game-lib
Hyrule Astronomy Club Game Library- base library for a game development

## Name change

With the growing popularity of the library we decided that it could not longer be named after our little science club.

So we took the decision to rename it to [**pygamelib**](https://pypi.org/project/pygamelib/). In the process the whole file/class hierarchy as been reworked.

Therefore the pygamelib 1.2.0+ is ***not*** backward compatible with the hac-game-lib. We are talking about **name compatibility**, 
the conversion to the new library is very easy (please see bellow for a guide). Everything else is 100% compatible (it's the same library coded by the same people).

## How to upgrade to pygamelib

Simply upgrade using pip:
```bash
pip3 install --upgrade --user hac-game-lib
```

This will automatically install pygamelib and obsoletes the hac-game-lib module. 

If you want to install system wide, not just for your current user, remove the --user option from the command line. 

## Convert from the hac-game-lib to pygamelib

The files and directories naming are now more "pythonesque", and we used the fact that lower casing all names was going
to break everything to reduce the proliferation of modules with just one class. We rationalized a bit.

So without further ado:

 * gamelib.Game, gamelib.Board, gamelib.Inventory are now unified into **pygamelib.game**.
 * gamelib.HacExceptions and gamelib.Utils are now unified into **pygamelib.base**. Hac prefix was replaced by Pgl but for convenience mirror classes were added to not break existing games.
 * gamelib.BoardItems, gamelib.Movable, gamelib.Immovable, gamelib.Characters are now unified into **pygamelib.board_items**.
 * gamelib.Actuators.Actuator, gamelib.Actuators.SimpleActuators, gamelib.Actuators.AdvancedActuators are now unified into **pygamelib.actuators**.
 * gamelib.Structures was moved to **pygamelib.assets.structures**.
 * gamelib.Sprites was deprecated in favor of gamelib.Assets.Graphics.Sprites and is now removed.
 * gamelib.Assets is now **pygamelib.assets**.
 * gamelib.Assets.Graphics is now **pygamelib.assets.graphics**.
 * gamelib.Assets.Graphics.Sprites has been renamed to **pygamelib.assets.graphics.Models**.

The gamelib.Utils module is the one that is probably going to require the most attention. It is being exploded and removed.

 * The colored squares and rectangle are now in pygamelib.assets.graphics with the exact same name.
 * 

There is also new modules and features but please see the release notes of [pygamelib](https://pypi.org/project/pygamelib/).

The general idea is to limit the number of imports and to group things by functional similitude.

Hopefully it's not too much work to convert your software. 