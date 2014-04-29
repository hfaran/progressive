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


def u(s):
    """Cast ``s`` as unicode string

    This is a convenience function to make up for the fact
        that Python3 does not have a unicode() cast (for obvious reasons)

    :rtype: unicode
    :returns: Equivalent of unicode(s) (at least I hope so)
    """
    return u'{}'.format(s)
