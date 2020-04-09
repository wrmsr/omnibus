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


class Storage:

    def __init__(self, ctx: BuildContext, self_name: str) -> None:
        super().__init__()

        self._ctx = check.isinstance(ctx, BuildContext)
        self._self_name = self_name

    @property
    def ctx(self) -> BuildContext:
        return self._ctx

    @property
    def self_name(self) -> str:
        return self._self_name

    @properties.cached
    def init_fields(self) -> ta.List[dc.Field]:
        return [f for f in self.ctx.spec.fields if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]

    def install_field_attrs(self) -> None:
        for f in self.ctx.spec.fields:
            setattr(self.ctx.cls, f.name, f)

    def build_field_assign(self, name, value) -> str:
        if self.ctx.params.frozen:
            return f'BUILTINS.object.__setattr__({self.self_name}, {name!r}, {value})'

        return f'{self.self_name}.{name} = {value}'
