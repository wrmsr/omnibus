import dataclasses as dc
import functools
import inspect
import typing as ta

from .. import check
from .. import codegen
from .. import collections as ocol
from .. import properties
from .context import BuildContext
from .defdecls import CheckerDefdcel
from .defdecls import PostInitDefdecl
from .defdecls import ValidatorDefdecl
from .fields import Fields
from .internals import create_fn
from .internals import field_init
from .internals import FieldType
from .internals import get_field_type
from .internals import HAS_DEFAULT_FACTORY
from .internals import init_param
from .internals import POST_INIT_NAME
from .types import CheckException
from .types import ValidateMetadata


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
        return '__dataclass_self__' if 'self' in self.fields else 'self'

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
        def _type_validator(fld: dc.Field):
            from .validation import build_default_field_validation
            return build_default_field_validation(fld)

        ret = []
        for fld in self.fields:
            vld_md = fld.metadata.get(ValidateMetadata)
            if callable(vld_md):
                ret.append(f'{self.nsb.put(vld_md)}({fld.name})')
            elif vld_md is True or (vld_md is None and self.ctx.extra_params.validate is True):
                ret.append(f'{self.nsb.put(_type_validator(fld))}({fld.name})')
            elif vld_md is False or vld_md is None:
                pass
            else:
                raise TypeError(vld_md)
        return ret

    def build_validator_lines(self) -> ta.List[str]:
        ret = []
        for vld in self.ctx.defdecls[ValidatorDefdecl]:
            vld_args = self.get_flat_fn_args(vld.fn)
            for arg in vld_args:
                check.in_(arg, self.fields)
            ret.append(f'{self.nsb.put(vld.fn)}({", ".join(vld_args)})')
        return ret

    def build_check_lines(self) -> ta.List[str]:
        ret = []

        for chk in self.ctx.defdecls[CheckerDefdcel]:
            chk_args = self.get_flat_fn_args(chk.fn)
            for arg in chk_args:
                check.in_(arg, self.fields)

            def build_chk_exc(chk, chk_args, *args):
                if len(chk_args) != len(args):
                    raise TypeError(chk_args, args)
                raise CheckException({k: v for k, v in zip(chk_args, args)}, chk)

            bound_build_chk_exc = functools.partial(build_chk_exc, chk, chk_args)

            ret.append(
                f'if not {self.nsb.put(chk.fn)}({", ".join(chk_args)}): '
                f'raise {self.nsb.put(bound_build_chk_exc)}({", ".join(chk_args)})'
            )

        return ret

    def build_field_init_lines(self, locals: ta.Dict[str, ta.Any]) -> ta.List[str]:
        ret = []
        for f in self.init_fields:
            line = field_init(f, self.ctx.params.frozen, locals, self.self_name)
            # line is None means that this field doesn't require initialization (it's a pseudo-field).  Just skip it.
            if line:
                ret.append(line)
        return ret

    def build_post_init_lines(self) -> ta.List[str]:
        ret = []
        if hasattr(self.ctx.cls, POST_INIT_NAME):
            params_str = ','.join(f.name for f in self.init_fields if get_field_type(f) is FieldType.INIT)
            ret.append(f'{self.self_name}.{POST_INIT_NAME}({params_str})')
        return ret

    def build_extra_post_init_lines(self) -> ta.List[str]:
        ret = []
        for pi in self.ctx.defdecls[PostInitDefdecl]:
            ret.append(f'{self.nsb.put(pi.fn)}({self.self_name})')
        return ret

    def __call__(self) -> None:
        locals = {f'_type_{f.name}': f.type for f in self.init_fields}
        locals.update({
            'MISSING': dc.MISSING,
            '_HAS_DEFAULT_FACTORY': HAS_DEFAULT_FACTORY,
        })

        lines = []
        lines.extend(self.build_validate_lines())
        lines.extend(self.build_validator_lines())
        lines.extend(self.build_check_lines())
        lines.extend(self.build_field_init_lines(locals))
        lines.extend(self.build_post_init_lines())
        lines.extend(self.build_extra_post_init_lines())

        ocol.guarded_map_update(locals, self.nsb)

        if not lines:
            lines = ['pass']

        return create_fn(
            '__init__',
            [self.self_name] + [init_param(f) for f in self.init_fields if f.init],
            lines,
            locals=locals,
            globals=self.ctx.globals,
            return_type=None,
        )
