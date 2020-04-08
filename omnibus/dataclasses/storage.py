"""
TODO:
 - nesting
 - rebuilding from existing
  - stubbing (query comp cache)

NOTES:
 - can change ctor
  - config takes only a source
 - dc.replace has to work
  - is only way to modify tuple/pyrsistent / any frozen
   - backend.is_frozen

Backends:
 - default
  - slots
 - tuple
 - pyrsistent
 - struct
 - arrays
  - numpy
  - mmap
 - configs
"""
