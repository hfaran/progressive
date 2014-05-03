# -*- coding: utf-8 -*-
"""Examples

Usage:
`python -c "from examples import *; two_bar()"` as an example
"""
import random
from time import sleep

from blessings import Terminal

from progressive.bar import Bar
from progressive.tree import TreeProgress, Value, BarDescriptor


def tree_progress():
    """Example showing tree progress view"""

    #############
    # Test data #
    #############

    # For this example, we're obviously going to be feeding fictitious data
    #   to TreeProgress, so here it is
    leaf_values = [Value(0) for i in range(5)]

    test_d = {
        "Warp Jump": {
            "1) Prepare fuel": {
                "Load Tanks": {
                    "Tank 1": BarDescriptor(type=Bar, value=leaf_values[0]),
                    "Tank 2": BarDescriptor(type=Bar, value=leaf_values[1]),
                },
                "Refine tylium ore": BarDescriptor(type=Bar,
                                                   value=leaf_values[2]),
            },
            "2) Calculate jump co-ordinates": {
                "Resolve common name to co-ordinates": {
                    "Querying resolution from baseship": BarDescriptor(
                        type=Bar, value=leaf_values[3]
                    ),
                },
            },
            "3) Check FTL drive readiness": BarDescriptor(
                type=Bar, value=leaf_values[4]
            )
        }
    }

    # We'll use this function to bump up the leaf values
    def incr_value(obj):
        for val in leaf_values:
            if val.value == 100:
                pass
            elif val.value >= 98:
                val.value = 100
            else:
                val.value += random.choice(range(3))

    # And this to check if we're to stop drawing
    def are_we_done(obj):
        return all(val.value == 100 for val in leaf_values)

    ###################
    # The actual code #
    ###################

    # Create blessings.Terminal instance
    t = Terminal()
    # Initialize a TreeProgress instance
    n = TreeProgress(term=t)
    # We'll use the clear_lines method to make sure the terminal
    #   is filled out with all the room we need
    n.clear_lines(test_d)

    # Before starting to write, save the cursor position so we can restore
    #   back to it before writing again
    t.stream.write(t.save)
    while not are_we_done(test_d):
        sleep(0.1 * random.random())

        t.stream.write(t.restore)
        # We use our incr_value method to bump the fake numbers
        incr_value(test_d)
        # Actually draw out the bars
        n.draw(test_d)


def two_bar():
    """Two-bar example using just the Bar class

    This example is intended to show usage of the Bar class at the lowest
    level.
    """
    MAX_VALUE = 100
    LINES_REQUIRED = 4

    # Create blessings.Terminal instance
    t = Terminal()
    # Create our test progress bars
    bar1 = Bar(t, max_value=MAX_VALUE, indent=0,
               title_pos="above", fallback=True)
    bar2 = Bar(t, max_value=MAX_VALUE, indent=4,
               title_pos="above", fallback=True)

    # Move the cursor down, then back up LINES_REQUIRED rows
    # This is a very important step that ensures that the terminal
    #   has enough room at the bottom for printing; if this step is not
    #   the cursor will not be able to restore properly
    # NOTE: Usually before doing this, you should make sure your terminal
    #   actually has enough height to display all the bars you would like
    for i in range(LINES_REQUIRED):
        t.stream.write(t.move_down)
    for i in range(LINES_REQUIRED):
        t.stream.write(t.move_up)

    # Before beginning to draw our bars, we save the position
    #   of our cursor so we can restore back to this position before writing
    #   the next time.
    t.stream.write(t.save)
    for i in range(MAX_VALUE + 1):
        sleep(0.1 * random.random())

        # We restore the cursor to saved position before writing
        t.stream.write(t.restore)

        # Now we draw the first bar
        bar1.draw(value=i)
        # The following two writes act as a newline
        t.stream.write(t.move_down)  # Move the cursor down a row
        t.stream.write(t.clear_bol)  # Clear to the beginning of the line

        # Do the same for the second bar
        bar2.draw(value=i)
        t.stream.write(t.move_down)
        t.stream.write(t.clear_bol)

        # Finally, we can flush all of this to stdout
        t.stream.flush()
