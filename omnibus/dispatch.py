import abc
import functools
import inspect
import typing as ta

from . import c3
from . import check
from . import lang
from . import reflect as rfl


T = ta.TypeVar('T')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]
TypeVars = ta.Mapping[ta.Any, TypeOrSpec]


def generic_issubclass(left: ta.Type, right: ta.Type) -> bool:
    if rfl.is_generic(right):
        right = check.not_none(rfl.erase_generic(right))
    return issubclass(left, right)


def generic_compose_mro(
        cls: T,
        types: ta.Sequence[T] = None,
):
    return c3.compose_mro(
        cls,
        list(types),
        getbases=rfl.generic_bases,
        issubclass=generic_issubclass,
    )


class Manifest(lang.Final):

    def __init__(
            self,
            _cls: TypeOrSpec,
            _match: TypeOrSpec,
            _vars: TypeVars
    ) -> None:
        super().__init__()

        self._cls = _cls
        self._match = _match
        self._vars = _vars

        self._key: ta.Iterable[ta.Tuple[ta.Any, ta.Type]] = tuple(sorted(_vars.items(), key=hash))
        self._hash = hash((self._cls, self._match, self._key))

    @property
    def cls(self) -> TypeOrSpec:
        return self._cls

    @property
    def match(self) -> TypeOrSpec:
        return self._match

    @property
    def vars(self) -> TypeVars:
        return self._vars

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._cls!r}, {self._match!r}, {self._vars!r})'

    def __iter__(self) -> ta.Iterator[ta.Type]:
        if rfl.is_generic(self._cls):
            return self._cls.__args__
        else:
            raise TypeError

    def __getitem__(self, item: ta.TypeVar) -> ta.Type:
        return self._vars[item]

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self._cls == other._type and
            self._match == other._match and
            self._key == other._key
        )


def get_manifest_injection_kwargs(impl: ta.Optional[ta.Callable]) -> ta.Optional[ta.Set[str]]:
    if impl is None:
        return None
    try:
        implargspec = inspect.getfullargspec(impl)
    except TypeError:
        return None
    else:
        return {a for a in implargspec.kwonlyargs if implargspec.annotations.get(a) is Manifest}


def inject_manifest(impl: ta.Optional[ta.Callable], manifest: Manifest) -> ta.Callable:
    manifestkw = get_manifest_injection_kwargs(impl)
    if manifestkw:
        impl = functools.partial(impl, **{k: manifest for k in manifestkw})
    return impl


class Dispatcher(ta.Generic[Impl]):

    @staticmethod
    def key(obj: ta.Any) -> TypeOrSpec:
        return obj.__class__

    @abc.abstractmethod
    def __setitem__(self, key: TypeOrSpec, value: Impl):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, key: TypeOrSpec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        raise NotImplementedError


class ErasingDictDispatcher(Dispatcher[Impl]):

    _dict: ta.Dict[ta.Type, Impl]

    def __init__(self, dict: ta.Dict[ta.Type, Impl] = None) -> None:
        super().__init__()

        if dict is not None:
            self._dict = dict
        else:
            self._dict = {}

    def _resolve(self, cls: ta.Type) -> ta.Optional[ta.Tuple[ta.Type, Impl]]:
        mro = generic_compose_mro(cls, list(self._dict.keys()))
        match = None
        for t in mro:
            if match is not None:
                # If *match* is an implicit ABC but there is another unrelated,
                # equally matching implicit ABC, refuse the temptation to guess.
                if (
                        t in self._dict and
                        t not in cls.__mro__ and
                        match not in cls.__mro__ and
                        not issubclass(match, t)
                ):
                    raise RuntimeError(f'Ambiguous dispatch: {match} or {t}')
                break
            if t in self._dict:
                match = t
        return match, self._dict.get(match)

    def _erase(self, cls: TypeOrSpec) -> ta.Type:
        return check.isinstance(rfl.erase_generic(cls.erased_cls if isinstance(cls, rfl.TypeSpec) else cls), type)

    def __setitem__(self, cls: TypeOrSpec, impl: Impl) -> None:
        cls = self._erase(cls)
        if cls in self._dict:
            raise KeyError(cls)
        self._dict[cls] = impl

    def __getitem__(self, cls: TypeOrSpec) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
        cls = self._erase(cls)
        try:
            impl = self._dict[cls]
        except KeyError:
            match, impl = self._resolve(cls)
            return impl, Manifest(cls, match, {})
        else:
            return impl, Manifest(cls, cls, {})

    def __contains__(self, cls: TypeOrSpec) -> bool:
        cls = self._erase(cls)
        return cls in self._dict

    def items(self) -> ta.Iterable[ta.Tuple[TypeOrSpec, Impl]]:
        return self._dict.items()


class CacheGuard(lang.Abstract):

    @abc.abstractmethod
    def update(self, cls: TypeOrSpec) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def maybe_clear(self) -> bool:
        raise NotImplementedError


class AbcCacheGuard(CacheGuard):

    def __init__(self, lock: ta.Any, clear: ta.Callable) -> None:
        super().__init__()

        self._lock = lock
        self._clear = clear

        self._cache_token = abc.get_cache_token()

    def update(self, cls: TypeOrSpec) -> bool:
        if isinstance(cls, type):
            if not hasattr(cls, '__abstractmethods__'):
                return False
        elif isinstance(cls, rfl.Spec):
            if not any(hasattr(t.erased_cls, '__abstractmethods__') for t in cls.all_types):
                return False
        else:
            return False
        self._cache_token = abc.get_cache_token()
        return True

    def maybe_clear(self) -> bool:
        if self._cache_token is not None:
            if self._cache_token != abc.get_cache_token():
                with self._lock:
                    current_token = abc.get_cache_token()
                    if self._cache_token != current_token:
                        self._clear()
                        self._cache_token = current_token
                        return True

        return False


DefaultDispatcher = ErasingDictDispatcher
DefaultCacheGuard = AbcCacheGuard
