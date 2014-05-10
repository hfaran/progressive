from progressive.blocks.block import Block
from progressive.util import ensure, u, floor


class BaseBar(Block):
    """BaseBar Block

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
    :param fallback: If this is False, no color will be applied to the bar.
    """
    def __init__(self, value, max_value=100, width=15, filled_color="green",
                 empty_color="white", back_color=None, filled_char=u' ',
                 empty_char=u' ', color_enabled=True):
        pass
