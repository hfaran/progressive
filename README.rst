.. contents::
   :depth: 3
..

``progressive``
===============

|Build Status| |Coverage Status| |PyPI version| |Stories in Ready|

Colorful progress bars and trees for your terminal, powered by
`blessings <https://github.com/erikrose/blessings>`__. Compatible with
both Python 2 and 3.

Introduction
------------

``progressive`` lets you view progress of complex workflows as well as
simple ones:

|Tree Progress View|

Installation
------------

-  For the possibly stable

::

    pip install progressive

-  For the latest and greatest

::

    git clone https://github.com/hfaran/progressive.git
    cd progressive
    python setup.py install

Getting Started
---------------

-  Documentation is coming soon, but in the meantime check out the
   `examples <https://github.com/hfaran/progressive/blob/master/progressive/examples.py>`__.
-  ``progressive`` supports graceful fallback modes for terminals
   without colors, `but you really should upgrade your terminal to 256
   colors <http://pastelinux.wordpress.com/2010/12/01/upgrading-linux-terminal-to-256-colors/>`__
   to make full use of ``progressive``.

.. |Build Status| image:: https://travis-ci.org/hfaran/progressive.svg
   :target: https://travis-ci.org/hfaran/progressive
.. |Coverage Status| image:: https://coveralls.io/repos/hfaran/progressive/badge.png
   :target: https://coveralls.io/r/hfaran/progressive
.. |PyPI version| image:: https://badge.fury.io/py/progressive.svg
   :target: http://badge.fury.io/py/progressive
.. |Stories in Ready| image:: https://badge.waffle.io/hfaran/progressive.png?label=Ready
   :target: http://waffle.io/hfaran/progressive
.. |Tree Progress View| image:: https://raw.githubusercontent.com/hfaran/progressive/master/example.gif
   :target: https://github.com/hfaran/progressive
