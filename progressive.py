# -*- coding: utf-8 -*-


import types
from signal import signal, SIGWINCH
from ensure import check


class ColorUnsupportedError(StandardError):
    """Color is not supported by terminal"""


class Bar(object):
    """Progress Bar with blessings

    Many parts of this class are thanks to Erik Rose's implementation
    of ``ProgressBar`` in ``nose-progressive``, licensed under
    The MIT License.
    `MIT <http://opensource.org/licenses/MIT>`_
    `nose-progressive/noseprogressive/bar.py <https://github.com/erikrose/nose-progressive/blob/master/noseprogressive/bar.py>`_

    :type  term: blessings.Terminal()
    :param term: blessings.Terminal instance for the terminal of display
    :type  max: int
    :param max: The capacity of the bar, i.e., ``index/max_value``
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

    def __init__(self, term, max_value=100, filled_color="cyan",
                 empty_color="white", back_color=None,
                 filled_char=u' ', empty_char=u' ',
                 start_char=u'', end_char=u'', fallback=False,
                 fallback_empty_char=u'◯', fallback_filled_char=u'◉'):
        self._term = term
        self.stream = term.stream
        self.max_value = max_value

        # Setup callables and characters depending on if terminal has
        #   has color support
        self._has_color = self._check_has_color(term, filled_color, empty_color)
        if self._has_color:
            self._filled_char = filled_char
            self._empty_char = empty_char
            self._filled = self._get_format_callable(term, filled_color, back_color)
            self._empty = self._get_format_callable(term, empty_color, back_color)
        else:
            if fallback:
                self._empty_char = fallback_empty_char
                self._filled_char = fallback_filled_char
                self._filled = self._empty = lambda s: s
            else:
                raise ColorUnsupportedError

        self.start_char = start_char
        self.end_char = end_char

        self._measure_terminal()

        # Handle window resize
        signal(SIGWINCH, self._handle_winch)

    ###################
    # Private Methods #
    ###################

    @staticmethod
    def _check_has_color(term, filled_color, empty_color):
        try:
            for color in [filled_color, empty_color]:
                if isinstance(color, str):
                    req_colors = 16 if "bright" in color else 8
                    check(term.number_of_colors
                    ).is_greater_than_or_equal_to(
                        req_colors).or_raise(ColorUnsupportedError)
                elif isinstance(color, int):
                    check(term.number_of_colors
                    ).is_greater_than_or_equal_to(
                        color).or_raise(ColorUnsupportedError)
            else:
                return True
        except ColorUnsupportedError:
            return False

    @staticmethod
    def _get_format_callable(term, color, back_color):
        """Get blessings.Terminal() callable"""
        if isinstance(color, str):
            assert any(isinstance(back_color,
                                  t) for t in [str, types.NoneType])
            if back_color:
                return getattr(term, color)
            elif back_color is None:
                return getattr(term, "_".join(
                    [color, "on", back_color]
                ))
            else:
                raise TypeError("Invalid type {} for self.back_color".format(
                    type(back_color)
                ))
        elif isinstance(color, int):
            return term.on_color(color)
        else:
            raise TypeError("Invalid type {} for color".format(
                type(color)
            ))

    def _handle_winch(self, *args):
        # self.erase()  # Doesn't seem to help.
        self._measure_terminal()
        # TODO: Reprint the bar but at the new width.


    def _measure_terminal(self):
        self.lines, self.columns = (
            self._term.height or 24,
            self._term.width or 80
        )

    ##################
    # Public Methods #
    ##################

    @property
    def filled(self):
        return self._filled

    @property
    def empty(self):
        return self._empty
