# -*- coding: utf-8 -*-

from abc import abstractproperty, ABCMeta


class Block(metaclass=ABCMeta):
    """Building block for a progress view"""

    @abstractproperty
    def repr(self):
        """Returns a unicode string representing the block

        :rtype: unicode|str
        """
        raise NotImplementedError

    @abstractproperty
    def len(self):
        """A more accurate ``len(self.repr)`` if ``self.repr``
        has custom formatting for which ``len`` gives incorrect output.

        :rtype: list|int
        """
        raise NotImplementedError

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.repr)
