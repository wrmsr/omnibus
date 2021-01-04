def test_gettid():
    from .. import os

    assert isinstance(os.gettid(), int)
