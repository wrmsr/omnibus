"""
TODO:
 - inner=False ** InnerMeta
 - EnumData - frozen+abstract (but not sealed by default, but can be) + bequeath={'frozen', 'final'}
 - PureData - frozen+final
"""
import abc
import dataclasses as dc
import typing as ta

from .. import check
from .. import lang
from .api import dataclass
from .pickling import SimplePickle
from .types import MetaParams


T = ta.TypeVar('T')


# def _compose_fields(cls: ta.Type) -> ta.Dict[str, dc.Field]:
#     fields = {}
#     for b in cls.__mro__[-1:0:-1]:
#         base_fields = getattr(b, FIELDS, None)
#         if base_fields:
#             for f in base_fields.values():
#                 fields[f.name] = f
#     cls_annotations = cls.__dict__.get('__annotations__', {})
#     cls_fields = [get_field(cls, name, type) for name, type in cls_annotations.items()]
#     for f in cls_fields:
#         fields[f.name] = f
#     return fields


# def _has_default(fld: dc.Field) -> bool:
#     return fld.default is not dc.MISSING or fld.default_factory is not dc.MISSING


# def _check_bases(mro: ta.Sequence[ta.Type], *, frozen=False) -> None:
#     any_frozen_base = False
#     has_dataclass_bases = False
#     for b in mro[-1:0:-1]:
#         base_fields = getattr(b, FIELDS, None)
#         if base_fields:
#             has_dataclass_bases = True
#             if getattr(b, PARAMS).frozen:
#                 any_frozen_base = True
#     if has_dataclass_bases:
#         if any_frozen_base and not frozen:
#             raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
#         if not any_frozen_base and frozen:
#             raise TypeError('cannot inherit frozen dataclass from a non-frozen one')


# def _do_reorder(cls, params):
#     flds = _compose_fields(cls)
#     new_flds = {k: v for d in [False, True] for k, v in flds.items() if _has_default(v) == d}
#     if list(flds.keys()) != list(new_flds.keys()):
#         _check_bases(cls.__mro__, frozen=params.frozen)
#         anns = {name: fld.type for name, fld in new_flds.items()}
#         ns = {'__annotations__': anns, METADATA_ATTR: {OriginMetadata: cls}, **new_flds}
#         new_dc = dc.dataclass(type('_Reordered', (object,), ns))  #, **fwd_kwargs)
#         ret = post_process(cls, type(cls.__name__, (new_dc, cls), {}))  # , **post_process_kwargs)
#         ret.__module__ = cls.__module__
#         return ret


# class OriginMetadata(lang.Marker):
#     pass


def _meta_build(
        mcls,
        name,
        bases,
        namespace,
        meta_params,
        **kwargs
):
    namespace = dict(namespace)

    bases = tuple(b for b in bases if b is not Data)
    if meta_params.final and lang.Final not in bases:
        bases += (lang.Final,)
    if meta_params.sealed and lang.Sealed not in bases:
        bases += (lang.Sealed,)

    # FIXME: full control now, build exactly once
    cls = dataclass(lang.super_meta(super(_Meta, mcls), mcls, name, bases, namespace), **kwargs)
    flds = dc.fields(cls)

    rebuild = False

    check.isinstance(meta_params.slots, bool)
    if meta_params.slots and '__slots__' not in namespace:
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

    if meta_params.abstract and '__init__' not in cls.__abstractmethods__:
        kwargs['init'] = False
        namespace['__init__'] = abc.abstractmethod(_build_init())
        rebuild = True
    elif not meta_params.abstract and '__init__' in cls.__abstractmethods__:
        bases = (lang.new_type('$Dataclass', (Data,), {'__init__': _build_init()}, init=False),) + bases
        rebuild = True

    if meta_params.pickle and cls.__reduce__ is object.__reduce__:
        namespace['__reduce__'] = SimplePickle.__reduce__
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
            pickle=False,
            reorder=False,
            **kwargs
    ):
        check.arg(not (abstract and final))

        meta_params = MetaParams(
            slots=slots,
            abstract=abstract,
            final=final,
            sealed=sealed,
            pickle=pickle,
            reorder=reorder,
        )

        return _meta_build(mcls, name, bases, namespace, meta_params, **kwargs)


class Data(metaclass=_Meta):

    def __post_init__(self, *args, **kwargs) -> None:
        try:
            spi = super().__post_init__
        except AttributeError:
            if args or kwargs:
                raise TypeError(args, kwargs)
        else:
            spi(*args, **kwargs)
