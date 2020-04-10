import dataclasses as dc
import typing as ta

from ... import check
from ... import collections as ocol
from ... import properties
from ..internals import create_fn
from ..internals import FieldType
from ..internals import get_field_type
from ..internals import POST_INIT_NAME
from ..types import Deriver
from ..types import ExtraFieldParams
from ..types import PostInit
from .context import FunctionBuildContext
from .storage import Storage
from .utils import get_flat_fn_args
from .validation import Validation

T = ta.TypeVar('T')
TypeT = ta.TypeVar('TypeT', bound=type, covariant=True)


class InitBuilder:

    def __init__(
            self,
            fctx: FunctionBuildContext,
            storage_builder: Storage.InitBuilder,
            validation_builder: Validation.InitBuilder,
    ) -> None:
        super().__init__()

        self._fctx = check.isinstance(fctx, FunctionBuildContext)
        self._storage_builder = check.isinstance(storage_builder, Storage.InitBuilder)
        self._validation_builder = check.isinstance(validation_builder, Validation.InitBuilder)

        self.check_invariants()

    @property
    def fctx(self) -> FunctionBuildContext:
        return self._fctx

    @property
    def storage_builder(self) -> Storage.InitBuilder:
        return self._storage_builder

    @property
    def validation_builder(self) -> Validation.InitBuilder:
        return self._validation_builder

    @properties.cached
    def init_fields(self) -> ta.List[dc.Field]:
        return [f for f in self.fctx.ctx.spec.fields if get_field_type(f) in (FieldType.INSTANCE, FieldType.INIT)]

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
            f.name: self.fctx.nsb.put(f'_{f.name}_type', f.type)
            for f in self.init_fields
            if f.type is not dc.MISSING
        }

    @properties.cached
    def default_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self.fctx.nsb.put(f'_{f.name}_default', f.default)
            for f in self.init_fields
            if f.default is not dc.MISSING
        }

    @properties.cached
    def default_factory_names_by_field_name(self) -> ta.Mapping[str, str]:
        return {
            f.name: self.fctx.nsb.put(f'_{f.name}_default_factory', f.default_factory)
            for f in self.init_fields
            if f.default_factory is not dc.MISSING
        }

    @properties.cached
    def has_default_factory_name(self) -> str:
        return self.fctx.nsb.put('_has_default_factory')

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
        return self.storage_builder.build_field_init_lines(dct, self.fctx.self_name)

    def build_post_init_lines(self) -> ta.List[str]:
        ret = []
        if hasattr(self.fctx.ctx.cls, POST_INIT_NAME):
            params_str = ','.join(f.name for f in self.init_fields if get_field_type(f) is FieldType.INIT)
            ret.append(f'{self.fctx.self_name}.{POST_INIT_NAME}({params_str})')
        return ret

    def build_extra_post_init_lines(self) -> ta.List[str]:
        ret = []
        for pi in self.fctx.ctx.spec.rmro_extras_by_cls[PostInit]:
            ret.append(f'{self.fctx.nsb.put(pi.fn)}({self.fctx.self_name})')
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

    class DeriverNode(ta.NamedTuple):
        fn: ta.Callable
        ias: ta.FrozenSet[str]
        oas: ta.FrozenSet[str]

    @properties.cached
    def deriver_nodes(self) -> ta.Sequence[DeriverNode]:
        nodes: ta.List[InitBuilder.DeriverNode] = []

        field_derivers_by_field = {
            f: efp.derive
            for f in self.fctx.ctx.spec.fields
            if ExtraFieldParams in f.metadata
            for efp in [f.metadata[ExtraFieldParams]]
            if efp.derive is not None
        }
        for f, fd in field_derivers_by_field.items():
            ias = get_flat_fn_args(fd)
            for ia in ias:
                check.in_(ia, self.fctx.ctx.spec.fields)
            nodes.append(self.DeriverNode(fd, frozenset(ias), frozenset([f.name])))

        extra_derivers = self.fctx.ctx.spec.rmro_extras_by_cls[Deriver]
        for ed in extra_derivers:
            ias = get_flat_fn_args(ed.fn)
            for ia in ias:
                check.in_(ia, self.fctx.ctx.spec.fields)
            if isinstance(ed.attrs, str):
                oas = [ed.attrs]
            elif isinstance(ed.attrs, ta.Iterable):
                oas = ed.attrs
            else:
                raise TypeError(ed)
            for oa in oas:
                check.isinstance(oa, str)
                check.in_(oa, self.fctx.ctx.spec.fields)
            nodes.append(self.DeriverNode(ed.fn, frozenset(ias), frozenset(oas)))

        return tuple(nodes)

    def __call__(self) -> None:
        # TODO: ** hijack default factory machinery **
        if self.deriver_nodes:
            print(self.deriver_nodes)

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
            [self.fctx.self_name] + [self.build_init_param(f) for f in self.init_fields if f.init],
            lines,
            locals=dict(self.fctx.nsb),
            globals=self.fctx.ctx.spec.globals,
            return_type=None,
        )
