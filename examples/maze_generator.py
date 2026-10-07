import examples_includes  # noqa: F401

# The maze generators live in the assets sub-module.
from pygamelib.assets import graphics, maze_generators

# Pick a palette: walls are dark blocks, floors are light blocks and the
# entrance/exit are vertical lines.
palette = maze_generators.Palette(
    wall=graphics.Blocks.DARK_SHADE,
    floor=graphics.Blocks.LIGHT_SHADE,
    door=graphics.BoxDrawings.LIGHT_VERTICAL,
)

# Create a generator. The seed makes the result reproducible, which is handy
# while developing a level.
generator = maze_generators.MazeGenerator(
    width=18,
    height=10,
    algorithm=maze_generators.Sidewinder,
    palette=palette,
    seed=42,
)

# generate() returns a ready to use pygamelib Board.
maze = generator.generate(name="The Maze")
maze.display()
