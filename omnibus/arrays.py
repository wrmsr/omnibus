import typing as ta

from . import dataclasses as dc


T = ta.TypeVar('T')
Value = ta.Union[int, float, str]


def _build_glyph_dict(*objs: 'TypeCode') -> ta.Mapping[str, 'TypeCode']:
    d = {}
    for o in objs:
        if o.glyph in objs:
            raise KeyError(o.glyph)
        d[o.glyph] = o
    return d


class TypeCode(dc.Pure):
    glyph: str
    name: str
    type: ta.Type[Value]
    min_size: int
    unsigned: bool = None
    obsolete: bool = False


TYPE_CODES = _build_glyph_dict(
    TypeCode('b', 'signed char', int, 1),
    TypeCode('B', 'unsigned char', int, 1, unsigned=True),
    TypeCode('u', 'Py_UNICODE', str, 2, obsolete=True),
    TypeCode('h', 'signed short', int, 2),
    TypeCode('H', 'unsigned short', int, 2, unsigned=True),
    TypeCode('i', 'signed int', int, 2),
    TypeCode('I', 'unsigned int', int, 2, unsigned=True),
    TypeCode('l', 'signed long', int, 4),
    TypeCode('L', 'unsigned long', int, 4, unsigned=True),
    TypeCode('q', 'signed long long', int, 8),
    TypeCode('Q', 'unsigned long long', int, 8, unsigned=True),
    TypeCode('f', 'float', float, 4),
    TypeCode('d', 'double', float, 8),
)
