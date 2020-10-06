import dataclasses as dc


def my_dataclass(*args, **kwargs):
    return dc.dataclass(*args, **kwargs)


@my_dataclass(frozen=True)
class Pt:
    x: int
    y: int


pt0 = Pt(1, 2)  # noqa
pt1 = Pt(1, 'two')  # noqa
