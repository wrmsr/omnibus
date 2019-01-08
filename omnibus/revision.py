import errno
import typing as ta

import pkg_resources

from .lang import cached_nullary


@cached_nullary
def get_revision() -> ta.Optional[str]:
    try:
        return pkg_resources.resource_string(__package__.rpartition('.')[0], '.revision').decode('utf-8').strip()
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

    return None


if __name__ == '__main__':
    print(get_revision())
