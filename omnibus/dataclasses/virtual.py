import dataclasses as dc


class _VirtualClassMeta(type):

    def __subclasscheck__(cls, subclass):
        return dc.is_dataclass(subclass)

    def __instancecheck__(cls, instance):
        return dc.is_dataclass(instance)


class VirtualClass(metaclass=_VirtualClassMeta):

    def __new__(cls, *args, **kwargs):
        raise TypeError

    def __init_subclass__(cls, **kwargs):
        raise TypeError
