.. image:: https://travis-ci.org/cjrh/cjrh_math.svg?branch=master
    :target: https://travis-ci.org/cjrh/cjrh_math

.. image:: https://coveralls.io/repos/github/cjrh/cjrh_math/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/cjrh_math?branch=master

.. image:: https://img.shields.io/pypi/pyversions/cjrh_math.svg
    :target: https://pypi.python.org/pypi/cjrh_math

.. image:: https://img.shields.io/github/tag/cjrh/cjrh_math.svg
    :target: https://img.shields.io/github/tag/cjrh/cjrh_math.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20cjrh_math-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20cjrh_math-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/cjrh_math.svg
    :target: https://img.shields.io/pypi/v/cjrh_math.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/


cjrh_math
======================

A collection of handy maths functions.

Streaming mean and variance
---------------------------

Sometimes it can be very useful to update an *existing* mean and variance
with new data, rather than have to calculate it again over the whole set.
The functions below implement one of the algorithms described
in `Wikipedia <https://en.wikipedia.org/wiki/Standard_deviation#Rapid_calculation_methods>`_.

.. code-block:: python

    def update_mean(n: int, mean: float, value: float) -> float

Given a new ``value``, calculate a new mean using the existing ``mean`` and
the size of data, ``n``, seen so far.

.. code-block:: python

    def update_pvariance(n: int, mean: float, var: float, value: float) -> float
    def update_variance(n: int, mean: float, var: float, value: float) -> float

Given a new ``value``, calculate a new variance using the existing ``mean``,
existing variance ``var``, and the size of data, ``n``, seen so far.

Note that ``update_variance()`` is for *sample* variance while
``update_pvariance()`` is for *population* variance.

All functions are pure and therefore thread-safe.
