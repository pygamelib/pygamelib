.. image:: pygamelib-logo.png
    :alt: menu
    :align: center

pygamelib - documentation
=========================

Forewords
^^^^^^^^^

Historically, this library was (and still is) used as a base to teach coding to kids 
from 6 to 15. It aims at giving an environment to new and learning developers (including
kids) that let them focus on the algorithm instead of the lousy display or precise
management.

It started as a very simple library with very little capabilities, but over time it
became something more. To the point that it is now possible to make very decent terminal
games with it.

So this is **obviously** still extremely simple compared to other game framework and it
still does not have the pretention of being anything serious for real game developers.
However, it can now be used by aspiring game developers for an introduction to 2D games
development.

Introduction
^^^^^^^^^^^^

First of all, his module is exclusively compatible with python 3.6+.

The core concept is that writting a game mostly involve the 
:class:`~pygamelib.engine.Game` object, the :class:`~pygamelib.engine.Board` object and
the derivatives of :ref:`boarditem-module`.

More advanced game will use the :ref:`gfx_ui-module` module to create terminal user interfaces
(or TUI) and the GFX :ref:`gfx_core-module` module to improve the graphics with 
:class:`~pygamelib.gfx.core.Sprite` and :class:`~pygamelib.gfx.core.Color`.

Here is an example of what the current version allow to build:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/9l18dhJ-kJE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

And a quick peak at the new features in the most recent version:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/AyzSMH5msU4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Tutorials
^^^^^^^^^

Most tutorials to teach you how to use the library to build games are (or will be) on the 
`wiki <https://github.com/pygamelib/pygamelib/wiki>`_.

Tutorials that teach you how to expand the library are (or will be) centralized here.

The complete API documentation is referenced bellow.

.. toctree::
   :caption: Contents (API reference):

   actuators
   assets
   base
   board_items
   constants
   engine
   gfx
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
