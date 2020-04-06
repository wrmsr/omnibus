from .. import dataclasses as dc
from .configs import Config


def build_dataclass_config(dcls):
    spec = dc.get_spec(dcls)
    cls = type(dcls.__name__, )
    raise NotImplementedError
