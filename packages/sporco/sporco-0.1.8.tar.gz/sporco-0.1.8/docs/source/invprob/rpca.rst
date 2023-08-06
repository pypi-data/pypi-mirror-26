Module rpca
===========

This module includes the :class:`.RobustPCA` class for solving the
problem

.. math::
   \mathrm{argmin}_{X, Y} \;
   \| X \|_* + \lambda \| Y \|_1 \quad \text{ such that }
   \quad X + Y = S



Usage Examples
--------------

.. container:: toggle

    .. container:: header

        :class:`.RobustPCA` usage

    .. literalinclude:: ../../../examples/misc/demo_rpca.py
       :language: python
       :lines: 9-
