# -*- coding: utf-8 -*-
"""Examples

Usage:
`python -c "import examples; examples.simple_two_bar()"`
"""
import random
from time import sleep
from blessings import Terminal

from progressive.bar import Bar
from progressive.nest import NestedProgress


def simple_two_bar():
    """Two-bar example using just the Bar class

    This example is intended to show usage of the Bar class at the barest
    level.

    Usage: `python -c "import examples; examples.simple_two_bar_example()"`
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

    for i in range(MAX_VALUE + 1):
        sleep(0.1 * random.random())

        # Before beginning to draw our bars, we save the position
        #   of our cursor so we can restore back to this position after writing
        t.stream.write(t.save)

        # Now we draw the first bar
        bar1.draw(value=i)
        # The following two writes act as a newline
        t.stream.write(t.move_down)  # Move the cursor down a row
        t.stream.write(t.clear_bol)  # Clear to the beginning of the line

        # Do the same for the second bar
        bar2.draw(value=i)
        t.stream.write(t.move_down)
        t.stream.write(t.clear_bol)

        # We're done writing, so time to restore the cursor to the top;
        #   we do the restore for every iteration EXCEPT the last one
        #   (the reason why, is left as an exercise for the reader)
        if i < MAX_VALUE:
            t.stream.write(t.restore)

        # Finally, we can flush all of this to stdout
        t.stream.flush()


def nested_progress():
    test_d = {
        "Job1": {
            "Task1": {
                "SubTask1": 0,
                "SubTask2": 0,
            },
            "Task2": {
                "SubTask1": 0,
                "SubTask2": 0,
            },
        },
        "Job2": {
            "Task1": {
                "SubTask1": 0,
                "SubTask2": 0,
            },
            "Task2": {
                "SubTask1": 0,
                "SubTask2": 0,
            },
        }
    }

    def incr_value(obj):
        if isinstance(obj, dict):
            for k in obj:
                if isinstance(obj[k], dict):
                    incr_value(obj[k])
                elif isinstance(obj[k], int):
                    if obj[k] == 100:
                        pass
                    elif obj[k] >= 97:
                        obj[k] = 100
                    else:
                        obj[k] += random.choice(range(3))

    # Create blessings.Terminal instance
    t = Terminal()
    n = NestedProgress(term=t)
    n.clear_lines(test_d)

    t.stream.write(t.save)
    while 1:
        sleep(0.1 * random.random())

        t.stream.write(t.restore)

        incr_value(test_d)

        n.draw(test_d)

        t.stream.flush()
