from .. import lang


def test_imports():
    for m in lang.yield_import_all(
            __package__.split('.')[0],
            recursive=True,
            filter=lambda s: not any(s.endswith(e) for e in ['.tests', '.pytest']),
    ):
        print(m)
