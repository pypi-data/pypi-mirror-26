======
lineno
======

.. image:: https://img.shields.io/pypi/v/lineno.svg
        :target: https://pypi.python.org/pypi/lineno

.. image:: https://img.shields.io/travis/bulv1ne/lineno.svg
        :target: https://travis-ci.org/bulv1ne/lineno


Outputs the lines from specified file


Features
--------

.. code:: bash

    $ lineno -l 1-3,15,16 README.rst
    ======
    lineno
    ======
    Features
    --------

Usage in vim:

.. code:: vim

    :r! lineno -l 1-3,15,16 -l 27-31 README.rst


=======
History
=======

Unreleased
----------

0.2.1 (2017-10-24)
------------------

* Fix README.rst documentation

0.2.0 (2017-10-24)
------------------

* Add -l/--line-number argument instead of requiring that the line number sequence is the first argument.

0.1.0 (2017-07-01)
------------------

* First release on PyPI.


