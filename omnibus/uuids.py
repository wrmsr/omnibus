"""
TODO:
 - cython
 - fastuuid
"""
import typing as ta
import uuid


ZERO = uuid.UUID('00000000-0000-0000-0000-000000000000')


DASH_SLICES = [
    slice(0, 8),
    slice(8, 12),
    slice(12, 16),
    slice(16, 20),
    slice(20, 32),
]


def int_to_uuid_str(i: int) -> str:
    s = '%032x' % (i,)
    return '-'.join(s[sl] for sl in DASH_SLICES)


def int_to_uuid(i: int) -> uuid.UUID:
    return uuid.UUID(int_to_uuid_str(i))


def uuid_to_int(u: ta.Union[uuid.UUID, str]) -> int:
    return int(str(u).replace('-', ''), 16)
