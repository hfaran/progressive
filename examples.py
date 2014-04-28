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
        for val in map(lambda x: x * 10, range(11)):
            sleep(1 * random.random())
            bar.show(val)


def progress_progress_example():
    from progress.bar import FillingCirclesBar

    bar = FillingCirclesBar("Job Progress", max=100)
    for i in map(lambda x: x * 10, range(11)):
        sleep(1 * random.random())
        bar.index = i
        bar.update()
    bar.finish()


def blessings_progress_example():
    from blessings import Terminal

    t = term = Terminal()

    for i in range(11):
        sleep(1 * random.random())
        t.clear_bol()
        term.stream.write(t.cyan_on_white(" " * i))
        term.stream.flush()
    print(t.normal)


def progressive_example():
    from blessings import Terminal
    from progressive import Bar
    from curses import tigetstr

    t = term = Terminal()
    b = Bar(term, max_value=10, indent=4, title_pos="left", fallback=True)

    for i in range(11):
        sleep(1 * random.random())
        # This context manager is equivalent to using:
        # t.stream.write(t.save)
        # ...
        # t.stream.write(t.restore)
        t.stream.write(tigetstr('sc'))
        b.value = i
        b.draw()
        t.stream.write(tigetstr('cud1'))
        t.stream.write(tigetstr('el1'))
        b.draw()
        t.stream.write(tigetstr('cud1'))
        t.stream.write(tigetstr('el1'))
        if i != 10:
            t.stream.write(tigetstr('rc'))
        t.stream.flush()

    print(t.normal)


if __name__ == "__main__":
    progressive_example()
    #clint_progress_example()
    #progress_progress_example()
    #blessings_progress_example()

