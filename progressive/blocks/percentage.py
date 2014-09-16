# -*- coding: utf-8 -*-

from progressive.blocks.block import Block
from progressive.util import floor


class Percentage(Block):
    """Percentage complete of a task

    :type decimal_value: float
    :param decimal_value: 0<=x<=1, usually value/max_value
    """

    def __init__(self, decimal_value):
        self._repr = u"{}%".format(str(floor(decimal_value * 100.0)).rjust(3))

    @property
    def view(self):
        return self._repr

    @property
    def len(self):
        return len(self._repr)


class Fraction(Block):
    """Fraction complete of a task"""

    def __init__(self, numerator, denominator):
        self._repr = u"{}/{}".format(numerator, denominator)

    @property
    def view(self):
        return self._repr

    @property
    def len(self):
        return len(self._repr)
