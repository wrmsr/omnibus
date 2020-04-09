"""
TODO:
 - class-level descriptor proto not optional / overridable, but instance level fully so
"""
import dataclasses as dc
import typing as ta

from ... import check
from ... import lang
from ... import properties
from ..internals import FieldType
from ..internals import get_field_type
from .context import BuildContext


class HasDefaultFactory(lang.Marker):
    pass


def field_assign(frozen, name, value, self_name):
    if frozen:
        return f'BUILTINS.object.__setattr__({self_name},{name!r},{value})'
    return f'{self_name}.{name}={value}'


def field_init(f, frozen, globals, self_name):
    default_name = f'_dflt_{f.name}'

    if f.default_factory is not dc.MISSING:
        globals[default_name] = f.default_factory
        if f.init:
            value = f'{default_name}() if {f.name} is _HAS_DEFAULT_FACTORY else {f.name}'
        else:
            value = f'{default_name}()'

    elif f.init:
        if f.default is not dc.MISSING:
            globals[default_name] = f.default
        value = f.name

    else:
        return None

    if get_field_type(f) is FieldType.INIT:
        return None

    return field_assign(frozen, f.name, value, self_name)


def init_param(f):
    if f.default is dc.MISSING and f.default_factory is dc.MISSING:
        default = ''
    elif f.default is not dc.MISSING:
        default = f'=_dflt_{f.name}'
    elif f.default_factory is not dc.MISSING:
        default = '=_HAS_DEFAULT_FACTORY'
    else:
        raise TypeError
    return f'{f.name}:_type_{f.name}{default}'


class Storage:

    def __init__(self, ctx: BuildContext) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @properties.cached
    def init_fields(self) -> ta.List[dc.Field]:
        return [f for f in self.ctx.spec.fields if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]

    def install_field_attrs(self) -> None:
        for f in self.ctx.spec.fields:
            setattr(self.ctx.cls, f.name, f)

    def build_init_lines(
            self,
            locals: ta.Dict[str, ta.Any],
            self_name: str,
    ) -> ta.List[str]:
        ret = []
        for f in self.init_fields:
            line = field_init(f, self.ctx.params.frozen, locals, self_name)
            # line is None means that this field doesn't require initialization (it's a pseudo-field).  Just skip it.
            if line:
                ret.append(line)
        return ret
