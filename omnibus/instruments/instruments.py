"""
TODO:
 - errors: rollbar
 - metrics: datadog
 - tracing: ddtrace
 - profiling: yappi, cprofile, pyinstrument
 - queues: sqs, ..., internal?
 - mv ifaces? interfaces? integrations?
  - when move from omnibus.integrations.queues.queue to omnibus.queues.types?
   - move out when impls no longer stubs or trivial, or when non-trivial support machinery
  - integrations can have iface impls from non-omnibus.interface pkgs (bigger)
  - there can also be opt-libs that aren't full 'integrations' (collections, ...)
 - bittorrent?
 - ssh? (paramiko + bltin expect)
"""
