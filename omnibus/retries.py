"""
TODO:
 - coordination (redis? coord iface?)
 - dogpile
 - mv faults

https://engineering.shopify.com/blogs/engineering/circuit-breaker-misconfigured
"""
import time
import typing as ta

from . import check
from . import dataclasses as dc
from . import lang


lang.warn_unstable()


class RetryCall:

    def __init__(
            self,
            retrier: 'Retrier',
            fn: ta.Callable,
            args: ta.Optional[ta.Iterable[ta.Any]] = None,
            kwargs: ta.Optional[ta.Mapping[str, ta.Any]] = None,
    ) -> None:
        super().__init__()

        self._retrier = check.isinstance(retrier, Retrier)
        self._fn = check.callable(fn)
        self._args = list(args or ())
        self._kwargs = dict(kwargs or {})

        self._start_time = time.time()

        # self._attempt_number = 1
        # self._outcome = None
        # self._outcome_timestamp = None
        # self._idle_for = 0.
        # self._next_action = None

    @classmethod
    def of(cls, retrier: 'Retrier', fn: ta.Callable, *args, **kwargs) -> 'RetryCall':
        return cls(retrier, fn, args, kwargs)


class _ReprFn:

    def __init__(self, rpr: str, fn: ta.Callable) -> None:
        super().__init__()

        self._rpr = check.isinstance(rpr, str)
        self._fn = check.callable(fn)

    def __repr__(self) -> str:
        return self._rpr

    def __get__(self, instance, owner=None):
        return type(self)(self._rpr, self._fn.__get__(instance, owner))  # noqa

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


def _repr_fn(rpr: str, fn: ta.Callable) -> ta.Callable:
    return _ReprFn(rpr, fn)


WaitFn = ta.Callable[['RetryCall'], float]
StopFn = ta.Callable[['RetryCall'], bool]


class Wait(lang.Namespace):
    NONE = _repr_fn('Wait.NONE', lambda _: 0.)


class Stop(lang.Namespace):
    NEVER = _repr_fn('Stop.NEVER', lambda _: False)


class Retrier:

    def __init__(
            self,
            *,
            sleep: ta.Callable[[float], None] = dc.field(time.sleep, kwonly=True),
            wait: WaitFn = Wait.NONE,
            stop: StopFn = Stop.NEVER,
    ) -> None:
        super().__init__()

        self._sleep = check.callable(sleep)

        # stop = stop_never,
        # wait = wait_none(),
        # retry = retry_if_exception_type(),
        # before = before_nothing,
        # after = after_nothing,
        # before_sleep = None,
        # reraise = False,
        # retry_error_cls = RetryError,
        # retry_error_callback = None,

    def call(self, fn: ta.Callable, *args, **kwargs) -> RetryCall:
        return RetryCall.of(self, fn, *args, **kwargs)

    def __call__(self, fn: ta.Callable, *args, **kwargs) -> RetryCall:
        return self.call(fn, *args, **kwargs)
