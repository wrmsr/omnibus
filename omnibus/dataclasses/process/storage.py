"""
TODO:
 - need to re-run checks/validators on all mutations
 - nesting
 - rebuilding from existing
  - stubbing (query comp cache)

Backends:
 - struct
  - w/ bitfield packing
 - arrays
  - numpy
  - mmap
 - configs
"""
import abc
import dataclasses as dc
import typing as ta

from . import bootstrap
from ... import check
from ... import code
from ... import lang
from ... import properties
from ..fields import Fields
from ..internals import FieldType
from ..internals import get_field_type
from ..internals import PARAMS
from ..types import ExtraFieldParams
from ..types import ExtraParams
from ..types import Mangling
from ..types import METADATA_ATTR
from .types import Aspect
from .types import attach
from .types import InitPhase


StorageT = ta.TypeVar('StorageT', bound='Storage', covariant=True)


class Storage(Aspect, lang.Abstract):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [bootstrap.Fields]

    def check(self) -> None:
        self.check_frozen()

    def process(self) -> None:
        self.process_mangling()
        self.process_frozen()
        self.process_descriptors()

    @staticmethod
    def build_mangling(
            fields: Fields,
            extra_params: ExtraParams,
    ) -> Mangling:
        dct = {}
        names = set(fields.by_name)
        for fld in fields:
            efp = fld.metadata.get(ExtraFieldParams)
            if efp is not None and efp.mangled is not None:
                mang = efp.mangled
            else:
                if extra_params.mangler is not None:
                    fn = extra_params.mangler
                else:
                    fn = lambda n: '_' + n
                mang = fn(fld.name)
            if mang in dct or mang in names:
                raise NameError(dct)
            dct[mang] = fld.name
        return ta.cast(Mangling, dct)

    def process_mangling(self) -> None:
        mangling = self.build_mangling(
            self.ctx.spec.fields,
            self.ctx.spec.extra_params,
        )

        metadata = self.ctx.cls.__dict__.get(METADATA_ATTR, {})
        if Mangling in metadata:
            raise KeyError(Mangling)
        metadata[Mangling] = mangling
        check.state(self.ctx.spec.mangling is mangling)
        check.state(self.ctx.spec.unmangling is not None)

    def check_frozen(self) -> None:
        dc_rmro = [b for b in self.ctx.spec.rmro[:-1] if dc.is_dataclass(b)]
        if dc_rmro:
            any_frozen_base = any(getattr(b, PARAMS).frozen for b in dc_rmro)
            if any_frozen_base:
                if not self.ctx.params.frozen:
                    raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            elif self.ctx.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    @abc.abstractmethod
    def process_frozen(self) -> None:
        raise NotImplementedError

    class Descriptor(lang.Abstract, ta.Generic[StorageT]):

        def __init__(self, field: dc.Field) -> None:
            super().__init__()

            self._field = check.isinstance(field, dc.Field)

        @abc.abstractmethod
        def __get__(self, instance, owner=None):
            raise NotImplementedError

        @abc.abstractmethod
        def __set__(self, instance, value):
            raise NotImplementedError

        @abc.abstractmethod
        def __delete__(self, instance):
            raise NotImplementedError

    @abc.abstractmethod
    def process_descriptors(self) -> None:
        raise NotImplementedError

    @attach(Aspect.Function)
    class Helper(Aspect.Function[StorageT]):

        @properties.cached
        def setattr_name(self) -> str:
            return self.fctx.nsb.put(object.__setattr__, '__setattr__')

        def build_set_field(self, fld: dc.Field, value: str) -> str:
            umd = self.fctx.ctx.spec.unmangling
            name = umd[fld.name] if umd is not None else fld.name
            return f'{self.setattr_name}({self.fctx.self_name}, {name!r}, {value})'

    @attach('init')
    class Init(Aspect.Function[StorageT]):

        @attach(InitPhase.SET_ATTRS)
        def build_set_attr_lines(self) -> ta.List[str]:
            ret = []
            for f in self.fctx.ctx.spec.fields.init:
                if get_field_type(f) is not FieldType.INSTANCE:
                    continue
                # FIXME:
                # if not f.init and f.default_factory is dc.MISSING:
                #     continue
                ret.append(self.fctx.get_aspect(self.aspect.Helper).build_set_field(f, f.name))
            return ret


class StandardStorage(Storage):

    def process_frozen(self) -> None:
        if not self.ctx.params.frozen:
            return

        if not self.ctx.extra_params.allow_setattr:
            locals = {
                'cls': self.ctx.cls,
                'FrozenInstanceError': dc.FrozenInstanceError,
                'allowed': frozenset(self.ctx.spec.fields.by_name) | frozenset(self.ctx.spec.mangling),
            }

            for fnname in ['__setattr__', '__delattr__']:
                args = ['name'] + (['value'] if fnname == '__setattr__' else [])
                fn = code.create_function(
                    fnname,
                    code.ArgSpec(['self'] + args),
                    '\n'.join([
                        f'if type(self) is cls and name in allowed:',
                        f'    raise FrozenInstanceError(f"Cannot overwrite attribute {{name!r}}")',
                        f'super(cls, self).{fnname}({", ".join(args)})',
                    ]),
                    locals=locals,
                    globals=self.ctx.spec.globals,
                )
                self.ctx.set_new_attribute(fn.__name__, fn)

    class Descriptor(Storage.Descriptor['StandardStorage']):

        def __init__(
                self,
                field: dc.Field,
                mangled: str,
                *,
                frozen: bool = None,
                field_attrs: bool = False,
        ) -> None:
            super().__init__(field)

            self._mangled = mangled
            self._frozen = bool(frozen if frozen is not None else field.metadata.get(ExtraFieldParams, ExtraFieldParams()).frozen)  # noqa
            self._field_attrs = field_attrs

        def __get__(self, instance, owner=None):
            if instance is not None:
                return getattr(instance, self._mangled)
            elif self._field_attrs:
                return self._field
            elif self._field.default is not dc.MISSING:
                return self._field.default
            else:
                raise AttributeError(self._field.name)

        def __set__(self, instance, value):
            if self._frozen:
                raise dc.FrozenInstanceError(f'cannot assign to field {self._field.name!r}')
            setattr(instance, self._mangled, value)

        def __delete__(self, instance):
            if self._frozen:
                raise dc.FrozenInstanceError(f'cannot delete field {self._field.name!r}')
            delattr(instance, self._mangled)

    def process_descriptors(self) -> None:
        for fld in self.ctx.spec.fields.instance:
            dsc = self.Descriptor(
                fld,
                self.ctx.spec.unmangling[fld.name],
                frozen=self.ctx.spec.params.frozen,
                field_attrs=self.ctx.spec.extra_params.field_attrs,
            )
            # FIXME: check not overwriting
            setattr(self.ctx.cls, fld.name, dsc)
