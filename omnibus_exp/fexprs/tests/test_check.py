import sys
import threading
import types
import typing as ta

import pytest

from .. import recon as recon_
from .. import values as values_
from ... import check
from ...threading import forbid_recursion


def _build_frame_check_exception(
        raise_frame: types.FrameType,
        exc_cls: ta.Type[Exception],
        *args,
        **kwargs
) -> Exception:
    assert raise_frame.f_code.co_name == '_raise'
    assert raise_frame.f_globals is vars(check)

    check_frame = raise_frame.f_back
    assert not check_frame.f_code.co_name.startswith('_')
    assert check_frame.f_globals is vars(check)

    call_frame = check_frame.f_back
    assert call_frame.f_globals is not vars(check)

    xv = recon_.reconstruct_frame_call_arg(call_frame)

    print(xv)
    print(values_.render(xv))
    print()

    return exc_cls(*args, **kwargs)  # noqa


@pytest.mark.xfail
def test_check(monkeypatch):
    import dis
    dis.dis(test_check)

    is_recursing = threading.local()
    is_recursing.value = False

    @forbid_recursion(check._default_exception_factory)
    def _fexpr_check_exception_factory(exc_cls: ta.Type[Exception], *args, **kwargs) -> Exception:
        raise_frame = sys._getframe(2)  # noqa
        return _build_frame_check_exception(raise_frame, exc_cls, *args, **kwargs)

    monkeypatch.setattr(check, '_EXCEPTION_FACTORY', _fexpr_check_exception_factory)

    x = 2
    y = 3
    z = 4
    with pytest.raises(ValueError):
        check.arg((x + y) == z)
