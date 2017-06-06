from contextlib import contextmanager

"""Implements the python 3 suppress context manager, allowing for cleaner suppression of errors where no action is required."""

@contextmanager
def suppress(*args):
    for t in args: assert (issubclass(t, BaseException))
    try: yield
    except tuple(args): pass

