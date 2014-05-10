from progressive.blocks.block import Block
from progressive.util import u


class Indent(Block):
    """Indent Block

    :type  length: int
    :param length: Length of indent
    :type  character: unicode|str
    :param character: Character that indent is composed of
    """
    def __init__(self, length=4, character=u" "):
        self._length = length
        self._repr = u(character*length)

    @property
    def repr(self):
        return self._repr

    @property
    def len(self):
        return self._length
