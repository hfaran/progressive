from __future__ import division

from copy import deepcopy
from blessings import Terminal

from progressive.bar import Bar
from progressive.util import floor, ensure
from progressive.exceptions import LengthOverflowError


class Value(object):

    def __init__(self, value):
        self.value = value


class BarDescriptor(dict):
    """Bar descriptor"""


class NestedProgress(object):
    """Nested progress"""

    def __init__(self, term=None, indent=4):
        self.term = Terminal() if term is None else term
        self.indent = indent

    def draw(self, obj, flush=True):
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
        if flush:
            self.term.flush()

    def clear_lines(self, obj):
        lines_req = self.lines_required(obj)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_down)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_up)

    def lines_required(self, obj, count=0):
        if all([
            isinstance(obj, dict),
            type(obj) != BarDescriptor
        ]):
            return sum(self.lines_required(v, count=count)
                       for v in obj.values()) + 2
        elif isinstance(obj, BarDescriptor):
            if obj.get("kwargs", {}).get("title_pos") in ["left", "right"]:
                return 1
            else:
                return 2

    def _calculate_values(self, obj):
        if all([
            isinstance(obj, dict),
            type(obj) != BarDescriptor
        ]):
            items = len(obj)
            value = 0
            for k in obj:
                bar_desc = self._calculate_values(obj[k])
                val = bar_desc["value"].value
                obj[k] = (bar_desc, obj[k])
                value += val
            return BarDescriptor(type=Bar, value=Value(floor(value / items)))
        elif isinstance(obj, BarDescriptor):
            return obj
        else:
            raise TypeError("Unexpected type {}".format(type(obj)))

    def _draw(self, obj, indent=0):
        if all([
            isinstance(obj, dict),
            type(obj) != BarDescriptor
        ]):
            for k, v in sorted(obj.items()):
                bar_desc, subdict = v[0], v[1]

                args = [self.term] + bar_desc.get("args", [])
                kwargs = dict(title_pos="above", indent=indent, title=k)
                kwargs.update(bar_desc.get("kwargs", {}))

                b = Bar(*args, **kwargs)
                b.draw(bar_desc["value"].value)
                self.term.stream.write(self.term.move_down)
                self.term.stream.write(self.term.clear_bol)

                self._draw(subdict, indent=indent + self.indent)
