import typing as ta

from .. import check
from .. import defs
from .. import lang
from .. import properties
from .types import Checker
from .types import Deriver
from .types import METADATA_ATTR
from .types import PostInit
from .types import Validator


T = ta.TypeVar('T', bound=ta.Callable, covariant=True)
DefdeclT = ta.TypeVar('DefdeclT', bound='Defdecl', covariant=True)


class Defdecls(lang.Marker):
    pass


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
        cls_dct.setdefault(METADATA_ATTR, {}).setdefault(Defdecls, []).append(cls(*args, **kwargs))


class CheckerDefdcel(CallableDefdecl[Checker], lang.Final):
    pass


class DeriverDefdecl(CallableDefdecl[Deriver], lang.Final):
    pass


class PostInitDefdecl(CallableDefdecl[PostInit], lang.Final):
    pass


class ValidatorDefdecl(CallableDefdecl[Validator], lang.Final):
    pass


check_ = CheckerDefdcel.install
derive = DeriverDefdecl.install
post_init = PostInitDefdecl.install
validate = ValidatorDefdecl.install


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
            if METADATA_ATTR in bc.__dict__
            for dd in bc.__dict__[METADATA_ATTR].get(Defdecls, [])
        ]

    def __len__(self) -> int:
        return len(self.all)

    def __iter__(self) -> ta.Iterable[Defdecl]:
        return iter(self.all)

    def __getitem__(self, ddcls: ta.Type[DefdeclT]) -> ta.Sequence[DefdeclT]:
        try:
            return self._cache[ddcls]
        except KeyError:
            ret = []
            for dd in self.all:
                if isinstance(dd, ddcls):
                    ret.append(dd)
            self._cache[ddcls] = ret
            return ret
