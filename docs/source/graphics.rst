.. _graphics-module:

graphics
========

.. Important:: The Graphics module was introduced in version 1.1.0.

The Graphics module hold many variables that aims at simplifying the use of
unicode characters in the game development process.

This module also import colorama. All styling features are accessible through:

 * Graphics.Fore for Foreground colors.
 * Graphics.Back for Background colors.
 * Graphics.Style for styling options.

For convenience, the different entities are scattered in grouping classes:

 * All emojis are in the Models class.
 * The UI/box drawings are grouped into the BoxDrawings class.
 * The block glyphs are in the Blocks class.
 * The geometric shapes are in the GeometricShapes class.

This modules defines a couple of colored squares and rectangles that should displays
correctly in all terminals.

These are kept for legacy purpose (I personally have a lot of kids that are still using
it), but for anyone starting fresh, it is better to use the <color>_rect() and
<color>_square() static methods of the :class:`~pygamelib.gfx.core.Sprixel` class.
Particularly if you are going to use them as background for your Board.

Colored rectangles:

 * WHITE_RECT
 * BLUE_RECT
 * RED_RECT
 * MAGENTA_RECT
 * GREEN_RECT
 * YELLOW_RECT
 * BLACK_RECT
 * CYAN_RECT

Then colored squares:

 * WHITE_SQUARE
 * MAGENTA_SQUARE
 * GREEN_SQUARE
 * RED_SQUARE
 * BLUE_SQUARE
 * YELLOW_SQUARE
 * BLACK_SQUARE
 * CYAN_SQUARE

And finally an example of composition of rectangles to make different colored squares:

 * RED_BLUE_SQUARE = RED_RECT+BLUE_RECT
 * YELLOW_CYAN_SQUARE = YELLOW_RECT+CYAN_RECT


The Graphics module contains the following classes:

.. toctree::
    pygamelib.assets.graphics.Blocks
    pygamelib.assets.graphics.BoxDrawings
    pygamelib.assets.graphics.GeometricShapes
    pygamelib.assets.graphics.Models

.. automodule:: pygamelib.assets.graphics
    :noindex: