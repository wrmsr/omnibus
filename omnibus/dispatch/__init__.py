from .. import lang as _lang
from .caching import AbcCacheGuard  # noqa
from .caching import CachingDispatcher  # noqa
from .classes import Class  # noqa
from .classes import Property  # noqa
from .classes import property_ as property  # noqa
from .erasing import ErasingDispatcher  # noqa
from .functions import function  # noqa
from .generic import GenericDispatcher  # noqa
from .manifests import inject_manifest  # noqa
from .types import AmbiguousDispatchError  # noqa
from .types import CacheGuard  # noqa
from .types import Dispatcher  # noqa
from .types import DispatchError  # noqa
from .types import Manifest  # noqa
from .types import UnregisteredDispatchError  # noqa


_lang.warn_unstable()
