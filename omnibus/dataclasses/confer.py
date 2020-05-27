import dataclasses as dc
import typing as ta

from .. import check
from .internals import DataclassParams
from .reflect import get_cls_spec
from .types import EXTRA_PARAMS_CONFER_DEFAULTS
from .types import ExtraParams
from .types import METACLASS_PARAMS_CONFER_DEFAULTS
from .types import MetaclassParams
from .types import PARAMS_CONFER_DEFAULTS
from .types import SUPER


def confer_params(
        bases: ta.Sequence[type],
        params: DataclassParams,
        extra_params: ExtraParams,
        metaclass_params: ta.Optional[MetaclassParams] = None,
) -> ta.Tuple[
    DataclassParams,
    ExtraParams,
    ta.Optional[MetaclassParams],
]:
    check.isinstance(params, DataclassParams)
    check.isinstance(extra_params, ExtraParams)
    if metaclass_params is not None:
        check.isinstance(metaclass_params, MetaclassParams)

    pc = {}
    epc = {}
    mcpc = {}

    for base in bases:
        if not dc.is_dataclass(base):
            continue
        base_spec = get_cls_spec(base)
        confer = base_spec.extra_params.confer
        if not confer:
            continue

        def update(given_params, base_params, confer_defaults, conferred):
            for a, v in confer_defaults.items():
                if getattr(given_params, a) is not dc.MISSING or a not in confer:
                    continue
                if isinstance(confer, ta.Mapping):
                    if confer[a] is not SUPER:
                        v = confer[a]
                elif base_params is not None:
                    v = getattr(base_params, a)
                if v is dc.MISSING:
                    continue
                if a in conferred:
                    if conferred[a] != v:
                        raise ValueError(f'Incompatible conferred params: base={base} a={a}')
                else:
                    conferred[a] = v

        update(params, base_spec.params, PARAMS_CONFER_DEFAULTS, pc)
        update(extra_params, base_spec.extra_params, EXTRA_PARAMS_CONFER_DEFAULTS, epc)
        if metaclass_params is not None:
            update(metaclass_params, base_spec.metaclass_params, METACLASS_PARAMS_CONFER_DEFAULTS, mcpc)

    params = DataclassParams(**{
        **PARAMS_CONFER_DEFAULTS,
        **{
            a: v for a in DataclassParams.__slots__
            for v in [getattr(params, a)]
            if a not in PARAMS_CONFER_DEFAULTS or v is not dc.MISSING
        },
        **pc,
    })

    extra_params = ExtraParams(**{
        **EXTRA_PARAMS_CONFER_DEFAULTS,
        **{
            a: v
            for fld in dc.fields(ExtraParams)
            for a in [fld.name]
            for v in [getattr(extra_params, a)]
            if a not in EXTRA_PARAMS_CONFER_DEFAULTS or v is not dc.MISSING
        },
        **epc,
    })

    if metaclass_params is not None:
        metaclass_params = MetaclassParams(**{
            **METACLASS_PARAMS_CONFER_DEFAULTS,
            **{
                a: v
                for fld in dc.fields(MetaclassParams)
                for a in [fld.name]
                for v in [getattr(metaclass_params, a)]
                if a not in METACLASS_PARAMS_CONFER_DEFAULTS or v is not dc.MISSING
            },
            **mcpc,
        })

    return params, extra_params, metaclass_params
