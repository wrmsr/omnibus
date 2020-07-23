import typing as ta

from ... import check
from ..fields import build_cls_fields
from ..internals import DataclassParams
from ..internals import PARAMS
from ..types import ExtraParams
from ..types import MetaclassParams
from ..types import METADATA_ATTR
from ..types import Original
from .types import Aspect


class Params(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return []

    def process(self) -> None:
        self.ctx.set_new_attribute(PARAMS, self.ctx.params, raise_=True)
        check.state(self.ctx.spec.params is self.ctx.params)

        if METADATA_ATTR in self.ctx.cls.__dict__:
            md = getattr(self.ctx.cls, METADATA_ATTR)
        else:
            md = {}
            self.ctx.set_new_attribute(METADATA_ATTR, md, raise_=True)
        check.state(self.ctx.spec._metadata is md)

        md[ExtraParams] = self.ctx.extra_params
        md[MetaclassParams] = self.ctx.metaclass_params

        md[Original(DataclassParams)] = self.ctx.original_params
        md[Original(ExtraParams)] = self.ctx.original_extra_params
        md[Original(MetaclassParams)] = self.ctx.original_metaclass_params


class Fields(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Params]

    def process(self) -> None:
        build_cls_fields(
            self.ctx.cls,
            reorder=self.ctx.extra_params.reorder,
            install=True,
        )


class Slots(Aspect):

    @property
    def deps(self) -> ta.Collection[ta.Type[Aspect]]:
        return [Params]

    @property
    def slots(self) -> ta.AbstractSet[str]:
        return {'__weakref__'} if not self.ctx.spec.metaclass_params.no_weakref else set()

    def check(self) -> None:
        seen = set()
        for a in self.ctx.aspects:
            for s in a.slots:
                if s in seen:
                    raise NameError(s)
                seen.add(s)
