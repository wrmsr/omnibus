from .. import wrapped as wrapped_


def test_wrapped():
    l = []
    w = wrapped_.WrappedSequence(lambda x: x + 10, lambda x: x - 10, l)

    assert not w
    w.append(5)
    assert l == [15]
    assert w == [5]
