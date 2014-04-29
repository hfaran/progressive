import math


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
