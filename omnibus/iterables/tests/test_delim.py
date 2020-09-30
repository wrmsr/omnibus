import io

from ..delim import yield_delimited_str_chunks


def test_yield_delimited_str_chunks():
    d = '\n==='
    s = """
abcd
efgh
===
ijk
lmnopq
===
x
    """
    e = s.split(d)

    for cs in [7, *range(1, len(s)), 0xFFFF]:
        ls = []
        for chunks in yield_delimited_str_chunks(io.StringIO(s), d, chunk_size=cs):
            ls.append(list(chunks))
        g = [''.join(l) for l in ls]
        assert g == e
