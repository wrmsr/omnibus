"""
TODO:
 - inner=False ** InnerMeta
"""
import abc
import dataclasses as dc
import typing as ta

from . import process
from .. import check
from .. import lang
from .. import properties
from .api import MISSING_TYPE
from .confer import confer_params
from .internals import DataclassParams
from .types import _Placeholder
from .types import Conferrer
from .types import ExtraParams
from .types import MetaclassParams
from .types import METADATA_ATTR
from .types import SUPER


T = ta.TypeVar('T')


IGNORED_ATTRS = frozenset(a for a in dir(type('_', (object,), {})) if a.startswith('__') and a.endswith('__'))


class _MetaBuilder:

    def __init__(
            self,
            mcls: '_Meta',
            name: str,
            bases: ta.Iterable[type],
            namespace: ta.Mapping[str, ta.Any],
            *,

            slots: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            no_weakref: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            abstract: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            final: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            sealed: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False

            **kwargs
    ) -> None:
        super().__init__()

        self._mcls = check.issubclass(mcls, _Meta)
        self._name = name

        self._orig_bases = list(bases)
        self._orig_namespace = dict(namespace)
        self._orig_kwargs = dict(kwargs)

        self._slots = slots
        self._no_weakref = no_weakref
        self._abstract = abstract
        self._final = final
        self._sealed = sealed

        kwargs = dict(self._orig_kwargs)
        if 'aspects' in kwargs:
            kwargs['aspects'] = list(kwargs['aspects'])
        if 'confer' in kwargs:
            kwargs['confer'] = dict(kwargs['confer']) \
                if isinstance(kwargs['confer'], ta.Mapping) else set(kwargs['confer'])

        self._orig_params = DataclassParams(**{
            a: kwargs.pop(a, dc.MISSING)
            for a in DataclassParams.__slots__
        })

        self._orig_extra_params = ExtraParams(**{
            a: kwargs.pop(a, dc.MISSING)
            for fld in dc.fields(ExtraParams)
            for a in [fld.name]
        })

        self._orig_metaclass_params = MetaclassParams(
            slots=self._slots,
            no_weakref=self._no_weakref,
            abstract=self._abstract,
            final=self._final,
            sealed=self._sealed,
        )

        params, extra_params, metaclass_params = \
            confer_params(self._orig_bases, self._orig_params, self._orig_extra_params, self._orig_metaclass_params)

        check.arg(not (metaclass_params.abstract and metaclass_params.final))

        self._kwargs = kwargs
        self._params = params
        self._extra_params = extra_params
        self._metaclass_params = metaclass_params

    @property
    def bases(self) -> ta.Sequence[type]:
        return [b for b in self._orig_bases if b is not Data]

    @property
    def new_bases(self) -> ta.Sequence[type]:
        bases = list(self.bases)
        if self._metaclass_params.final and lang.Final not in bases:
            bases.append(lang.Final)
        if self._metaclass_params.sealed and lang.Sealed not in bases:
            bases.append(lang.Sealed)
        if self._metaclass_params.abstract and lang.Abstract not in bases:
            bases.append(lang.Abstract)
        return bases

    @properties.cached
    def proto_cls(self) -> type:
        def clone_base(bcls):
            if bcls is object:
                return bcls
            try:
                return cloned_base_dct[bcls]
            except KeyError:
                ccls = cloned_base_dct[bcls] = abc.ABCMeta(
                    bcls.__name__,
                    tuple(clone_base(bbcls) for bbcls in bcls.__bases__),
                    {k: v for k, v in bcls.__dict__.items() if k not in IGNORED_ATTRS},
                )
                return ccls

        cloned_base_dct = {}
        cloned_bases = [clone_base(bcls) for bcls in self.bases]

        proto_ns = {**self._orig_namespace, METADATA_ATTR: dict(self._orig_namespace.get(METADATA_ATTR, {}))}
        return lang.super_meta(super(_Meta, self._mcls), self._mcls, self._name, tuple(cloned_bases), proto_ns)

    @properties.cached
    def proto_ctx(self) -> process.Context:
        proto_ctx = process.Context(
            self.proto_cls,
            self._params,
            self._extra_params,
            metaclass_params=self._orig_metaclass_params,
        )
        proto_drv = process.Driver(proto_ctx)
        proto_drv()
        return proto_ctx

    @properties.cached
    def proto_abs(self) -> ta.AbstractSet[str]:
        return getattr(self.proto_cls, '__abstractmethods__', set()) - {'__forceabstract__'}

    @properties.cached
    def namespace(self) -> ta.Mapping[str, ta.Any]:
        ns = dict(self._orig_namespace)

        if not self._metaclass_params.abstract:
            for a in set(self.proto_ctx.spec.fields.by_name) & self.proto_abs:
                if a not in ns:
                    ns[a] = _Placeholder

        slots = {s for a in self.proto_ctx.aspects for s in a.slots}
        if self._metaclass_params.slots and '__slots__' not in ns:
            ns['__slots__'] = tuple(sorted(slots))

        pha = (set(slots) & set(self.proto_abs)) - {'__weakref__'} - set(ns)
        ns.update({a: _Placeholder for a in pha})

        return ns

    def build(self) -> type:
        cls = lang.super_meta(
            super(_Meta, self._mcls),
            self._mcls,
            self._name,
            tuple(self.new_bases),
            self.namespace,
            **self._kwargs
        )
        ctx = process.Context(
            cls,
            self._orig_params,
            self._orig_extra_params,
            metaclass_params=self._orig_metaclass_params,
        )
        drv = process.Driver(ctx)
        drv()
        return cls


class _Meta(abc.ABCMeta):

    def __new__(
            mcls,
            name,
            bases,
            namespace,
            **kwargs
    ):
        bld = _MetaBuilder(mcls, name, bases, namespace, **kwargs)
        return bld.build()


class Data(metaclass=_Meta):

    def __post_init__(self, *args, **kwargs) -> None:
        try:
            spi = super().__post_init__
        except AttributeError:
            if args or kwargs:
                raise TypeError(args, kwargs)
        else:
            spi(*args, **kwargs)


class Frozen(
    Data,
    abstract=True,
    frozen=True,
    slots=True,
    no_weakref=True,
    confer={
        'frozen',
        'reorder',
        'allow_setattr',
        'confer',
    },
):
    pass


class Pure(
    Data,
    abstract=True,
    frozen=True,
    slots=True,
    no_weakref=True,
    confer={
        'final': True,
        'frozen': True,
    },
):
    pass


def _confer_enum_final(att, sub, sup):
    return sub['abstract'] is dc.MISSING or not sub['abstract']


class Enum(
    Data,
    abstract=True,
    frozen=True,
    slots=True,
    no_weakref=True,
    confer={
        'abstract': True,
        'frozen': True,
        'confer': {
            'final': Conferrer(_confer_enum_final),
            'repr': SUPER,
            'frozen': True,
            'reorder': SUPER,
            'allow_setattr': SUPER,
            'slots': SUPER,
            'aspects': SUPER,
            'confer': SUPER,
        },
    },
):
    pass
