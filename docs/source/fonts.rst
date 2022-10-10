.. _assets_fonts-module:

Fonts
=====

Fonts in the pygamelib are nothing more than a specially organized sprite collection.

The way to use it is extremely simple: you instantiate a Font object and ask it to load the data from a specific font.

For example to load the 8bits font, you do:

Example::
    from pygamelib.gfx import core

    my_font = core.Font('8bits')

That's it! The you can use it to format Text objects.

.. toctree::

    pygamelib.assets.fonts.8bits.rst
    pygamelib.assets.fonts.figlet-caligraphy.rst
    pygamelib.assets.fonts.figlet-doom.rst
    pygamelib.assets.fonts.figlet-graffiti.rst
    pygamelib.assets.fonts.figlet-mirror.rst
    pygamelib.assets.fonts.figlet-pepper.rst
    pygamelib.assets.fonts.figlet-poison.rst
    pygamelib.assets.fonts.figlet-puffy.rst
    pygamelib.assets.fonts.figlet-rounded.rst
    pygamelib.assets.fonts.figlet-stampatello.rst
    pygamelib.assets.fonts.figlet-univers.rst
    pygamelib.assets.fonts.figlet-wavy.rst
