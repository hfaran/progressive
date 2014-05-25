# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

from progressive.util import floor, ensure, u, check_color_support
from progressive.exceptions import ColorUnsupportedError, WidthOverflowError
from progressive.blocks.indent import Indent
from progressive.blocks.bar import BaseBar
from progressive.blocks.title import Title
from progressive.blocks.percentage import Fraction, Percentage


class Bar(object):
    """Basic progress bar

    :type  cursor: progressive.cursor.Cursor
    :type  max_value: int
    :param max_value: The capacity of the bar, i.e., ``value/max_value``
    :type  width: str
    :param width: Must be of format {num: int}{unit: c|%}. Unit "c"
        can be used to specify number of maximum columns; unit "%".
        to specify percentage of the total terminal width to use.
        e.g., "20c", "25%", etc.
    :type  title_pos: str
    :param title_pos: Position of title relative to the progress bar;
        can be any one of ["left", "right", "above", "below"]
    :type  title: str
    :param title: Title of the progress bar
    :type  num_rep: str
    :param num_rep: Numeric representation of completion;
        can be one of ["fraction", "percentage"]
    :type  indent: int
    :param indent: Spaces to indent the bar from the left-hand side
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
    :type  start_char: unicode
    :param start_char: Character at the start of the progress bar
    :type  end_char: unicode
    :param end_char: Character at the end of the progress bar
    :type  fallback: bool
    :param fallback: If this is set, if the terminal does not support
        provided colors, this will fall back to plain formatting
        that works on terminals with no color support, using the
        provided ``fallback_empty_char` and ``fallback_filled_char``
    :type  force_color: bool|NoneType
    :param force_color: ``True`` forces color to be used even if it
        may not be supported by the terminal; ``False`` forces use of
        the fallback formatting; ``None`` does not force anything
        and allows automatic detection as usual.
    """

    def __init__(
            self, cursor, max_value=100, width="25%", title_pos="left",
            title="Progress", num_rep="fraction", indent=0,
            filled_color="green", empty_color="white", back_color=None,
            filled_char=u' ', empty_char=u' ', start_char=u'',
            end_char=u'', fallback=True, fallback_empty_char=u'◯',
            fallback_filled_char=u'◉', force_color=None
    ):
        self.cursor = cursor
        self.term = self.cursor.term

        (self.x, self.y) = self._measure_terminal()

        self.width = width
        self.max_value = max_value

        ensure(title_pos in ["left", "right", "above", "below"], ValueError,
               "Invalid choice for title position.")
        self.title_pos = title_pos
        self.title = title
        ensure(num_rep in ["fraction", "percentage"], ValueError,
               "num_rep must be either 'fraction' or 'percentage'.")
        self.num_rep = num_rep
        self.indent = indent

        self.start_char = start_char
        self.end_char = end_char

        # Setup callables and characters depending on if terminal has
        #   has color support
        if force_color is not None:
            supports_colors = force_color
        else:
            supports_colors = check_color_support(
                term=self.term,
                raise_err=not fallback,
                colors=(filled_color, empty_color)
            )
        if supports_colors:
            self.filled_char = filled_char
            self.empty_char = empty_char
            self.filled_color = filled_color
            self.empty_color = empty_color
            self.back_color = back_color
        else:
            self.empty_char = fallback_empty_char
            self.filled_char = fallback_filled_char


    def _measure_terminal(self):
        return (
            self.term.height or 24,
            self.term.width or 80
        )

    def draw(self, value, newline=True, flush=True):
        """"""
        (self.x, self.y) = self._measure_terminal()

