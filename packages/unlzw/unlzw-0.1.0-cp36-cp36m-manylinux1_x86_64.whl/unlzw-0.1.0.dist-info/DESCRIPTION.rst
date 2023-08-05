========
Overview
========



Bindings for Mark Adler's `unlzw
<https://mathematica.stackexchange.com/questions/60531/how-can-i-read-compressed-z-file-automatically-by-mathematica/60879#60879>`_
library.

* Free software: BSD 3-Clause License

Installation
============

::

    pip install unlzw

Documentation
=============

.. code-block:: python

    from unlzw import unlzw

    assert unlzw(b'\x1f\x9d\x90f\xde\xbc\x11\x13FN\xc0\x81\x05\x0f\x124(p\xa1\xc2\x82') == b'foobarfoobarfoobarfoobarfoobar'


Changelog
=========

0.1.0 (2017-10-25)
------------------

* First release on PyPI.


