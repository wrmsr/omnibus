"""
TODO:
 - do not use HAS_FACTORY - use native MISSING marker
 - deep interop w defaults
 - kinda has to take over init..
  - move InitBuilder to Processor?
 - post-init? .. why not.
 - ** rebuild / subclass config ala compcache w/ config storage** - ctors will check.isinstance

Q:
 - existing conventional ctor vs unary 'source' ctor
  - q of lazy vs eager
  - **DECREE** going with unary 'source' ctor PREEMPTIVELY despite initially being overkill
"""

# from .. import dataclasses as dc
# from .configs import Config
#
#
# def build_dataclass_config(dcls):
#     spec = dc.get_spec(dcls)
#     cls = type(dcls.__name__, )
#     raise NotImplementedError
