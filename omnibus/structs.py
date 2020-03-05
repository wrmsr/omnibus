"""
TODO:
- cython
- optional dep / interop: bitstrings
- translate packed to unpacked fmt and expand after
"""
import struct  # noqa
import typing as ta

from . import dataclasses as dc
from . import lang


lang.warn_unstable()


T = ta.TypeVar('T')
Value = ta.Union[bool, int, bytes, float]


def _build_glyph_dict(*objs: ta.Sequence[T]) -> ta.Mapping[str, T]:
    d = {}
    for o in objs:
        if o.glyph in objs:
            raise KeyError(o.glyph)
        d[o.glyph] = o
    return d


class Size(lang.AutoEnum):
    NATIVE = ...
    STANDARD = ...


class Alignment(lang.AutoEnum):
    NATIVE = ...
    NONE = ...


@dc.dataclass(frozen=True)
class Ordering:
    glyph: str
    name: str
    size: Size
    alignment: Alignment


ORDERINGS = _build_glyph_dict(
    Ordering('@', 'native', Size.NATIVE, Alignment.NATIVE),
    Ordering('=', 'native', Size.STANDARD, Alignment.NONE),
    Ordering('<', 'little-endian', Size.STANDARD, Alignment.NONE),
    Ordering('>', 'big-endian', Size.STANDARD, Alignment.NONE),
    Ordering('!', 'network', Size.STANDARD, Alignment.NONE),
)


class POINTER(lang.Marker):
    pass


class VARIABLE(lang.Marker):
    pass


@dc.dataclass(frozen=True)
class Format:
    glyph: str
    name: str
    type: ta.Type[Value]
    size: ta.Union[int, ta.Type[POINTER], ta.Type[VARIABLE]]
    unsigned: bool = None


FORMATS = _build_glyph_dict(
    Format('x', 'pad', type(None), 0),
    Format('c', 'char', bytes, 1),
    Format('b', 'signed char', int, 1),
    Format('B', 'unsigned char', int, 1, unsigned=True),
    Format('?', 'bool', bool, 1),
    Format('h', 'short', int, 2),
    Format('H', 'unsigned short', int, 2, unsigned=True),
    Format('i', 'int', int, 4),
    Format('I', 'unsigned int', int, 4, unsigned=True),
    Format('l', 'long', int, 4),
    Format('L', 'unsigned long', int, 4, unsigned=True),
    Format('q', 'long long', int, 8),
    Format('Q', 'unsigned long long', int, 8, unsigned=True),
    Format('n', 'ssize_t', int, POINTER),
    Format('N', 'size_t', int, POINTER),
    Format('e', 'float16', float, 2),
    Format('f', 'float', float, 4),
    Format('d', 'double', float, 8),
    Format('s', 'char[]', bytes, VARIABLE),
    Format('p', 'char[]', bytes, VARIABLE),
    Format('P', 'void *', int, POINTER),
)


@dc.dataclass(frozen=True)
class BitFormat(Format):
    pass


BIT_FORMATS = _build_glyph_dict(
    BitFormat('j', 'packed bytes', bytes, VARIABLE),
    BitFormat('t', 'packed int', int, VARIABLE),
    BitFormat('T', 'unsigned packed int', int, VARIABLE, unsigned=True),
    BitFormat('X', 'pad bits', int, VARIABLE),
    *FORMATS.values()
)


class bits(lang.Namespace):

    @staticmethod
    def pack(format: str, *values: ta.Any) -> bytes:
        raise NotImplementedError

    @staticmethod
    def pack_into(format: str, buffer: lang.BytesLike, offset: int, *values: Value) -> None:
        raise NotImplementedError

    @staticmethod
    def unpack(format: str, buffer: lang.BytesLike) -> ta.Tuple[Value]:
        raise NotImplementedError

    @staticmethod
    def unpack_from(format: str, buffer: lang.BytesLike, offset: int = 0) -> ta.Tuple[Value]:
        raise NotImplementedError

    @staticmethod
    def iter_unpack(format: str, buffer: lang.BytesLike) -> ta.Iterator[Value]:
        raise NotImplementedError

    @staticmethod
    def calcsize(format: str) -> int:
        raise NotImplementedError
