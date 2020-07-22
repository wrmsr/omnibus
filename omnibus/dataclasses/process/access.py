import dataclasses as dc

from ... import code
from ... import properties
from ..internals import frozen_get_del_attr
from ..internals import PARAMS
from ..types import ExtraFieldParams
from .types import Aspect
from .types import attach


# class Descriptor:
#
#     def __init__(
#             self,
#             field: dc.Field,
#             *,
#             frozen: bool = None,
#             field_attrs: bool = False,
#     ) -> None:
#         super().__init__()
#
#         self._field = field
#         self._frozen = bool(frozen if frozen is not None else field.metadata.get(ExtraFieldParams, ExtraFieldParams()).frozen)  # noqa
#         self._field_attrs = field_attrs
#
#     def __get__(self, instance, owner=None):
#         if instance is not None:
#             dct = getattr(instance, self._dict_attr)
#             try:
#                 return dct[self._field.name]
#             except KeyError:
#                 raise AttributeError(self._field.name)
#         elif self._field_attrs is not None:
#             return self._field
#         else:
#             return self
#
#     def __set__(self, instance, value):
#         if self._frozen:
#             raise dc.FrozenInstanceError(f'cannot assign to field {self._field.name!r}')
#         getattr(instance, self._dict_attr)[self._field.name] = value
#
#     def __delete__(self, instance):
#         if self._frozen:
#             raise dc.FrozenInstanceError(f'cannot delete field {self._field.name!r}')
#         del getattr(instance, self._dict_attr)[self._field.name]


class Access(Aspect):

    def check(self) -> None:
        self.check_frozen()

    def process(self) -> None:
        self.process_frozen()
        self.process_field_attrs()

    @attach(Aspect.Function)
    class Function(Aspect.Function['Access']):

        @properties.cached
        def setattr_name(self) -> str:
            return self.fctx.nsb.put(object.__setattr__, '__setattr__')

        def build_setattr(self, name: str, value: str) -> str:
            if self.fctx.ctx.params.frozen:
                return f'{self.setattr_name}({self.fctx.self_name}, {name!r}, {value})'
            else:
                return f'{self.fctx.self_name}.{name} = {value}'

    def check_frozen(self) -> None:
        dc_rmro = [b for b in self.ctx.spec.rmro[:-1] if dc.is_dataclass(b)]
        if dc_rmro:
            any_frozen_base = any(getattr(b, PARAMS).frozen for b in dc_rmro)
            if any_frozen_base:
                if not self.ctx.params.frozen:
                    raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
            elif self.ctx.params.frozen:
                raise TypeError('cannot inherit frozen dataclass from a non-frozen one')

    def process_frozen(self) -> None:
        if not self.ctx.params.frozen:
            return

        if self.ctx.extra_params.allow_setattr:
            locals = {
                'cls': self.ctx.cls,
                'FrozenInstanceError': dc.FrozenInstanceError,
                'fields': frozenset(self.ctx.spec.fields.by_name),
            }

            for fnname in ['__setattr__', '__delattr__']:
                args = ['name'] + (['value'] if fnname == '__setattr__' else [])
                fn = code.create_function(
                    fnname,
                    code.ArgSpec(['self'] + args),
                    '\n'.join([
                        f'if type(self) is cls and name in fields:',
                        f'    raise FrozenInstanceError(f"Cannot assign to field {{name!r}}")',
                        f'super(cls, self).{fnname}({", ".join(args)})',
                    ]),
                    locals=locals,
                    globals=self.ctx.spec.globals,
                )
                if self.ctx.set_new_attribute(fn.__name__, fn):
                    raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.ctx.cls.__name__}')

        else:
            for fn in frozen_get_del_attr(
                    self.ctx.cls,
                    self.ctx.spec.fields.instance,
                    self.ctx.spec.globals
            ):
                if self.ctx.set_new_attribute(fn.__name__, fn):
                    raise TypeError(f'Cannot overwrite attribute {fn.__name__} in class {self.ctx.cls.__name__}')

    def process_field_attrs(self) -> None:
        if not self.ctx.extra_params.field_attrs:
            return

        for f in self.ctx.spec.fields:
            setattr(self.ctx.cls, f.name, f)
