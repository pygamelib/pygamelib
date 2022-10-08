.. :changelog:

Release notes
=============

1.3.0 (2022-10-07)
------------------

This release is massive. Please read the documentation for specific changes to classes. It is available at https://pygamelib.readthedocs.io/en/latest/index.html.

⬆️ Main updates
^^^^^^^^^^^^^^^

 * **New feature:** The ``pygamelib.engine.Screen`` class now has a new **Improved Screen Management** double buffered system. This set of methods allow for a simplified management of the console screen. It is also faster than the *Legacy Direct Display* system. Please read the documentation (https://pygamelib.readthedocs.io/en/latest/pygamelib.engine.Screen.html) and the wiki on the Github repository for more about the differences. You will probably want to switch to the new stack as soon as possible. Both systems are clearly identified in the documentation by visible tags. Most of the new features of this release are **NOT** compatible with the *Legacy Direct Display* system. It still received updates and new features but will probably be deprecated in future updates.
 * **New feature:** Introducing the ``pygamelib.gfx.ui`` module! The beginning of a module for all your game/application user interface needs. The module is in alpha for the moment, feel free to voice your feedback. This module is only compatible with the **Improved Screen Management**.
 * **New feature:** A new tool has been added to the library: pgl-sprite-editor. An editor to create or edit sprites and sprite based animations.
 * **New feature:** ``pygamelib.engine.Game`` can now be created as a Singleton through the ``instance()`` method.
 * **New feature:** Add a particle system to the library! It includes a number of new classes that are located in the ``pygamelib.gfx.particles`` submodule. This module is only compatible with the **Improved Screen Management**.
 * **New feature:** introducing ``pygamelib.gfx.core.Font``, a Sprite based font system. This release come with an "8bits" font and a couple of font imported from FIGlet!
 * **New feature:** Add a Color class (``pygamelib.gfx.core.Color``) to entirely abstract the color system.
 * **New feature:** All objects can now be properly serialized and loaded through a streamlined process. Look for the `serialize()` and `load()` methods.
 * **New feature:** New base object ``pygamelib.base.PglBaseObject``, all objects that inherits from python's ``object`` are now inheriting from this new one. It implements a couple of base features but the most important is the modified `Observer` design pattern that is the base of a refactoring to event base communication within the library.
 * **New feature:** Added a new board item: ``pygamelib.board_item.Camera``. It is a specific item that is not shown on the board. It can be used for cinematic for example. Please read the documentation for more information.
 * **New feature/improvement:** The `Board` object has been reworked to allow for a third dimension. It now has a new property called `layer`. Layers are automatically added and removed to fit the need of overlapping items. `Board.place_item()` also accept a new layer parameter to set the layer (if you want to put stuff over the player for example). An example is visible here: https://www.youtube.com/watch?v=9cOt63ZAJOk.
 * *Improvement:* Most resources intensive array/list have been replaced by numpy arrays. This brings better performances for ``pygamelib.engine.Board`` and for ``pygamelib.engine.Screen``.
 * *Improvement:* Add a new algorithm to the PathFinder actuator: A*.
 * *Improvement*: ``pygamelib.gfx.core.Sprite`` can now be tinted or modulated with a color. Both operation do the same thing: change the color of the sprite by applying a color at a given ratio. However, ``tint()`` returns a new sprite and does not modify the original sprite while ``modulate()`` returns nothing and modify the sprite directly.

⚠️ Breaking changes
^^^^^^^^^^^^^^^^^^^

 * ``pygamelib.board_items.BoardItem`` constructor parameter changed: ``type`` is now ``item_type``.
 * ``pygamelib.board_items.BoardItem``: there was a conflict with ``inventory_space``. It was defined both as a property and a method. The method has been removed and `BoardItem.inventory_space` is now a proper python property. Concretely: you might have to remove parenthesis when using ``any_item.inventory_space`` (vs the old ``any_item.inventory_space()``).
 * The new ``pygamelib.gfx.core.Color`` replaces ``Terminal.on_color_rgb()`` and ``Terminal.color_rgb()``. It is much easier to use (just use the Color object and the pygamelib will manage foreground and background differences) but it requires to change the initialization of every Sprixel and Text of your game (sorry...).
 * When using the new Improved Screen Management stack and partial display at the same time, you now have to set ``Board.partial_display_focus``. It is not breaking anything in existing code but it will not behave as you want is you just ``Screen.place()`` your board (that uses partial display) without setting the `partial_display_focus` to the player first.

🔧 Other changes
^^^^^^^^^^^^^^^^

 * *Improvement*: pgl-editor now uses Sprixels instead of regular characters allowing for more possible customization and features in the Board and Screen.
 * *Improvement*: in pgl-editor it is now possible to generate a random color in the color editor.
 * *Improvement*: All actuators now return ``pygamelib.constants.NO_DIR`` if there is no direction available to ``next_move()``. This makes the actuators behavior more consistent particularly when they are overloaded.
 * *Improvement*: The ``RandomActuator`` behavior has been reworked. It now choose a direction and follow it for a certain distance before choosing a new direction. It also detect when it is stuck an, in that case, pick a new direction.
 * *Improvement*: Add ``display_sprite()`` and ``display_sprite_at()`` method to Screen. These methods can display a ``pygamelib.gfx.core.Sprite`` on screen.
 * *Improvement*: Inventory has been improved to be more versatile and less limited. It now behaves like an enhanced list of objects. A rudimentary constraints system was added (for example to limit the number of certain types of items). The new inventory is also fully plugged into the observer/notifications system.
 * *Improvement*: All `BoardItem` now have configurable properties for `restorable`, `overlappable`, `pickable` and `can_move`.
 * *Improvement*: ``pygamelib.board_items.BoardComplexItem.sprite`` is now a `@property` instead of a class variable. That property automatically call `update_sprite()`.
 * *Improvement*: When ``Game.mode`` is set to ``pygamelib.constants.MODE_RT``, all ``pygamelib.board_items.Movable`` now accumulate movement vectors (when using vectors). This means that non unit movement patterns are now possible. 
 * *Improvement*: The new ``pygamelib.base.Console`` implements a Singleton design pattern. You can now get a unique reference to the ``blessed.Terminal`` (the object wrapped in Console) object by calling `Console.instance()`.
 * Fixed a bug in ``pygamelib.engine.Screen.display_at()``: it was not possible to display anything after (below a Board). It is now possible.
 * *Improvement*: ``pygamelib.base.Text`` has improved a lot. It can now use the Font system, has new attributes and is now a `PglBaseObject`. Please read the documentation for more.
 * *Improvement*: Sprixels and Sprites now have their own deepcopy operator: ``Sprixel.copy()`` and ``Sprite.copy()``.
 * *Improvement*: It is now possible to set the transparency of all sprixels of a sprite by using ``Sprite.set_transparency()``.
 * Fixed a bug with `restorable` items: now all board items can be set to be restorable.
 * Fixed a bug in pgl-editor when editing large boards that require partial display. The viewport was not correctly restored.
 * Fixed issues with the library's inheritance graph.
 * Fixed a bug in ``pygamelib.engine.Game`` where the partial display settings (when set at in the Game instance), were not correctly passed down to the Board.
 * Fixed the sphinx dependencies (for building the doc).
 * Fixed the mess in the sphinx files to generate the documentation.
 * Fixed an issue with linting dependencies.
 * Removed legacy files from older version of the library.

I would like to thank all the contributors (https://pygamelib.readthedocs.io/en/latest/authors.html) for their work on this massive update.

The new pygamelib logo was done by an awesome artist: Jack Tseng (https://hellojacktseng.carrd.co/ https://twitter.com/HelloJackTseng) please have a look at their amazing work!!

1.2.3 (2020-09-01)
------------------

Emergency release: fix a regression introduced by v1.2.2.

1.2.2 (2020-09-01)
------------------

 * Fix issue with imports for Python 3.6
 * Fix an issue with the way pygamelib.engine.Screen test the terminal on Windows.


1.2.0 (2020-08-29)
------------------

 * Renamed the entire library from hac-game-lib to pygamelib.
 * ***Breaking change:*** The library has been heavily refactored and this creates some issues. Please have a look at `the migration notes <https://github.com/arnauddupuis/pygamelib/wiki/Migrating-from-hac%E2%80%90game%E2%80%90lib-1.1.x-to-pygamelib-1.2.0>`_
 * **New feature:** Items that can be represented on more than one cell. We call them complex items. There's a lot of new complex items: ComplexPlayer and ComplexNPC of course, but also ComplexWall, ComplexDoor, ComplexTreasure and the general purpose Tile object.
 * **New feature:** Going, with complex item we now have a proper sprite system with the gfx.core.Sprite class.
 * **New feature:** In addition to the regular model we now have a new concept: the Sprixel. A Sprite is made of many Sprixels.
 * **New feature:** New JSON based file format to save, load and distribute sprites and/or sprixels.
 * **New feature:** All these sprites can be grouped into a SpriteCollection that in turn can be saved in our new sprite file format.
 * **New feature:** New Math library. This one starts small but will grow. It makes calculating the distance and intersections easier.
 * **New feature:** New Vector2D class to represent forces and movement as a vector. It is now possible to give a vector to the move() method.
 * **New feature:** Gave some love to text. There are now 2 objects dedicated to text: base.Text to manipulate text and board_items.TextItem to easily place text on a board.
 * **New feature:** A Screen object has been added to make the screen manipulation simpler.
 * **New feature:** The Game object now has a run() method that act as the main game loop. It calls a user defined update function and takes care of a lot of things. It runs until the Game.state is set to STOPPED.
 * **New feature:** The Game object can now turn by turn or real time. All movables can be configured to have time based or turn based movement speed.
 * *Improvement*: The Animation class now support both regular strings (models), Sprixel and Sprite.
 * *Improvement*: All complex items obviously support (actually requires) sprites but all regular board items now supports sprixels.
 * *Improvement*: Test coverage dramatically improved. It has jumped from 25% to 98%.
 * *Improvement*: Lots of objects now have attributes to easily access and/or set properties like position (mostly read only), width, height, etc.
 * *Improvement*: Converted the editor to pygamelib and renamed it pgl-editor.py. Also added a multi page selector and integrated the new graphic assets.
 * *Improvement*: All movables can now have different vertical and horizontal "steps" parameters.
 * Cleaned up the repository (it was becoming seriously messy).
 * Change the prefix of all exceptions from HAc to Pgl.
 * Added a NO_PLAYER constant to tell the game object that he should not expect a player object.
 * Improve the generated documentation.
 * Various improvements in exceptions raising across the library. Please see the documentation (that was also updated).
 * Various bug fixing in the Suparex example.

I also need to give some kudos to the kids of the Hyrule Astronomy Club for thorough testing of Suparex. They found well hidden bug and exploitable bugs. Special thanks to Arthur who found many glitches.
Congratulations to Arthur and Hadrien that successfully exploited them to achieve extremely high scores (up to 12000!!!).


1.1.1 (2020-07-18)
------------------

* Fix a bug in hgl-editor: when using previously recorded parameters to create a board the editor was crashing.
* *Improvement*: Automatically enable partial display and map bigger than 40x40.
* Fix a bug a coordinates in Board.item()

1.1.0 (2020-06-12)
------------------

* Fix many issues with strings all across the library.
* Fix many issues with variables interpolation in exceptions.
* Fix a bug in Game.load_board() that was causing corruptions.
* Fix multiple typos in the documentation.
* Fix an issue with the user directory in hgl-editor
* Fix many issues with the PatrolActuator.
* **New feature:** partial display (dynamically display only a part of a board)
* **New feature:** new mono directional actuator.
* **New feature:** projectiles (can be sent and completely managed by the game object)
* **New feature:** new assets module to hold many non core submodules.
* **New feature:** Assets.Graphics that add thousands of glyphs (including emojis) to
  the current capacities of the library.
* **New feature:** Add support for PatrolActuator in hgl-editor.
* **New feature:** Add support for PathFinder actuator in hgl-editor.
* **New feature:** Add an object parent system.
* **New feature:** Add a configuration system to hgl-editor.
* *Improvement*: Add full configuration features to the Game object.
* *Improvement*: Add a new example in the form of a full procedural generation platform
  game (see examples/suparex).
* *Improvement*: Improved performances particularly around the features that relies on
  Board.place_item(). Up to 70 times faster.
* *Improvement*: It is now possible to specify the first frame index in Animation.
* *Improvement*: Formatted all the code with black.
* *Improvement*: PathFinder.add_waypoint() now sets the destination if it wasn't set
  before.

1.0.1 (2020-05-17)
------------------

* Fix a huge default save directory issue (see complete announcement) in hgl-editor.
* Fix lots of strings in hgl-editor.
* Fix a type issue in the Inventory class for the not_enough_space exception.
* Improve Board.display() performances by 15% (average).

1.0.0 (2020-03-20)
------------------

* Add AdvancedActuators.PathFinder `@arnauddupuis`_
* Add test cases for BoardItem `@grimmjow8`_ `@Arekenaten`_
* Add test cases for Board `@grimmjow8`_ `@Arekenaten`_
* Add support to load files from the directories in directories.json `@kaozdl`_
* Add a new SimpleActuators.PatrolActuator `@kaozdl`_
* Add Animation capabilities `@arnauddupuis`_
* Improve navigation in hgl-editor by using arrow keys `@bwirtz`_
* Improve selection of maps in hgl-editor `@gunjanraval`_ `@kaozdl`_
* Improve documentation for SimpleActuators.PathActuator `@achoudh5`_
* Improve documentation for launching the test suite `@bwirtz`_
* Migration from pip install to pipenv `@kaozdl`_
* Fix board saving bug in hgl-editor `@gunjanraval`_
* Fix back menu issues in hgl-editor `@synackray`_
* Fix README and setup.py `@fbidu`_
* Make the module compatible with Flake8: `@bwirtz`_ `@arnauddupuis`_ `@kaozdl`_
  `@f-osorio`_ `@guilleijo`_ `@diego-caceres`_ `@spassarop`_
* CircleCI integration `@caballerojavier13`_ `@bwirtz`_


.. _`@arnauddupuis`: https://github.com/arnauddupuis
.. _`@kaozdl`: https://github.com/kaozdl
.. _`@Dansyuqri`: https://github.com/Dansyuqri
.. _`@grimmjow8`: https://github.com/grimmjow8
.. _`@Arekenaten`: https://github.com/Arekenaten
.. _`@gunjanraval`: https://github.com/gunjanraval
.. _`@achoudh5`: https://github.com/achoudh5
.. _`@synackray`: https://github.com/synackray
.. _`@fbidu`: https://github.com/fbidu
.. _`@bwirtz`: https://github.com/bwirtz
.. _`@f-osorio`: https://github.com/f-osorio
.. _`@guilleijo`: https://github.com/guilleijo
.. _`@diego-caceres`: https://github.com/diego-caceres
.. _`@spassarop`: https://github.com/spassarop
.. _`@caballerojavier13`: https://github.com/caballerojavier13


2019.5
------

* Please see `the official website <https://astro.hyrul.es/news/hac-game-lib-may-2019-update.html>`_.

pre-2019.5
----------

* Please see the `Github <https://github.com/arnauddupuis/hac-game-lib/commits/master>`_ for history.
