from progressive.blocks.block import Block
from progressive.util import u


class Title(Block):
    """Title Block

    :type  title: unicode|str
    :param title: Title for progress view (or just a simple string to be
        used anywhere)
    :type  length: int|NoneType
    :param length: Custom length of ``title``; defaults as None in which
        it is calculated using len
    """
    def __init__(self, title, length=None):
        self._repr = u(title)
        self._length = length if length is not None else len(self._repr)

    @property
    def repr(self):
        return self._repr

    @property
    def len(self):
        return self._length
