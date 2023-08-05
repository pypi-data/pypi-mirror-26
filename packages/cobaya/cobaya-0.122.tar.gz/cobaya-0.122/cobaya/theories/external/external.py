"""
.. module:: external

:Synopsis: External theory code, that would implement the necessary methods for the likelihoods.
:Author: Jesus Torrado

.. |br| raw:: html

   <br />

This dummy module simply interfaces an external class, whose methods are called instead of
those of a real theory class.

Usage
-----

Just pass an instance of a class thorugh the parameter ``instance``,
 containing the necessary methods for the likelihood to retrieve observables.

.. todo::

   Add example!


"""

# Python 2/3 compatibility
from __future__ import absolute_import
from __future__ import division

# Global
import inspect

# Local
from cobaya.theory import Theory
from cobaya.tools import yaml_custom_load

class external(Theory):

    def initialise(self):
        # Make the methods of the external instance callable from this class
        for name, method in inspect.getmembers(self.instance, predicate=inspect.ismethod):
            if name == "__init__":
                continue
            setattr(self, name, method)
