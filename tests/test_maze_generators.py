"""
Unit tests for the maze generators in pygamelib.assets.maze_generators.
"""

import unittest
from collections import deque

from pygamelib import base
from pygamelib.assets import graphics, maze_generators


class TestMazeGenerator(unittest.TestCase):
    def _reachable_cells(self, board):
        """Return the set of maze cells (odd, odd) reachable from the top-left."""
        height, width = board.size[1], board.size[0]

        def is_wall(row, column):
            return board._matrix[row][column][-1].name in ("wall", "Door")

        start = (1, 1)
        seen = {start}
        queue = deque([start])
        while queue:
            row, column = queue.popleft()
            for d_row, d_column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n_row, n_column = row + d_row, column + d_column
                if (
                    0 <= n_row < height
                    and 0 <= n_column < width
                    and (n_row, n_column) not in seen
                    and not is_wall(n_row, n_column)
                ):
                    seen.add((n_row, n_column))
                    queue.append((n_row, n_column))
        return {
            (row, column) for row, column in seen if row % 2 == 1 and column % 2 == 1
        }

    def _all_cells(self, board):
        return {
            (row, column)
            for row in range(1, board.size[1], 2)
            for column in range(1, board.size[0], 2)
        }

    def _pattern(self, board):
        """Return the maze as a string of the top item's model per cell."""
        rows = []
        for row in range(board.size[1]):
            rows.append(
                "".join(
                    board._matrix[row][column][-1].sprixel.model
                    for column in range(board.size[0])
                )
            )
        return "\n".join(rows)

    def test_generate_board_dimensions(self):
        generator = maze_generators.MazeGenerator(width=6, height=4)
        board = generator.generate()
        self.assertEqual(board.size, [13, 9])
        self.assertEqual(board.name, "Maze")

    def test_custom_name(self):
        board = maze_generators.MazeGenerator(width=3, height=3).generate(name="Level1")
        self.assertEqual(board.name, "Level1")

    def test_every_maze_cell_is_floor(self):
        board = maze_generators.MazeGenerator(width=5, height=5, seed=1).generate()
        for row, column in self._all_cells(board):
            self.assertNotIn(board._matrix[row][column][-1].name, ("wall", "Door"))

    def test_outer_border_is_wall_except_doors(self):
        board = maze_generators.MazeGenerator(width=5, height=5, seed=1).generate()
        height, width = board.size[1], board.size[0]
        entrance = (0, 1)
        exit_position = (height - 1, width - 2)
        for column in range(width):
            self.assertEqual(
                board._matrix[0][column][-1].name,
                "Door" if (0, column) == entrance else "wall",
            )
            self.assertEqual(
                board._matrix[height - 1][column][-1].name,
                "Door" if (height - 1, column) == exit_position else "wall",
            )
        for row in range(height):
            self.assertEqual(board._matrix[row][0][-1].name, "wall")
            self.assertEqual(board._matrix[row][width - 1][-1].name, "wall")

    def test_no_doors(self):
        board = maze_generators.MazeGenerator(width=5, height=5, seed=1).generate(
            doors=False
        )
        height, width = board.size[1], board.size[0]
        self.assertEqual(board._matrix[0][1][-1].name, "wall")
        self.assertEqual(board._matrix[height - 1][width - 2][-1].name, "wall")

    def test_maze_is_fully_connected(self):
        for algorithm in (maze_generators.BinaryTree, maze_generators.Sidewinder):
            board = maze_generators.MazeGenerator(
                width=8, height=6, algorithm=algorithm, seed=7
            ).generate()
            reachable = self._reachable_cells(board)
            self.assertEqual(reachable, self._all_cells(board))

    def test_seed_makes_generation_reproducible(self):
        first = maze_generators.MazeGenerator(width=6, height=6, seed=99).generate()
        second = maze_generators.MazeGenerator(width=6, height=6, seed=99).generate()
        self.assertEqual(self._pattern(first), self._pattern(second))

    def test_different_seeds_differ(self):
        first = maze_generators.MazeGenerator(
            width=10, height=10, seed=1, algorithm=maze_generators.Sidewinder
        ).generate()
        second = maze_generators.MazeGenerator(
            width=10, height=10, seed=2, algorithm=maze_generators.Sidewinder
        ).generate()
        self.assertNotEqual(self._pattern(first), self._pattern(second))

    def test_algorithm_can_be_an_instance(self):
        algorithm = maze_generators.BinaryTree(width=4, height=4, seed=3)
        board = maze_generators.MazeGenerator(algorithm=algorithm).generate()
        self.assertEqual(board.size, [9, 9])

    def test_default_algorithm_is_binary_tree(self):
        generator = maze_generators.MazeGenerator(width=4, height=4)
        self.assertIs(generator.algorithm, maze_generators.BinaryTree)
        board = generator.generate()
        self.assertEqual(board.size, [9, 9])

    def test_custom_palette(self):
        palette = maze_generators.Palette(
            wall=graphics.Blocks.DARK_SHADE,
            floor=graphics.Blocks.LIGHT_SHADE,
            door=graphics.BoxDrawings.LIGHT_VERTICAL,
        )
        board = maze_generators.MazeGenerator(
            width=3, height=3, palette=palette, seed=1
        ).generate()
        self.assertEqual(
            board._matrix[0][0][-1].sprixel.model, graphics.Blocks.DARK_SHADE
        )
        self.assertEqual(
            board._matrix[1][1][-1].sprixel.model, graphics.Blocks.LIGHT_SHADE
        )
        self.assertEqual(
            board._matrix[0][1][-1].sprixel.model,
            graphics.BoxDrawings.LIGHT_VERTICAL,
        )

    def test_invalid_algorithm_type(self):
        with self.assertRaises(base.PglInvalidTypeException):
            maze_generators.MazeGenerator(algorithm=object).generate()
        with self.assertRaises(base.PglInvalidTypeException):
            maze_generators.MazeGenerator(algorithm="not an algorithm").generate()

    def test_invalid_dimensions(self):
        with self.assertRaises(base.PglInvalidTypeException):
            maze_generators.MazeGenerator(width=0, height=5)
        with self.assertRaises(base.PglInvalidTypeException):
            maze_generators.MazeGenerator(width=5, height=-1)

    def test_algorithm_base_cannot_carve(self):
        algorithm = maze_generators.AlgorithmBase(width=2, height=2)
        with self.assertRaises(NotImplementedError):
            algorithm.generate()

    def test_algorithm_base_invalid_dimensions(self):
        with self.assertRaises(base.PglInvalidTypeException):
            maze_generators.AlgorithmBase(width=0, height=2).generate()


class TestMazeGrid(unittest.TestCase):
    def test_carve_is_symmetric(self):
        grid = maze_generators._MazeGrid(3, 3)
        self.assertTrue(grid.carve(1, 1, maze_generators.EAST))
        self.assertTrue(grid.is_open(1, 1, maze_generators.EAST))
        self.assertTrue(grid.is_open(1, 2, maze_generators.WEST))

    def test_carve_out_of_bounds_returns_false(self):
        grid = maze_generators._MazeGrid(2, 2)
        self.assertFalse(grid.carve(0, 0, maze_generators.NORTH))
        self.assertFalse(grid.carve(0, 0, maze_generators.WEST))
        self.assertFalse(grid.is_open(0, 0, maze_generators.NORTH))

    def test_new_grid_has_no_openings(self):
        grid = maze_generators._MazeGrid(2, 2)
        for row in range(2):
            for column in range(2):
                for direction in (
                    maze_generators.NORTH,
                    maze_generators.EAST,
                    maze_generators.SOUTH,
                    maze_generators.WEST,
                ):
                    self.assertFalse(grid.is_open(row, column, direction))


class TestPalette(unittest.TestCase):
    def test_default_palette(self):
        palette = maze_generators.Palette()
        self.assertEqual(palette.wall, graphics.Blocks.FULL_BLOCK)
        self.assertEqual(palette.floor, " ")
        self.assertEqual(palette.door, graphics.BoxDrawings.LIGHT_VERTICAL)


if __name__ == "__main__":
    unittest.main()
