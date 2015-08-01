.. progressive documentation master file, created by
   sphinx-quickstart on Sat Aug  1 01:36:56 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to progressive's documentation!
=======================================

``progressive`` allows you to progress of complex (and simple) workflows
in your terminal.

If your aim is to draw progress bars, nested or otherwise, you've come
to the right place.

.. code-block:: python

   from progressive.bar import Bar

   bar = Bar(max_value=100)
   bar.cursor.clear_lines(2)  # Make some room
   bar.cursor.save()  # Mark starting line
   for i in range(101):
       sleep(0.1)  # Do some work
       bar.cursor.restore()  # Return cursor to start
       bar.draw(value=i)  # Draw the bar!

More examples are available in ``progressive.examples``!

.. image:: ../example.gif

.. literalinclude:: ../progressive/examples.py


API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   progressive
