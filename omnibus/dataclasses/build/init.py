import dataclasses as dc
import functools
import inspect
import typing as ta

from ... import check
from ... import codegen
from ... import properties
from ..fields import Fields
from ..internals import create_fn
from ..internals import FieldType
from ..internals import get_field_type
from ..internals import POST_INIT_NAME
from ..types import Checker
from ..types import CheckException
from ..types import ExtraFieldParams
from ..types import PostInit
from ..types import SelfChecker
from ..types import SelfValidator
from ..types import Validator
from ..validation import build_default_field_validation
from .context import BuildContext
from .storage import Storage

T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class InitBuilder:

    def __init__(self, ctx: BuildContext, fields: Fields) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)
        self._fields = check.isinstance(fields, Fields)

        self._nsb = codegen.NamespaceBuilder(codegen.name_generator(unavailable_names=fields))

        self.check_invariants()

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @property
    def fields(self) -> Fields:
        return self._fields

    @property
    def nsb(self) -> codegen.NamespaceBuilder:
        return self._nsb

    @properties.cached
    def self_name(self) -> str:
        return self._nsb.put('self', None)

    @properties.cached
    def init_fields(self) -> ta.List[dc.Field]:
        return [f for f in self.fields if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]

    def check_invariants(self) -> None:
        # Make sure we don't have fields without defaults following fields with defaults.  This actually would be caught
        # when exec-ing the function source code, but catching it here gives a better error message, and future-proofs
        # us in case we build up the function using ast.
        seen_default = False
        for f in self.init_fields:
            # Only consider fields in the __init__ call.
            if f.init:
                if not (f.default is dc.MISSING and f.default_factory is dc.MISSING):
                    seen_default = True
                elif seen_default:
                    raise TypeError(f'non-default argument {f.name!r} follows default argument')

    @properties.cached
    def type_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self._nsb.put(f'_{f.name}_type', f.type)
            for f in self.init_fields
            if f.type is not dc.MISSING
        }

    @properties.cached
    def default_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self._nsb.put(f'_{f.name}_default', f.default)
            for f in self.init_fields
            if f.default is not dc.MISSING
        }

    @properties.cached
    def default_factory_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self._nsb.put(f'_{f.name}_default_factory', f.default_factory)
            for f in self.init_fields
            if f.default_factory is not dc.MISSING
        }

    @properties.cached
    def has_default_factory_name(self) -> str:
        return self._nsb.put('_has_default_factory')

    @staticmethod
    def get_flat_fn_args(fn) -> ta.List[str]:
        argspec = inspect.getfullargspec(fn)
        if (
                argspec.varargs or
                argspec.varkw or
                argspec.defaults or
                argspec.kwonlyargs or
                argspec.kwonlydefaults
        ):
            raise TypeError(fn)
        return list(argspec.args)

    def build_validate_lines(self) -> ta.List[str]:
        ret = []
        for fld in self.fields:
            vld_md = fld.metadata.get(ExtraFieldParams, ExtraFieldParams()).validate
            if callable(vld_md):
                ret.append(f'{self.nsb.put(vld_md)}({fld.name})')
            elif vld_md is True or (vld_md is None and self.ctx.extra_params.validate is True):
                ret.append(f'{self.nsb.put(build_default_field_validation(fld))}({fld.name})')
            elif vld_md is False or vld_md is None:
                pass
            else:
                raise TypeError(vld_md)
        return ret

    def build_validator_lines(self) -> ta.List[str]:
        ret = []

        for vld in self.ctx.spec.rmro_extras_by_cls[Validator]:
            vld_args = self.get_flat_fn_args(vld.fn)
            for arg in vld_args:
                check.in_(arg, self.fields)
            ret.append(f'{self.nsb.put(vld.fn)}({", ".join(vld_args)})')

        for self_vld in self.ctx.spec.rmro_extras_by_cls[SelfValidator]:
            ret.append(f'{self.nsb.put(self_vld.fn)}({self.self_name})')

        return ret

    def build_checker_lines(self) -> ta.List[str]:
        ret = []

        def build_chk_exc(chk, chk_args, *args):
            if len(chk_args) != len(args):
                raise TypeError(chk_args, args)
            raise CheckException({k: v for k, v in zip(chk_args, args)}, chk)

        for chk in self.ctx.spec.rmro_extras_by_cls[Checker]:
            chk_args = self.get_flat_fn_args(chk.fn)
            for arg in chk_args:
                check.in_(arg, self.fields)
            bound_build_chk_exc = functools.partial(build_chk_exc, chk, chk_args)
            ret.append(
                f'if not {self.nsb.put(chk.fn)}({", ".join(chk_args)}): '
                f'raise {self.nsb.put(bound_build_chk_exc)}({", ".join(chk_args)})'
            )

        for self_chk in self.ctx.spec.rmro_extras_by_cls[SelfChecker]:
            self_chk_arg = check.single(self.get_flat_fn_args(self_chk.fn))
            bound_build_chk_exc = functools.partial(build_chk_exc, self_chk, self_chk_arg)
            ret.append(
                f'if not {self.nsb.put(self_chk.fn)}({self.self_name}): '
                f'raise {self.nsb.put(bound_build_chk_exc)}([{self.self_name}])'
            )

        return ret

    def build_field_init_lines(self) -> ta.List[str]:
        dct = {}
        for f in self.init_fields:
            if get_field_type(f) is FieldType.INIT:
                continue
            elif f.default_factory is not dc.MISSING:
                default_factory_name = self.default_factory_names_by_field_name[f.name]
                if f.init:
                    value = f'{default_factory_name}() if {f.name} is {self.has_default_factory_name} else {f.name}'
                else:
                    value = f'{default_factory_name}()'
            elif f.init:
                value = f.name
            else:
                continue
            dct[f.name] = value
        storage = Storage(self.ctx)
        return storage.build_field_init_lines(dct, self.self_name)

    def build_post_init_lines(self) -> ta.List[str]:
        ret = []
        if hasattr(self.ctx.cls, POST_INIT_NAME):
            params_str = ','.join(f.name for f in self.init_fields if get_field_type(f) is FieldType.INIT)
            ret.append(f'{self.self_name}.{POST_INIT_NAME}({params_str})')
        return ret

    def build_extra_post_init_lines(self) -> ta.List[str]:
        ret = []
        for pi in self.ctx.spec.rmro_extras_by_cls[PostInit]:
            ret.append(f'{self.nsb.put(pi.fn)}({self.self_name})')
        return ret

    def build_init_param(self, fld: dc.Field) -> str:
        if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
            default = ''
        elif fld.default is not dc.MISSING:
            default = ' = ' + self.default_names_by_field_name[fld.name]
        elif fld.default_factory is not dc.MISSING:
            default = ' = ' + self.has_default_factory_name
        else:
            raise TypeError
        return f'{fld.name}: {self.type_names_by_field_name[fld.name]}{default}'

    def __call__(self) -> None:
        lines = []
        lines.extend(self.build_validate_lines())
        lines.extend(self.build_validator_lines())
        lines.extend(self.build_checker_lines())
        lines.extend(self.build_field_init_lines())
        lines.extend(self.build_post_init_lines())
        lines.extend(self.build_extra_post_init_lines())

        if not lines:
            lines = ['pass']

        return create_fn(
            '__init__',
            [self.self_name] + [self.build_init_param(f) for f in self.init_fields if f.init],
            lines,
            locals=dict(self.nsb),
            globals=self.ctx.spec.globals,
            return_type=None,
        )
