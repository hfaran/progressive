# -*- coding: utf-8 -*-
import math
import copy
from itertools import chain

import blessings

from progressive.exceptions import ColorUnsupportedError


def floor(x):
    """Returns the floor of ``x``

    :returns: floor of ``x``
    :rtype: int
    """
    return int(math.floor(x))


def ensure(expr, exc, *args, **kwargs):
    """
    :raises ``exc``: With ``*args`` and ``**kwargs`` if not ``expr``
    """
    if not expr:
        raise exc(*args, **kwargs)


def u(s):
    """Cast ``s`` as unicode string

    This is a convenience function to make up for the fact
        that Python3 does not have a unicode() cast (for obvious reasons)

    :rtype: unicode
    :returns: Equivalent of Python2 ``unicode(s)``
    """
    return u'{}'.format(s)


def merge_dicts(dicts, deepcopy=False):
    """Merges dicts

    In case of key conflicts, the value kept will be from the latter
    dictionary in the list of dictionaries

    :type dicts: list
    :param dicts: [dict, ...]
    :type deepcopy: bool
    :param deepcopy: deepcopy items within dicts
    """
    assert isinstance(dicts, list) and all(isinstance(d, dict) for d in dicts)
    return dict(chain(*[copy.deepcopy(d).items() if deepcopy else d.items()
                        for d in dicts]))


def check_color_support(term, raise_err, colors):
    """Check if ``term`` supports ``colors``

    :raises ColorUnsupportedError: This is raised if ``raise_err``
        is ``False`` and a color in ``colors`` is unsupported by ``term``
    :type term: :class:`blessings.Terminal`
    :type raise_err: bool
    :param raise_err: Set to ``False`` to return a ``bool`` indicating
        color support rather than raising ColorUnsupportedError
    :param colors: Colors to check support for (list of strings)
    :type  colors: list
    """
    for color in colors:
        try:
            if isinstance(color, str):
                req_colors = 16 if "bright" in color else 8
                ensure(term.number_of_colors >= req_colors,
                       ColorUnsupportedError,
                       "{} is unsupported by your terminal.".format(color))
            elif isinstance(color, int):
                ensure(term.number_of_colors >= color,
                       ColorUnsupportedError,
                       "{} is unsupported by your terminal.".format(color))
        except ColorUnsupportedError as e:
            if raise_err:
                raise e
            else:
                return False
    else:
        return True
