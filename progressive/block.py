from abc import abstractproperty, ABCMeta


class Block(metaclass=ABCMeta):
    """Building block for a progress view"""

    @abstractproperty
    def repr(self):
        """Returns a unicode string representing the block or a list of
        unicode strings with separation of each representing a newline.

        :rtype: list|unicode|str
        """
        raise NotImplementedError

    @abstractproperty
    def len(self):
        """A more accurate ``len(self.repr)`` if ``self.repr``
        has custom formatting for which ``len`` gives incorrect output.

        If self.repr has no newlines, should return an ``int``, otherwise,
        a list of ints, each of the length of each line separated by newlines.
        This will let us know of how many lines to allocate using
        ``clear_lines`` and if the terminal is wide enough for displaying
        everything in the classes that are composed of ``Block``s.

        :rtype: list|int
        """
        raise NotImplementedError
