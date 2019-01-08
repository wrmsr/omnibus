import datetime


# http://bugs.python.org/issue7980
datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')


def _test_install():
    try:
        from . import conftest  # noqa
    except ImportError:
        pass
    else:
        raise EnvironmentError
