# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

import blessings
from progressive.blocks.block import Block
from progressive.util import ensure, u, floor


class BaseBar(Block):
    """BaseBar Block

    :type  term: :class:`blessings.Terminal`|NoneType
    :param term: :class:`blessings.Terminal` instance for the terminal of display
    :type  value: int
    :param value: Amount of the bar filled relative to ``max_value``
    :type  max_value: int
    :param max_value: The capacity of the bar
    :type  width: int
    :param width: The width of the bar in characters
    :type  filled_color: str|int
    :param filled_color: color of the ``filled_char``; can be a string
        of the color's name or number representing the color; see the
        ``blessings`` documentation for details
    :type  empty_color: str|int
    :param empty_color: color of the ``empty_char``
    :type  back_color: str|NoneType
    :param back_color: Background color of the progress bar; must be
        a string of the color name, unused if numbers used for
        ``filled_color`` and ``empty_color``. If set to None,
        will not be used.
    :type  filled_char: unicode
    :param filled_char: Character representing completeness on the
        progress bar
    :type  empty_char: unicode
    :param empty_char: The complement to ``filled_char``
    :type  color_enabled: bool
    :param color_enabled: If this is False, no color will be
        applied to the bar.
    """

    def __init__(self, term, value, max_value=100, width=15,
                 filled_color="green", empty_color="white", back_color=None,
                 filled_char=u' ', empty_char=u' ', color_enabled=True):
        self._width = width

        get_format_callable = lambda color: self.get_format_callable(
            term=term,
            color=color,
            back_color=back_color
        ) if color_enabled else lambda x: x

        filled_f = get_format_callable(filled_color)
        empty_f = get_format_callable(empty_color)

        amount_complete = value / max_value
        fill_amount = floor(amount_complete * width)
        empty_amount = width - fill_amount

        self._bar_str = u''.join([
            u(filled_f(filled_char * fill_amount)),
            u(empty_f(empty_char * empty_amount)),
        ])

    @staticmethod
    def get_format_callable(term, color, back_color):
        """Get string-coloring callable

        Get callable for string output using ``color`` on ``back_color``
            on ``term``

        :param term: :class:`blessings.Terminal` instance
        :param color: Color that callable will color the string it's passed
        :param back_color: Back color for the string
        :returns: callable(s: str) -> str
        :rtype: callable
        """
        if isinstance(color, str):
            ensure(
                any(isinstance(back_color, t) for t in [str, type(None)]),
                TypeError,
                "back_color must be a str or NoneType"
            )
            if back_color:
                return getattr(term, "_".join(
                    [color, "on", back_color]
                ))
            elif back_color is None:
                return getattr(term, color)
        elif isinstance(color, int):
            return term.on_color(color)
        else:
            raise TypeError("Invalid type {} for color".format(
                type(color)
            ))

    @property
    def repr(self):
        return self._bar_str

    @property
    def len(self):
        return self._width
