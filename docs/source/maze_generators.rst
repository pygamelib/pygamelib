maze generators
===============

The maze generators module provides a set of algorithms to generate mazes and a
:class:`~pygamelib.assets.maze_generators.MazeGenerator` class that turns them into a
ready to use :class:`~pygamelib.engine.Board`.

The :class:`~pygamelib.assets.maze_generators.MazeGenerator` builds a board where walls
are :class:`~pygamelib.board_items.Wall` items and the floor is made of
:class:`~pygamelib.board_items.Tile` items. The models used for the walls, the floor
and the entrance/exit doors are configured through a
:class:`~pygamelib.assets.maze_generators.Palette`.

The generation is fully reproducible when a ``seed`` is given, which is useful while
developing a level. Two algorithms are provided out of the box:

 * :class:`~pygamelib.assets.maze_generators.BinaryTree`
 * :class:`~pygamelib.assets.maze_generators.Sidewinder`

New algorithms can be added by subclassing
:class:`~pygamelib.assets.maze_generators.AlgorithmBase`.

Example::

    from pygamelib.assets import maze_generators

    generator = maze_generators.MazeGenerator(
        width=18,
        height=10,
        algorithm=maze_generators.Sidewinder,
        seed=42,
    )
    board = generator.generate()
    board.display()

The maze generators module contains the following classes:

.. toctree::
    pygamelib.assets.maze_generators.AlgorithmBase
    pygamelib.assets.maze_generators.BinaryTree
    pygamelib.assets.maze_generators.MazeGenerator
    pygamelib.assets.maze_generators.Palette
    pygamelib.assets.maze_generators.Sidewinder

.. automodule:: pygamelib.assets.maze_generators
    :noindex:
