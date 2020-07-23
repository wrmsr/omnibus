import abc
import functools
import types
import typing as ta
import weakref

from ... import check
from ... import code
from ... import collections as ocol
from ... import lang
from ... import properties
from ..confer import confer_params
from ..internals import DataclassParams
from ..reflect import DataSpec
from ..reflect import get_cls_spec
from ..types import _Placeholder
from ..types import ExtraParams
from ..types import MetaclassParams


T = ta.TypeVar('T')
U = ta.TypeVar('U')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)
AspectT = ta.TypeVar('AspectT', bound='Aspect', covariant=True)


class AspectCollection(ta.Generic[T], lang.Abstract):

    def __init__(
            self,
            aspects: ta.Iterable[ta.Union[T, ta.Callable[..., T]]],
            aspect_cls: ta.Type[T],
    ) -> None:
        super().__init__()

        self._aspect_cls = aspect_cls
        self._aspects = [a if isinstance(a, aspect_cls) else a(self) for a in aspects]
        self._aspects.sort(key=lambda a: (type(a).__qualname__, id(a)))
        for a in self._aspects:
            check.isinstance(a, aspect_cls)

    @property
    def aspects(self) -> ta.Sequence[T]:
        return self._aspects

    @property
    def aspect_cls(self) -> ta.Type[T]:
        return self._aspect_cls

    def get_aspects(self, cls: ta.Type[U]) -> ta.Sequence[U]:
        return [a for a in self._aspects if isinstance(a, cls)]

    def get_aspect(self, cls: ta.Type[U]) -> U:
        return check.single(self.get_aspects(cls))


class Context(AspectCollection['Aspect'], ta.Generic[TypeT]):

    def __init__(
            self,
            cls: TypeT,
            params: DataclassParams,
            extra_params: ExtraParams,
            *,
            metaclass_params: ta.Optional[MetaclassParams] = None,
            aspects: ta.Optional[ta.Iterable[ta.Union['Aspect', ta.Callable[..., 'AspectT']]]] = None,
    ) -> None:
        self._original_params = check.isinstance(params, DataclassParams)
        self._original_extra_params = check.isinstance(extra_params, ExtraParams)
        self._original_metaclass_params = check.isinstance(metaclass_params, (MetaclassParams, type(None)))
        params, extra_params, metaclass_params = confer_params(cls.__bases__, params, extra_params, metaclass_params)

        if aspects is None:
            aspects = extra_params.aspects
            if aspects is None:
                from .driver import DEFAULT_ASPECTS
                aspects = DEFAULT_ASPECTS

        super().__init__(aspects, Aspect)

        self._cls = check.isinstance(cls, type)
        self._params = params
        self._extra_params = extra_params
        self._metaclass_params = metaclass_params

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
    def metaclass_params(self) -> ta.Optional[MetaclassParams]:
        return self._metaclass_params

    @property
    def original_params(self) -> DataclassParams:
        return self._original_params

    @property
    def original_extra_params(self) -> ExtraParams:
        return self._original_extra_params

    @property
    def original_metaclass_params(self) -> ta.Optional[MetaclassParams]:
        return self._original_metaclass_params

    @properties.cached
    @property
    def aspect_plan(self) -> ta.Sequence[ta.Sequence['Aspect']]:
        dct = {}
        for a in self.aspects:
            ds = set()
            for dc in a.deps:
                da = None
                for dac in self.aspects:
                    if isinstance(dac, dc):
                        if da is None:
                            da = dac
                        else:
                            raise Exception(f'Ambiguous dependency {dc} in aspect {a} resolved to {da} and {dac}')
                if da is None:
                    raise Exception(f'Unresolved dependency {dc} in aspect {a}')
                ds.add(da)
            dct[a] = ds
        lst = list(ocol.toposort(dct))
        return [sorted(al, key=lambda la: type(la).__name__) for al in lst]

    @properties.stateful_cached
    @property
    def spec(self) -> DataSpec:
        return get_cls_spec(self._cls)

    def set_new_attribute(self, name: str, value: ta.Any, *, raise_: bool = False) -> bool:
        if name in self.cls.__dict__:
            ev = self.cls.__dict__[name]
            if ev is not _Placeholder:
                if raise_:
                    raise TypeError(f'Cannot overwrite attribute {name}')
                return False
        setattr(self.cls, name, value)
        return True

    class Function(AspectCollection['Aspect.Function'], ta.Generic[TypeT]):

        def __init__(
                self,
                ctx: 'Context[TypeT]',
                aspects: ta.Iterable[ta.Union['Aspect.Function', ta.Callable[..., 'Aspect.Function']]],
        ) -> None:
            super().__init__(aspects, Aspect.Function)

            self._ctx = check.isinstance(ctx, Context)

        @property
        def ctx(self) -> 'Context[TypeT]':
            return self._ctx

        @properties.cached
        @property
        def nsb(self) -> code.NamespaceBuilder:
            return code.NamespaceBuilder(unavailable_names=self.ctx.spec.fields.by_name)

        @properties.cached
        def self_name(self) -> str:
            return self.nsb.put(None, 'self')

    def function(self, attachment_keys: ta.Iterable[ta.Any] = ()) -> Function[TypeT]:
        check.arg(not isinstance(attachment_keys, str))
        attachment_keys = list(attachment_keys)
        if Aspect.Function not in attachment_keys:
            attachment_keys.append(Aspect.Function)
        attachments = []
        seen = set()
        for aspect in self.aspects:
            for key in attachment_keys:
                for attachment in aspect.attachment_lists_by_key.get(key, []):
                    if attachment is None or attachment in seen:
                        continue
                    attachments.append(functools.partial(attachment, aspect))
                    seen.add(attachment)
        return Context.Function(self, attachments)


ATTACHMENTS = weakref.WeakKeyDictionary()


def attach(key):
    # FIXME: steal a better word from aop than 'attach'
    def inner(obj):
        ATTACHMENTS.setdefault(obj, []).append(key)
        return obj
    return inner


def get_keys_by_attachment_name(obj: ta.Any) -> ta.Mapping[ta.Any, ta.Any]:
    if isinstance(obj, type):
        rmro = reversed(obj.__mro__[1:])
    else:
        rmro = reversed(type(obj).__mro__)
    keys_by_name = {}
    for items in [list(c.__dict__.items()) for c in rmro] + [list(obj.__dict__.items())]:
        for n, v in items:
            try:
                ks = ATTACHMENTS[v]
            except (KeyError, TypeError):
                continue
            for k in ks:
                keys_by_name[n] = k
    return keys_by_name


def get_attachment_lists_by_key(obj: ta.Any) -> ta.Mapping[ta.Any, ta.Sequence[ta.Any]]:
    ret = {}
    for attachment_name, key in get_keys_by_attachment_name(obj).items():
        ret.setdefault(key, []).append(getattr(obj, attachment_name))
    return ret


class AttachmentCollection(lang.Abstract):

    @properties.cached
    def attachment_lists_by_key(self) -> ta.Mapping[ta.Any, ta.Sequence[ta.Any]]:
        return get_attachment_lists_by_key(self)


class Aspect(AttachmentCollection, lang.Abstract):

    def __init__(self, ctx: Context[TypeT]) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, Context)

    @property
    def ctx(self) -> Context:
        return self._ctx

    @abc.abstractproperty
    def deps(self) -> ta.Collection[ta.Type['Aspect']]:
        raise NotImplementedError

    @property
    def slots(self) -> ta.AbstractSet[str]:
        return frozenset()

    def check(self) -> None:
        pass

    def process(self) -> None:
        pass

    class Function(AttachmentCollection, lang.Abstract, ta.Generic[AspectT]):

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

        @property
        def argspec(self) -> code.ArgSpec:
            raise TypeError

        def build(self, name: str) -> types.FunctionType:
            lines = []

            for phase in InitPhase.__members__.values():
                for aspect in self.fctx.aspects:
                    for attachment in aspect.attachment_lists_by_key.get(phase, []):
                        lines.extend(attachment())

            if not lines:
                lines = ['pass']

            return code.create_function(
                name,
                self.argspec,
                '\n'.join(lines),
                locals=dict(self.fctx.nsb),
                globals=self.fctx.ctx.spec.globals,
            )

    @classmethod
    def nop(cls: ta.Type[AspectT]) -> ta.Type[AspectT]:
        ans = get_keys_by_attachment_name(cls)
        return type(
            cls.__qualname__ + '$nop',
            (cls,),
            {
                'check': lambda self: None,
                'process': lambda self: None,
                **{n: None for n in ans},
            },
        )


class InitPhase(lang.AutoEnum):
    BOOTSTRAP = ...
    DEFAULT = ...
    VALIDATE = ...
    SET_ATTRS = ...
    POST_SET_ATTRS = ...
    POST_INIT = ...
    RETURN = ...
