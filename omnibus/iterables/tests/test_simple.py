from .. import simple as simple_


def test_split_filter():
    t, f = simple_.split_filter(lambda x: x % 2 == 0, range(10))
    assert t == [0, 2, 4, 6, 8]
    assert f == [1, 3, 5, 7, 9]
