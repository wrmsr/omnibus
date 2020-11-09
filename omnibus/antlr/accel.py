import contextlib
import functools
import logging
import textwrap
import typing as ta

from .. import lang
from .._vendor import antlr4


T = ta.TypeVar('T')


log = logging.getLogger(__name__)


def _patch_cache_hash(cls: type, fn_name: str = '__hash__') -> type:
    orig_fn = getattr(cls, fn_name)
    if orig_fn is getattr(object, fn_name, None):
        raise TypeError(cls)

    cache_attr = f'__hash_cached__{fn_name}'

    ns = {'orig': orig_fn}
    exec(textwrap.dedent(f"""
    def {fn_name}(self):
        try:
            return self.{cache_attr}
        except AttributeError:
            val = self.{cache_attr} = orig(self)
            return val
    """), ns)
    cache_fn = functools.wraps(orig_fn)(ns[fn_name])

    return lang.setattr_context(cls, fn_name,  cache_fn)


def _patch_const_hash(obj: T, fn_name: str = '__hash__') -> T:
    cls = type(obj)
    orig_fn = getattr(cls, fn_name)
    if orig_fn is getattr(object, fn_name, None):
        raise TypeError(cls)

    val = hash(obj)

    ns = {}
    exec(textwrap.dedent(f"""
    def {fn_name}(self):
        return {val!r}
    """), ns)
    cache_fn = functools.wraps(orig_fn)(ns[fn_name])

    return lang.setattr_context(cls, fn_name, cache_fn)


@contextlib.contextmanager
def patch_hash_context():
    with contextlib.ExitStack() as es:
        from .._vendor.antlr4.atn.ATNConfig import ATNConfig
        es.enter_context(_patch_cache_hash(ATNConfig))
        es.enter_context(_patch_cache_hash(ATNConfig, 'hashCodeForConfigSet'))

        from .._vendor.antlr4.atn.SemanticContext import Predicate
        es.enter_context(_patch_cache_hash(Predicate))

        from .._vendor.antlr4.PredictionContext import SingletonPredictionContext
        es.enter_context(_patch_cache_hash(SingletonPredictionContext))

        from .._vendor.antlr4.PredictionContext import EmptyPredictionContext
        es.enter_context(_patch_cache_hash(EmptyPredictionContext))

        yield


@contextlib.contextmanager
def patch_simulator_context():
    """FIXME: write full self-contained impl in pure py, then cythonize"""

    try:
        from .._ext.cy import antlr as cy
    except ImportError:
        log.exception('Exception importing antlr cython extensions')
        yield
        return

    with contextlib.ExitStack() as es:
        es.enter_context(lang.setattr_context(
            antlr4.LexerATNSimulator,
            'closure',
            cy.LexerATNSimulator__closure,
        ))
        es.enter_context(lang.setattr_context(
            antlr4.LexerATNSimulator,
            'computeStartState',
            cy.LexerATNSimulator__computeStartState,
        ))

        yield
