import collections.abc
import typing as ta

from .. import collections as ocol
from .. import defs
from .. import lang
from .. import properties
from .. import reflect
from .types import Checker
from .types import Deriver
from .types import METADATA_ATTR
from .types import PostInit
from .types import Validator


T = ta.TypeVar('T', bound=ta.Callable, covariant=True)
DefdeclT = ta.TypeVar('DefdeclT', bound='Defdecl', covariant=True)
ClsDefdecls = ocol.ItemListTypeMap['Defdecl']


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

    @properties.cached_class
    def target(cls) -> ta.Any:
        [b] = [b for b in reflect.get_spec(cls).bases if b.erased_cls is CallableDefdecl]
        [a] = b.args
        a.erased_cls is collections.abc.Callable
        breakpoint()

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


def get_cls_defdecls(cls: type) -> ClsDefdecls:
    return ocol.ItemListTypeMap([
        dd
        for bc in reversed(cls.__mro__)
        if METADATA_ATTR in bc.__dict__
        for dd in bc.__dict__[METADATA_ATTR].get(Defdecls, [])
    ])
