import array
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


class TypeCode(dc.Frozen, allow_setattr=True):
    glyph: str
    name: str
    type: ta.Type[Value]
    min_size: int
    zero: ta.Any
    unsigned: ta.Optional[bool] = None
    obsolete: bool = False

    def __post_init__(self) -> None:
        self._size = array.array(self.glyph, [self.zero]).itemsize

    @property
    def size(self) -> int:
        return self._size


TYPE_CODES = _build_glyph_dict(
    TypeCode('b', 'signed char', int, 1, 0, unsigned=False),
    TypeCode('B', 'unsigned char', int, 1, 0, unsigned=True),
    TypeCode('u', 'Py_UNICODE', str, 2, '\0', obsolete=True),
    TypeCode('h', 'signed short', int, 0, 2, unsigned=False),
    TypeCode('H', 'unsigned short', int, 2, 0, unsigned=True),
    TypeCode('i', 'signed int', int, 0, 2, unsigned=False),
    TypeCode('I', 'unsigned int', int, 2, 0, unsigned=True),
    TypeCode('l', 'signed long', int, 0, 4, unsigned=False),
    TypeCode('L', 'unsigned long', int, 4, 0, unsigned=True),
    TypeCode('q', 'signed long long', int, 8, 0, unsigned=False),
    TypeCode('Q', 'unsigned long long', int, 8, 0, unsigned=True),
    TypeCode('f', 'float', float, 4, 0.),
    TypeCode('d', 'double', float, 8, 0.),
)


def _get_int_glyph(sz: int, unsigned: bool) -> str:
    for e in TYPE_CODES.values():
        if e.type is int and e.size == sz and e.unsigned == unsigned:
            return e.glyph
    raise ValueError


INT_SIZES = [1, 2, 4, 8]
INT_GLYPHS_BY_SIZE = {sz: _get_int_glyph(sz, False) for sz in INT_SIZES}
UINT_GLYPHS_BY_SIZE = {sz: _get_int_glyph(sz, True) for sz in INT_SIZES}
