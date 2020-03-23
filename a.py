imp = __builtins__.__import__

def f(*args, **kwargs):
    print(args[0])
    return imp(*args, **kwargs)

__builtins__.__import__ = f


import collections.abc
