from blessings import Terminal


class Cursor(object):
    """Common methods for cursor manipulation

    :type  term: blessings.Terminal
    """

    def __init__(self, term=None):
        self.term = Terminal() if term is None else term
        self._saved = False

    def save(self):
        """Saves current cursor position, so that it can be restored later"""
        self.term.stream.write(self.term.save)
        self._saved = True

    def restore(self):
        """Restores cursor to the previously saved location

        Cursor position will only be restored IF it was previously saved
            by this instance (and not by any external force)
        """
        if self._saved:
            self.term.stream.write(self.term.restore)
