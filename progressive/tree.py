from __future__ import division

from copy import deepcopy

from blessings import Terminal

from progressive.bar import Bar
from progressive.util import floor, ensure
from progressive.exceptions import LengthOverflowError


class Value(object):
    """Container class for use with ``BarDescriptor``

    Should be used for ``value`` argument when initializing
        ``BarDescriptor``, e.g., ``BarDescriptor(type=..., value=Value(10))``
    """

    def __init__(self, val=0):
        self.value = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = floor(val)


class BarDescriptor(dict):
    """Bar descriptor

    To be used in leaf of a tree describing a hierarchy for ``TreeProgress``,
    e.g.,:

        tree = {"Job":
            {"Task1": BarDescriptor(...)},
            {"Task2":
                {"Subtask1": BarDescriptor(...)},
            },
        }

    :type  type: Bar|subclass of Bar
    :param type: The type of Bar to use to display that leaf
    :type  value: Value
    :param value: Amount to fill the progress bar vs. its max value
    :type  args: list
    :param args: A list of args to instantiate ``type`` with
    :type  kwargs: dict
    :param kwargs: A dict of kwargs to instantiate ``type`` with
    """


class TreeProgress(object):
    """Progress display for trees

    For drawing a hierarchical progress view from a tree

    :type  term: NoneType|blessings.Terminal
    :param term: Terminal instance; if not given, will be created by the class
    :type  indent: int
    :param indent: The amount of indentation between each level in hierarchy
    """

    def __init__(self, term=None, indent=4):
        self.term = Terminal() if term is None else term
        self.indent = indent
        self._saved = False

    ##################
    # Public Methods #
    ##################

    def draw(self, tree, save_cursor=True, flush=True):
        """Draw ``tree`` to the terminal

        :type  tree: dict
        :param tree: ``tree`` should be a tree representing a hierarchy; each
            key should be a string describing that hierarchy level and value
            should also be ``dict`` except for leaves which should be
            ``BarDescriptors``. See ``BarDescriptor`` for a tree example.
        :type  flush: bool
        :param flush: If this is set, output written will be flushed
        :type  save_cursor: bool
        :param save_cursor: If this is set, cursor location will be saved before
            drawing; this will OVERWRITE a previous save, so be sure to set
            this accordingly (to your needs).
        """
        if save_cursor:
            self.save()

        tree = deepcopy(tree)
        # TODO: Automatically collapse hierarchy so something
        #   will always be displayable (well, unless the top-level)
        #   contains too many to display
        lines_required = self.lines_required(tree)
        ensure(lines_required <= self.term.height,
               LengthOverflowError,
               "Terminal is not long enough to fit all bars.")
        self._calculate_values(tree)
        self._draw(tree)
        if flush:
            self.term.flush()

    def save(self):
        """Saves current cursor position, so that it can be restored later"""
        self.term.stream.write(self.term.save)
        self._saved = True

    def restore(self):
        """Restores cursor to the previously saved location

        This is useful after calling TreeProgress.draw(..., save_cursor=True)
            to restore the cursor to the position it was in before drawing,
            before drawing again.

        Cursor position will only be restored IF it was previously saved
            by this TreeProgress instance (and not by any external force)
        """
        if self._saved:
            self.term.stream.write(self.term.restore)

    def clear_lines(self, tree):
        """Clear lines in terminal below current cursor position as required

        This is important to do before drawing to ensure sufficient
        room at the bottom of your terminal.

        :type  tree: dict
        :param tree: tree as described in ``BarDescriptor``
        """
        lines_req = self.lines_required(tree)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_down)
        for i in range(lines_req):
            self.term.stream.write(self.term.move_up)

    def lines_required(self, tree, count=0):
        """Calculate number of lines required to draw ``tree``"""
        if all([
            isinstance(tree, dict),
            type(tree) != BarDescriptor
        ]):
            return sum(self.lines_required(v, count=count)
                       for v in tree.values()) + 2
        elif isinstance(tree, BarDescriptor):
            if tree.get("kwargs", {}).get("title_pos") in ["left", "right"]:
                return 1
            else:
                return 2

    ###################
    # Private Methods #
    ###################

    def _calculate_values(self, tree):
        """Calculate values for drawing bars of non-leafs in ``tree``

        Recurses through ``tree``, replaces ``dict``s with
            ``(BarDescriptor, dict)`` so ``TreeProgress._draw`` can use
            the ``BarDescriptor``s to draw the tree
        """
        if all([
            isinstance(tree, dict),
            type(tree) != BarDescriptor
        ]):
            items = len(tree)
            value = 0
            for k in tree:
                bar_desc = self._calculate_values(tree[k])
                val = bar_desc["value"].value
                tree[k] = (bar_desc, tree[k])
                value += val
            return BarDescriptor(type=Bar, value=Value(floor(value / items)))
        elif isinstance(tree, BarDescriptor):
            return tree
        else:
            raise TypeError("Unexpected type {}".format(type(tree)))

    def _draw(self, tree, indent=0):
        """Recurse through ``tree`` and draw all nodes"""
        if all([
            isinstance(tree, dict),
            type(tree) != BarDescriptor
        ]):
            for k, v in sorted(tree.items()):
                bar_desc, subdict = v[0], v[1]

                args = [self.term] + bar_desc.get("args", [])
                kwargs = dict(title_pos="above", indent=indent, title=k)
                kwargs.update(bar_desc.get("kwargs", {}))

                b = Bar(*args, **kwargs)
                b.draw(bar_desc["value"].value)
                self.term.stream.write(self.term.move_down)
                self.term.stream.write(self.term.clear_bol)

                self._draw(subdict, indent=indent + self.indent)
