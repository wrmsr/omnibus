import typing as ta

from .. import check
from .. import defs
from .. import lang
from .. import properties
from .types import Checker
from .types import Deriver
from .types import PostInit
from .types import Validator


T = ta.TypeVar('T', bound=ta.Callable, covariant=True)


DEFDECLS_ATR = '__dataclass_defdecls__'


class Defdecl(lang.Abstract):
    pass


class CallableDefdecl(Defdecl, ta.Generic[T], lang.Abstract):

    def __init__(self, fn: ta.Callable) -> None:
        super().__init__()
        self._fn = fn

    defs.repr('fn')

    @property
    def fn(self) -> ta.Callable:
        return self._fn

    @lang.cls_dct_fn()
    @classmethod
    def install(cls, cls_dct, *args, **kwargs) -> None:
        cls_dct.setdefault(DEFDECLS_ATR, []).append(cls(*args, **kwargs))


class CheckerDefdcel(CallableDefdecl, lang.Final):
    pass


class DeriverDefdecl(CallableDefdecl, lang.Final):
    pass


class PostInitDefdecl(CallableDefdecl, lang.Final):
    pass


class ValidatorDefdecl(CallableDefdecl, lang.Final):
    pass


class ClsDefdecls:

    def __init__(self, cls: type) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._cache = {}

    defs.repr('cls')

    @property
    def cls(self) -> type:
        return self._cls

    @properties.cached
    def all(self) -> ta.Sequence[Defdecl]:
        return [
            dd
            for bc in reversed(self._cls.__mro__)
            if DEFDECLS_ATR in bc.__dict__
            for dd in bc.__dict__[DEFDECLS_ATR]
        ]

    def __len__(self) -> int:
        return len(self.all)

    def __iter__(self) -> ta.Iterable[Defdecl]:
        return iter(self.all)

    def __getitem__(self, ddcls: type) -> ta.Sequence[Defdecl]:
        try:
            return self._cache[ddcls]
        except KeyError:
            ret = []
            for dd in self.all:
                if isinstance(dd, ddcls):
                    ret.append(dd)
            self._cache[ddcls] = ret
            return ret
