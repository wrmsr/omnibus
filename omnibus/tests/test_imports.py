from .. import lang


IGNORED_SUFFIXES = {
    '.tests',
    '.pytest',
}


def test_imports():
    for m in lang.yield_import_all(
            __package__.split('.')[0],
            recursive=True,
            filter=lambda s: not any(s.endswith(e) for e in IGNORED_SUFFIXES),
    ):
        print(m)
