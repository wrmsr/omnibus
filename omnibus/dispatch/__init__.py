from .. import lang
from .caching import AbcCacheGuard  # noqa
from .caching import CachingDispatcher  # noqa
from .erasing import ErasingDispatcher  # noqa
from .functions import function  # noqa
from .manifests import inject_manifest  # noqa
from .registry import Class  # noqa
from .registry import Property  # noqa
from .registry import property_ as property  # noqa
from .types import AmbiguousDispatchError  # noqa
from .types import CacheGuard  # noqa
from .types import Dispatcher  # noqa
from .types import DispatchError  # noqa
from .types import Manifest  # noqa
from .types import UnregisteredDispatchError  # noqa


lang.warn_unstable()
