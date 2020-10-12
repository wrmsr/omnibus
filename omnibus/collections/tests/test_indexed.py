from .. import indexed as idxd


def test_indexed_seq():
    s = idxd.IndexedSeq(['a', 'b', 'c'])
    assert s[1] == 'b'
    assert s.idxs['b'] == 1


def test_indexed_set_seq():
    s = idxd.IndexedSetSeq([['a', 'b', ], ['c'], ['d', 'e', 'f']])
    assert set(s[2]) == {'d', 'e', 'f'}
    assert s.idxs['b'] == 0
    assert s.idxs['c'] == 1
    assert s.idxs['e'] == 2
