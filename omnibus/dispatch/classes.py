import abc
import types
import typing as ta
import weakref

from .. import c3
from .. import lang
from .. import reflect as rfl
from .. import registries
from .caching import CachingDispatcher
from .erasing import ErasingDispatcher
from .manifests import inject_manifest
from .types import Dispatcher
from .types import Manifest


T = ta.TypeVar('T')
R = ta.TypeVar('R')
Impl = ta.TypeVar('Impl')
TypeOrSpec = ta.Union[ta.Type, rfl.Spec]


class Property(registries.Property):

    def __init__(self) -> None:
        super().__init__(bind=True)

        self._dispatcher_by_tcls_by_scls: ta.MutableMapping[ta.Type, ta.MutableMapping[ta.Type, Dispatcher]] = weakref.WeakKeyDictionary()  # noqa

    def get_dispatcher(self, scls: ta.Type, tcls: ta.Type = None) -> Dispatcher:
        if tcls is None:
            tcls = scls
        try:
            return self._dispatcher_by_tcls_by_scls[scls][tcls]
        except KeyError:
            try:
                tdct = self._dispatcher_by_tcls_by_scls[scls]
            except KeyError:
                tdct = self._dispatcher_by_tcls_by_scls[scls] = weakref.WeakKeyDictionary()
            registry = self.get_registry(scls, tcls)
            dispatcher = CachingDispatcher(ErasingDispatcher(registry))
            tdct[tcls] = dispatcher
            return dispatcher

    class Accessor(registries.Property.Accessor):

        def __init__(self, owner, obj, cls, tcls=None):
            super().__init__(owner, obj, cls, tcls)

            self._dispatcher = owner.get_dispatcher(cls, tcls)
            self._bound_cache: ta.Dict[ta.Any, callable] = {}

        def bind(self, key):
            try:
                bound = self._bound_cache[key]
            except KeyError:
                impl, manifest = self._dispatcher.dispatch(key)
                impl = inject_manifest(impl, manifest)
                bound = self._bound_cache[key] = impl.__get__(self._obj, self._cls)
            return bound

        def __call__(self, arg, *args, **kwargs):
            key = self._dispatcher.key(arg)
            bound = self.bind(key)
            return bound(arg, *args, **kwargs)

        def dispatch(self, cls: ta.Any) -> ta.Tuple[ta.Optional[Impl], ta.Optional[Manifest]]:
            return self._dispatcher.dispatch(cls)

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


class _PropertyProxy:

    def __init__(self, prop: Property, tcls: ta.Type) -> None:
        super().__init__()
        self._prop = prop
        self._tcls = tcls

    def __get__(self, instance, owner=None):
        if owner is None:
            return self
        return self._prop.__get__(instance, owner, self._tcls)


class _ClassMeta(abc.ABCMeta):

    class RegisteringNamespace:

        def __init__(self, props: ta.Mapping[str, Property]) -> None:
            super().__init__()
            self._dict = {}
            self._props = dict(props)
            self._used_props = set()

        def __contains__(self, item):
            return item in self._dict

        def __getitem__(self, item):
            return self._dict[item]

        def __setitem__(self, key, value):
            try:
                reg = self._props[key]

            except KeyError:
                self._dict[key] = value
                if isinstance(value, Property):
                    self._props[key] = value

            else:
                if isinstance(reg, Property):
                    reg.register(value, cls_dct=self._dict)
                    self._dict[f'__{hex(id(value))[2:]}'] = value
                    self._used_props.add(key)

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
        props = {}
        mro = c3.merge([list(b.__mro__) for b in bases])
        for bmro in reversed(mro):
            for k, v in bmro.__dict__.items():
                if isinstance(v, Property):
                    props[k] = v
                elif isinstance(v, _PropertyProxy):
                    props[k] = v._prop

        return cls.RegisteringNamespace(props)

    def __new__(mcls, name, bases, namespace, **kwargs):
        if not isinstance(namespace, mcls.RegisteringNamespace):
            raise TypeError(namespace)

        dct = dict(namespace._dict)
        cls = super().__new__(mcls, name, bases, dct, **kwargs)

        for prop in namespace._used_props:
            setattr(cls, prop, _PropertyProxy(namespace._props[prop], cls))

        return cls


class Class(metaclass=_ClassMeta):
    pass
