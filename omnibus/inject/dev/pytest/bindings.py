"""
TODO:
 - switches
"""
import dataclasses as dc

import pytest

from ... import bind as bnd
from .... import lang
from ....dev.pytest.plugins import ci
from .harness import register


@dc.dataclass(frozen=True)
class Ci(lang.Final):
    value: bool

    def __bool__(self) -> bool:
        return self.value

    def skip(self) -> None:
        if self:
            pytest.skip(f'ci disabled')


def _provide_ci() -> Ci:
    return Ci(ci.is_ci())


binder = bnd.create_binder()
binder.bind_callable(_provide_ci, as_eager_singleton=True)
register(binder)
