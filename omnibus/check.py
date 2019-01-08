"""
~com.google.common.base.Preconditions
"""
import collections
import typing as ta


T = ta.TypeVar('T')
MR = ta.TypeVar('MR', bound=ta.Union[None, str, ta.Tuple])
M = ta.TypeVar('M', bound=ta.Union[None, str, ta.Callable[..., MR]])
IH = ta.TypeVar('IH', bound=ta.Iterable[ta.Hashable])


_isinstance = isinstance
_issubclass = issubclass
_callable = callable


def _raise(
        exception_type: type,
        default: ta.Optional[str],
        message: M,
        *args: ta.Any,
        **kwargs: ta.Any
) -> ta.NoReturn:
    if _callable(message):
        message = message(*args, **kwargs)
        if _isinstance(message, tuple):
            message, *args = message
    if message is None:
        message = default
    if message is not None:
        args = message, *args
    raise exception_type(*args, **kwargs)


def state(condition: bool, message: M = None) -> None:
    if not condition:
        _raise(RuntimeError, 'State condition not met', message)


def arg(condition: bool, message: M = None) -> None:
    if not condition:
        _raise(RuntimeError, 'Argument condition not met', message)


def isinstance(obj: T, spec: ta.Union[ta.Type[T], ta.Tuple[ta.Type[T]]], message: M = None) -> T:
    if not _isinstance(obj, spec):
        _raise(TypeError, None, message, spec)
    return obj


def issubclass(obj: T, spec, message: M = None) -> T:
    if not _issubclass(obj, spec):
        _raise(TypeError, 'Must be subclass', message, spec)
    return obj


def not_none(obj: T, message: M = None) -> T:
    if obj is None:
        _raise(TypeError, 'May not be None', message)
    return obj


def none(obj: T, message: M = None) -> None:
    if obj is not None:
        _raise(TypeError, 'Must be None', message)
    return None


def empty(obj: ta.Sized, message: M = None) -> T:
    if len(obj) != 0:
        _raise(RuntimeError, 'Must be empty', message)
    return obj


def not_empty(obj: ta.Sized, message: M = None) -> T:
    if len(obj) == 0:
        _raise(RuntimeError, 'May not be empty', message)
    return obj


def single(obj: ta.Iterable[T], message: M = None) -> T:
    try:
        [value] = obj
    except ValueError:
        _raise(RuntimeError, 'Must be single', message)
    else:
        return value


def unique(it: IH, message: M = None) -> IH:
    dupes = [e for e, c in collections.Counter(it).items() if c > 1]
    if dupes:
        _raise(ValueError, 'Must be unique', message, dupes)
    return it


def in_(item: T, container: ta.Container[T], message: M = None) -> T:
    if item not in container:
        _raise(ValueError, 'Must be in', message, item, container)
    return item


def not_in(item: T, container: ta.Container[T], message: M = None) -> T:
    if item in container:
        _raise(ValueError, 'Must not be in', message, item, container)
    return item


def callable(obj: T, message: M = None) -> T:
    if not _callable(obj):
        _raise(TypeError, 'Must be callable', message)
    return obj


def replacing_none(old: ta.Any, new: T, message: M = None) -> T:
    if old is not None:
        _raise(TypeError, 'Must be None', message)
    return new


def raises(fn: ta.Callable, exc: ta.Type[BaseException] = BaseException, message: M = None) -> None:
    try:
        fn()
    except BaseException as e:
        if not _isinstance(e, exc):
            _raise(TypeError, 'Must raise correct exception', message, exc, e)
    else:
        _raise(TypeError, 'Must raise', message, exc)


def sets_equal(given: ta.Set[T], expected: ta.Set[T], message: M = None) -> None:
    if given != expected:
        missing = expected - given
        unexpected = given - expected
        _raise(KeyError, f'Set difference - missing: {missing} unexpected: {unexpected}', message, given, expected)  # noqa


def exhausted(it: ta.Iterator[T], message: M = None) -> None:
    try:
        next(it)
    except StopIteration:
        pass
    else:
        _raise(ValueError, 'Iterator should be exhausted', message)


def one_of(*conditions: bool, message: M = None) -> None:
    num_true = len([b for b in conditions if b])
    if num_true != 1:
        _raise(ValueError, f'Exactly one condition must be true, got {num_true}', message)
