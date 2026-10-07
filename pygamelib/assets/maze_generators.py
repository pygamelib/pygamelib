"""
pygamelib

A library for Python 2D games.

This module contains maze generation utilities for pygamelib.

The main entry point is the :class:`~pygamelib.assets.maze_generators.MazeGenerator`
class. It uses an :class:`~pygamelib.assets.maze_generators.AlgorithmBase` subclass to
decide how the maze is carved and returns a ready to use
:class:`~pygamelib.engine.Board`.

Example::

    from pygamelib.assets import maze_generators

    generator = maze_generators.MazeGenerator(
        width=10, height=10, algorithm=maze_generators.BinaryTree, seed=42
    )
    board = generator.generate()
    board.display()
"""

__docformat__ = "restructuredtext"

import random

from pygamelib import base, board_items, engine
from pygamelib.assets import graphics
from pygamelib.gfx import core

#: The four cardinal directions used to describe the openings of a maze cell.
NORTH = "N"
EAST = "E"
SOUTH = "S"
WEST = "W"

_DIRECTION_OFFSETS = {
    NORTH: (-1, 0, SOUTH),
    EAST: (0, 1, WEST),
    SOUTH: (1, 0, NORTH),
    WEST: (0, -1, EAST),
}


class Palette(base.PglBaseObject):
    """
    A Palette describes the graphic elements used to render a maze.

    Each attribute is the model (a single character or a unicode glyph) used to build
    the :class:`~pygamelib.board_items.BoardItem` that represents a tile of the maze.

    Example::

        from pygamelib.assets import graphics, maze_generators

        palette = maze_generators.Palette(
            wall=graphics.Blocks.DARK_SHADE,
            floor=graphics.Blocks.LIGHT_SHADE,
            door=graphics.BoxDrawings.LIGHT_VERTICAL,
        )

    :param wall: Model used for the walls of the maze.
    :type wall: str
    :param floor: Model used for the walkable floor of the maze.
    :type floor: str
    :param door: Model used for the entrance and exit of the maze.
    :type door: str
    """

    def __init__(
        self,
        wall: str = graphics.Blocks.FULL_BLOCK,
        floor: str = " ",
        door: str = graphics.BoxDrawings.LIGHT_VERTICAL,
    ):
        super().__init__()
        self.wall = wall
        self.floor = floor
        self.door = door

    def __repr__(self) -> str:  # pragma: no cover
        return f"Palette(wall={self.wall!r}, floor={self.floor!r}, door={self.door!r})"


class _MazeGrid:
    """
    Internal representation of a maze.

    A grid is a ``rows`` by ``cols`` matrix of cells. Each cell stores the set of
    directions that are open (i.e. where there is no wall). Two adjacent cells that
    are connected share the corresponding opening, so carving is always symmetric.

    :param cols: Number of columns of the maze.
    :type cols: int
    :param rows: Number of rows of the maze.
    :type rows: int
    """

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.open = [[set() for _ in range(cols)] for _ in range(rows)]

    def carve(self, row: int, column: int, direction: str) -> bool:
        """
        Remove the wall between a cell and its neighbor in ``direction``.

        Both cells are updated so that the opening is symmetric. If the neighbor is
        outside of the grid, nothing is done.

        :param row: Row of the cell.
        :type row: int
        :param column: Column of the cell.
        :type column: int
        :param direction: One of :data:`NORTH`, :data:`EAST`, :data:`SOUTH`,
           :data:`WEST`.
        :type direction: str
        :return: ``True`` if the wall was removed, ``False`` otherwise.
        :rtype: bool
        """
        d_row, d_column, opposite = _DIRECTION_OFFSETS[direction]
        n_row, n_column = row + d_row, column + d_column
        if not (0 <= n_row < self.rows and 0 <= n_column < self.cols):
            return False
        self.open[row][column].add(direction)
        self.open[n_row][n_column].add(opposite)
        return True

    def is_open(self, row: int, column: int, direction: str) -> bool:
        """
        Tell if a cell has an opening in a given direction.

        :param row: Row of the cell.
        :type row: int
        :param column: Column of the cell.
        :type column: int
        :param direction: One of :data:`NORTH`, :data:`EAST`, :data:`SOUTH`,
           :data:`WEST`.
        :type direction: str
        :return: ``True`` if the cell is open in that direction.
        :rtype: bool
        """
        return direction in self.open[row][column]


class AlgorithmBase(base.PglBaseObject):
    """
    Base class for all maze generation algorithms.

    An algorithm is responsible for carving a :class:`_MazeGrid`. Subclasses must
    implement :meth:`carve`.

    Example::

        class MyAlgorithm(AlgorithmBase):
            def carve(self, grid, rng):
                # carve the grid however you like
                ...

        generator = MazeGenerator(algorithm=MyAlgorithm)

    :param width: Width (number of columns) of the maze to generate.
    :type width: int
    :param height: Height (number of rows) of the maze to generate.
    :type height: int
    :param seed: Optional seed used to make the generation reproducible.
    :type seed: int
    """

    def __init__(self, width: int = 10, height: int = 10, seed: int = None):
        super().__init__()
        self.width = width
        self.height = height
        self.seed = seed

    def generate(self) -> _MazeGrid:
        """
        Create a grid of the algorithm's size and carve it.

        :return: The carved maze grid.
        :rtype: :class:`_MazeGrid`
        """
        if self.width < 1 or self.height < 1:
            raise base.PglInvalidTypeException(
                f"Maze dimensions must be positive integers, got "
                f"{self.width}x{self.height}."
            )
        grid = _MazeGrid(self.width, self.height)
        rng = random.Random(self.seed)
        self.carve(grid, rng)
        return grid

    def carve(self, grid: _MazeGrid, rng: random.Random) -> None:
        """
        Carve the maze grid.

        This method must be implemented by subclasses.

        :param grid: The grid to carve.
        :type grid: :class:`_MazeGrid`
        :param rng: The random number generator to use.
        :type rng: :class:`random.Random`
        """
        raise NotImplementedError(
            "AlgorithmBase subclasses must implement the carve() method."
        )


class BinaryTree(AlgorithmBase):
    """
    The binary tree algorithm.

    For each cell of the maze, the algorithm randomly carves either the northern or
    the eastern neighbor (when they exist). It is very simple and fast but produces a
    strong bias towards the north-east corner (every cell has a passage to the north
    or to the east, so the whole north row and east column are corridors).
    """

    def carve(self, grid: _MazeGrid, rng: random.Random) -> None:
        for row in range(grid.rows):
            for column in range(grid.cols):
                choices = []
                if row > 0:
                    choices.append(NORTH)
                if column < grid.cols - 1:
                    choices.append(EAST)
                if choices:
                    grid.carve(row, column, rng.choice(choices))


class Sidewinder(AlgorithmBase):
    """
    The sidewinder algorithm.

    The algorithm walks each row from west to east while growing a "run" of cells. At
    each step it either extends the run to the east or closes it by carving a passage
    to the north from a random member of the run. The top row is always a single
    corridor.
    """

    def carve(self, grid: _MazeGrid, rng: random.Random) -> None:
        for row in range(grid.rows):
            run = []
            for column in range(grid.cols):
                run.append((row, column))
                at_eastern_boundary = column == grid.cols - 1
                at_northern_boundary = row == 0
                close_run = at_eastern_boundary or (
                    not at_northern_boundary and rng.random() < 0.5
                )
                if close_run:
                    member = rng.choice(run)
                    if member[0] > 0:
                        grid.carve(member[0], member[1], NORTH)
                    run = []
                else:
                    grid.carve(row, column, EAST)


class MazeGenerator(base.PglBaseObject):
    """
    Generate a maze as a :class:`~pygamelib.engine.Board`.

    The generator is configured with a size, an algorithm and a palette. Calling
    :meth:`generate` builds a board where walls are
    :class:`~pygamelib.board_items.Wall` items and the floor is made of
    :class:`~pygamelib.board_items.Tile` items, using the models from the palette.

    The board is twice as big as the maze (plus one row and one column for the outer
    walls): a maze of ``width`` by ``height`` cells becomes a board of
    ``2 * width + 1`` by ``2 * height + 1`` cells.

    Example::

        from pygamelib.assets import maze_generators

        generator = maze_generators.MazeGenerator(
            width=15, height=10, algorithm=maze_generators.Sidewinder
        )
        board = generator.generate()
        board.display()

    :param width: Width (number of cells) of the maze.
    :type width: int
    :param height: Height (number of cells) of the maze.
    :type height: int
    :param algorithm: The algorithm to use. It can be a subclass of
       :class:`AlgorithmBase` or an instance of one.
    :type algorithm: type
    :param palette: The palette used to render the maze.
    :type palette: :class:`Palette`
    :param seed: Optional seed used to make the generation reproducible.
    :type seed: int
    """

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        algorithm=None,
        palette: Palette = None,
        seed: int = None,
    ):
        super().__init__()
        if width < 1 or height < 1:
            raise base.PglInvalidTypeException(
                f"Maze dimensions must be positive integers, got {width}x{height}."
            )
        self.width = width
        self.height = height
        self.algorithm = BinaryTree if algorithm is None else algorithm
        self.palette = Palette() if palette is None else palette
        self.seed = seed

    def _make_algorithm(self) -> AlgorithmBase:
        """
        Instantiate the configured algorithm.

        :return: An algorithm ready to carve a grid.
        :rtype: :class:`AlgorithmBase`
        """
        algorithm = self.algorithm
        if isinstance(algorithm, type):
            if not issubclass(algorithm, AlgorithmBase):
                raise base.PglInvalidTypeException(
                    f"{algorithm!r} is not a subclass of AlgorithmBase."
                )
            return algorithm(width=self.width, height=self.height, seed=self.seed)
        if isinstance(algorithm, AlgorithmBase):
            return algorithm
        raise base.PglInvalidTypeException(
            f"{algorithm!r} is neither a subclass nor an instance of AlgorithmBase."
        )

    def _is_wall(self, grid: _MazeGrid, row: int, column: int) -> bool:
        """
        Tell if a board cell (in board coordinates) is a wall.

        Board cells alternate between maze cells (odd, odd) and the walls that
        separate them.

        :param grid: The carved grid.
        :type grid: :class:`_MazeGrid`
        :param row: Row in board coordinates.
        :type row: int
        :param column: Column in board coordinates.
        :type column: int
        :return: ``True`` if the board cell is a wall.
        :rtype: bool
        """
        if row % 2 == 1 and column % 2 == 1:
            # That's the center of a maze cell: always a floor.
            return False
        if row % 2 == 1 and column % 2 == 0:
            # Vertical wall between two horizontally adjacent cells.
            cell_row = (row - 1) // 2
            cell_column = column // 2
            if cell_column == 0 or cell_column == grid.cols:
                return True
            return not grid.is_open(cell_row, cell_column - 1, EAST)
        if row % 2 == 0 and column % 2 == 1:
            # Horizontal wall between two vertically adjacent cells.
            cell_row = row // 2
            cell_column = (column - 1) // 2
            if cell_row == 0 or cell_row == grid.rows:
                return True
            return not grid.is_open(cell_row - 1, cell_column, SOUTH)
        # Posts (corners between four cells) are always walls.
        return True

    def generate(self, name: str = "Maze", doors: bool = True) -> engine.Board:
        """
        Generate the maze and return it as a :class:`~pygamelib.engine.Board`.

        :param name: The name of the generated board.
        :type name: str
        :param doors: If ``True`` (default) the outer wall is opened at the top-left
           and bottom-right corners and the openings are marked with the palette's
           door model.
        :type doors: bool
        :return: A board containing the maze.
        :rtype: :class:`~pygamelib.engine.Board`
        """
        grid = self._make_algorithm().generate()
        board_width = grid.cols * 2 + 1
        board_height = grid.rows * 2 + 1
        board = engine.Board(name=name, size=[board_width, board_height])

        entrance = (0, 1)
        exit_position = (board_height - 1, board_width - 2)

        wall_item = board_items.Wall(model=self.palette.wall)
        door_item = board_items.Door(model=self.palette.door)

        for row in range(board_height):
            for column in range(board_width):
                position = (row, column)
                if doors and position in (entrance, exit_position):
                    board.place_item(door_item, row, column)
                elif self._is_wall(grid, row, column):
                    board.place_item(wall_item, row, column)
                else:
                    board.place_item(
                        board_items.Tile(
                            sprite=core.Sprite(
                                size=[1, 1],
                                default_sprixel=core.Sprixel(model=self.palette.floor),
                            )
                        ),
                        row,
                        column,
                    )
        return board
