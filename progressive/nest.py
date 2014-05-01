from __future__ import division

from copy import deepcopy
from blessings import Terminal

from progressive.bar import Bar
from progressive.util import floor, ensure
from progressive.exceptions import LengthOverflowError


class NestedProgress(object):
    """Nested progress"""

    def __init__(self, term=None, indent=4):
        self.term = Terminal() if term is None else term
        self.indent = indent

    def draw(self, obj):
        obj = deepcopy(obj)
        # TODO: Automatically collapse hierarchy so something
        #   will always be displayable (well, unless the top-level)
        #   contains too many to display
        lines_required = self.lines_required(obj)
        ensure(lines_required <= self.term.height,
               LengthOverflowError,
               "Terminal is not long enough to fit all bars.")
        self._calculate_values(obj)
        self._draw(obj)

    def clear_lines(self, obj):
        lines_req = self.lines_required(obj)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_down)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_up)

    def lines_required(self, obj, count=0):
        if isinstance(obj, dict):
            return sum(self.lines_required(v, count=count)
                       for v in obj.values()) + 2
        elif isinstance(obj, int):
            return 2

    def _calculate_values(self, obj):
        if isinstance(obj, dict):
            items = len(obj)
            value = 0
            for k in obj:
                val = self._calculate_values(obj[k])
                obj[k] = (val, obj[k])
                value += val
            return floor(value/items)
        elif any(isinstance(obj, t) for t in [int, float]):
            return floor(obj)
        else:
            raise TypeError("Unexpected type {}".format(type(obj)))

    def _draw(self, obj, indent=0):
        if isinstance(obj, dict):
            for k, v in sorted(obj.items()):
                val, subdict = v[0], v[1]
                b = Bar(self.term, title_pos="above", indent=indent, title=k)
                b.draw(val)
                self.term.stream.write(self.term.move_down)
                self.term.stream.write(self.term.clear_bol)

                self._draw(subdict, indent=indent+self.indent)
