"""
~com.google.common.base.Preconditions

TODO:
 - pluggable _unpack_isinstance_spec - reflect? or at least lang.Callable
 - and, still: fexprs
"""
import collections
import typing as ta


T = ta.TypeVar('T')
MR = ta.TypeVar('MR', bound=ta.Union[None, str, ta.Tuple])
HashableT = ta.TypeVar('HashableT', bound=ta.Hashable)
IterableHashableT = ta.TypeVar('IterableHashableT', bound=ta.Iterable[HashableT])  # type: ignore
Messageable = ta.Union[None, str, ta.Callable[..., MR]]
SizedT = ta.TypeVar('SizedT', bound=ta.Sized)


_isinstance = isinstance
_issubclass = issubclass
_callable = callable
_NONE_TYPE = type(None)


def _default_exception_factory(exc_cls: ta.Type[Exception], *args, **kwargs) -> Exception:
    return exc_cls(*args, **kwargs)  # noqa


_EXCEPTION_FACTORY = _default_exception_factory


def _raise(
        exception_type: ta.Type[Exception],
        default: ta.Optional[str],
        message: Messageable,
        *args: ta.Any,
        **kwargs: ta.Any
) -> ta.NoReturn:
    if _callable(message):
        message = ta.cast(ta.Callable, message)(*args, **kwargs)
        if _isinstance(message, tuple):
            message, *args = message  # type: ignore
    if message is None:
        message = default
    if message is not None:
        args = message, *args
    exc = _EXCEPTION_FACTORY(exception_type, *args, **kwargs)
    raise exc


def state(condition: bool, message: Messageable = None) -> None:
    if not condition:
        _raise(RuntimeError, 'State condition not met', message)


def arg(condition: bool, message: Messageable = None) -> None:
    if not condition:
        _raise(ValueError, 'Argument condition not met', message)


def _unpack_isinstance_spec(spec: ta.Any) -> tuple:
    if not _isinstance(spec, tuple):
        spec = (spec,)
    if None in spec:
        spec = tuple(filter(None, spec)) + (_NONE_TYPE,)  # type: ignore
    if ta.Any in spec:
        spec = (object,)
    return spec


def isinstance(obj: ta.Any, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if not _isinstance(obj, _unpack_isinstance_spec(spec)):
        _raise(TypeError, 'Must be instance', message, obj, spec)
    return obj  # type: ignore


def of_isinstance(spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> ta.Callable[[ta.Any], T]:
    def inner(obj):
        return isinstance(obj, spec, message)
    return inner


def issubclass(obj: T, spec: ta.Union[ta.Type[T], ta.Tuple, type], message: Messageable = None) -> T:
    if not _issubclass(obj, spec):  # type: ignore
        _raise(TypeError, 'Must be subclass', message, obj, spec)
    return obj


def of_issubclass(spec: ta.Union[ta.Type[T], ta.Tuple, type], message: Messageable = None) -> ta.Callable[[ta.Any], T]:
    def inner(obj):
        return issubclass(obj, spec, message)
    return inner


def not_isinstance(obj: ta.Any, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if _isinstance(obj, _unpack_isinstance_spec(spec)):
        _raise(TypeError, 'Must be not instance', message, obj, spec)
    return obj  # type: ignore


def of_not_isinstance(spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> ta.Callable[[ta.Any], T]:
    def inner(obj):
        return not_isinstance(obj, spec, message)
    return inner


def not_issubclass(obj: T, spec: ta.Union[ta.Type[T], ta.Tuple, type], message: Messageable = None) -> T:
    if _issubclass(obj, spec):  # type: ignore
        _raise(TypeError, 'Must be not subclass', message, obj, spec)
    return obj


def of_not_issubclass(spec: ta.Union[ta.Type[T], ta.Tuple, type], message: Messageable = None) -> ta.Callable[[ta.Any], T]:  # noqa
    def inner(obj):
        return not_issubclass(obj, spec, message)
    return inner


def cast(obj: ta.Any, cls: ta.Type[T], message: Messageable = None) -> T:
    if not _isinstance(obj, cls):
        _raise(TypeError, 'Must be instance', message, obj, cls)
    return obj  # type: ignore


def not_none(obj: ta.Optional[T], message: Messageable = None) -> T:
    if obj is None:
        _raise(TypeError, 'May not be None', message)
    return obj


def none(obj: T, message: Messageable = None) -> None:
    if obj is not None:
        _raise(TypeError, 'Must be None', message, obj)
    return None  # type: ignore


def empty(obj: SizedT, message: Messageable = None) -> SizedT:
    if len(obj) != 0:
        _raise(ValueError, 'Must be empty', message, obj)
    return obj


def not_empty(obj: SizedT, message: Messageable = None) -> SizedT:
    if len(obj) == 0:
        _raise(ValueError, 'May not be empty', message, obj)
    return obj


def non_empty_str(obj: ta.Optional[str], message: Messageable = None) -> str:
    if not isinstance(obj, str) or not obj:
        _raise(ValueError, 'Must be non-empty str', message, obj)
    return obj


def single(obj: ta.Iterable[T], message: Messageable = None) -> T:
    try:
        [value] = obj
    except ValueError:
        _raise(ValueError, 'Must be single', message, obj)
    else:
        return value


def unique(it: IterableHashableT, message: Messageable = None) -> IterableHashableT:
    dupes = [e for e, c in collections.Counter(it).items() if c > 1]  # type: ignore
    if dupes:
        _raise(ValueError, 'Must be unique', message, it, dupes)
    return it


def in_(item: T, container: ta.Container[T], message: Messageable = None) -> T:
    if item not in container:
        _raise(ValueError, 'Must be in', message, item, container)
    return item


def not_in(item: T, container: ta.Container[T], message: Messageable = None) -> T:
    if item in container:
        _raise(ValueError, 'Must not be in', message, item, container)
    return item


def callable(obj: T, message: Messageable = None) -> T:
    if not _callable(obj):
        _raise(TypeError, 'Must be callable', message, obj)
    return obj


def replacing(expected: ta.Any, old: ta.Any, new: T, message: Messageable = None) -> T:
    if old != expected:
        _raise(TypeError, 'Must be replacing', message, expected, old, new)
    return new


def replacing_none(old: ta.Any, new: T, message: Messageable = None) -> T:
    return replacing(None, old, new, message=message)


def raises(fn: ta.Callable, exc: ta.Type[BaseException] = BaseException, message: Messageable = None) -> None:
    try:
        fn()
    except BaseException as e:
        if not _isinstance(e, exc):
            _raise(TypeError, 'Must raise correct exception', message, fn, exc, e)
    else:
        _raise(TypeError, 'Must raise', message, fn, exc)


def sets_equal(given: ta.Set[T], expected: ta.Set[T], message: Messageable = None) -> None:
    if given != expected:
        missing = expected - given
        unexpected = given - expected
        _raise(KeyError, f'Set difference - missing: {missing} unexpected: {unexpected}', message, given, expected)  # noqa


def exhausted(it: ta.Iterator[T], message: Messageable = None) -> None:
    try:
        next(it)
    except StopIteration:
        pass
    else:
        _raise(ValueError, 'Iterator should be exhausted', message, it)


def one_of(*items: T, **kwargs) -> T:
    not_set = object()

    default = kwargs.pop('default', not_set)
    default_factory = kwargs.pop('default_factory', not_set)
    if default is not not_set and default_factory is not not_set:
        raise ValueError('Expected at most one of default and default_factory')

    test = kwargs.pop('test', not_set)
    not_none = kwargs.pop('not_none', not_set)
    if test is not not_set and not_none is not not_set:
        raise ValueError('Expected at most one of test and not_none')
    if not_none is not not_set:
        if not not_none:
            raise ValueError('Expected truthy value for not_none')
        test = lambda v: v is not None
    elif test is not_none:
        test = bool

    message: Messageable = kwargs.pop('message', None)
    if kwargs:
        raise ValueError(kwargs)

    value = not_set
    for item in items:
        if test(item):
            if value is not not_set:
                _raise(ValueError, f'Expected exactly one of {items}, got {value} and {item}', message, items, kwargs, value, item)  # noqa
            value = item
    if value is not not_set:
        return ta.cast(T, value)
    if default is not not_set:
        return default  # type: ignore
    if default_factory is not not_set:
        return default_factory()  # type: ignore

    _raise(ValueError, f'Expected exactly one of {items}, got none', message, items, kwargs)
