import sys


if not sys.version_info >= (3, 7):
    raise EnvironmentError


if '__path__' in globals():
    import pkgutil
    globals()['__path__'] = pkgutil.extend_path(globals()['__path__'], __name__)


def _test_install():
    try:
        from . import conftest  # noqa
    except ImportError:
        pass
    else:
        raise EnvironmentError

    from . import revision
    rev = revision.get_revision()
    if not isinstance(rev, str) or len(rev) != 40:
        raise ValueError(rev)
