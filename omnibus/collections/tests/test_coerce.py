import typing as ta

import pytest

from .. import coerce as co_
from .. import frozen as frz_


def test_coerce():
    r = co_.seq_of(str)([1, 2])
    assert r == ['1', '2']
    assert isinstance(r, frz_.Frozen)
    assert isinstance(r, ta.Sequence)

    c = co_.seq_of((int,))  # type: ignore
    assert c([1, 2]) == [1, 2]
    with pytest.raises(TypeError):
        c([1, '2'])

    c = co_.seq_of((int, None))  # type: ignore
    assert c([1, 2, None]) == [1, 2, None]
