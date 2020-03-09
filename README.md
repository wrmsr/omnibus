Omnibus is my personal collection of portable, general purpose python tools. Although documentation is.. lacking.. this code is intended for (and is actively seeing) production use - this is not experimental or hack code.

Its modules include:
- [lang](https://github.com/wrmsr/omnibus/blob/master/omnibus/lang.py), a large collection of language-level helpers including:
    - [Final classes](https://github.com/wrmsr/omnibus/blob/41520c4191303540bc340718a19668cf2920835b/omnibus/lang.py#L375)
    - [Sealed classes](https://github.com/wrmsr/omnibus/blob/41520c4191303540bc340718a19668cf2920835b/omnibus/lang.py#L395)
    - [ContextManager utilities](https://github.com/wrmsr/omnibus/blob/41520c4191303540bc340718a19668cf2920835b/omnibus/lang.py#L625)
    - Some low-levele [Async utlities](https://github.com/wrmsr/omnibus/blob/41520c4191303540bc340718a19668cf2920835b/omnibus/lang.py#L1158)
    - As well as various string, datetime, class, enum, and a other such utilities.
- [caches](https://github.com/wrmsr/omnibus/blob/41520c4191303540bc340718a19668cf2920835b/omnibus/caches.py#L92), containing a pretty beefy cache implementation inspired by [Guava's CacheBuilder](https://guava.dev/releases/snapshot-jre/api/docs/).
- [check](https://github.com/wrmsr/omnibus/blob/master/omnibus/check.py), non-optional assertions inspired by [Guava Preconditions](https://guava.dev/releases/snapshot-jre/api/docs/).
- [collections](https://github.com/wrmsr/omnibus/blob/master/omnibus/collections.py), including:
    - Sorted collections powered either by [sortedcontainers](https://pypi.org/project/sortedcontainers) or a builtin fallback skiplist
    - topological sorting (added to functools in python 3.9 but not present in 3.7)
    - Identity and Frozen collections
- [defs](https://github.com/wrmsr/omnibus/blob/master/omnibus/defs.py), a self-awarely relatively unpythonic set of helpers for defining common boilerplate methods (repr, hash_eq, delegates, etc) in class definitions. Should be used sparingly for methods not directly used by humans (like repr) - @property's should remain @property's for type annotation, tool assistance, debugging, and otherwise, but these are still nice to have in certain circumstances (the real-world alternative usually being simply not adding them).
- [dynamic](https://github.com/wrmsr/omnibus/blob/master/omnibus/dynamic.py), dynamically [scoped](https://en.wikipedia.org/wiki/Scope_(computer_science)#Dynamic_scoping) variables (implemented by stackwalking). Unlike threadlocals these are generator-correct both in binding and retrieval, and unlike [ContextVars](https://docs.python.org/3/library/contextvars.html) they require no manual context management. They are however *slow* and should be used sparingly (once per sql statement executed not once per inner function call).
- [inject](https://github.com/wrmsr/omnibus/blob/master/omnibus/inject.py), a dependency injection system **heavily** inspired by [Guice](https://github.com/google/guice) (specifically [MiniGuice](https://github.com/google/guice/blob/2f2c3a629eaf7e9a4e3687ae17004789fd41fed6/extensions/mini/src/com/google/inject/mini/MiniGuice.java)). Supports annotation powered introspection, private modules, set and dict binders, and guice-style scopes and child injectors, with intended support for proxies / circular injection, type converters, and overriding modules as needed. Being aware of the two-dozen odd other python DI systems I'm still happiest with mine, basically 'doing what Guice does' (impl-wise, not just skin deep) but with a tenth the complexity (python kwargs over builders, little regard for its error messages as its graphs tend to be smaller, etc).
- [iterables](https://github.com/wrmsr/omnibus/blob/master/omnibus/iterables.py), a collection of composable, _transparent_ iterable transformations, which unlike most opaque generator compositions can be externally inspected, analyzed, rewritten, and optimized and fused as desired (as well as carrying with them more descriptive reprs and debug information).
- [properties](https://github.com/wrmsr/omnibus/blob/master/omnibus/properties.py), a set of @property-like descriptors like cached, locked_cached, set_once, class_, cached_class, and more interesting ones like an mro-honoring registry property (with optional singledispatch).
- [pydevd](https://github.com/wrmsr/omnibus/blob/master/omnibus/pydevd.py) utilties, a small but likely growing collection of (completely optional) tools to make pydevd (PyCharm's, among other python IDE's, debugger) do hard things. Originally explored and added to get spark jvm python subprocesses to connect back to an already-debugging PyCharm instance to debug PySpark jobs.
- [reflect](https://github.com/wrmsr/omnibus/blob/master/omnibus/reflect.py), an imo missing stdlib component for breaking apart and representing python's ever-expanding generic typing machinery in a more stable and friendly object hierarchy. Frees users from having to deal with notoriously version-volatile typing impl detail like ```__args__```, ```__origin__```, Generic's ```__mro_entries__```, and such - ideally approximating something stable like java.lang.reflect.
- [replserver](https://github.com/wrmsr/omnibus/blob/master/omnibus/replserver.py), a background thread that opens a unix socket server accepting connections to an in-proc python repl (from which one can inspect module globals, live thread stacks, and other such things).

Many other modules are in the works now that this has some of my attention again but none are stable enough yet for inclusion in master.

It unapologetically requires python 3.7+. It has one single mandatory dependency: [toolz](https://pypi.org/project/toolz) - itself having no dependencies. It does however optionally interop with a number of other libraries including:
- [sortedcontainers](https://pypi.org/project/sortedcontainers)
- [pyrsistent](https://pypi.org/project/pyrsistent)
- [wrapt](https://pypi.org/project/wrapt)
- [ujson](https://pypi.org/project/ujson)
- [billiard](https://pypi.org/project/billiard)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy)
- various sql drivers
- [docker](https://pypi.org/project/docker)
- various compression and serialization codecs
- and a number of others

But again, the only required dependency is toolz, and toolz has no transitive dependencies.

Notably the code is organized, python-stdlib-style, into a flat list of relatively large files. This is, again, largely in keeping tradition with python's stdlib, and in practice thus far nothing has yet justified breaking into a subpackage (though that may soon be changing). My app-level code tends to be much more decomposed into subdirectories of smaller files, but this is lib code.
