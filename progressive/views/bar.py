# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

from progressive.cursor import Cursor
from progressive.util import floor, ensure, u
from progressive.exceptions import ColorUnsupportedError, WidthOverflowError
from progressive.blocks.indent import Indent
from progressive.blocks.bar import BaseBar
from progressive.blocks.title import Title
from progressive.blocks.percentage import Fraction, Percentage


class Bar(object):
    """Progress Bar with blessings

    Several parts of this class are thanks to Erik Rose's implementation
    of ``ProgressBar`` in ``nose-progressive``, licensed under
    The MIT License.
    `MIT <http://opensource.org/licenses/MIT>`_
    `nose-progressive/noseprogressive/bar.py <https://github.com/erikrose/nose-progressive/blob/master/noseprogressive/bar.py>`_

    Terminal with 256 colors is recommended. See
        `this <http://pastelinux.wordpress.com/2010/12/01/upgrading-linux-terminal-to-256-colors/>`_ for Ubuntu
        installation as an example.

    :type  term: blessings.Terminal|NoneType
    :param term: blessings.Terminal instance for the terminal of display
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
            self, term=None, max_value=100, width="25%", title_pos="left",
            title="Progress", num_rep="fraction", indent=0,
            filled_color="green", empty_color="white", back_color=None,
            filled_char=u' ', empty_char=u' ', start_char=u'',
            end_char=u'', fallback=True, fallback_empty_char=u'◯',
            fallback_filled_char=u'◉', force_color=None
    ):
        self.cursor = Cursor(term)
        self.term = self.cursor.term

        self._measure_terminal()

        self._width_str = width
        self.max_value = max_value

        ensure(title_pos in ["left", "right", "above", "below"], ValueError,
               "Invalid choice for title position.")
        self._title_pos = title_pos
        self.title = title
        ensure(num_rep in ["fraction", "percentage"], ValueError,
               "num_rep must be either 'fraction' or 'percentage'.")
        self._num_rep = num_rep
        self._indent = indent

        self._start_char = start_char
        self._end_char = end_char

        # Setup callables and characters depending on if terminal has
        #   has color support
        if force_color is not None:
            supports_colors = force_color
        else:
            supports_colors = self._supports_colors(
                term=self.term,
                raise_err=not fallback,
                colors=(filled_color, empty_color)
            )
        if supports_colors:
            self._filled_char = filled_char
            self._empty_char = empty_char
            self._filled = self._get_format_callable(
                term=self.term,
                color=filled_color,
                back_color=back_color
            )
            self._empty = self._get_format_callable(
                term=self.term,
                color=empty_color,
                back_color=back_color
            )
        else:
            self._empty_char = fallback_empty_char
            self._filled_char = fallback_filled_char
            self._filled = self._empty = lambda s: s

        ensure(self.full_line_width <= self.columns, WidthOverflowError,
               "Attempting to initialize Bar with full_line_width {}; "
               "terminal has width of only {}.".format(
                   self.full_line_width,
                   self.columns))
