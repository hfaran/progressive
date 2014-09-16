# -*- coding: utf-8 -*-

from abc import abstractproperty, ABCMeta

from progressive.blocks.block import Block
from progressive.util import u


# TODO: If necessary, implement a ``View`` abstraction from which to subclass
#   and create views from; the necessity of this will be determined after
#   creating a few views that use lines.


class Line(object):
    """Line composed of ``Block``s

    :type blocks: list
    :param blocks: List of ``Block`` instances from which this Line is composed
    :type separator: unicode|str
    :param separator: Separator between ``blocks``; empty by default
    """

    def __init__(self, blocks, separator=u''):
        assert all([isinstance(blocks, list),
                    all(isinstance(b, Block) for b in blocks)])
        self.blocks = blocks
        self.sep = u(separator)

    def view(self):
        return self.sep.join([b.view for b in self.blocks])

    def len(self):
        return sum(b.len for b in self.blocks)
