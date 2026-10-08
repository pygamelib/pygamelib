terrain generators
==================

The terrain generators module builds random outdoor terrain as a ready to use
:class:`~pygamelib.engine.Board`.

It samples an OpenSimplex noise field to decide the altitude of every cell and
classifies it into a :class:`~pygamelib.assets.terrain_generators.TerrainFeature`
(deep water, water, shore, plain, forest, hill, mountain or snow). The board is then
filled with :class:`~pygamelib.board_items.Tile` items built from a
:class:`~pygamelib.assets.terrain_generators.TerrainPalette`, so the terrain can be
displayed or used as the base of an outdoor level.

Features are rendered with the models, colors and sprites of the palette, which makes
it possible to use the unicode glyphs from the
:class:`~pygamelib.assets.graphics` module or a full
:class:`~pygamelib.gfx.core.Sprite` for a richer feature such as a tree.

The generation is fully reproducible when a ``seed`` is given, which is useful while
developing a level. Setting ``island`` to ``True`` applies a radial falloff so the
result is an island surrounded by deep water instead of a continental land mass.

Example::

    from pygamelib.assets import terrain_generators

    generator = terrain_generators.TerrainGenerator(
        width=60,
        height=30,
        seed=42,
        island=True,
    )
    board = generator.generate()
    board.display()

The terrain generators module contains the following classes:

.. toctree::
    pygamelib.assets.terrain_generators.TerrainFeature
    pygamelib.assets.terrain_generators.TerrainPalette
    pygamelib.assets.terrain_generators.TerrainGenerator

.. automodule:: pygamelib.assets.terrain_generators
    :noindex:
