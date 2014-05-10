from progressive.blocks.block import Block
from progressive.util import ensure, u, floor


class BaseBar(Block):
    """BaseBar Block

    :type  max_value: int
    :param max_value: The capacity of the bar, i.e., ``value/max_value``
    """
    def __init__(self, value, max_value=100, width=10, filled_color=4,
                 empty_color=7, back_color=None, filled_char=u' ',
                 empty_char=u' ', fallback=True,
                 fallback_empty_char=u'◯', fallback_filled_char=u'◉',
                 force_color=None):
