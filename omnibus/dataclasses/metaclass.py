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
from .api import MISSING_TYPE
from .confer import confer_params
from .fields import build_cls_fields
from .internals import DataclassParams
from .types import _Placeholder
from .types import Conferrer
from .types import ExtraParams
from .types import MetaclassParams
from .types import SUPER


T = ta.TypeVar('T')


class _Meta(abc.ABCMeta):

    def __new__(
            mcls,
            name,
            bases,
            namespace,
            *,

            slots: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            no_weakref: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            abstract: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            final: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            sealed: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False

            **kwargs
    ):
        if 'aspects' in kwargs:
            kwargs['aspects'] = list(kwargs['aspects'])
        if 'confer' in kwargs:
            kwargs['confer'] = dict(kwargs['confer']) \
                if isinstance(kwargs['confer'], ta.Mapping) else set(kwargs['confer'])

        original_params = DataclassParams(**{
            a: kwargs.pop(a, dc.MISSING)
            for a in DataclassParams.__slots__
        })

        original_extra_params = ExtraParams(**{
            a: kwargs.pop(a, dc.MISSING)
            for fld in dc.fields(ExtraParams)
            for a in [fld.name]
        })

        original_metaclass_params = MetaclassParams(
            slots=slots,
            no_weakref=no_weakref,
            abstract=abstract,
            final=final,
            sealed=sealed,
        )

        params, extra_params, metaclass_params = \
            confer_params(bases, original_params, original_extra_params, original_metaclass_params)

        check.arg(not (metaclass_params.abstract and metaclass_params.final))

        bases = tuple(b for b in bases if b is not Data)

        def clone_base(bcls):
            if bcls is object:
                return bcls
            try:
                return cloned_base_dct[bcls]
            except KeyError:
                ccls = cloned_base_dct[bcls] = abc.ABCMeta(
                    bcls.__name__,
                    tuple(clone_base(bbcls) for bbcls in bcls.__bases__),
                    {k: v for k, v in bcls.__dict__.items() if not k.startswith('__')},
                )
                return ccls

        cloned_base_dct = {}
        cloned_bases = tuple(clone_base(bcls) for bcls in bases)

        proto_cls = lang.super_meta(super(_Meta, mcls), mcls, name, cloned_bases, namespace)
        proto_abs = getattr(proto_cls, '__abstractmethods__', set()) - {'__forceabstract__'}
        proto_flds = build_cls_fields(proto_cls, reorder=extra_params.reorder)

        aspects = kwargs.get('aspects')
        if aspects is None:
            aspects = extra_params.aspects
            if aspects is None:
                from .process.driver import DEFAULT_ASPECTS
                aspects = DEFAULT_ASPECTS
        storage = check.single(
            a for a in aspects
            if isinstance(a, process.Storage) or (isinstance(a, type) and issubclass(a, process.Storage))
        )

        if metaclass_params.final and lang.Final not in bases:
            bases += (lang.Final,)
        if metaclass_params.sealed and lang.Sealed not in bases:
            bases += (lang.Sealed,)
        if metaclass_params.abstract and lang.Abstract not in bases:
            bases += (lang.Abstract,)

        if not metaclass_params.abstract:
            for a in set(proto_flds.by_name) & proto_abs:
                if a not in namespace:
                    namespace[a] = _Placeholder

        mangling = storage.build_mangling(proto_flds, extra_params)
        if metaclass_params.slots and '__slots__' not in namespace:
            slots = tuple(sorted(mangling))
            if not metaclass_params.no_weakref and '__weakref__' not in slots:
                slots += ('__weakref__',)
            namespace['__slots__'] = slots
        if '__slots__' not in namespace:
            for a in mangling:
                if a not in namespace and a in proto_abs:
                    namespace[a] = _Placeholder

        cls = lang.super_meta(super(_Meta, mcls), mcls, name, bases, namespace, **kwargs)
        ctx = process.Context(
            cls,
            original_params,
            original_extra_params,
            metaclass_params=original_metaclass_params,
        )
        drv = process.Driver(ctx)
        drv()
        return cls


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
    confer={
        'abstract': True,
        'frozen': True,
        'confer': {
            'final': Conferrer(_confer_enum_final),
            'repr': SUPER,
            'frozen': True,
            'reorder': SUPER,
            'allow_setattr': SUPER,
            'confer': SUPER,
        },
    },
):
    pass
