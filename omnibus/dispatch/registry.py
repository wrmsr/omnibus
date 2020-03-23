import abc
import types
import typing as ta
import weakref

from .. import c3
from .. import lang
from .. import properties
from .. import reflect as rfl
from .caching import CachingDispatcher
from .erasing import ErasingDispatcher
from .manifests import inject_manifest
from .types import Dispatcher


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]


class Property(properties.RegistryProperty):

    def __init__(self) -> None:
        super().__init__(bind=True)

        self._dispatcher_cache: ta.MutableMapping[ta.Type, Dispatcher] = weakref.WeakKeyDictionary()

    def get_dispatcher(self, cls: ta.Type) -> Dispatcher:
        try:
            return self._dispatcher_cache[cls]

        except KeyError:
            registry = self.get_registry(cls)

            dispatcher = CachingDispatcher(ErasingDispatcher(registry))

            self._dispatcher_cache[cls] = dispatcher

            return dispatcher

    class Accessor(properties.RegistryProperty.Accessor):

        def __init__(self, owner, obj, cls):
            super().__init__(owner, obj, cls)

            self._dispatcher = owner.get_dispatcher(cls)
            self._bound_cache: ta.Dict[ta.Any, callable] = {}

        def __call__(self, arg, *args, **kwargs):
            key = self._dispatcher.key(arg)
            try:
                bound = self._bound_cache[key]
            except KeyError:
                impl, manifest = self._dispatcher[key]
                impl = inject_manifest(impl, manifest)
                bound = self._bound_cache[key] = impl.__get__(self._obj, self._cls)

            return bound(arg, *args, **kwargs)

        def dispatch(self, cls: ta.Any) -> ta.Callable:
            return self._dispatcher[cls]

    @lang.cls_dct_fn()
    def register(self, cls_dct, *args):
        if len(args) == 1 and isinstance(args[0], types.FunctionType):
            [meth] = args

            ann = getattr(meth, '__annotations__', {})
            if not ann:
                raise TypeError

            _, key = next(iter(ta.get_type_hints(meth).items()))
            if not isinstance(key, type):
                raise TypeError(key)

            self._register(cls_dct, meth, [key])
            return meth

        else:
            return super().register(*args, cls_dct=cls_dct)


def property_() -> Property:  # noqa
    return Property()


class _ClassMeta(abc.ABCMeta):

    class RegisteringNamespace:

        def __init__(self, regs: ta.Mapping[str, Property]) -> None:
            super().__init__()
            self._dict = {}
            self._regs = dict(regs)

        def __contains__(self, item):
            return item in self._dict

        def __getitem__(self, item):
            return self._dict[item]

        def __setitem__(self, key, value):
            try:
                reg = self._regs[key]

            except KeyError:
                self._dict[key] = value
                if isinstance(value, Property):
                    self._regs[key] = value

            else:
                if isinstance(reg, Property):
                    reg.register(value, cls_dct=self._dict)
                    self._dict[f'__{hex(id(value))}'] = value

        def __delitem__(self, key):
            del self._dict[key]

        def get(self, k, d=None):
            try:
                return self[k]
            except KeyError:
                return d

        def setdefault(self, k, d=None):
            try:
                return self[k]
            except KeyError:
                self[k] = d
                return d

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        regs = {}
        mro = c3.merge([list(b.__mro__) for b in bases])
        for bmro in reversed(mro):
            for k, v in bmro.__dict__.items():
                if isinstance(v, Property):
                    regs[k] = v

        return cls.RegisteringNamespace(regs)

    def __new__(mcls, name, bases, namespace, **kwargs):
        if not isinstance(namespace, mcls.RegisteringNamespace):
            raise TypeError(namespace)

        namespace = namespace._dict
        return super().__new__(mcls, name, bases, namespace, **kwargs)


class Class(metaclass=_ClassMeta):
    pass
