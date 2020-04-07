import abc
import dataclasses as dc
import typing as ta

from .. import check
from .. import lang
from .build import dataclass
from .pickling import SimplePickle


T = ta.TypeVar('T')


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
            **kwargs
    ):
        check.arg(not (abstract and final))
        namespace = dict(namespace)

        bases = tuple(b for b in bases if b is not Data)
        if final and lang.Final not in bases:
            bases += (lang.Final,)
        if sealed and lang.Sealed not in bases:
            bases += (lang.Sealed,)

        cls = dataclass(lang.super_meta(super(), mcls, name, bases, namespace), **kwargs)
        flds = dc.fields(cls)

        rebuild = False

        check.isinstance(slots, bool)
        if slots and '__slots__' not in namespace:
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

        if abstract and '__init__' not in cls.__abstractmethods__:
            kwargs['init'] = False
            namespace['__init__'] = abc.abstractmethod(_build_init())
            rebuild = True
        elif not abstract and '__init__' in cls.__abstractmethods__:
            bases = (lang.new_type('$Dataclass', (Data,), {'__init__': _build_init()}, init=False),) + bases
            rebuild = True

        if pickle and cls.__reduce__ is object.__reduce__:
            namespace['__reduce__'] = SimplePickle.__reduce__
            rebuild = True

        if rebuild:
            cls = dataclass(lang.super_meta(super(), mcls, name, bases, namespace), **kwargs)
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
