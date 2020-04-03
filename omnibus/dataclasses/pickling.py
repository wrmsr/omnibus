from .dataclasses import asdict


class SimplePickle:

    def __reduce__(self):
        return (Reducer(), (type(self).__module__, type(self).__qualname__, asdict(self),))


class Reducer:

    def __call__(self, mod, name, dct):
        cur = __import__(mod)
        for part in mod.split('.')[1:]:
            cur = getattr(cur, part)
        for part in name.split('.'):
            cur = getattr(cur, part)
        return cur(**dct)
