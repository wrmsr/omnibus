import dataclasses as dc
import time

from ... import dataclasses as odc


def test_perf():
    @dc.dataclass(frozen=True)
    class C0:
        x: int

    class C1(odc.Frozen):
        x: int

    class C2(odc.Pure):
        x: int

    class C3(odc.Tuple):
        x: int

    for C in [C0, C1, C2, C3]:
        print(C)

        c = C(1)
        assert c.x == 1

        start = time.time()

        for _ in range(10_000_000):
            c.x  # noqa

        end = time.time()
        print(end - start)
