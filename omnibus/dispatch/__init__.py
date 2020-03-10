from .. import lang
from .caching import AbcCacheGuard  # noqa
from .caching import CachingDispatcher  # noqa
from .erasing import ErasingDispatcher  # noqa
from .function import function  # noqa
from .registry import Class  # noqa
from .registry import Property  # noqa
from .registry import property_  # noqa
from .types import AmbiguousDispatchError  # noqa
from .types import CacheGuard  # noqa
from .types import Dispatcher  # noqa
from .types import DispatchError  # noqa
from .types import Manifest  # noqa
from .types import UnregisteredDispatchError  # noqa


lang.warn_unstable()
