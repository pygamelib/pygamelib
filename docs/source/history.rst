.. :changelog:

History
-------
1.1.1 (2020-07-15)
~~~~~~~~~~~~~~~~~~

* Fix a bug in hgl-editor: when using previously recorded parameters to create a board the editor was crashing.
* *Improvement*: Automatically enable partial display and map bigger than 40x40.

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
