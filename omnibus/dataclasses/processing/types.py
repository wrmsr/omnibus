import typing as ta
import weakref

from ... import check
from ... import codegen
from ... import lang
from ... import properties
from ..internals import DataclassParams
from ..reflect import DataSpec
from ..reflect import get_cls_spec
from ..types import ExtraParams


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)
AspectT = ta.TypeVar('AspectT', bound='Aspect', covariant=True)


ATTACHMENTS = weakref.WeakKeyDictionary()


def attach(key):
    # FIXME: steal a better word from aop than 'attach'
    def inner(obj):
        ATTACHMENTS[obj] = key
        return obj
    return inner


class Context(ta.Generic[TypeT]):

    def __init__(
            self,
            cls: TypeT,
            params: DataclassParams,
            extra_params: ExtraParams,
            aspects: ta.Iterable['Aspect'],
    ) -> None:
        super().__init__()

        self._cls = check.isinstance(cls, type)
        self._params = check.isinstance(params, DataclassParams)
        self._extra_params = check.isinstance(extra_params, ExtraParams)
        self._aspects = tuple(aspects)
        for a in self._aspects:
            check.isinstance(a, Aspect)

    @property
    def cls(self) -> TypeT:
        return self._cls

    @property
    def params(self) -> DataclassParams:
        return self._params

    @property
    def extra_params(self) -> ExtraParams:
        return self._extra_params

    @property
    def aspects(self) -> ta.Sequence['Aspect']:
        return self._aspects

    def get_aspects(self, cls: ta.Type[T]) -> ta.Sequence[T]:
        return [a for a in self._aspects if isinstance(a, cls)]

    def get_aspect(self, cls: ta.Type[T]) -> T:
        return check.single(self.get_aspects(cls))

    @properties.cached
    def spec(self) -> DataSpec:
        return get_cls_spec(self._cls)

    def set_new_attribute(self, name: str, value: ta.Any) -> bool:
        if name in self.cls.__dict__:
            return True
        setattr(self.cls, name, value)
        return False

    class Function(ta.Generic[TypeT]):

        def __init__(
                self,
                ctx: 'Context[TypeT]',
                aspects: ta.Iterable['Aspect.Function'],
        ) -> None:
            super().__init__()

            self._ctx = check.isinstance(ctx, Context)
            self._aspects = tuple(aspects)
            for a in self._aspects:
                check.isinstance(a, Aspect.Function)

        @property
        def ctx(self) -> 'Context[TypeT]':
            return self._ctx

        @property
        def aspects(self) -> ta.Sequence['Aspect.Function']:
            return self._aspects

        def get_aspects(self, cls: ta.Type[T]) -> ta.Sequence[T]:
            return [a for a in self._aspects if isinstance(a, cls)]

        def get_aspect(self, cls: ta.Type[T]) -> T:
            return check.single(self.get_aspects(cls))

        @properties.cached
        def nsb(self) -> codegen.NamespaceBuilder:
            return codegen.NamespaceBuilder(codegen.name_generator(unavailable_names=self.ctx.spec.fields.by_name))

        @properties.cached
        def self_name(self) -> str:
            return self.nsb.put('self', None)


class Aspect(lang.Abstract):

    def __init__(self, ctx: Context[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, Context)

        self.check()

    @property
    def ctx(self) -> Context:
        return self._ctx

    def check(self) -> None:
        pass

    def process(self) -> None:
        pass

    class Function(ta.Generic[AspectT]):

        def __init__(self, aspect: AspectT, fctx: Context.Function) -> None:
            super().__init__()

            self._aspect = aspect
            self._fctx = check.isinstance(fctx, Context.Function)

        @property
        def aspect(self) -> AspectT:
            return self._aspect

        @property
        def fctx(self) -> Context.Function:
            return self._fctx


class InitPhase(lang.AutoEnum):
    PRE_SET_ATTRS = ...
    SET_ATTRS = ...
    POST_SET_ATTRS = ...
    POST_INIT = ...
