import sys
import typing as ta

from ..lang import new_type


def _extension_ignored_attrs() -> ta.Set[str]:
    class C:
        pass
    return set(C.__dict__)


_EXTENSION_IGNORED_ATTRS = _extension_ignored_attrs()


class _ExtensionMeta(type):

    def __new__(mcls, name, bases, namespace, *, _bind=None):
        if not bases:
            return super().__new__(mcls, name, bases, namespace)
        if _bind is not None:
            if bases != (Extension,):
                raise TypeError
            return super().__new__(mcls, name, bases, {'__extensionbind__': _bind, **namespace})

        newbases = []
        binds = []
        for base in bases:
            if issubclass(base, Extension):
                if base.__bases__ != (Extension,) or not hasattr(base, '__extensionbind__'):
                    raise TypeError
                binds.append(base.__extensionbind__)
                del base.__extensionbind__
            else:
                newbases.append(base)

        cls = super().__new__(mcls, name, tuple(newbases), namespace)
        newns = {}
        for mrocls in reversed(cls.__mro__):
            if mrocls is object:
                continue
            for k, v in mrocls.__dict__.items():
                if k not in _EXTENSION_IGNORED_ATTRS:
                    newns[k] = v

        for bind in binds:
            for k, v in newns.items():
                if k in bind.__dict__:
                    raise NameError(k)
                setattr(bind, k, v)

        return None

    def __getitem__(self, bind):
        return new_type(f'{self.__name__}[{bind!r}]', (self,), {}, _bind=bind)


class Extension(metaclass=_ExtensionMeta):
    pass


_MIXIN_IGNORED_ATTRS = {
    '__module__',
    '__qualname__',
}


class _MixinMeta(type):

    def __new__(mcls, name, bases, namespace):
        if 'Mixin' not in globals():
            return super().__new__(mcls, name, bases, namespace)
        try:
            return namespace['__mixin__']
        except KeyError:
            raise RuntimeError('Must call Mixin.capture in class body')


class Mixin(metaclass=_MixinMeta):

    @staticmethod
    def capture() -> None:
        frame = sys._getframe(1)
        body, globals = frame.f_code, frame.f_globals

        def mixin():
            locals = sys._getframe(1).f_locals
            if not all(k in locals for k in _MIXIN_IGNORED_ATTRS):
                raise RuntimeError('Must invoke mixin from class definition body')
            restores = {k: locals[k] for k in _MIXIN_IGNORED_ATTRS}
            exec(body, globals, locals)
            locals.update(restores)

        frame.f_locals['__mixin__'] = mixin
