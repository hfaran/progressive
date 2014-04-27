# -*- coding: utf-8 -*-


import types
from signal import signal, SIGWINCH


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
    """

    def __init__(self, term, max_value=100, filled_color="cyan",
                 empty_color="white", back_color=None,
                 filled_char=u' ', empty_char=u' ',
                 start_char=u'', end_char=u''):
        self._term = term
        self.stream = term.stream
        self.max_value = max_value
        self.filled_color = filled_color
        self.empty_color = empty_color
        self.back_color = back_color
        self.filled_char = filled_char
        self.empty_char = empty_char
        self.start_char = start_char
        self.end_char = end_char

        self._measure_terminal()
        # Handle window resize
        signal(SIGWINCH, self._handle_winch)

    ###################
    # Private Methods #
    ###################

    def _get_format_callable(self, color):
        """Get blessings.Terminal() callable"""
        if isinstance(color, str):
            assert any(isinstance(self.back_color,
                                  t) for t in [str, types.NoneType])
            if self.back_color:
                return getattr(self._term, color)
            elif self.back_color is None:
                return getattr(self._term, "_".join(
                    [color, "on", self.back_color]
                ))
            else:
                raise TypeError("Invalid type {} for self.back_color".format(
                    type(self.back_color)
                ))
        elif isinstance(color, int):
            return self._term.on_color(color)
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
        return self._get_format_callable(self.filled_color)

    @property
    def empty(self):
        return self._get_format_callable(self.empty_color)
