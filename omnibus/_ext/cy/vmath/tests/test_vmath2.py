import array

from .. import vmath2 as vm2  # type: ignore
from .. import _vmath2_ops as vm2o
from ..... import arrays


def test_add():
    l = 10
    z = arrays.zeroes('f', l)
    a1 = z[:]
    a2 = array.array('f', list(map(float, range(l))))
    a3 = array.array('f', list(map(float, range(l, l * 2))))
    vm2.op(vm2o._pfn_op_add_sz_pf32_pf32_pf32, [('sz', l), ('pf32', a1), ('pf32', a2), ('pf32', a3)])
    assert list(a1) == [l + r for l, r in zip(a2, a3)]
    assert list(z) == [0.] * len(z)
