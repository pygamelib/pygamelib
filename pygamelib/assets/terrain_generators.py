"""
pygamelib

A library for Python 2D games.

This module contains terrain generation utilities for pygamelib.

The main entry point is the
:class:`~pygamelib.assets.terrain_generators.TerrainGenerator` class. It samples an
OpenSimplex noise field to decide, for each cell of a
:class:`~pygamelib.engine.Board`, which :class:`TerrainFeature` sits there. The board is
filled with :class:`~pygamelib.board_items.Tile` items using the glyphs, colors and
sprites of a :class:`TerrainPalette`, so it can be displayed or used as the base of an
outdoor level.

Example::

    from pygamelib.assets import terrain_generators

    generator = terrain_generators.TerrainGenerator(width=40, height=20, seed=42)
    board = generator.generate()
    board.display()

The generation is reproducible as long as the same ``seed`` is used.
"""

__docformat__ = "restructuredtext"

import math

from pygamelib import base, board_items, engine
from pygamelib.assets import graphics
from pygamelib.gfx import core

try:
    import opensimplex
except ImportError:  # pragma: no cover
    opensimplex = None


#: The default color palette. It maps each feature of the
#: :class:`TerrainFeature` enumeration to a foreground color.
DEFAULT_COLORS = {
    "deep_water": core.Color(13, 42, 92),
    "water": core.Color(28, 96, 153),
    "shore": core.Color(226, 212, 158),
    "plain": core.Color(126, 174, 84),
    "forest": core.Color(51, 110, 57),
    "hill": core.Color(120, 110, 74),
    "mountain": core.Color(150, 150, 150),
    "snow": core.Color(240, 245, 250),
}


class TerrainFeature(base.PglBaseObject):
    """
    Describe a single terrain feature (a biome).

    A feature carries everything needed to render a cell of the terrain: the model (a
    single character or a unicode glyph), a foreground color and an optional sprite.
    The sprite, when given, is preferred over the model: it allows for richer
    multi-cell features such as a tree or a house.

    Features are compared by name, which makes them usable as dictionary keys and easy
    to test.

    Example::

        from pygamelib.assets import graphics, terrain_generators

        forest = terrain_generators.TerrainFeature(
            name="forest",
            model=graphics.MiscTechnicals.EARTH_GROUND,
        )

    :param name: The name of the feature. It identifies the feature.
    :type name: str
    :param model: The model used to render the feature.
    :type model: str
    :param fg_color: The foreground color of the feature.
    :type fg_color: :class:`~pygamelib.gfx.core.Color`
    :param bg_color: The background color of the feature. Defaults to ``None``
       (transparent).
    :type bg_color: :class:`~pygamelib.gfx.core.Color`
    :param sprite: An optional sprite used instead of the model.
    :type sprite: :class:`~pygamelib.gfx.core.Sprite`
    """

    def __init__(
        self,
        name: str,
        model: str = " ",
        fg_color: core.Color = None,
        bg_color: core.Color = None,
        sprite: core.Sprite = None,
    ):
        super().__init__()
        self.name = name
        self.model = model
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.sprite = sprite

    def __eq__(self, other):
        if isinstance(other, TerrainFeature):
            return self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"TerrainFeature({self.name!r}, model={self.model!r})"

    def make_item(self) -> board_items.Tile:
        """
        Build the :class:`~pygamelib.board_items.Tile` that represents this feature.

        If the feature has a sprite, the tile uses it. Otherwise a 1x1 sprite is built
        out of the feature's model and colors.

        :return: A tile ready to be placed on a board.
        :rtype: :class:`~pygamelib.board_items.Tile`
        """
        if self.sprite is not None:
            sprite = self.sprite
        else:
            sprite = core.Sprite(
                size=[1, 1],
                default_sprixel=core.Sprixel(
                    model=self.model,
                    fg_color=self.fg_color,
                    bg_color=self.bg_color,
                ),
            )
        return board_items.Tile(sprite=sprite)

    def serialize(self) -> dict:
        """
        Serialize the feature.

        :return: A dictionary containing the feature's properties.
        :rtype: dict
        """
        return {
            "name": self.name,
            "model": self.model,
            "fg_color": self.fg_color.serialize() if self.fg_color else None,
            "bg_color": self.bg_color.serialize() if self.bg_color else None,
            "sprite": self.sprite.serialize() if self.sprite else None,
        }

    @classmethod
    def load(cls, data: dict) -> "TerrainFeature":
        """
        Create a feature from serialized data.

        :param data: The serialized data.
        :type data: dict
        :return: The loaded feature.
        :rtype: :class:`TerrainFeature`
        """
        return cls(
            name=data["name"],
            model=data["model"],
            fg_color=core.Color.load(data["fg_color"]) if data["fg_color"] else None,
            bg_color=core.Color.load(data["bg_color"]) if data["bg_color"] else None,
            sprite=core.Sprite.load(data["sprite"]) if data["sprite"] else None,
        )


class TerrainPalette(base.PglBaseObject):
    """
    A palette maps every :class:`TerrainFeature` to the way it is rendered.

    The palette is built around the seven features a
    :class:`TerrainGenerator` can produce. Each one can be customized independently
    through :meth:`set_feature` or by passing a dictionary of
    :class:`TerrainFeature` to the constructor.

    Example::

        from pygamelib.assets import graphics, terrain_generators
        from pygamelib.gfx import core

        palette = terrain_generators.TerrainPalette()
        palette.set_feature(
            "forest",
            terrain_generators.TerrainFeature(
                name="forest",
                model=graphics.MiscTechnicals.EARTH_GROUND,
                fg_color=core.Color(20, 90, 30),
            ),
        )

    :param features: An optional mapping of feature name to
       :class:`TerrainFeature`. Any feature that is not provided is created from the
       module defaults.
    :type features: dict
    """

    def __init__(self, features: dict = None):
        super().__init__()
        self._features = self._default_features()
        if features:
            for name, feature in features.items():
                self.set_feature(name, feature)

    @staticmethod
    def _default_features() -> dict:
        return {
            "deep_water": TerrainFeature(
                name="deep_water",
                model="~",
                fg_color=DEFAULT_COLORS["deep_water"],
            ),
            "water": TerrainFeature(
                name="water",
                model="~",
                fg_color=DEFAULT_COLORS["water"],
            ),
            "shore": TerrainFeature(
                name="shore",
                model=".",
                fg_color=DEFAULT_COLORS["shore"],
            ),
            "plain": TerrainFeature(
                name="plain",
                model='"',
                fg_color=DEFAULT_COLORS["plain"],
            ),
            "forest": TerrainFeature(
                name="forest",
                model=graphics.MiscTechnicals.EARTH_GROUND,
                fg_color=DEFAULT_COLORS["forest"],
            ),
            "hill": TerrainFeature(
                name="hill",
                model="^",
                fg_color=DEFAULT_COLORS["hill"],
            ),
            "mountain": TerrainFeature(
                name="mountain",
                model="^",
                fg_color=DEFAULT_COLORS["mountain"],
            ),
            "snow": TerrainFeature(
                name="snow",
                model="*",
                fg_color=DEFAULT_COLORS["snow"],
            ),
        }

    def set_feature(self, name: str, feature: TerrainFeature):
        """
        Replace or add the feature identified by ``name``.

        The name of the feature is forced to ``name`` so it stays consistent with the
        palette's keys.

        :param name: The name of the feature.
        :type name: str
        :param feature: The feature to use for that name.
        :type feature: :class:`TerrainFeature`
        """
        if not isinstance(feature, TerrainFeature):
            raise base.PglInvalidTypeException(
                f"feature must be a TerrainFeature, got {type(feature)}."
            )
        feature.name = name
        self._features[name] = feature

    def feature(self, name: str) -> TerrainFeature:
        """
        Return the feature identified by ``name``.

        :param name: The name of the feature.
        :type name: str
        :return: The feature.
        :rtype: :class:`TerrainFeature`
        """
        if name not in self._features:
            raise base.PglException(
                "UNKNOWN_TERRAIN_FEATURE",
                f"Unknown terrain feature {name!r}. "
                f"Known features: {', '.join(sorted(self._features))}.",
            )
        return self._features[name]

    def serialize(self) -> dict:
        """
        Serialize the palette.

        :return: A dictionary containing the palette's features.
        :rtype: dict
        """
        return {name: f.serialize() for name, f in self._features.items()}

    @classmethod
    def load(cls, data: dict) -> "TerrainPalette":
        """
        Create a palette from serialized data.

        :param data: The serialized data.
        :type data: dict
        :return: The loaded palette.
        :rtype: :class:`TerrainPalette`
        """
        return cls(features={name: TerrainFeature.load(d) for name, d in data.items()})


class TerrainGenerator(base.PglBaseObject):
    """
    Generate an outdoor terrain as a :class:`~pygamelib.engine.Board`.

    The generator samples a two dimensional OpenSimplex noise field. Each cell is
    classified into a :class:`TerrainFeature` from its altitude. Water bodies are
    placed first, either from a sea level threshold or from a separate continent noise
    field (``island``), which gives more natural coastlines than a plain threshold.

    The board is filled with :class:`~pygamelib.board_items.Tile` items built from the
    palette. Terrain is not the same everywhere: the noise is sampled at a configurable
    frequency and can be combined with an octave, which adds smaller details on top of
    the large land masses.

    Example::

        from pygamelib.assets import terrain_generators

        generator = terrain_generators.TerrainGenerator(
            width=60, height=30, seed=42, island=True
        )
        board = generator.generate()
        board.display()

    :param width: Width of the generated board.
    :type width: int
    :param height: Height of the generated board.
    :type height: int
    :param palette: The palette used to render the terrain.
    :type palette: :class:`TerrainPalette`
    :param seed: Optional seed used to make the generation reproducible.
    :type seed: int
    :param scale: Distance (in board cells) between two noise samples. A larger scale
       gives larger, smoother land masses.
    :type scale: float
    :param octaves: Number of noise layers. Each extra layer adds finer details.
    :type octaves: int
    :param persistence: How much each extra octave contributes to the result. It must
       be between 0 and 1.
    :type persistence: float
    :param water_level: Altitude below which a cell is water. It must be between 0 and
       1.
    :type water_level: float
    :param island: When ``True``, a radial falloff is applied so the terrain is an
       island surrounded by deep water.
    :type island: bool
    """

    #: Altitude thresholds used to classify a land cell. They are compared, in order,
    #: against the cell's altitude.
    _LAND_THRESHOLDS = (
        (0.30, "shore"),
        (0.52, "plain"),
        (0.66, "forest"),
        (0.80, "hill"),
        (0.92, "mountain"),
    )

    def __init__(
        self,
        width: int = 40,
        height: int = 20,
        palette: TerrainPalette = None,
        seed: int = None,
        scale: float = 12.0,
        octaves: int = 3,
        persistence: float = 0.5,
        water_level: float = 0.35,
        island: bool = False,
    ):
        super().__init__()
        if width < 1 or height < 1:
            raise base.PglInvalidTypeException(
                f"Terrain dimensions must be positive integers, got {width}x{height}."
            )
        if scale <= 0:
            raise base.PglInvalidTypeException(
                f"scale must be a positive number, got {scale}."
            )
        if octaves < 1:
            raise base.PglInvalidTypeException(
                f"octaves must be at least 1, got {octaves}."
            )
        if not 0 < persistence <= 1:
            raise base.PglInvalidTypeException(
                f"persistence must be in ]0, 1], got {persistence}."
            )
        if not 0 <= water_level < 1:
            raise base.PglInvalidTypeException(
                f"water_level must be in [0, 1[, got {water_level}."
            )
        self.width = width
        self.height = height
        self.palette = TerrainPalette() if palette is None else palette
        self.seed = seed
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.water_level = water_level
        self.island = island
        self.__simplex = None

    def _simplex(self):
        """
        Return the OpenSimplex instance, creating it on first use.

        :return: The noise generator.
        :rtype: :class:`opensimplex.OpenSimplex`
        """
        if opensimplex is None:
            raise base.PglException(
                "MISSING_OPENSIMPLEX",
                "The terrain generators require the opensimplex module. "
                "Please install it with 'pip install opensimplex'.",
            )
        if self.__simplex is None:
            self.__simplex = opensimplex.OpenSimplex(seed=self.seed)
        return self.__simplex

    #: Exponent of the radial falloff used when ``island`` is ``True``. A value
    #: greater than 2 keeps a wide, mostly flat interior while still dropping the
    #: coast to deep water.
    _ISLAND_FALLOFF_EXPONENT = 3.5

    def _island_falloff(self, row: int, column: int) -> float:
        """
        Compute the radial falloff applied to a cell when ``island`` is ``True``.

        The falloff is 1 in the middle of the board and goes down to 0 on the edges.

        :param row: Row of the cell.
        :type row: int
        :param column: Column of the cell.
        :type column: int
        :return: The falloff factor.
        :rtype: float
        """
        nx = 2 * column / (self.width - 1) - 1 if self.width > 1 else 0
        ny = 2 * row / (self.height - 1) - 1 if self.height > 1 else 0
        distance = min(1.0, math.sqrt(nx * nx + ny * ny))
        return 1.0 - distance**self._ISLAND_FALLOFF_EXPONENT

    def altitude(self, row: int, column: int) -> float:
        """
        Return the normalized altitude (between 0 and 1) of a board cell.

        The value is the sum of ``octaves`` noise layers, remapped from OpenSimplex'
        [-1, 1] range to [0, 1] and then redistributed with a smoothstep so that the
        terrain is more varied than a plain average. When ``island`` is ``True`` the
        radial falloff is applied afterwards.

        :param row: Row of the cell.
        :type row: int
        :param column: Column of the cell.
        :type column: int
        :return: The altitude of the cell.
        :rtype: float
        """
        simplex = self._simplex()
        total = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_amplitude = 0.0
        for _ in range(self.octaves):
            total += (
                simplex.noise2(
                    column * frequency / self.scale,
                    row * frequency / self.scale,
                )
                * amplitude
            )
            max_amplitude += amplitude
            amplitude *= self.persistence
            frequency *= 2
        value = (total / max_amplitude + 1) / 2
        # Summed octaves cluster around 0.5, which would make almost every land cell
        # a plain. A smoothstep pushes values towards the extremes and gives a much
        # more varied terrain.
        value = value * value * (3 - 2 * value)
        if self.island:
            value *= self._island_falloff(row, column)
        return value

    def feature_at(self, row: int, column: int) -> TerrainFeature:
        """
        Return the :class:`TerrainFeature` that should be placed at a cell.

        :param row: Row of the cell.
        :type row: int
        :param column: Column of the cell.
        :type column: int
        :return: The feature for that cell.
        :rtype: :class:`TerrainFeature`
        """
        value = self.altitude(row, column)
        if value < self.water_level * 0.5:
            return self.palette.feature("deep_water")
        if value < self.water_level:
            return self.palette.feature("water")
        # The remaining altitude range is [water_level, 1]. It is rescaled to [0, 1]
        # so that the land thresholds are independent from the water level.
        span = 1 - self.water_level
        land = (value - self.water_level) / span
        for threshold, name in self._LAND_THRESHOLDS:
            if land < threshold:
                return self.palette.feature(name)
        return self.palette.feature("snow")

    def generate(self, name: str = "Terrain") -> engine.Board:
        """
        Generate the terrain and return it as a :class:`~pygamelib.engine.Board`.

        :param name: The name of the generated board.
        :type name: str
        :return: A board containing the terrain.
        :rtype: :class:`~pygamelib.engine.Board`
        """
        board = engine.Board(name=name, size=[self.width, self.height])
        for row in range(self.height):
            for column in range(self.width):
                board.place_item(
                    self.feature_at(row, column).make_item(), row, column
                )
        return board

    def serialize(self) -> dict:
        """
        Serialize the generator's configuration.

        :return: A dictionary containing the generator's properties.
        :rtype: dict
        """
        return {
            "width": self.width,
            "height": self.height,
            "palette": self.palette.serialize(),
            "seed": self.seed,
            "scale": self.scale,
            "octaves": self.octaves,
            "persistence": self.persistence,
            "water_level": self.water_level,
            "island": self.island,
        }

    @classmethod
    def load(cls, data: dict) -> "TerrainGenerator":
        """
        Create a generator from serialized data.

        :param data: The serialized data.
        :type data: dict
        :return: The loaded generator.
        :rtype: :class:`TerrainGenerator`
        """
        return cls(
            width=data["width"],
            height=data["height"],
            palette=TerrainPalette.load(data["palette"]),
            seed=data["seed"],
            scale=data["scale"],
            octaves=data["octaves"],
            persistence=data["persistence"],
            water_level=data["water_level"],
            island=data["island"],
        )
