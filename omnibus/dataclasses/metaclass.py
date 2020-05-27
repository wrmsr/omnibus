"""
TODO:
 - inner=False ** InnerMeta
 - EnumData - frozen+abstract (but not sealed by default, but can be) + confer={'frozen', 'final'}
 - PureData - frozen+final
"""
import abc
import dataclasses as dc
import typing as ta

from . import process
from .. import check
from .. import lang
from .api import dataclass
from .api import MISSING_TYPE
from .confer import confer_params
from .types import DataclassParams
from .types import ExtraParams
from .types import MetaclassParams


T = ta.TypeVar('T')


def _build_stub_init():
    def __init__(self):
        raise NotImplementedError

    return __init__


class _Meta(abc.ABCMeta):

    def __new__(
            mcls,
            name,
            bases,
            namespace,
            *,

            slots: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            abstract: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            final: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            sealed: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False
            inner: ta.Union[bool, MISSING_TYPE] = dc.MISSING,  # False

            **kwargs
    ):
        if 'aspects' in kwargs:
            kwargs['aspects'] = list(kwargs['aspects'])
        if 'confer' in kwargs:
            kwargs['confer'] = set(kwargs['confer'])

        original_params = DataclassParams(**{
            a: kwargs.pop(a, dc.MISSING)
            for a in DataclassParams.__slots__
        })

        original_extra_params = ExtraParams(**{
            a: kwargs.pop(a)
            for fld in dc.fields(ExtraParams)
            for a in [fld.name]
            if a in kwargs
        })

        original_metaclass_params = MetaclassParams(
            slots=slots,
            abstract=abstract,
            final=final,
            sealed=sealed,
            inner=inner,
        )

        params, extra_params, metaclass_params = \
            confer_params(bases, original_params, original_extra_params, original_metaclass_params)

        check.arg(not (metaclass_params.abstract and metaclass_params.final))

        bases = tuple(b for b in bases if b is not Data)
        if metaclass_params.final and lang.Final not in bases:
            bases += (lang.Final,)
        if metaclass_params.sealed and lang.Sealed not in bases:
            bases += (lang.Sealed,)

        # FIXME: slots
        # fields = build_cls_fields()
        # check.isinstance(metaclass_params.slots, bool)
        # if metaclass_params.slots and '__slots__' not in namespace:
        #     namespace['__slots__'] = tuple(f.name for f in flds)
        #     rebuild = True
        # if '__slots__' not in namespace:
        #     for fld in dc.fields(cls):
        #         if fld.name not in namespace and fld.name in getattr(cls, '__abstractmethods__', []):
        #             namespace[fld.name] = dc.MISSING

        # FIXME: abstract
        # if metaclass_params.abstract and '__init__' not in cls.__abstractmethods__:
        #     kwargs['init'] = False
        #     namespace['__init__'] = abc.abstractmethod(_build_stub_init)
        # elif not metaclass_params.abstract and '__init__' in cls.__abstractmethods__:
        #     bases = (lang.new_type('$Dataclass', (Data,), {'__init__': _build_stub_init()}, init=False),) + bases

        # FIXME: inner

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


class PureData(Data):
    pass


class EnumData(Data):
    pass
