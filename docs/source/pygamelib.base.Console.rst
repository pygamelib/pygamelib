Console
=======

.. currentmodule:: pygamelib.base

.. autoclass:: Console
   :members:
   :inherited-members:
   :undoc-members:
   :show-inheritance:


    The Console class is a singleton wrapper around the blessed.Terminal() class.
    Since the library is using Terminal a lot, it is both useful and efficient to have a
    quick access to a single instance of the class.

    This class only expose one method: :func:`~pygamelib.base.Console.instance()` that
    returns the singleton instance.


   .. rubric:: Methods

   .. autosummary::
   
      ~Console.instance
   
   

   
   
   