.. :changelog:

History
-------
1.2.0 (2020-08-29)
~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~

* Fix a bug in hgl-editor: when using previously recorded parameters to create a board the editor was crashing.
* *Improvement*: Automatically enable partial display and map bigger than 40x40.
* Fix a bug a coordinates in Board.item()

1.1.0 (2020-06-12)
~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~

* Fix a huge default save directory issue (see complete announcement) in hgl-editor.
* Fix lots of strings in hgl-editor.
* Fix a type issue in the Inventory class for the not_enough_space exception.
* Improve Board.display() performances by 15% (average).

1.0.0 (2020-03-20)
~~~~~~~~~~~~~~~~~~~

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
~~~~~~

* Please see `the official website <https://astro.hyrul.es/news/hac-game-lib-may-2019-update.html>`_.

pre-2019.5
~~~~~~~~~~

* Please see the `Github <https://github.com/arnauddupuis/hac-game-lib/commits/master>`_ for history.
