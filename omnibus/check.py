"""
~com.google.common.base.Preconditions
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


def _raise(
        exception_type: type,
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
    raise exception_type(*args, **kwargs)


def state(condition: bool, message: Messageable = None) -> None:
    if not condition:
        _raise(RuntimeError, 'State condition not met', message)


def arg(condition: bool, message: Messageable = None) -> None:
    if not condition:
        _raise(RuntimeError, 'Argument condition not met', message)


def isinstance(obj: ta.Any, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if _isinstance(spec, tuple) and None in spec:  # type: ignore
        spec = tuple(filter(None, spec)) + (_NONE_TYPE,)  # type: ignore
    if not _isinstance(obj, spec):
        _raise(TypeError, 'Must be instance', message, spec)
    return obj


def issubclass(obj: T, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if not _issubclass(obj, spec):  # type: ignore
        _raise(TypeError, 'Must be subclass', message, spec)
    return obj


def not_isinstance(obj: ta.Any, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if _isinstance(spec, tuple) and None in spec:  # type: ignore
        spec = tuple(filter(None, ta.cast(ta.Sequence, spec))) + (_NONE_TYPE,)
    if _isinstance(obj, spec):
        _raise(TypeError, 'Must be not instance', message, spec)
    return obj


def not_issubclass(obj: T, spec: ta.Union[ta.Type[T], ta.Tuple], message: Messageable = None) -> T:
    if _issubclass(obj, spec):  # type: ignore
        _raise(TypeError, 'Must be not subclass', message, spec)
    return obj


def cast(obj: ta.Any, cls: ta.Type[T], message: Messageable = None) -> T:
    if not _isinstance(obj, cls):
        _raise(TypeError, 'Must be instance', message, cls)
    return obj


def not_none(obj: T, message: Messageable = None) -> T:
    if obj is None:
        _raise(TypeError, 'May not be None', message)
    return obj


def none(obj: T, message: Messageable = None) -> None:
    if obj is not None:
        _raise(TypeError, 'Must be None', message)
    return None  # type: ignore


def empty(obj: SizedT, message: Messageable = None) -> SizedT:
    if len(obj) != 0:
        _raise(RuntimeError, 'Must be empty', message)
    return obj


def not_empty(obj: SizedT, message: Messageable = None) -> SizedT:
    if len(obj) == 0:
        _raise(RuntimeError, 'May not be empty', message)
    return obj


def single(obj: ta.Iterable[T], message: Messageable = None) -> T:
    try:
        [value] = obj
    except ValueError:
        _raise(RuntimeError, 'Must be single', message)
    else:
        return value


def unique(it: IterableHashableT, message: Messageable = None) -> IterableHashableT:
    dupes = [e for e, c in collections.Counter(it).items() if c > 1]  # type: ignore
    if dupes:
        _raise(ValueError, 'Must be unique', message, dupes)
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
        _raise(TypeError, 'Must be callable', message)
    return obj


def replacing(expected: ta.Any, old: ta.Any, new: T, message: Messageable = None) -> T:
    if old != expected:
        _raise(TypeError, 'Must be replacing', message, expected, old)
    return new


def replacing_none(old: ta.Any, new: T, message: Messageable = None) -> T:
    return replacing(None, old, new, message=message)


def raises(fn: ta.Callable, exc: ta.Type[BaseException] = BaseException, message: Messageable = None) -> None:
    try:
        fn()
    except BaseException as e:
        if not _isinstance(e, exc):
            _raise(TypeError, 'Must raise correct exception', message, exc, e)
    else:
        _raise(TypeError, 'Must raise', message, exc)


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
        _raise(ValueError, 'Iterator should be exhausted', message)


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
                raise ValueError(f'Expected exactly one of {items}, got {value} and {item}', items, value, item)
            value = item
    if value is not not_set:
        return ta.cast(T, value)
    if default is not not_set:
        return default
    if default_factory is not not_set:
        return default_factory()

    _raise(ValueError, f'Expected exactly one of {items}, got none', message, items)
