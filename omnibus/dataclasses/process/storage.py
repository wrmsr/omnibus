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
from ..internals import FieldType
from ..internals import get_field_type
from ..internals import PARAMS
from ..types import ExtraFieldParams
from ..types import Mangling
from ..types import METADATA_ATTR
from .descriptors import FieldDescriptor
from .types import Aspect
from .types import attach
from .types import InitPhase


StorageT = ta.TypeVar('StorageT', bound='Storage', covariant=True)


class Storage(Aspect, lang.Abstract):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [bootstrap.Fields]

    @property
    def slots(self) -> ta.AbstractSet[str]:
        return set(self.mangling)

    def check(self) -> None:
        self.check_frozen()

    def process(self) -> None:
        self.process_mangling()
        self.process_frozen()
        self.process_descriptors()

    @properties.cached
    def mangling(self) -> Mangling:
        dct = {}
        names = set(self.ctx.spec.fields.by_name)
        for fld in self.ctx.spec.fields:
            efp = fld.metadata.get(ExtraFieldParams)
            if efp is not None and efp.mangled is not None:
                mang = efp.mangled
            else:
                if self.ctx.spec.extra_params.mangler is not None:
                    fn = self.ctx.spec.extra_params.mangler
                else:
                    fn = lambda n: '_' + n
                mang = fn(fld.name)
            if mang in dct or mang in names:
                raise NameError(dct)
            dct[mang] = fld.name
        return ta.cast(Mangling, dct)

    def process_mangling(self) -> None:
        metadata = self.ctx.cls.__dict__.get(METADATA_ATTR, {})
        if Mangling in metadata:
            raise KeyError(Mangling)
        metadata[Mangling] = self.mangling
        check.state(self.ctx.spec.mangling is self.mangling)
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
                if not f.init and f.default_factory is dc.MISSING:
                    continue
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
                        f'    raise FrozenInstanceError(f"cannot assign to field {{name!r}}")',
                        f'super(cls, self).{fnname}({", ".join(args)})',
                    ]),
                    locals=locals,
                    globals=self.ctx.spec.globals,
                )
                self.ctx.set_new_attribute(fn.__name__, fn, raise_=True)

    def process_descriptors(self) -> None:
        # FIXME: should ClassVars should get field_attrs (instead of returning default)?
        for fld in self.ctx.spec.fields.instance:
            default = fld if self.ctx.spec.extra_params.field_attrs else \
                fld.default if fld.default is not dc.MISSING else dc.MISSING
            fefp = fld.metadata.get(ExtraFieldParams, ExtraFieldParams())
            frozen = bool(fefp.frozen if fefp.frozen is not None else self.ctx.spec.params.frozen)
            dsc = FieldDescriptor(
                self.ctx.spec.unmangling[fld.name],
                default_=default,
                frozen=frozen,
                name=fld.name,
            )
            # FIXME: check not overwriting
            setattr(self.ctx.cls, fld.name, dsc)
