========
Overview
========



This package contains various useful bits of code for use in Django projects. I
consider the things here to be too small to warrant a package of their own, but
I don't want to copy and paste them from project to project. I will accept bug
reports  and pull requests for this package, but I make no promise to maintain
it or keep any kind of backwards compatibility. Use at your own risk.

* Free software: BSD license

Installation
============

::

    pip install rf-django-misc

Documentation
=============

https://rf-django-misc.readthedocs.io/

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

0.1.0 (2016-12-12)
-----------------------------------------

* First release on PyPI.


