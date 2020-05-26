"""
TODO:
 - inner=False ** InnerMeta
 - EnumData - frozen+abstract (but not sealed by default, but can be) + confer={'frozen', 'final'}
 - PureData - frozen+final
"""
import abc
import dataclasses as dc
import typing as ta

from .. import check
from .. import lang
from .api import dataclass
from .types import MetaclassParams


T = ta.TypeVar('T')


def _meta_build(
        mcls,
        name,
        bases,
        namespace,
        metaclass_params,
        **kwargs
):
    namespace = dict(namespace)

    bases = tuple(b for b in bases if b is not Data)
    if metaclass_params.final and lang.Final not in bases:
        bases += (lang.Final,)
    if metaclass_params.sealed and lang.Sealed not in bases:
        bases += (lang.Sealed,)

    # FIXME: full control now, build exactly once
    cls = dataclass(lang.super_meta(super(_Meta, mcls), mcls, name, bases, namespace), **kwargs)
    flds = dc.fields(cls)

    rebuild = False

    check.isinstance(metaclass_params.slots, bool)
    if metaclass_params.slots and '__slots__' not in namespace:
        namespace['__slots__'] = tuple(f.name for f in flds)
        rebuild = True
    if '__slots__' not in namespace:
        for fld in dc.fields(cls):
            if fld.name not in namespace and fld.name in getattr(cls, '__abstractmethods__', []):
                namespace[fld.name] = dc.MISSING
                rebuild = True

    def _build_init():
        def __init__(self):
            raise NotImplementedError

        return __init__

    if metaclass_params.abstract and '__init__' not in cls.__abstractmethods__:
        kwargs['init'] = False
        namespace['__init__'] = abc.abstractmethod(_build_init())
        rebuild = True
    elif not metaclass_params.abstract and '__init__' in cls.__abstractmethods__:
        bases = (lang.new_type('$Dataclass', (Data,), {'__init__': _build_init()}, init=False),) + bases
        rebuild = True

    if rebuild:
        cls = dataclass(lang.super_meta(super(_Meta, mcls), mcls, name, bases, namespace), **kwargs)
    return cls


class _Meta(abc.ABCMeta):

    def __new__(
            mcls,
            name,
            bases,
            namespace,
            *,
            slots=False,
            abstract=False,
            final=False,
            sealed=False,
            **kwargs
    ):
        check.arg(not (abstract and final))

        metaclass_params = MetaclassParams(
            slots=slots,
            abstract=abstract,
            final=final,
            sealed=sealed,
        )

        return _meta_build(mcls, name, bases, namespace, metaclass_params, **kwargs)


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
