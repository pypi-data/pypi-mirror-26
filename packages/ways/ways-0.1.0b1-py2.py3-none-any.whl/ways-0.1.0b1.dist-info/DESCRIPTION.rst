========
Overview
========



An string-based AMS toolkit for Python

* Free software: MIT license

Installation
============

::

    pip install ways

Documentation
=============

https://ways.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0b1 (2017-10-28)
--------------------

* First release on PyPI.


