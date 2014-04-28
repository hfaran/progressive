# -*- coding: utf-8 -*-

from __future__ import division

from signal import signal, SIGWINCH
from math import floor


class ColorUnsupportedError(Exception):
    """Color is not supported by terminal"""


def ensure(expr, exc, *args, **kwargs):
    """
    :raises ``exc``: With ``*args`` and ``**kwargs`` if not ``expr``
    """
    if not expr:
        raise exc(*args, **kwargs)


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

    :type  term: blessings.Terminal()
    :param term: blessings.Terminal instance for the terminal of display
    :type  max_value: int
    :param max_value: The capacity of the bar, i.e., ``index/max_value``
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
        that works on terminals with no color support
    """

    def __init__(self, term, max_value=100, width="25%", title_pos="left",
                 title="Progress", num_rep="fraction", indent=0,
                 filled_color=10,
                 empty_color=240, back_color=None,
                 filled_char=u' ', empty_char=u' ',
                 start_char=u'', end_char=u'', fallback=False,
                 fallback_empty_char=u'◯', fallback_filled_char=u'◉'):
        self._term = term
        self._measure_terminal()

        self._width_str = width
        self.max_value = max_value
        self._value = 0

        ensure(title_pos in ["left", "right", "above", "below"], ValueError,
               "Invalid choice for title position.")
        self.title_pos = title_pos
        self.title = title
        ensure(num_rep in ["fraction", "percentage"], ValueError,
               "num_rep must be either 'fraction' or 'percentage'.")
        self.num_rep = num_rep
        ensure(indent < self.columns, ValueError,
               "Indent must be smaller than terminal width.")
        self.indent = indent

        self.start_char = start_char
        self.end_char = end_char

        # Setup callables and characters depending on if terminal has
        #   has color support
        supports_colors = self._supports_colors(
            term=term,
            raise_err=not fallback,
            colors=(filled_color, empty_color)
        )
        if supports_colors:
            self._filled_char = filled_char
            self._empty_char = empty_char
            self._filled = self._get_format_callable(
                term=term,
                color=filled_color,
                back_color=back_color
            )
            self._empty = self._get_format_callable(
                term=term,
                color=empty_color,
                back_color=back_color
            )
        else:
            self._empty_char = fallback_empty_char
            self._filled_char = fallback_filled_char
            self._filled = self._empty = lambda s: s

        # Handle window resize
        # TODO: Winch handling should be done by user of Bar
        # signal(SIGWINCH, self._handle_winch)

    ###################
    # Private Methods #
    ###################

    @staticmethod
    def _supports_colors(term, raise_err, colors):
        """Check if ``term`` supports ``colors``

        :raises ColorUnsupportedError: This is raised if ``raise_err``
            is ``False`` and a color in ``colors`` is unsupported by ``term``
        :type raise_err: bool
        :param raise_err: Set to ``False`` to return a ``bool`` indicating
            color support rather than raising ColorUnsupportedError
        :type  colors: [str, ...]
        """
        for color in colors:
            try:
                if isinstance(color, str):
                    req_colors = 16 if "bright" in color else 8
                    ensure(term.number_of_colors >= req_colors,
                           ColorUnsupportedError, color,
                           "{} is unsupported by your terminal.".format(color))
                elif isinstance(color, int):
                    ensure(term.number_of_colors >= color,
                           ColorUnsupportedError, color,
                           "{} is unsupported by your terminal.".format(color))
            except ColorUnsupportedError as e:
                if raise_err:
                    raise e
                else:
                    return False
        else:
            return True

    @staticmethod
    def _get_format_callable(term, color, back_color):
        """Get string-coloring callable

        Get callable for string output using ``color`` on ``back_color``
            on ``term``

        :param term: blessings.Terminal instance
        :param color: Color that callable will color the string it's passed
        :param back_color: Back color for the string
        :returns: callable(s: str) -> str
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

    # TODO: Winch handling should be done by user of Bar
    # def _handle_winch(self, *args):
    #     # self.erase()  # Doesn't seem to help.
    #     self._measure_terminal()
    #     self.draw()

    def _measure_terminal(self):
        self.lines, self.columns = (
            self._term.height or 24,
            self._term.width or 80
        )

    ##################
    # Public Methods #
    ##################

    @property
    def max_width(self):
        """
        :rtype: int
        :returns: Maximum column width of progress bar
        """
        value, unit = float(self._width_str[:-1]), self._width_str[-1]

        ensure(unit in ["c", "%"], ValueError,
               "Width unit must be either 'c' or '%'")

        if unit == "c":
            ensure(value <= self.columns, ValueError,
                   "Terminal only has {} columns, cannot draw "
                   "bar of size {}.".format(self.columns, value))
            retval = value
        else:  # unit == "%"
            ensure(0 < value <= 100, ValueError,
                   "value=={} does not satisfy 0 < value <= 100".format(value))
            dec = value / 100
            retval = dec * self.columns

        return int(floor(retval))

    @property
    def filled(self):
        """
        :rtype: callable
        """
        return self._filled

    @property
    def empty(self):
        """
        :rtype: callable
        """
        return self._empty

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def draw(self):
        amount_complete = self.value / self.max_value
        fill_amount = int(floor(amount_complete * self.max_width))
        empty_amount = self.max_width - fill_amount

        # '10/20' if 'fraction' or '50%' if 'percentage'
        amount_complete_str = (
            "{}/{}".format(self.value, self.max_value)
            if self.num_rep == "fraction" else
            "{}%".format(int(floor(amount_complete * 100)))
        )

        # Construct just the progress bar
        bar_str = ''.join([
            # str() casting for type-hinting
            str(self.filled(self._filled_char * fill_amount)),
            str(self.empty(self._empty_char * empty_amount)),
        ])
        # Wrap with start and end character
        bar_str = "{}{}{}".format(self.start_char, bar_str, self.end_char)
        # Add on title if supposed to be on left or right
        if self.title_pos == "left":
            bar_str = "{} {}".format(self.title, bar_str)
        elif self.title_pos == "right":
            bar_str = "{} {}".format(bar_str, self.title)
        # Add indent
        bar_str = ''.join([" " * self.indent, bar_str])
        # Add complete percentage of fraction
        bar_str = "{} {}".format(bar_str, amount_complete_str)

        # Write and flush
        self._term.stream.write(bar_str)
        self._term.stream.flush()
