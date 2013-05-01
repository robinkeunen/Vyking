# defines some usefull functions
__author__ = 'Robin Keunen'

from functools import update_wrapper


def decorator(d):
    """Make function d a decorator: d wraps a function fn."""

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def add_to_class(Cls):
    """
    Adds decorated function to class C.
    """

    def dec_f(f):
        setattr(Cls, f.__name__, f)
        return f

    return dec_f
