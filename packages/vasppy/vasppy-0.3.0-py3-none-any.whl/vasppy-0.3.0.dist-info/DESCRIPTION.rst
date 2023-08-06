vasppy - a Python suite for manipulating VASP files
===================================================

|DOI| |Build Status| |Test Coverage|

``vasppy`` is a suite of Python tools and scripts written in Python for
manipulating and processing `VASP <https://www.vasp.at/>`__ input and
output files.

Installation of executable scripts
----------------------------------

The suite of executable scripts can be installed by running
``install.py``. This creates symbolic links with a default destination
of ``$HOME/bin/``. For more options, such as installing selected
scripts, or uninstalling (removing symbolic links) ) use
``./install.py --help``

Tests
-----

Automated testing of the latest build happens
`here <https://travis-ci.org/bjmorgan/vasppy>`__.

Manual tests can be run using

::

    python3 -m unittest discover

Contributors
------------

Benjamin J. Morgan Lucy Whalley

.. |DOI| image:: https://zenodo.org/badge/17946870.svg
   :target: https://zenodo.org/badge/latestdoi/17946870
.. |Build Status| image:: https://travis-ci.org/bjmorgan/vasppy.svg?branch=master
   :target: https://travis-ci.org/bjmorgan/vasppy
.. |Test Coverage| image:: https://codeclimate.com/github/bjmorgan/vasppy/badges/coverage.svg
   :target: https://codeclimate.com/github/bjmorgan/vasppy/coverage


