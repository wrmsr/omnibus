"""
Responsibilities:
 - signature, typeanns
 - defaults, defaut_factories, derivers
 - coercions
 - validations
 - field assignment
 - post-inits
"""
import dataclasses as dc
import typing as ta

from ... import check
from ... import properties
from ..internals import create_fn
from ..internals import FieldType
from ..internals import get_field_type
from ..internals import POST_INIT_NAME
from ..types import PostInit
from .context import FunctionBuildContext
from .defaulting import Defaulting
from .storage import Storage
from .validation import Validation


T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class InitBuilder:

    def __init__(
            self,
            fctx: FunctionBuildContext,
            defaulting_builder: Defaulting.InitBuilder,
            storage_builder: Storage.InitBuilder,
            validation_builder: Validation.InitBuilder,
    ) -> None:
        super().__init__()

        self._fctx = check.isinstance(fctx, FunctionBuildContext)
        self._defaulting_builder = check.isinstance(defaulting_builder, Defaulting.InitBuilder)
        self._storage_builder = check.isinstance(storage_builder, Storage.InitBuilder)
        self._validation_builder = check.isinstance(validation_builder, Validation.InitBuilder)

    @property
    def fctx(self) -> FunctionBuildContext:
        return self._fctx

    @property
    def defaulting_builder(self) -> Defaulting.InitBuilder:
        return self._defaulting_builder

    @property
    def storage_builder(self) -> Storage.InitBuilder:
        return self._storage_builder

    @property
    def validation_builder(self) -> Validation.InitBuilder:
        return self._validation_builder

    @properties.cached
    def type_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self.fctx.nsb.put(f'_{f.name}_type', f.type)
          for f in self.fctx.ctx.spec.fields.init
            if f.type is not dc.MISSING
       }

    def build_field_init_lines(self) -> ta.List[str]:
        dct = {}
        for f in self.fctx.ctx.spec.fields.init:
            if get_field_type(f) is FieldType.INIT:
                continue
            elif f.default_factory is not dc.MISSING:
                default_factory_name = self.default_factory_names_by_field_name[f.name]
                if f.init:
                    value = f'{default_factory_name}() if {f.name} is {self.has_factory_name} else {f.name}'
                else:
                    value = f'{default_factory_name}()'
            elif f.init:
                value = f.name
            else:
                continue
            dct[f.name] = value
        return self.storage_builder.build_field_init_lines(dct, self.fctx.self_name)

    def build_post_init_lines(self) -> ta.List[str]:
        ret = []
        if hasattr(self.fctx.ctx.cls, POST_INIT_NAME):
            params_str = ','.join(f.name for f in self.fctx.ctx.spec.fields.by_field_type.get(FieldType.INIT, []))
            ret.append(f'{self.fctx.self_name}.{POST_INIT_NAME}({params_str})')
        return ret

    def build_extra_post_init_lines(self) -> ta.List[str]:
        ret = []
        for pi in self.fctx.ctx.spec.rmro_extras_by_cls[PostInit]:
            ret.append(f'{self.fctx.nsb.add(pi.fn)}({self.fctx.self_name})')
        return ret

    def build_init_param(self, fld: dc.Field) -> str:
        if fld.default is dc.MISSING and fld.default_factory is dc.MISSING:
            default = ''
        elif fld.default is not dc.MISSING:
            default = ' = ' + self.default_names_by_field_name[fld.name]
        elif fld.default_factory is not dc.MISSING:
            default = ' = ' + self.has_factory_name
        else:
            raise TypeError
        return f'{fld.name}: {self.type_names_by_field_name[fld.name]}{default}'

    def __call__(self) -> None:
        lines = []
        lines.extend(self.validation_builder.build_pre_attr_lines())
        lines.extend(self.build_field_init_lines())
        lines.extend(self.validation_builder.build_post_attr_lines())
        lines.extend(self.build_post_init_lines())
        lines.extend(self.build_extra_post_init_lines())

        if not lines:
            lines = ['pass']

        return create_fn(
            '__init__',
            [self.fctx.self_name] + [self.build_init_param(f) for f in self.fctx.ctx.spec.fields.init if f.init],
            lines,
            locals=dict(self.fctx.nsb),
            globals=self.fctx.ctx.spec.globals,
            return_type=None,
        )
