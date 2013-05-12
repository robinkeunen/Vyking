# -----------------------------------------------------------------------------
# misc.py
# Defines some usefull functions
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------


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


@decorator
def trace(f):
    indent = '    '

    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print('%s--> %s' % (trace.level * indent, signature))
        trace.level += 1
        try:
            result = f(*args)
            print('%s<-- %s == %s' % ((trace.level - 1) * indent,
                                      signature, result))
        finally:
            trace.level -= 1
        return result

    trace.level = 0
    return _f