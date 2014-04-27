# -*- coding: utf-8 -*-
"""Examples for reference using clint, progress, and blessings"""

import random
from time import sleep


def clint_progress_example():
    import clint

    assert clint.textui.progress.BAR_TEMPLATE == '%s[%s%s] %i/%i - %s\r'
    clint.textui.progress.BAR_TEMPLATE = '%s %s%s %i/%i - %s\r'
    chars = (u'◯', u'◉')
    # chars = (u' ', u'█')

    with clint.textui.progress.Bar(label="Job Progress", expected_size=100,
                                   filled_char=chars[1], empty_char=chars[0]) as bar:
        for val in map(lambda x: (x + 1) * 10, xrange(10)):
            sleep(2 * random.random())
            bar.show(val)


def progress_progress_example():
    from progress.bar import FillingCirclesBar

    bar = FillingCirclesBar("Job Progress", max=100)
    for i in map(lambda x: (x + 1) * 10, xrange(10)):
        sleep(2 * random.random())
        bar.index = i
        bar.update()
    bar.finish()


def blessings_progress_example():
    from blessings import Terminal

    t = term = Terminal()

    for i in xrange(10):
        sleep(2 * random.random())
        t.clear_bol()
        term.stream.write(t.white_on_black(" " * i))
        term.stream.flush()
    print t.normal


if __name__ == "__main__":
    blessings_progress_example()
    clint_progress_example()
    progress_progress_example()

