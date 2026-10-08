import examples_includes  # noqa: F401

# The terrain generators live in the assets sub-module.
from pygamelib.assets import graphics, terrain_generators
from pygamelib.gfx import core

# Pick a palette: the terrain is drawn with unicode glyphs and colors. The forest is
# rendered with the earth ground glyph to stand out from the plains.
palette = terrain_generators.TerrainPalette()
palette.set_feature(
    "forest",
    terrain_generators.TerrainFeature(
        name="forest",
        model=graphics.MiscTechnicals.EARTH_GROUND,
        fg_color=core.Color(51, 110, 57),
    ),
)

# Create a generator. The seed makes the result reproducible, which is handy while
# developing a level. island=True surrounds the land with deep water.
generator = terrain_generators.TerrainGenerator(
    width=60,
    height=30,
    palette=palette,
    seed=42,
    island=True,
)

# generate() returns a ready to use pygamelib Board.
world = generator.generate(name="The Island")
world.display()
