import pickle as pickle_
import struct as struct_
import typing as ta

from .. import defs
from .. import lang
from .registries import EXTENSION_REGISTRY
from .registries import MIME_TYPE_REGISTRY
from .types import Codec


F = ta.TypeVar('F')
T = ta.TypeVar('T')


class StructCodec(Codec[F, bytes], lang.Final):

    def __init__(self, fmt: str) -> None:
        super().__init__()

        self._fmt = fmt

    defs.repr()

    def encode(self, o: F) -> bytes:
        return struct_.pack(self._fmt, *o)

    def decode(self, o: bytes) -> F:
        return struct_.unpack(self._fmt, o)


struct = StructCodec


@EXTENSION_REGISTRY.registering('pickle')
@MIME_TYPE_REGISTRY.registering('application/python-pickle')
class PickleCodec(Codec[F, bytes], lang.Final):

    def __init__(self, protocol=None, *, fix_imports=True) -> None:
        super().__init__()

        self._protocol = protocol
        self._fix_imports = fix_imports

    defs.repr()

    def encode(self, o: F) -> bytes:
        return pickle_.dumps(o, self._protocol, fix_imports=self._fix_imports)

    def decode(self, o: bytes) -> F:
        return pickle_.loads(o)


pickle = PickleCodec


@EXTENSION_REGISTRY.registering('yaml', 'yml')
@MIME_TYPE_REGISTRY.registering(
    'application/x-yaml',
    'text/x-yaml',
    'text/yaml',
)
class YamlCodec(Codec[F, str], lang.Final):
    _MODULE = lang.lazy_import('yaml')

    def __init__(self) -> None:
        super().__init__()

    defs.repr()

    def encode(self, o: F) -> str:
        return self._MODULE().dump(o)

    def decode(self, o: str) -> F:
        mod = self._MODULE()
        return mod.load(o, Loader=mod.FullLoader)


yaml = YamlCodec
