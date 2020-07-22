import dataclasses as dc
import inspect
import typing as ta

from ... import check
from ... import properties
from ..fields import build_cls_fields
from ..internals import cmp_fn
from ..internals import DataclassParams
from ..internals import FieldType
from ..internals import hash_action
from ..internals import PARAMS
from ..internals import POST_INIT_NAME
from ..internals import repr_fn
from ..internals import tuple_str
from ..pickling import SimplePickle
from ..types import ExtraFieldParams
from ..types import ExtraParams
from ..types import MANGLING
from ..types import MetaclassParams
from ..types import METADATA_ATTR
from ..types import Original
from ..types import PostInit
from .types import Aspect
from .types import attach
from .types import InitPhase
from .types import Phase


class Params(Aspect):

    @property
    def phase(self) -> Phase:
        return Phase.BOOTSTRAP

    def process(self) -> None:
        self.ctx.set_new_attribute(PARAMS, self.ctx.params)
        check.state(self.ctx.spec.params is self.ctx.params)

        if METADATA_ATTR in self.ctx.cls.__dict__:
            md = getattr(self.ctx.cls, METADATA_ATTR)
        else:
            md = {}
            self.ctx.set_new_attribute(METADATA_ATTR, md)
        check.state(self.ctx.spec._metadata is md)

        md[ExtraParams] = self.ctx.extra_params
        md[MetaclassParams] = self.ctx.metaclass_params

        md[Original(DataclassParams)] = self.ctx.original_params
        md[Original(ExtraParams)] = self.ctx.original_extra_params
        md[Original(MetaclassParams)] = self.ctx.original_metaclass_params


class Fields(Aspect):

    @property
    def phase(self) -> Phase:
        return Phase.BOOTSTRAP

    def process(self) -> None:
        build_cls_fields(
            self.ctx.cls,
            reorder=self.ctx.extra_params.reorder,
            install=True,
        )


class Mangling(Aspect):

    @property
    def phase(self) -> Phase:
        return Phase.PREPARE

    def process(self) -> None:
        dct = {}
        names = set(self.ctx.spec.fields.by_name)
        for fld in self.ctx.spec.fields:
            efp = fld.metadata.get(ExtraFieldParams)
            if efp is not None and efp.mangled is not None:
                mang = efp.efp.mangled
            else:
                if self.ctx.extra_params.mangler is not None:
                    fn = self.ctx.extra_params.mangler
                else:
                    fn = lambda n: '_' + n
                mang = fn(fld.name)
            if mang in dct or mang in names:
                raise NameError(dct)
            dct[fld.name] = mang

        md = getattr(self.ctx.cls, METADATA_ATTR)
        md[MANGLING] = dct


class Repr(Aspect):

    def process(self) -> None:
        if not self.ctx.params.repr:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.repr]
        self.ctx.set_new_attribute('__repr__', repr_fn(flds, self.ctx.spec.globals))


class Eq(Aspect):

    def process(self) -> None:
        if not self.ctx.params.eq:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        self.ctx.set_new_attribute(
            '__eq__',
            cmp_fn(
                '__eq__',
                '==',
                self_tuple,
                other_tuple,
                globals=self.ctx.spec.globals,
            )
        )


class Order(Aspect):

    def check(self) -> None:
        if self.ctx.params.order and not self.ctx.params.eq:
            raise ValueError('eq must be true if order is true')

    def process(self) -> None:
        if not self.ctx.params.order:
            return

        flds = [f for f in self.ctx.spec.fields.instance if f.compare]
        self_tuple = tuple_str('self', flds)
        other_tuple = tuple_str('other', flds)
        for name, op in [
            ('__lt__', '<'),
            ('__le__', '<='),
            ('__gt__', '>'),
            ('__ge__', '>='),
        ]:
            if self.ctx.set_new_attribute(
                    name,
                    cmp_fn(
                        name,
                        op,
                        self_tuple,
                        other_tuple,
                        globals=self.ctx.spec.globals,
                    )
            ):
                raise TypeError(
                    f'Cannot overwrite attribute {name} in class {self.ctx.cls.__name__}. '
                    f'Consider using functools.total_ordering')


class Hash(Aspect):

    @properties.cached
    def cache_attr(self) -> str:
        return '__%s_%x_hash' % (self.ctx.cls.__name__, id(self.ctx.cls))

    def process(self) -> None:
        # Was this class defined with an explicit __hash__?  Note that if __eq__ is defined in this class, then python
        # will automatically set __hash__ to None.  This is a heuristic, as it's possible that such a __hash__ == None
        # was not auto-generated, but it close enough.
        class_hash = self.ctx.cls.__dict__.get('__hash__', dc.MISSING)
        has_explicit_hash = not (class_hash is dc.MISSING or (class_hash is None and '__eq__' in self.ctx.cls.__dict__))
        ha = hash_action[(
            bool(self.ctx.params.unsafe_hash),
            bool(self.ctx.params.eq),
            bool(self.ctx.params.frozen),
            has_explicit_hash,
        )]
        if not ha:
            return
        fn = ha(self.ctx.cls, self.ctx.spec.fields.instance, self.ctx.spec.globals)

        if self.ctx.spec.extra_params.cache_hash:
            attr = self.cache_attr
            self.ctx.set_new_attribute(attr, None)
            ofn = fn

            def fn(obj):
                hsh = getattr(obj, attr)
                if hsh is None:
                    hsh = ofn(obj)
                    object.__setattr__(obj, attr, hsh)
                return hsh

        self.ctx.cls.__hash__ = fn


class Doc(Aspect):

    @property
    def phase(self) -> Phase:
        return Phase.FINALIZE

    def process(self) -> None:
        if not getattr(self.ctx.cls, '__doc__'):
            sig = inspect.signature(self.ctx.cls)
            self.ctx.cls.__doc__ = self.ctx.cls.__name__ + str(sig).replace(' -> None', '')


class PostInitAspect(Aspect):

    @attach('init')
    class Init(Aspect.Function['PostInitAspect']):

        @attach(InitPhase.POST_INIT)
        def build_post_init_lines(self) -> ta.List[str]:
            if not self.fctx.ctx.spec.params.init:
                return []

            ret = []
            if hasattr(self.fctx.ctx.cls, POST_INIT_NAME):
                params_str = ','.join(f.name for f in self.fctx.ctx.spec.fields.by_field_type.get(FieldType.INIT, []))
                ret.append(f'{self.fctx.self_name}.{POST_INIT_NAME}({params_str})')
            return ret

        @attach(InitPhase.POST_INIT)
        def build_extra_post_init_lines(self) -> ta.List[str]:
            if not self.fctx.ctx.spec.params.init:
                return []

            ret = []
            for pi in self.fctx.ctx.spec.rmro_extras_by_cls[PostInit]:
                ret.append(f'{self.fctx.nsb.put(pi.fn)}({self.fctx.self_name})')
            return ret


class Pickle(Aspect):

    def process(self) -> None:
        if self.ctx.extra_params.pickle and self.ctx.cls.__reduce__ is object.__reduce__:
            setattr(self.ctx.cls, '__reduce__', SimplePickle.__reduce__)
